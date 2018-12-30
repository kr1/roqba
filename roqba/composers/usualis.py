import threading
from random import choice, random

from roqba.composers.abstract_composer import AbstractComposer, ComposerError
from roqba.static.usualis import Ambitus, end_word, next_valid_word, Note
from roqba.utilities.sine_controllers import MultiSine

# http://www.teoria.com/en/reference/g-h/gregorian.php
ambitus_by_mode = {
    'plagal': Ambitus(-6, 6),
    'authentic': Ambitus(0, 12)
}


class Composer(AbstractComposer):
    def __init__(self, gateway, settings, behaviour, scale="DIATONIC"):
        # General
        super(Composer, self).__init__(gateway,
                                      settings,
                                      behaviour)
        self.new_random_mode()
        # specific
        self.set_scale(self.scale)
        self.lengthening_prob = 0.07
        self.current_max_length = 30
        self.current_note = Note(0, 1)
        self.notes_since_caesura = 0
        self.word = self.next_word(self.current_max_length)
        self.gateway.mute_voice("drums", 1)
        self.during_end_word = False
        self.current_note_counter = 0
        self.current_note_length = 1
        self.selected_meters = ['n/a']
        self.use_meter = False
        self.zero_note_offset = 30
        self.offered_scales = [scale for scale in self.offered_scales
                               if scale in ('DIATONIC', 'GREEK_CHROMATIC', 'GREEK_ENHARMONIC')]
        for voice in self.voices.values():
            voice.slide = False
            args = [random() * 0.3 for n in range(4)]
            voice.pan_sine = MultiSine(args)

            if not settings['enable_adsr']:
                self.gateway.pd.send(["voice", voice.id, "adsr_enable", 0])

    def new_random_mode(self):
        self.mode = choice(ambitus_by_mode.keys())
        self.ambitus = ambitus_by_mode[self.mode]
        self.tone = "1st {}".format(self.mode)
        self.musical_logger.info("mode: {}".format(self.tone))

    def high_limit(self):
        return self.zero_note_offset + self.ambitus.upper

    def low_limit(self):
        return self.zero_note_offset + self.ambitus.lower

    def melody_headroom(self):
        precise = self.ambitus.upper - self.current_note.note
        return precise if precise >= 0 else 0

    def melody_legroom(self):
        precise = self.ambitus.lower - self.current_note.note
        return precise if precise <= 0 else 0

    def next_word(self, current_max_length):
        self.position_in_word = 0
        self.drone = None
        self.during_end_word = False
        if self.notes_since_caesura > current_max_length:
            try:
                self.musical_logger.info("trying to get end word for current note: {}".format(self.current_note))
                word = end_word(self.current_note.note)
                self.drone = choice((1, -1))
                self.musical_logger.info("getting end word: {}, drone: {}".format(word, self.drone))
                self.during_end_word = True
                return word
            except IndexError as error:
                self.gateway.stop_all_notes()
                self.musical_logger.error("error finding clausula from this note: {}".format(self.current_note))
                return [Note(2, 1), Note(1, 1)] if self.current_note.note < 0 else [Note(-1, 1), Note(-2, 1)]
        headroom = self.melody_headroom()
        legroom = self.melody_legroom()
        # print self.current_note, headroom, legroom
        word = next_valid_word(self.current_note.note, headroom, legroom)
        first_note = word[0].note 
        self.drone =  first_note
        self.musical_logger.info("getting next word: {}, drone: {}".format(word, self.drone))
        return word

    def choose_rhythm(self):
        pass

    def get_next_note(self):
        try:
            note = self.word[self.position_in_word]
            if not self.during_end_word and not self.current_note == 'caesura':
                note = Note(self.current_note.note + note.note, note.length)
            self.position_in_word += 1
            if len(self.word) == self.position_in_word and self.during_end_word:
                self.drone = note.note
                self.musical_logger.info("final note")
            self.musical_logger.info(note)
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
        self.current_note_counter += 1
        if (self.current_note == 'caesura'
                or self.current_note_counter >= self.current_note.length):
            self.current_note = self.get_next_note()
            self.current_note_counter = 0
            self.notes_since_caesura += 1
        if self.current_note == 'caesura':
            self.during_end_word = False
            self.notes_since_caesura = 0
            self.new_random_mode()
            self.musical_logger.info("caesura")
            return 'caesura'
        if self.current_note_counter == 0:
            for voice in self.voices.values():
                if len(self.voices) < self.num_voices:
                    raise RuntimeError("mismatch in voices count")
                if voice.id == 1 and self.drone is not None and self.use_drone:
                    voice.note = self.drone
                    voice.note_change = True
                    voice.real_note = self.real_scale[voice.note + self.zero_note_offset]
                    voice.duration_in_msec = int(self.current_note.length * state["speed"] * 1000)
                    continue
                voice.note = self.current_note.note
                self.musical_logger.debug("note {0}".format(voice.note))
                if self.current_note is None or voice.note == 0:
                    continue
                voice.note_change = True
                voice.real_note = self.real_scale[self.current_note.note + self.zero_note_offset]
                voice.duration_in_msec = int(self.current_note.length * state["speed"] * 1000)

            self.musical_logger.info("real-note voice {}: {}".format(voice, voice.real_note))
            self.gateway.hub.send(self.voices)  # this sends the voices to the hub
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

    def set_meter(self, _):
        pass
