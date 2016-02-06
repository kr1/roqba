import sys
import logging
import time
import threading
import random
from random import choice

from roqba.static.movement_probabilities import ORNAMENTS, DRUM_FILLS
from roqba.static.scales_and_harmonies import (ALL_STRICT_HARMONIES,
                                               BASE_HARMONIES,
                                               FOLLOWINGS,
                                               HARMONIC_INTERVALS,
                                               HARMONIES,
                                               NOTES_PER_SCALE,
                                               SCALES,
                                               SCALES_BY_FREQUENCY,
                                               STRICT_HARMONIES)
import roqba.static.note_length_groupings as note_length_groupings
from roqba.static.melodic_behaviours import registers
from roqba.drummer import Drummer
from roqba.voice import Voice
from roqba import metronome
from roqba.composers.abstract_composer import AbstractComposer
from roqba.static.meters import METERS



class Composer(AbstractComposer):
    def __init__(self,
                 gateway,
                 settings,
                 behaviour,
                 scale="DIATONIC"):
        # percussion
        self.settings = settings
        self.behaviour = behaviour
        self.drummer = Drummer(self)
        self.gateway = gateway
        # TODO: consider making NoteGateway a Singleton
        self.harm = {}
        self.num_voices = settings['number_of_voices']
        self.speed_lim = behaviour['embellishment_speed_lim']
        self.offered_scales = SCALES_BY_FREQUENCY
        self.offered_meters = METERS
        self.scale = scale
        self.selected_meters = ("meters" in self.behaviour.keys() and
                                self.behaviour["meters"] or METERS.keys())
        self.modified_note_in_current_frame = None
        self.max_binaural_diff = behaviour['max_binaural_diff']
        self.generate_real_scale(settings['lowest_note_num'],
                                 settings['highest_note_num'])
        self.registers = registers
        super(Composer, self).__init__()


    def generate(self, state):
        """main generating function, the next polyphonic step is produced here

        any of the voices can change.
        """
        tmp_harm = []
        counter = 0
        self.modified_note_in_current_frame = None
        for v in self.sort_voices_by_importance():
            if len(self.voices) < self.num_voices:
                raise (RuntimeError, "mismatch in voices count")
            v.generator.send(state)
            self.musical_logger.debug("note {0}".format(v.note))
            tmp_harm.append(v.note)
            if v.note == 0 or not v.note_change:
                continue
            if (state["weight"] == metronome.HEAVY or
                    state["weight"] == metronome.MEDIUM):
                patience = 0
                while not (self.acceptable_harm_for_length(tmp_harm,
                                                           counter) and
                           patience < 100):
                    if len(tmp_harm) > counter:
                        tmp_harm.pop()
                    v.generator.send(state)
                    tmp_harm.append(v.note)
                    patience += 1
            counter += 1

        # here we have arrived at the next level
        # now we set the "real note" field according to the present scale
        self.add_duration_in_msec(state)
        self.apply_scale()
        self.embellish(state)
        # the stream analyzer can be used to check for chords, simultaneities
        self.stream_analyzer()
        # percussion
        self.drummer.generator.send([state, state['cycle_pos']])
        for k, v in self.drummer.frame.items():
            if v["meta"]:
                if v["meta"] == 'empty':
                    threading.Thread(target=self.drum_fill_handler,
                                     args=(k, state)).start()
                if v["meta"] == 'mark':
                    threading.Thread(target=self.drum_mark_handler,
                                     args=(k, state)).start()
        self.gateway.drum_hub.send(self.drummer.frame)
        # send the voices to the note-hub
        self.gateway.hub.send(self.voices)  # this sends the voices to the hub
        self.notator.note_to_file({"notes": tmp_harm,
                                   "weight": state["weight"],
                                   "cycle_pos": state["cycle_pos"]})
        return self.comment

    def apply_scale(self):
        '''sets the real note for the scale-bound notes in each voice'''
        for v in self.voices.values():
            if v.note == 0:
                v.real_note = 0
                continue
            if v.note_change:
                v.real_note = self.real_scale[v.note]
        if self.modified_note_in_current_frame:
            self.musical_logger.info("modified note: '{0}'".format(
                                     self.modified_note_in_current_frame))
            which = self.modified_note_in_current_frame[0]
            for v in self.voices.values():
                num_notes = NOTES_PER_SCALE[self.scale]
                if v.note % num_notes == which % num_notes:
                    direction = self.modified_note_in_current_frame[1]
                    was_note = v.real_note
                    if direction == '-':
                        v.real_note -= 1
                    else:
                        v.real_note += 1
                    self.musical_logger.info("modified note: {0} from '{1}' to '{2}'".format(
                                             v.note, was_note, v.real_note))
#        for v in self.voices.values():
#            if v.note_change:
#                v.real_note = self.scale_walker(self.scale,
#                                                v.real_note,
#                                                v.note_delta)

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

    def sort_voices_by_importance(self, by='imp'):
        '''sorts the voices according to their importance.

        by: 'imp':
            - importance according to register

        by: 'dir':
            - voices having a registered direction first

        '''
        voices = self.voices.values()
        if by == 'imp':
            register_sort_dict = {}
            [register_sort_dict.__setitem__(reg["name"],
                                            reg["sort_importance"]) for
             reg in self.registers.values()]
            voices.sort(key=lambda x: register_sort_dict[x.register["name"]])
        else:
            dirs = filter(lambda x: x.dir, voices)
            no_dirs = list(set(voices) - set(dirs))
            voices = dirs + no_dirs
        melodic = filter(lambda v: v.playing_a_melody, voices)
        if len(melodic) > 0:
            voices.remove(melodic[0])
            voices = [melodic[0]] + voices
        return voices

    def choose_rhythm(self):
        '''chooses a new rhythm randomly from each voices groupings'''
        for v in self.voices.values():
            if not v.playing_a_melody:
                v.set_rhythm_grouping(choice(v.note_length_groupings))

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
        if val and val != 'random':
            if voice:
                voice.binaural_diff = val
                self.gateway.pd.send(["voice", "binaural", str(voice.id), val])
            else:
                self.gateway.pd.send(["voice", "binaural", -1, val])
                for v in self.voices.values():
                    v.binaural_diff = val
        else:
            for v in self.voices.values():
                if not self.behaviour.voice_get(v.id, "automate_binaural_diffs"):
                    continue
                val = random.random() * self.behaviour.voice_get(v.id, "max_binaural_diff")
                v.binaural_diff = val
                self.gateway.pd.send(["voice", "binaural", v.id, val])

    def drum_fill_handler(self, v, state):
        '''handles the sending of drum-fill notes'''
        identifier = 'cont' if v == 'cont2' else 'cont2'
        possible_fills = [fill for fill in DRUM_FILLS
                          if state['speed'] / len(fill) > self.behaviour['min_speed'] * 0.5 ]
        chosen = choice(possible_fills)
        for fraction in chosen:
            if (state["speed"] * 1000 * fraction) < self.drummer.peak_speed:
                break
            self.gateway.pd_send_drum_note(identifier, self.drummer.frame[identifier]["vol"],
                                           self.drummer.frame[identifier]["pan"],
                                           self.drummer.frame[identifier]["ctl"])
            time.sleep(state["speed"] * fraction)

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
            notes = choice(ORNAMENTS[key])

            ## check for the speed limit, if ornaments would be too fast,
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
                            self.behaviour.voice_get(v.id, "slide_duration_prop"))
                self.gateway.set_slide_msecs(v.id, (v.duration_in_msec *
                                                    dur_fraction *
                                                    dur_prop))
                self.gateway.pd_send_note(v.id, real_note)
            self.gateway.set_slide_msecs(
                v.id,
                (self.behaviour.voice_get(v.id, "use_proportional_slide_duration") and
                 self.behaviour.voice_get(v.id, "slide_duration_prop") or
                 self.behaviour.voice_get(v.id, "slide_duration_msecs")))

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
            if (self.is_base_harmony(harmony) and
                    not filter(lambda v: v.playing_a_melody, self.voices.values())):
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
    print HARMONIES
    print SCALES_BY_FREQUENCY
    print STRICT_HARMONIES

    print Composer().get_deltas([12, 8, 10, 15])
    print "get deltas([2, 5]):", Composer.get_deltas([2, 5])
    print Composer.acceptable_harmony(Composer.get_deltas([12, 8, 10, 15]))
    print Composer().acceptable_harmony([2, 4, 6])
    from voice import Voice
    c = Composer()
