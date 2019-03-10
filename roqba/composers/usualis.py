import threading
from random import choice, random

from roqba.composers.abstract_composer import AbstractComposer, ComposerError
from roqba.static.usualis import Ambitus, end_word, safe_next_valid_word, Note
from roqba.utilities.sine_controllers import MultiSine

# http://www.teoria.com/en/reference/g-h/gregorian.php
ambitus_by_mode = {
    'plagal': Ambitus(-6, 6),
    'authentic': Ambitus(0, 12)
}


class Composer(AbstractComposer):
    def __init__(self, gateway, settings, behaviour, scale="DIATONIC"):
        super(Composer, self).__init__(gateway,
                                      settings,
                                      behaviour)
        self.min_phrase_length = behaviour['min_phrase_length']
        self.max_double_length_prob = behaviour['max_double_length_prob']
        self.max_triple_length_prob = behaviour['max_triple_length_prob']
        self.min_double_length_prob = behaviour['min_double_length_prob']
        self.min_triple_length_prob = behaviour['min_triple_length_prob']
        self.drone_prob = behaviour['drone_prob']
        self.new_random_mode()
        self.set_scale(self.scale)
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
                               if scale in ('DIATONIC', 'GREEK_CHROMATIC', 'GREEK_ENHARMONIC',
                                            'PERSIAN_SEGAH', 'PERSIAN_SHUR')]
        for voice in list(self.voices.values()):
            voice.slide = False
            args = [random() * 0.3 for n in range(4)]
            voice.pan_sine = MultiSine(args)

            if not settings['enable_adsr']:
                self.gateway.pd.send(["voice", voice.id, "adsr_enable", 0])

    def new_random_mode(self):
        double_length_prob_range = (self.max_double_length_prob -
                                    self.min_double_length_prob)
        triple_length_prob_range = (self.max_triple_length_prob -
                                    self.min_triple_length_prob)
        self.double_length_prob = (random() * double_length_prob_range +
                                   self.min_double_length_prob)
        self.triple_length_prob = (random() * triple_length_prob_range +
                                   self.min_triple_length_prob)
        self.use_drone = random() < self.drone_prob
        self.current_max_length = int(random() * self.min_phrase_length)
        self.mode = choice(list(ambitus_by_mode.keys()))
        self.ambitus = ambitus_by_mode[self.mode]
        self.tone = "1st {}".format(self.mode)
        self.musical_logger.info("mode: {}".format(self.tone))

    def high_limit(self):
        return self.zero_note_offset + self.ambitus.upper

    def low_limit(self):
        return self.zero_note_offset + self.ambitus.lower

    def melody_headroom(self, ref_note):
        precise = self.ambitus.upper - ref_note
        return precise if precise >= 0 else 0

    def melody_legroom(self, ref_note):
        precise = self.ambitus.lower - ref_note
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
                self._log_word(word, 'selected end word: ')
                self.during_end_word = True
                return word
            except IndexError as error:
                self.gateway.stop_all_notes()
                self.musical_logger.error("error finding clausula from this note: {}".format(self.current_note))
                return [Note(2, 1), Note(1, 1)] if self.current_note.note < 0 else [Note(-1, 1), Note(-2, 1)]
        ref_note = 0 if self.current_note == 'caesura' else self.current_note.note
        headroom = self.melody_headroom(ref_note)
        legroom = self.melody_legroom(ref_note)
        word = safe_next_valid_word(ref_note, headroom, legroom, self.double_length_prob,
            self.triple_length_prob)
        first_note = word[0].note
        self.drone = first_note
        self._log_word(word, 'getting next word: ')
        return word

    def choose_rhythm(self):
        pass

    def get_next_note(self):
        try:
            if self.current_note == 'caesura':
                self.word = self.next_word(self.current_max_length)
            new_note = self.word[self.position_in_word]
        except IndexError:
            self.position_in_word = 0
            if self.during_end_word is True:
                return 'caesura'
            self.word = self.next_word(self.current_max_length)
            return self.get_next_note()
        if new_note == 'caesura':
            return 'caesura'
        if not self.during_end_word:
            ref_note = 0 if self.current_note == 'caesura' else self.current_note.note
            new_note = Note(ref_note + new_note.note, new_note.length)
        else:
            self.musical_logger.info("new end-word note: {}".format(new_note))
        self.current_note = new_note
        self.position_in_word += 1
        if len(self.word) == self.position_in_word and self.during_end_word:
            self.drone = new_note.note
            self.musical_logger.info("final note")
        self.musical_logger.info(new_note)
        return new_note

    def _log_word(self, word, prefix='word: '):
        if self.use_drone:
            drone_segment = ", drone: {}".format(self.drone)
        else:
            drone_segment = ""
        self.musical_logger.info("{}{}{}".format(prefix,
            [item.note for item in word], drone_segment))

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
            for voice in list(self.voices.values()):
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
                voice.note_change = True
                voice.real_note = self.real_scale[self.current_note.note + self.zero_note_offset]
                voice.duration_in_msec = int(self.current_note.length * state["speed"] * 1000)
                if self.current_note is None or voice.real_note == 0:
                    continue

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
        return ("<Usualis composer with tone: {}, current: {}\n"
                "scale: {}\nnotes since caesura: {}\nminimum phrase length: {}\n"
                "using drone: {}, note_lengthening_probs: 3: {} - 2: {}>").format(
                        self.tone, self.current_note, self.scale, self.notes_since_caesura,
                        self.min_phrase_length, self.use_drone, self.triple_length_prob,
                        self.double_length_prob)

    def set_meter(self, _):
        pass
