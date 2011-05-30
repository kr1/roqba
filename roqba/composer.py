import logging
import time
import threading
import random
from random import choice as sample

import metronome
from notator import Notator
from static.movement_probabilities import ORNAMENTS, DRUM_FILLS
from static.scales_and_harmonies import *
import static.note_length_groupings as note_length_groupings
from static.melodic_behaviours import registers
from drummer import Drummer
from static.meters import METERS

comp_logger = logging.getLogger("composer")
note_logger = logging.getLogger("transcriber")


class Composer(object):
    def __init__(self,
                 gateway,
                 settings,
                 behaviour,
                 num_voices=3,
                 scale="DIATONIC"):
                 #scale="PENTATONIC"):
                 #scale="PENTA_MINOR"):
        # percussion
        self.settings = settings
        self.behaviour = behaviour
        self.drummer = Drummer(self)
        self.percussion_hub = gateway.drum_hub()
        self.percussion_hub.next()
        self.harm = {}
        self.voices = {}
        self.num_voices = settings['number_of_voices']
        self.speed_lim = behaviour['embellishment_speed_lim']
        self.scale = scale
        self.selected_meters = ("meters" in self.behaviour.keys() and
                        self.behaviour["meters"] or METERS.keys())
        self.meter = behaviour['meter']
        self.set_meter(self.meter)
        self.applied_meter = METERS[self.meter]['applied']
        self.max_binaural_diff = behaviour['max_binaural_diff']
        self.generate_real_scale(settings['lowest_note_num'],
                                 settings['highest_note_num'])
        self.gateway = gateway
        self.hub = gateway.hub()
        # XxxxX consider making NoteGateway a Singleton
        self.hub.next()
        self.registers = registers
        self.notator = Notator(self.num_voices)

    def __repr__(self):
        return "<Composer-Inst with {0}>".format(self.harm)

    def report(self):
        '''utility function that prints info on  harmonies and single voices'''
        print "harmonies: {0}".format(self.harm)
        print "voices: {0}\nnotes:{1}".format(self.voices,
                            map(lambda x: x.note, self.voices.values()))

    def set_meter(self, meter):
        '''modifies composer-attributes for the specified meter.

        calls reload_register method of the voices and creates and
        sets the new meter also for the drummer-instance'''
        self.TERNARY_GROUPINGS = note_length_groupings.get_grouping(meter,
                                                                    "terns")
        self.HEAVY_GROUPINGS = note_length_groupings.get_grouping(meter,
                                                                  "heavy")
        self.DEFAULT_GROUPINGS = note_length_groupings.get_grouping(meter,
                                                                   "default")
        self.FAST_GROUPINGS = note_length_groupings.get_grouping(meter,
                                                                   "first")
        for v in self.voices.values():
            v.reload_register()
        self.drummer.create_pattern(METERS[meter]["applied"])

    def add_voice(self, id, voice):
        '''adds a voice to self.voices'''
        self.voices.update({id: voice})

    def generate(self, state):
        """main generating function, the next polyphonic step is produced here

        any of the voices can change.
        """
        tmp_harm = []
        counter = 0
        for v in self.sort_voices_by_importance():
            if len(self.voices) < self.num_voices:
                raise (RuntimeError, "mismatch in voices count")
            v.generator.send(state)
            tmp_harm.append(v.note)
            if v.note == 0 or not v.note_change:
                continue
            if (state["weight"] == metronome.HEAVY or
                state["weight"] == metronome.MEDIUM):
                patience = 0
                while not self.acceptable_harm_for_length(tmp_harm,\
                                                          counter) and\
                                                          patience < 100:
                    if len(tmp_harm) > counter:
                        tmp_harm.pop()
                    v.generator.send(state)
                    tmp_harm.append(v.note)
                    patience += 1
            counter += 1
        for v in self.voices.values():
            if v.behaviour == "SLAVE" and v.followed_voice.note_change:
                if v.followed_voice.note == 0:
                    v.note = 0
                    continue
                if v.following_counter == 0:
                    v.follow_dist = sample(FOLLOWINGS)
                if v.following_counter < v.follow_limit:
                    v.note = v.followed_voice.note + v.follow_dist
                    v.following_counter += 1
                else:
                    v.set_state("SLAVE")
        # here we have arrived at the next level
        # now we set the "real note" field according to the present scale
        self.add_duration_in_msec(state)
        self.apply_scale()
        # the stream analyzer can be used to check for chords, simultaneities
        self.embellish(state)
        self.stream_analyzer()
        # percussion
        self.drummer.generator.send(state)
        for k, v in self.drummer.frame.items():
            if v["meta"]:
                if v["meta"] == 'empty':
                    threading.Thread(target=self.drum_fill_handler,
                                     args=(k, state)).start()
                if v["meta"] == 'mark':
                    threading.Thread(target=self.drum_mark_handler,
                                     args=(k, state)).start()
        self.percussion_hub.send(self.drummer.frame)
        # send the voices to the note-hub
        self.hub.send(self.voices)  # this sends the voices to the hub
        self.notator.note_to_file({"notes": tmp_harm,
                                   "weight": state["weight"],
                                   "cycle_pos": state["cycle_pos"]})
        return self.comment

    def apply_scale(self):
        '''sets the real note for '''
        for v in self.voices.values():
            if v.note == 0:
                v.real_note = 0
                continue
            if v.note_change:
                v.real_note = self.real_scale[v.note]

#        for v in self.voices.values():
#            if v.note_change:
#                v.real_note = self.scale_walker(self.scale,
#                                                v.real_note,
#                                                v.note_delta)

    def set_scale(self, name, min=0, max=128):
        '''sets the specified scale and generates a new real scale'''
        self.scale = name
        self.generate_real_scale(min, max)

    def generate_real_scale(self, min=0, max=128):
        '''extends the one-octave scale over the specified range'''
        scale = SCALES[self.scale]
        self.real_scale = []
        value = 0
        for n in xrange(min, max):
            value += 1
            index = n % len(scale)
            if scale[index]:
                self.real_scale.append(value)
        #print self.real_scale

    def acceptable_harm_for_length(self, harm, length):
        '''checks if the specified (interval-set) are "harmonic"'''
        if length in [0, 1]:
            return True
        else:
            deltas = self.flatten_chord(self.get_deltas(harm))
            if length == 2:
                return deltas[0] in HARMONIC_INTERVALS
            else:
                return set(deltas) in ALL_STRICT_HARMONIES

    def sort_voices_by_importance(self):
        '''sorts the voices according to their importance.

        having a registered direction is the only determinant of importace
        for the tim being'''
        dirs = filter(lambda x: x.dir, self.voices.values())
        no_dirs = list(set(self.voices.values()) - set(dirs))
        return dirs + no_dirs

    def choose_rhythm(self):
        '''chooses a new rhythm randomly from each voices groupings'''
        for v in self.voices.values():
            v.set_rhythm_grouping(sample(v.note_length_groupings))

    def embellish(self, state):
        '''checks for embellishment markers of the single voices

        - starts a thread to handle the embellishment'''
        for v in self.voices.values():
            if v.do_embellish:
                v.do_embellish = False
                threading.Thread(target=self.ornament_handler,
                                 args=(v,
                                       v.note_duration_steps,
                                       v.note,
                                       v.note_delta,
                                       state)).start()

    def set_binaural_diffs(self, val=None, voice=None):
        '''"de-tunes" the specified voice by the specified interval (in hertz)

        - if no values are given, random values (in the configurated range)
        are set for each voice.
        '''
        if val:
            if voice:
                self.gateway.pd.send(["voice", "binaural", voice, val])
            else:
                self.gateway.pd.send(["voice", "binaural", -1, val])
        else:
            for v in self.voices.values():
                val = random.random() * self.max_binaural_diff
                self.gateway.pd.send(["voice", "binaural", v.id, val])

    def drum_fill_handler(self, v, state):
        '''handles the sending of drum-fill notes'''
        for f in sample(DRUM_FILLS):
            if (state["speed"] * 1000 * f) < self.drummer.peak_speed:
                break
            self.gateway.pd_send_drum_note(v, self.drummer.frame[v]["vol"],
                                           self.drummer.frame[v]["pan"],
                                           self.drummer.frame[v]["ctl"])
            time.sleep(state["speed"] * f)

    def drum_mark_handler(self, v, state):
        '''handles the sending of a drum mark'''
        vol = self.drummer.frame[v]["vol"],
        pan = self.drummer.frame[v]["pan"],
        ctl = self.drummer.frame[v]["ctl"],
        tick = state["speed"] / 50
        vol_tmp = vol[0]
        for idx in xrange(6):
            vol_tmp *= 0.9
            ctl_new = ctl[0] - ((idx ** 2) * (random.random() * 600 + 200))
            self.gateway.pd_send_drum_note(v, vol_tmp, pan[0], ctl_new)
            time.sleep(4 * tick)
            self.gateway.pd_send_drum_note(v, 0, pan[0], ctl_new)
            time.sleep(1 * tick)

    def ornament_handler(self, v, duration, note, note_delta, state):
        '''this method handles the sending of the ornament notes.

        the ornament is chosen randomly
        if the ornament would be too fast, it returns without action'''
        key = (abs(note_delta), duration)
        if key in ORNAMENTS:
            notes = sample(ORNAMENTS[key])

            ## check for the speed limit, if ornaments wold be too fast,
            ## don't embellish
            if min([n[0] * state["speed"] for n in notes]) < self.speed_lim:
                return

            for orn_note in notes:
                dur_fraction = orn_note[0]
                time.sleep(state["speed"] * dur_fraction)
                # add pos/neg multiplier
                multiplier = ((note_delta / abs(note_delta))
                              if note_delta != 0
                              else 0)
                next_note = note + (orn_note[1] * multiplier)
                real_note = self.real_scale[next_note]
                dur_prop = (v.slide_duration_prop or
                            behaviour["default_slide_duration_prop"])
                self.gateway.set_slide_msecs(v.id, (v.duration_in_msec *
                                                    dur_fraction *
                                                    dur_prop))
                self.gateway.pd_send_note(v.id, real_note)

    def stream_analyzer(self):
        """analyses the stream of notes.

        searches for target-harmonies and sets a flag"""
        # check if all notes are new
        self.comment = 'normal'
        note_changes = [v.note_change for v in self.voices.values()]
        all_notes_change = reduce(lambda x, y:
                                 x and y,
                                 note_changes)
        if all_notes_change:
            harmony = map(lambda x: x.note, self.voices.values())
            #print "all_notes_change: harmony {0}".format(harmony)
            if self.is_base_harmony(harmony):
                self.comment = "caesura"
                #print "all notes change to a base harmony"

    def acceptable_harmony(self, chord):
        '''checks if a chord is "harmonic"'''
        flat = self.flatten_chord(chord)
        return set(flat) in STRICT_HARMONIES

    def is_base_harmony(self, chord):
        '''checks if a chord is a the base tonality

        (either major or minor) of the current context'''
        flat = self.flatten_chord(chord)
        #print set(flat)
        return set(flat) in BASE_HARMONIES[self.num_voices]

    @staticmethod
    def flatten_chord(chord):
        '''maps a specified code to the base octave'''
        flat = map(lambda x: x % 7, chord)
        return flat

    @staticmethod
    def get_deltas(chord):
        '''returns an array of the intervals between the specified notes'''
        chord.sort()
        base = chord[0]
        return map(lambda x: x - base, chord)[1:]

    @staticmethod
    def scale_walker(scale, present_note, delta):
        """walks the <scale> <delta> steps starting at <present_note>"""
        if delta == 0:
            return present_note
        dir = delta / abs(delta)
        steps = 0
        index = 1
        octave = present_note // len(scale)
        mod = present_note % len(scale)
        while steps < abs(delta):
            check_index = (mod + (dir * index)) % len(scale)
            if scale[check_index]:
                steps += 1
                if steps == abs(delta):
                    break
                index += 1
            else:
                index += 1
            #print check_index, scale[check_index], index, steps
        return (index * dir) + mod + (octave * len(scale))

    def add_duration_in_msec(self, state):
        '''adds duration in milliseconds for each note in self.voices'''
        for v in self.voices.values():
            v.duration_in_msec = int(v.note_duration_steps *
                                     state["speed"] * 1000)

if __name__ == "__main__":
    print DIATONIC, len(DIATONIC)
    print HARMONIC, len(HARMONIC)
    print MELODIC, len(MELODIC)
    print HARMONIES
    print STRICT_HARMONIES

    print Composer().get_deltas([12, 8, 10, 15])
    print "get deltas([2, 5]):", Composer.get_deltas([2, 5])
    print Composer.acceptable_harmony(Composer.get_deltas([12, 8, 10, 15]))
    print Composer().acceptable_harmony([2, 4, 6])
    from voice import Voice
    c = Composer()
    v1 = Voice(1, None, c)
    v1.dir = 1
    c.add_voice(v1.id, v1)
    v2 = Voice(2, None, c)
    c.add_voice(v2.id, v2)
    v3 = Voice(3, None, c)
    v3.dir = 0
    c.add_voice(v3.id, v3)

    print c.sort_voices_by_importance()
