import threading
import itertools
from random import choice, randint, random

from roqba.composers.abstract_composer import AbstractComposer
from roqba.static.scales_and_harmonies import STRICT_HARMONIES, FOUR_NOTE_HARMONIES
from roqba.static.meters import METERS
from roqba.composers.rhythm_and_meter_mixin import RhythmAndMeterMixin

from roqba.utilities.sine_controllers import MultiSine
from roqba.utilities import pd_wavetables, naive_peak_detect


class Composer(RhythmAndMeterMixin, AbstractComposer):
    def __init__(self, gateway, settings, behaviour, scale="HARMONIC"):
        super(Composer, self).__init__(gateway,
                                       settings,
                                       behaviour)
        self.harm = {}
        self.speed_lim = behaviour['embellishment_speed_lim']
        self.selected_meters = ("meters" in self.behaviour.keys() and
                                self.behaviour["meters"] or METERS.keys())
        self.modified_note_in_current_frame = None
        self.generate_real_scale(settings['lowest_note_num'],
                                 settings['highest_note_num'])
        self.half_beat = self.behaviour['half_beat']
        self.second_beat_half = False

        # Rendezvous planning
        self.min_rendezvous_tickoffset = 2
        self.max_rendezvous_tickoffset = 12
        self.fixed_rendezvous_length = None
        self.max_rendezvous_length = 6
        self._setup_new_controller_wavetable()

        # Rendezvous handling
        self.num_rendezvous_between_caesurae = 15

        # setup state
        self.rendezvous_counter = 0
        self.ticks_counter = 0
        self.rendezvous_tick = False
        self.send_out_tick = -1
        self.select_next_harmony()
        self.select_next_anchor_tick(sendout_offset=1)
        self.prior_harmony = None

        self.set_binaural_diffs(self.behaviour['binaural_diff'])
        for voice in self.voices.values():
            voice.slide = False
            args = [random() * 0.3 for n in range(4)]
            voice.pan_sine = MultiSine(args)

    def generate(self, state):
        """main generating function, the next polyphonic step is produced here."""
        self.ticks_counter += 1
        self.comment = 'normal'
        send_to_notator = False
        current_slide_time = self.rendezvous_offset * state['speed'] * 1000
        if self.rendezvous_tick == self.ticks_counter:
            send_to_notator = True
            self.rendezvous_counter += 1
            if self.rendezvous_counter > self.num_rendezvous_between_caesurae:
                self.rendezvous_counter = 0
                self.comment = 'caesura'
            self.prior_harmony = self.next_harmony
            self.select_next_harmony()
            sendout_offset = (self.fixed_rendezvous_length
                              if self.fixed_rendezvous_length is not None
                              else randint(0, self.max_rendezvous_length))
            self.select_next_anchor_tick(sendout_offset=sendout_offset)
            self.gateway.set_slide_msecs_for_all_voices(current_slide_time)

        for voice in self.voices.values():
            if len(self.voices) < self.num_voices:
                raise (RuntimeError, "mismatch in voices count")
            next_note = self.next_voice_note(voice)
            if next_note:
                # send a rendezvous message
                # duration, start_index, end_index, start_note, end_note, start_multiplier and end_multiplier
                start_end = choice(
                    self.rendezvous_transitions['downwards' if next_note < voice.note else 'upwards'])
                self.gateway.pd.send([
                    "voice", voice.id, "rendezvous",
                    current_slide_time,
                    start_end['start'][0],  # index
                    start_end['end'][0],
                    voice.note, next_note,
                    start_end['start'][1],  # multiplier
                    start_end['end'][1],
                ])
            else:
                voice.note_change = False
                continue
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
            voice.update_current_microvolume()
            self.gateway.send_voice_pan(voice, voice.pan_sine.get_value())
            #self.gateway.send_voice_peak_level(voice, voice.current_microvolume)
        self.gateway.hub.send(self.voices)
        if send_to_notator:
            self.notator.note_to_file({"notes": self.prior_harmony,
                                       "weight": state["weight"],
                                       "cycle_pos": state["cycle_pos"]})
        return self.comment

    def _setup_new_controller_wavetable(self):
        self.controller_wavetable_string = pd_wavetables.random_wavetable(partials=randint(3, 10))
        self.controller_wavetable = pd_wavetables._apply_wavetable(self.controller_wavetable_string)
        self.controller_wavetable_extrema = naive_peak_detect.detect_local_extrema(self.controller_wavetable)
        self._extract_transitions()
        self.gateway.pd.send(["sys", "controller_wavetable", self.controller_wavetable_string])

    def select_next_harmony(self):
        """select the next rendezvous's harmony"""
        next_harmony_pattern = [0] + list(choice(STRICT_HARMONIES + FOUR_NOTE_HARMONIES))
        next_offset = randint(24, 36)  # TODO: make something musical
        self.next_harmony = [note + next_offset + (randint(0, 2) * 12) for note in next_harmony_pattern]

    def select_next_anchor_tick(self, sendout_offset=0):
        """set the next send-out and and rendezvous ticks"""
        self.send_out_tick = self.ticks_counter + sendout_offset
        self.rendezvous_offset = randint(self.min_rendezvous_tickoffset,
                                         self.max_rendezvous_tickoffset)
        self.rendezvous_tick = self.send_out_tick + self.rendezvous_offset

    def next_voice_note(self, voice):
        """return the next note for a voice if it is the correct tick"""
        if self.send_out_tick == self.ticks_counter:
            return self.next_harmony[voice.id - 1]
        return False

    def _extract_transitions(self):
        upwards = []
        downwards = []
        extrema = self.controller_wavetable_extrema
        all_ = itertools.permutations(extrema.keys(), 2)
        for start, end in all_:
            if extrema[start] == extrema[end]:
                continue
            elif extrema[start] > extrema[end]:
                target = downwards
            else:
                target = upwards
            target.append({
                'start': (start, extrema[start]),
                'end': (end, extrema[end])})
        self.rendezvous_transitions = {
            'upwards': upwards,
            'downwards': downwards,
        }
