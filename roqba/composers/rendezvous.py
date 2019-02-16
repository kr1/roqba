import threading
from random import choice, randint, random

from roqba.composers.abstract_composer import AbstractComposer
from roqba.static.scales_and_harmonies import STRICT_HARMONIES, FOUR_NOTE_HARMONIES
from roqba.static.meters import METERS
from roqba.composers.rhythm_and_meter_mixin import RhythmAndMeterMixin

from roqba.utilities.sine_controllers import MultiSine
from roqba.utilities import pd_wavetables, wavetable_peaks


class Composer(RhythmAndMeterMixin, AbstractComposer):
    def __init__(self, gateway, settings, behaviour, scale="HARMONIC"):
        super(Composer, self).__init__(gateway,
                                       settings,
                                       behaviour)
        self.harm = {}
        self.speed_lim = behaviour['embellishment_speed_lim']
        self.selected_meters = ("meters" in list(self.behaviour.keys()) and
                                self.behaviour["meters"] or list(METERS.keys()))
        self.modified_note_in_current_frame = None
        self.generate_real_scale(settings['lowest_note_num'],
                                 settings['highest_note_num'])
        self.half_beat = self.behaviour['half_beat']
        self.second_beat_half = False

        # Rendezvous planning
        self.min_rendezvous_tickoffset = behaviour['min_rendezvous_tickoffset']
        self.max_rendezvous_tickoffset = behaviour['max_rendezvous_tickoffset']
        self.fixed_rendezvous_length = behaviour['fixed_rendezvous_length']
        self.min_rendezvous_length = behaviour['min_rendezvous_length']
        self.max_rendezvous_length = behaviour['max_rendezvous_length']
        self._setup_new_controller_wavetable()
        self.strategy_max_deviation_mapping = {
            'conservative': 1.0,
            'lax': 2.0,
            'outgoing': 3.0,
            'random': 1000
        }
        # Rendezvous handling
        self.num_rendezvous_between_caesurae = behaviour['num_rendezvous_between_caesurae']

        # setup state
        self.rendezvous_counter = 0
        self.ticks_counter = 0
        self.rendezvous_tick = False
        self.send_out_tick = -1
        self.select_next_harmony()
        self.select_next_anchor_tick(sendout_offset=1)
        self.prior_harmony = None

        self.set_binaural_diffs(self.behaviour['binaural_diff'])
        for voice in list(self.voices.values()):
            voice.slide = False
            args = [random() * 0.3 for n in range(4)]
            voice.pan_sine = MultiSine(args)

            if not settings['enable_adsr']:
                self.gateway.pd.send(["voice", voice.id, "adsr_enable", 0])

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
                              else randint(self.min_rendezvous_length,
                                           self.max_rendezvous_length))
            self.select_next_anchor_tick(sendout_offset=sendout_offset)
        if self.send_out_tick == self.ticks_counter and self.behaviour['common_transitions']:
            transitions = self.determine_rendezvous_transition()
        for voice in list(self.voices.values()):
            if len(self.voices) < self.num_voices:
                raise RuntimeError("mismatch in voices count")
            next_note = self.next_voice_note(voice)
            if next_note:
                # send a rendezvous message
                # duration, start_index, end_index, start_note, end_note, start_multiplier
                # and end_multiplier
                if not self.behaviour['common_transitions']:
                    transitions = self.determine_rendezvous_transition(voice)
                transition = choice(transitions['downwards' if next_note <= voice.note else 'upwards'])

                self.gateway.pd.send([
                    "voice",
                    voice.id,
                    "rendezvous",
                    current_slide_time,
                    transition['start'][0],  # index
                    transition['end'][0],
                    voice.note, next_note,
                    transition['start'][1],  # multiplier
                    transition['end'][1],
                ])
                voice.note = next_note
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
        for k, v in list(self.drummer.frame.items()):
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
        for voice in list(self.voices.values()):
            voice.update_current_microvolume()
            self.gateway.send_voice_pan(voice, voice.pan_sine.get_value())
            # self.gateway.send_voice_peak_level(voice, voice.current_microvolume)
        if self.notate and send_to_notator:
            self.notator.note_to_file({"notes": self.prior_harmony,
                                       "weight": state["weight"],
                                       "cycle_pos": state["cycle_pos"]})
        return self.comment

    def determine_rendezvous_transition(self, voice=None):
        if self.behaviour['transition_strategy'] == 'direct':
            transitions = self._direct_transitions()
        elif self.behaviour['transition_strategy'] in list(self.strategy_max_deviation_mapping.keys()):
            transitions = self._transitions_by_deviation(self.behaviour['transition_strategy'])
        else:
            transitions = {
                'upwards': choice(self.rendezvous_transitions['upwards']),
                'downwards': choice(self.rendezvous_transitions['downwards'])
            }
        return transitions

    def _setup_new_controller_wavetable(self):
        self.controller_wavetable_string = pd_wavetables.random_wavetable(partials=randint(3, 10))
        self.gateway.pd.send(["sys", "controller_wavetable", self.controller_wavetable_string])
        self.controller_wavetable = pd_wavetables._apply_wavetable(self.controller_wavetable_string)
        # the transitions are used for the single voices moving from one peak point to another
        self.rendezvous_transitions = wavetable_peaks.extract_peak_passages(
            self.controller_wavetable)

    def select_next_harmony(self):
        """select the next rendezvous's harmony"""
        next_harmony_pattern = [0] + list(choice(STRICT_HARMONIES + FOUR_NOTE_HARMONIES))
        next_offset = randint(24, 48)  # TODO: make something musical
        self.next_harmony = [note + next_offset + (randint(0, 2) * 12)
                             for note in next_harmony_pattern]

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

    def _transitions_by_deviation(self, max_deviation):
        return {'upwards': [transition for transition in self.rendezvous_transitions['upwards']
                            if transition['deviation'] <= max_deviation],
                'downwards': [transition for transition in self.rendezvous_transitions['downwards']
                              if transition['deviation'] <= max_deviation]}

    def _direct_transitions(self):
        return {'upwards': [transition for transition in self.rendezvous_transitions['upwards']
                            if not transition['in_between']],
                'downwards': [transition for transition in self.rendezvous_transitions['downwards']
                              if not transition['in_between']]}
