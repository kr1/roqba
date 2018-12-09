import os
import itertools
import threading
from random import choice

from roqba.composers.abstract_composer import AbstractComposer
from roqba.static.scales_and_harmonies import FOLLOWINGS


class Composer(AbstractComposer):
    def __init__(self, gateway, settings, behaviour, scale="DIATONIC"):
        # General
        super(Composer, self).__init__(gateway,
                                       settings,
                                       behaviour)
        self.selected_meters = [self.behaviour['meter']]
        self.half_beat = self.behaviour['half_beat']
        self.second_beat_half = False
        # Amadinda specific
        self.tone_range = behaviour['tone_range']
        self.sequence_length = behaviour['sequence_length']
        self.number_of_tones_in_3rd_voice = behaviour['number_of_tones_in_3rd_voice']
        self.pattern_played_times = 0
        self.pattern_played_maximum = 90
        self.words = self.all_python_words()
        self.octave_offset = behaviour['octave_offset']
        self.transpose = 20

        for voice in self.voices.values():
            voice.duration_in_msec = 600
        self.set_scale(self.scale)
        self.make_new_pattern()
        self.gateway.mute_voice("drums", 1)

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
            self.musical_logger.debug("note {0}".format(voice.note))
            if voice.note == 0 or not voice.note_change:
                continue
            voice.note_change = True
            next_note = self.next_voice_note(voice, meter_pos)
            tmp_harm.append(next_note)
        cycle_pos = state['cycle_pos']
        send_drum = True
        if self.half_beat:
            if cycle_pos % 2 == 0:
                cycle_pos = cycle_pos / 2
                if self.second_beat_half:
                    cycle_pos += int(self.meter[0] / 2)
                self.drummer.generator.send([state, cycle_pos])
            else:
                send_drum = False
        else:
            self.drummer.generator.send([state, cycle_pos])
        for k, v in self.drummer.frame.items():
            # TODO: re-add the drum filler
            if False and v["meta"]:
                if v["meta"] == 'empty':
                    threading.Thread(target=self.drum_fill_handler,
                                     args=(k, state)).start()
                if v["meta"] == 'mark':
                    threading.Thread(target=self.drum_mark_handler,
                                     args=(k, state)).start()
        if send_drum:
            self.gateway.drum_hub.send(self.drummer.frame)
        for voice in self.voices.values():
            self.gateway.send_voice_peak_level(voice, voice.current_microvolume)
        self.gateway.hub.send(self.voices)
        if self.notate:
            self.notator.note_to_file({"notes": tmp_harm,
                                       "weight": state["weight"],
                                       "cycle_pos": state["cycle_pos"]})
        return self.comment

    def next_voice_note(self, voice, meter_pos):
        voice.update_current_microvolume()
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
        which_shift_index = int(self.pattern_played_times / (self.pattern_played_maximum / 4.999))
        next_note = self.patterns[which_shift_index][voice.id][meter_pos] or None
        voice.note = next_note
        voice.real_note = next_note and self.real_scale[next_note] or None
        self.pattern_played_times += 1.0 / len(self.patterns[0][1])
        return next_note

    def make_new_pattern(self):
        word1 = choice(self.words)
        pure_seq1 = [(ord(char) % self.tone_range) for char in word1][:self.sequence_length]
        word2 = choice(self.words)
        pure_seq2 = [(ord(char) % self.tone_range) for char in word2][:self.sequence_length]
        self.pattern_played_times = 0
        self.patterns = {}
        for offset in range(0, 5):
            self.patterns[offset] = self.shift_pattern(pure_seq1, pure_seq2, offset)

    def shift_pattern(self, seq1, seq2, offset):
        return self._apply_new_pattern([(entry + offset) % self.tone_range for entry in seq1],
                                       [(entry + offset) % self.tone_range for entry in seq2],)

    def _apply_new_pattern(self, pure_seq1, pure_seq2):
        self.applied_seq1 = list(itertools.chain(
            *zip([tone + self.transpose for tone in pure_seq1],
                 [0] * self.sequence_length)))
        self.applied_seq2 = list(itertools.chain(
            *zip([0] * self.sequence_length,
                 [tone + self.transpose for tone in pure_seq2])))
        seq3 = self._make_third_voice(self.applied_seq1, self.applied_seq2)
        return {
            1: self.applied_seq1,
            2: self.applied_seq2,
            3: seq3,
            4: seq3
        }

    def _make_third_voice(self, applied_seq1, applied_seq2):
        seq3 = []
        for idx in range(self.sequence_length * 2):
            if (applied_seq1[idx] > 0
                    and applied_seq1[idx] < self.transpose + (self.number_of_tones_in_3rd_voice)):
                seq3.append(applied_seq1[idx] + (2 * self.octave_offset - 1))
            elif (applied_seq2[idx] > 0
                    and applied_seq2[idx] < self.transpose + (self.number_of_tones_in_3rd_voice)):
                seq3.append(applied_seq2[idx] + (2 * self.octave_offset - 1))
            else:
                seq3.append(0)
        return seq3
