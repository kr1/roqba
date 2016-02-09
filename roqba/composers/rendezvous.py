import threading
from random import choice, random, randint

from roqba.composers.abstract_composer import AbstractComposer
from roqba.static.scales_and_harmonies import STRICT_HARMONIES
from roqba.static.meters import METERS
from roqba.composers.rhythm_and_meter_mixin import RhythmAndMeterMixin

from roqba.utilities.sine_controllers import MultiSine


class Composer(RhythmAndMeterMixin, AbstractComposer):
    def __init__(self, gateway, settings, behaviour, scale="DIATONIC"):
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
        self.half_beat = self.behaviour['half_beat']
        self.second_beat_half = False
        self.ticks_counter = 0
        self.next_anchor_tick = False
        self.send_out_tick = -1
        for voice in self.voices.values():
            args = [random() * 0.5 for n in range(5)]
            voice.freq_sine = MultiSine(args)

    def generate(self, state):
        """main generating function, the next polyphonic step is produced here

        any of the voices can change.
        """
        self.ticks_counter += 1
        self.comment = 'normal'
        tmp_harm = []
        meter_pos = state['cycle_pos']
        if self.next_anchor_tick == self.ticks_counter:
            self.select_next_harmony()
            self.select_next_anchor_tick(offset=randint(3, 6))

        for voice in self.voices.values():
            if len(self.voices) < self.num_voices:
                raise (RuntimeError, "mismatch in voices count")
            next_note = self.next_voice_note(voice)
            if next_note:
                tmp_harm.append(next_note)
                voice.note = next_note
                voice.real_note = next_note
                voice.note_change = True
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
            self.gateway.send_voice_peak_level(voice, voice.current_microvolume)
        self.gateway.hub.send(self.voices)
        self.notator.note_to_file({"notes": [int(note) for note in tmp_harm],
                                   "weight": state["weight"],
                                   "cycle_pos": state["cycle_pos"]})
        return self.comment

    def select_next_harmony(self):
        next_harmony_pattern = choice(STRICT_HARMONIES)
        next_offset = randint(30, 60)
        self.next_harmony = [note + next_offset for note in next_harmony_pattern]

    def select_next_anchor_tick(self, sendout_offset=0):
        self.send_out_tick = self.ticks_counter + sendout_offset
        self.next_anchor_tick = self.send_out_tick + randint(self.min_rendezvous_tickoffset,
                                                             self.max_rendezvous_tickoffset)

    def next_voice_note(self, voice):
        if self.send_out_tick == self.ticks_counter:
            return self.next_harmony[voice.id - 1]
        return False
