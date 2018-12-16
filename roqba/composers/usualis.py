import threading
from random import choice

from roqba.composers.abstract_composer import AbstractComposer


class Usualis(AbstractComposer):
    def __init__(self, gateway, settings, behaviour, scale="DIATONIC"):
        # General
        super(Usualis, self).__init__(gateway,
                                      settings,
                                      behaviour)
        # specific
        self.tone_range = behaviour['tone_range']

        self.set_scale(self.scale)
        self.word = self.next_word()
        self.gateway.mute_voice("drums", 1)

    def words(self):
        return USUALIS_WORDS[self.full_tone]

    def end_words(self):
        return USUALIS_WORDS[self.full_tone]

    def next_word(self, notes_since_caesura, current_max_length):
        if notes_since_caesura > current_max_length:
            word = choice(self.end_words())
        word = choice(self.words())
        self.notes_since_caesura += len(word)
        return word

    def choose_rhythm(self):
        pass

    def get_next_note(self):
        pass

    def generate(self, state):
        """main generating function, the next polyphonic step is produced here

        any of the voices can change.
        """
        self.comment = 'normal'
        next_note = self.get_next_note()
        for voice in self.voices.values():
            if len(self.voices) < self.num_voices:
                raise (RuntimeError, "mismatch in voices count")
            self.musical_logger.debug("note {0}".format(voice.note))
            if voice.note == 0 or not voice.note_change:
                continue
            voice.note_change = True
            self.set_next_voice_note(voice, next_note)
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
