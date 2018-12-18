import threading
from random import choice, random

from roqba.composers.abstract_composer import AbstractComposer
from roqba.static.usualis import end_word, next_valid_word, Note


class Composer(AbstractComposer):
    def __init__(self, gateway, settings, behaviour, scale="DIATONIC"):
        # General
        super(Composer, self).__init__(gateway,
                                      settings,
                                      behaviour)
        # specific
        self.set_scale(self.scale)
        self.lengthening_prob = 0.07
        self.current_max_length = 30
        self.current_note = Note(0, 1)
        self.tone = "1st plagal"
        self.notes_since_caesura = 0
        self.word = self.next_word(self.current_max_length)
        self.gateway.mute_voice("drums", 1)
        self.during_end_word = False
        self.current_note_counter = 0
        self.current_note_length = 1

    def high_limit(self):
        return 2

    def low_limit(self):
        return -2

    def next_word(self, current_max_length):
        self.position_in_word = 0
        self.during_end_word = False
        if self.notes_since_caesura > current_max_length:
            self.musical_logger.info("getting next word")
            try:
                word = end_word(self.current_note)
                self.during_end_word = True
                return word
            except IndexError:
                pass
        word = next_valid_word(self.current_note, self.high_limit(), self.low_limit())
        return word

    def choose_rhythm(self):
        pass

    def get_next_note(self):
        try:
            note = self.word[self.position_in_word]
            self.position_in_word += 1
            return note
        except IndexError:
            self.position_in_word = 0
            if self.during_end_word is True:
                return 'caesura'
            self.word = self.next_word(self.current_max_length)
            return self.get_next_note()

    def generate(self, state):
        """main generating function, the next polyphonic step is produced here

        any of the voices can change.
        """
        self.comment = 'normal'
        self.current_note_counter += 1
        self.notes_since_caesura += 1
        if self.current_note_counter >= self.current_note.length:
            self.current_note = self.get_next_note()
            self.current_note_counter = 0
        else:
            return
        if self.current_note == 'caesura':
            self.comment = 'caesura'
            self.notes_since_caesura = 0
            return 'caesura'
        for voice in self.voices.values():
            if len(self.voices) < self.num_voices:
                raise (RuntimeError, "mismatch in voices count")
            self.musical_logger.debug("note {0}".format(voice.note))
            if self.current_note is None or voice.note == 0 or not voice.note_change:
                continue
            voice.note_change = True
            voice.note = self.current_note.note
        #  TODO: add drums
        # send_drum = True
        # self.drummer.generator.send([state, cycle_pos])
        # for k, v in self.drummer.frame.items():
        #     # TODO: re-add the drum filler
        #     if False and v["meta"]:
        #         if v["meta"] == 'empty':
        #             threading.Thread(target=self.drum_fill_handler,
        #                              args=(k, state)).start()
        #         if v["meta"] == 'mark':
        #             threading.Thread(target=self.drum_mark_handler,
        #                              args=(k, state)).start()
        # if send_drum:
        #     self.gateway.drum_hub.send(self.drummer.frame)
        # for voice in self.voices.values():
        #     self.gateway.send_voice_peak_level(voice, voice.current_microvolume)
        # self.gateway.hub.send(self.voices)
        # if self.notate:
        #     self.notator.note_to_file({"notes": tmp_harm,
        #                                "weight": state["weight"],
        #                                "cycle_pos": state["cycle_pos"]})
        return self.comment

    def set_next_voice_note(self, voice, next_note):
        voice.update_current_microvolume()
        voice.note = next_note
        voice.real_note = next_note and self.real_scale[next_note] or None
        return next_note

    def __repr__(self):
        return "<Usualis composer with tone: {}, current: {}>".format(self.tone, self.current_note)
