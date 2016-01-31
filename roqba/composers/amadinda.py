import os
import itertools
import threading
from random import choice

from roqba.composers.abstract_composer import AbstractComposer
from roqba.static.melodic_behaviours import registers
from roqba.static.scales_and_harmonies import FOLLOWINGS, SCALES_BY_FREQUENCY
from roqba.static.meters import METERS


class Composer(AbstractComposer):
    def __init__(self, gateway, settings, behaviour, scale="DIATONIC"):
        self.gateway = gateway
        self.settings = settings
        self.behaviour = behaviour
        self.num_voices = settings['number_of_voices']
        self.scale = scale
        self.registers = registers
        self.selected_meters = [self.behaviour['meter']]
        self.offered_meters = METERS
        self.pattern_played_times = 0
        self.pattern_played_maximum = 12
        self.offered_scales = SCALES_BY_FREQUENCY
        self.words = self.all_python_words()
        super(Composer, self).__init__()
        for voice in self.voices.values():
            voice.duration_in_msec = 600
        self.set_scale(self.scale)
        self.make_new_pattern()

    def all_python_words(self):
        filepaths = itertools.chain(*[[os.path.join(entry[0], file_)
                                       for file_ in entry[2] if file_.endswith('py')]
                                      for entry in list(os.walk('.'))])
        lines = []
        for filepath in filepaths:
            with open(filepath) as file_:
                lines.extend(file_.readlines())
        words = itertools.chain(*[line.split(" ") for line in lines])
        return [word.strip() for word in words if word.strip() and len(word.strip()) >= 12]

    def choose_rhythm(self):
        pass

    def generate(self, state):
        """main generating function, the next polyphonic step is produced here

        any of the voices can change.
        """
        self.comment = 'normal'
        tmp_harm = []
        meter_pos = state['cycle_pos']
        for voice in self.voices.values():
            if len(self.voices) < self.num_voices:
                raise (RuntimeError, "mismatch in voices count")
            #voice.generator.send(state)
            self.musical_logger.debug("note {0}".format(voice.note))
            if voice.note == 0 or not voice.note_change:
                continue
            voice.note_change = True
            next_note = self.next_voice_note(voice, meter_pos)
            tmp_harm.append(next_note)
        self.drummer.generator.send(state)
        for k, v in self.drummer.frame.items():
            # TODO: re-add the drum filler
            if False and v["meta"]:
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

    def next_voice_note(self, voice, meter_pos):
        if voice.behaviour == "SLAVE":
            follow = self.voices[voice.followed_voice_id]
            res = 0
            if follow.note_change:
                if voice.following_counter == 0:
                    voice.follow_dist = choice(FOLLOWINGS)
                if voice.following_counter < voice.follow_limit:
                    res = follow.note and follow.note + voice.follow_dist or 0
                    voice.following_counter += 1
                else:
                    voice.reset_slave()
                    res = 0
                if follow.note == 0:
                    res = 0
                next_note = res
                voice.real_note = next_note and self.real_scale[next_note] or None
                return res
        if self.pattern_played_times >= self.pattern_played_maximum:
            self.make_new_pattern()
            self.comment = 'caesura'
            self.pattern_played_times = 0
        next_note = self.pattern[voice.id][meter_pos] or None
        voice.note = next_note
        voice.real_note = next_note and self.real_scale[next_note] or None
        self.pattern_played_times += 1.0 / len(self.pattern[1])
        return next_note
    def _make_third_voice(self, num_tones, tranpose, number_of_tones_in_3rd_voice):
        seq3 = []
        for idx in range(num_tones * 2):
            if (applied_seq1[idx] > 0
                    and applied_seq1[idx]  < transpose + (number_of_tones_in_3rd_voice)):
                seq3.append(applied_seq1[idx] + 2 * octave_offset)
            elif (applied_seq2[idx] > 0
                    and applied_seq2[idx] < transpose + (number_of_tones_in_3rd_voice)):
                seq3.append(applied_seq2[idx] + 2 * octave_offset)
            else:
                seq3.append(0)
        return seq3

    def shift_pattern(self):
        pass

    def make_new_pattern(self):
        num_tones = 12
        tone_range = 12
        transpose = 20
        octave_offset = 7
        number_of_tones_in_3rd_voice = 4
        word1 = choice(self.words)
        pure_seq1 = [(ord(char) % tone_range) for char in word1][:num_tones]
        applied_seq1 = list(itertools.chain(
            *zip([tone + transpose for tone in pure_seq1],
                 [0] * num_tones)))
        word2 = choice(self.words)
        pure_seq2 = [(ord(char) % tone_range) for char in word2][:num_tones]
        applied_seq2 = list(itertools.chain(
            *zip([0] * num_tones,
                 [tone + transpose for tone in pure_seq2])))
        seq3 = self._make_third_voice(num_tones, tranpose, number_of_tones_in_3rd_voice)
        self.pattern = {
            1: applied_seq1,
            2: applied_seq2,
            3: seq3,
            4: seq3
        }
