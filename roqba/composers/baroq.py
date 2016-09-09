import time
import threading
import random
from random import choice

from roqba.static.movement_probabilities import ORNAMENTS, DRUM_FILLS
from roqba.static.scales_and_harmonies import (ALL_STRICT_HARMONIES,
                                               BASE_HARMONIES,
                                               HARMONIC_INTERVALS,
                                               NOTES_PER_SCALE,
                                               STRICT_HARMONIES)
from roqba.static.meters import METERS
from roqba import metronome
from roqba.composers.abstract_composer import AbstractComposer
from roqba.composers.rhythm_and_meter_mixin import RhythmAndMeterMixin


class Composer(RhythmAndMeterMixin, AbstractComposer):
    def __init__(self,
                 gateway,
                 settings,
                 behaviour):
        super(Composer, self).__init__(gateway,
                                       settings,
                                       behaviour)
        self.harm = {}
        self.speed_lim = behaviour['embellishment_speed_lim']
        self.selected_meters = ("meters" in self.behaviour.keys() and
                                self.behaviour["meters"] or METERS.keys())
        self.modified_note_in_current_frame = None
        self.max_binaural_diff = behaviour['max_binaural_diff']
        self.generate_real_scale(settings['lowest_note_num'],
                                 settings['highest_note_num'])

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
        if self.notate:
            self.notator.notate_rhythm(self.meter, state["cycle_pos"])
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
            # print "all_notes_change: harmony {0}".format(harmony)
            if (self.is_base_harmony(harmony) and
                    not filter(lambda v: v.playing_a_melody, self.voices.values())):
                self.comment = "caesura"
                # print "all notes change to a base harmony"

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
