import random
import logging
from Queue import deque
from random import choice as sample

from static.movement_probabilities import DEFAULT_MOVEMENT_PROBS
from static.note_length_groupings import DEFAULT_NOTE_LENGTH_GROUPINGS as GROUPINGS
from static.note_length_groupings import analyze_grouping
from static.melodies import melodies
from static.scales_and_harmonies import FOLLOWINGS
from utilities.sine_controllers import MultiSine
from utilities import melody_player
from utilities import pd_wavetables as wavetables
from metronome import MEDIUM, HEAVY


class Voice(object):
    def __init__(self,
                 id,
                 composer,
                 note_range=[24, 48],
                 register=None,
                 behaviour=None,
                 note=None,
                 real_note=None,
                 note_length_grouping=sample(GROUPINGS)):

        # AFFILIATION
        self.composer = composer  # store the composer

        # IDENTITY
        self.id = id
        self.register = (self.composer.registers[register]
                         if register else
                         self.composer.registers[sample(self.composer.registers.keys())])

        # TECH
        self.track_me = False
        self.queue = deque([], composer.settings['track_voices_length'])

        # STARTUP
        self.pan_pos = composer.behaviour.voice_get(self.id, "default_pan_position")
        self.range = sorted(note_range)
        self.dir = 0
        self.prior_note = None
        self.note_change = True
        self.generator = self.voice()
        self.generator.next()  # set the coroutine to the yield-point
        self.counter = 0
        self.volume = composer.behaviour.voice_get(self.id, "default_volume")
        self.scale = composer.scale
        self.do_embellish = False
        self.note_delta = None
        self.weight = MEDIUM
        self.note = note or int((max(self.range)
                                 - min(self.range)) / 2) + min(self.range)
        self.real_note = (real_note
                          or int((max(self.range) - min(self.range)) / 2) + min(self.range))

        # BEHAVIOUR
        if behaviour:
            if isinstance(behaviour, basestring):
                self.behaviour = behaviour
            else:
                self.behaviour = behaviour[0]
                self.followed_voice_id = behaviour[1]
                self.following_counter = 0
                self.follow_limit = sample(range(5, 9))
        else:
            self.behaviour = self.composer.behaviour["default_behaviour"]
        self.should_play_a_melody = self.composer.behaviour.voice_get(
            self.id, 'should_play_a_melody')
        self.playing_a_melody = False
        self.duration_in_msec = 0
        self.change_rhythm_after_times = 1
        self.note_length_grouping = note_length_grouping
        self.set_rhythm_grouping(note_length_grouping)
        self.note_duration_steps = 1
        self.pause_prob = self.composer.behaviour.voice_get(self.id, 'default_pause_prob')
        self.legato_prob = 0.1  # to-do: really implement it
        # probability to have an embellishment-ornament during the current note
        self.embellishment_prob = self.composer.behaviour['default_embellishment_prob']
        self.movement_probs = DEFAULT_MOVEMENT_PROBS
        self.binaural_diff = 0  # this is not used in this module directly, but serves to track
        self.slide = self.composer.behaviour.voice_get(self.id, "automate_slide")
        self.slide_duration_prop = self.composer.behaviour.voice_get(
            self.id, 'slide_duration_prop')
        self.next_pat_length = None
        self.note_duration_prop = composer.behaviour['default_note_duration_prop']
        # WAVETABLE - this is used for non-automated wavetables
        self.wavetable_generation_type = sample(
            composer.behaviour.voice_get(self.id, 'wavetable_specs'))[0]
        self.partial_pool = sample(
            sample(self.composer.behaviour.voice_get(self.id, 'wavetable_specs'))[1])
        self.num_partials = composer.behaviour.voice_get(self.id, 'default_num_partial')

        self.set_state(register)
        self.add_setters_for_behaviour_dict()
        self.musical_logger = logging.getLogger('musical')
        if self.composer.behaviour['automate_microvolume_change']:
            self.new_microvolume_sine()
            self.microvolume_variation = self.composer.behaviour.voice_get(
                self.id, 'microvolume_variation')
            self.current_microvolume = self.update_current_microvolume()

    def new_microvolume_sine(self):
        args = [random.random() * self.composer.behaviour['microvolume_max_speed_in_hz']
                for n in range(10)]
        self.microvolume_sine = MultiSine(args)

    def update_current_microvolume(self):
        self.current_microvolume = self.microvolume_sine.get_value_as_factor(
            self.microvolume_variation)

    def add_setters_for_behaviour_dict(self):
        beh = self.composer.behaviour['per_voice'][self.id]
        beh.real_setters["slide_duration_prop"] = [setattr, self, "slide_duration_prop"]
        beh.real_setters["binaural_diff"] = [setattr, self, "binaural_diff"]

    def set_pan_pos(self, gateway, pan_pos):
        self.pan_pos = pan_pos
        gateway.send_voice_pan(self, pan_pos)

    def __str__(self):
        return str({"note": self.note,
                    "dir": self.dir,
                    "id": self.id,
                    "note_change": self.note_change})

    def __repr__(self):
        return "{0} - {1}".format(self.__class__, self.__str__())

    def voice(self):
        """the generator method of the Voice-class"""
        while True:
            state = (yield)
            meter_pos = state['cycle_pos']
            #print self.on_off_pattern, " for: ", self.id
            self.note_change = self.on_off_pattern[meter_pos]
            if random.random() < self.legato_prob:
                self.note_change = 0
            self.weight = state["weight"]
            if self.note_change:
                # calculate duration by checking for the next note
                # in the pattern
                tmp_list = self.on_off_pattern[(meter_pos + 1):]
                if 1 in tmp_list:
                    self.note_duration_steps = tmp_list.index(1) + 1
                else:
                    #self.note_duration_steps = 1
                    self.note_duration_steps = len(self.on_off_pattern) - meter_pos
                self.prior_note = self.note
                if random.random() < self.pause_prob and not self.playing_a_melody:
                    self.note = 0
                else:
                    self.note = self.next_note(state)
                    self.note_delta = self.note - self.prior_note
                if self.track_me:
                    self.queue.append(self.note)
                if random.random() < self.embellishment_prob:
                    self.do_embellish = True

    def next_note(self, state):
        """the next note is calculated/read here"""
        meter_pos = state["cycle_pos"]
        if self.behaviour == "SLAVE":
            follow = self.other_voices[self.followed_voice_id]
            if follow.note_change:
                if follow.note == 0:
                    return 0
                if self.following_counter == 0:
                    self.follow_dist = sample(FOLLOWINGS)
                if self.following_counter < self.follow_limit:
                    res = follow.note + self.follow_dist
                    self.following_counter += 1
                    return res
                else:
                    self.reset_slave()

        move = sample([-1, 1]) * sample(self.movement_probs)
        if self.dir:
            move = (self.dir * sample(self.movement_probs))
        elif self.playing_a_melody:
            try:
                move = self.manage_melody_note(meter_pos)
            except StopIteration:
                self.musical_logger.info("melody finished")
                self.playing_a_melody = False
        else:
            if (self.should_play_a_melody and self.note != 0 and
                    self.weight in [HEAVY, MEDIUM]):
                #if (self.melody_starts_on == (self.note % 7) and
                    # regarding the on-off pattern we try a minimum invasive strategy
                    # by modifying only those indexes of the pattern covered by the
                    # current note and the start of the following note
                #print "searching for a suitable melody"
                self.melody = self.search_suitable_melody(state['speed'])
                if self.melody:
                    self.musical_logger.info("starting the melody: {0}".format(self.melody))
                    self.melody_iterator = iter(self.melody["melody"])
                    move = self.manage_melody_note(meter_pos)
                    self.playing_a_melody = True
        res = self.note + move
        exceed = self.exceeds(res)
        if not self.playing_a_melody:
            if exceed:
                res, self.dir = exceed
                # self.musical_logger.info(
                #     "exceeding note of voice {2}: '{0}', going: \t{1}".format(res,
                #      self.dir > 0 and 'up' or 'down',
                #      self.id))
            if self.in_the_middle(res):
                self.dir = 0
            if self.exceeds(res):
                raise RuntimeError('''diabolus in musica: {0} is too low/high,
                             dir:{1}'''.format(res, self.dir))
        return res

    def search_suitable_melody(self, speed):
        candidates = []
        for melody_name, melody in melodies.items():
            speed_range = melody["speed_range"]
            right_note = self.note % 7 == melody["start_note"]
            right_scale = self.composer.scale == melody["scale"]
            right_speed = speed_range[0] < speed < speed_range[1]
            right_meter = self.composer.meter in melody["meters"]
            if right_note and right_scale and right_speed and right_meter:
                candidates.append({melody_name: melody})
        if len(candidates) > 0:
            chosen = sample(candidates).items()[0]
            self.musical_logger.info("new melody: {0}".format(chosen[0]))
            return chosen[1]

    def manage_melody_note(self, meter_pos):
        """retrieves next note-delta and length belonging to the melody.

        sets the following 'bits' of the off-on-pattern according to the
        specified length of the note.
        returns the pitch-related move (delta) and sets eventual modifier
        attribute on the composer"""
        move, length = self.melody_iterator.next()
        if type(move) == str:
            number, modifier = melody_player.extract_modified_move(move)
            self.composer.modified_note_in_current_frame = (number,
                                                            modifier)
            move = number
        if self.melody_iterator.__length_hint__() == 1:
            # TODO: communicate to director that a caesura is required
            pass
        self.musical_logger.info("melody move: {0} \tof length: {1} ".format(move, length))
        oop = self.on_off_pattern
        oop[meter_pos] = 1
        remaining = len(oop) - meter_pos
        if remaining < length:
            this_pat_length = remaining
            self.musical_logger.info("dbg: overhanging note")
            oop += [0] * (length - remaining) + [1]
            self.next_pat_length = length - remaining
            # self.apply_overhanging_notes()
        else:
            this_pat_length = length
            # this is for the following note,
            # if it is not run the next pattern will start with a note
            # anyway
            try:
                self.on_off_pattern[meter_pos + length] = 1
            except IndexError:
                pass
        for note_unit in range(1, this_pat_length):
            self.on_off_pattern[meter_pos + note_unit] = 0
        # Note: we set next_pat_length int if note is longer than the remaining
        # part of the cycle. upon next cycle the rest of the note is
        # applied to the new on-off-pattern.
        return move

    def apply_overhanging_notes(self):
        """applies overhanging notes of a registered melody

        to the next <on_off_pattern>"""
        if len(self.on_off_pattern) > self.next_pat_length:
            for idx in range(self.next_pat_length):
                self.on_off_pattern[idx] = 0
            # this might do the roundtrip.....
            # self.on_off_pattern[idx + 1] = 1
            self.next_pat_length = None
        else:
            self.next_pat_length -= len(self.on_off_pattern)

    def exceeds(self, note):
        """returns min/max limits and a bounce back direction coefficient

        if incoming int exceeds limits, returns False otherwise"""
        if self.composer.scale in ["PENTATONIC", "PENTA_MINOR"]:
            range = [int((x / 7.0) * 5) for x in self.range]
        else:
            range = self.range
        if note > range[1]:
            return (range[1] - sample([0, 0, 1, 1, 2]), -1)
        elif note < range[0]:
            return (range[0] + sample([0, 0, 1, 1, 2]), 1)
        else:
            False

    def set_rhythm_grouping(self, grouping):
        """setter method which creates also the on/off pattern"""
        if self.counter % self.change_rhythm_after_times == 0:
            self.note_length_grouping = grouping
            self.on_off_pattern = analyze_grouping(grouping)
            # here we check if we are playing a melody and if so if we have
            # remaining note parts to be applied.
            if self.playing_a_melody:
                if self.next_pat_length:
                    self.apply_overhanging_notes()
        self.counter += 1

    def in_the_middle(self, note):
        """returns true if int is in the center area of the range"""
        range_span = self.range[1] - self.range[0]
        lower_thresh = self.range[0] + (range_span * 0.333)
        upper_thresh = self.range[0] + (range_span * 0.666)
        return note > lower_thresh and note < upper_thresh

    def reset_slave(self, change_master=False):
        """resets values for slave voices.

        if <change_master> is an int:
          - it is used as the id new master-voice
        if <change_master> is 'True':
          - a new random master is chosen,
        """
        if change_master:
            if type(change_master) == int:
                self.followed_voice_id = change_master
            else:
                self.followed_voice_id = sample(self.others.keys())
        follow = self.other_voices[self.followed_voice_id]
        self.slide_duration_prop = follow.slide_duration_prop
        self.slide = follow.slide
        self.following_counter = 0
        self.follow_limit = sample(range(3, 9))

    def set_state(self, name):
        '''sets the state for the voice.

        state is one of "BASS", "ROCK_BASS", "MID", "HIGH", or "SLAVE".
        the state is a set of common settings for the voice, e.g.
        voice-range, embellishment probability, rhythmic variation,
        movement-mode, etc.'''
        self.reload_register()
        if name == "BASS":
            #self.behaviour = "AUTONOMOUS"
            self.note_length_groupings = self.composer.HEAVY_GROUPINGS
        if name == "ROCK_BASS":
            #self.behaviour = "AUTONOMOUS"
            self.note_length_groupings = self.composer.FAST_GROUPINGS
        elif name == "FLAT_MID":
            self.note_length_groupings = self.composer.FAST_GROUPINGS
        elif name == "MID":
            #self.behaviour = "AUTONOMOUS"
            self.note_length_groupings = self.composer.DEFAULT_GROUPINGS
        elif name == "HIGH":
            #self.behaviour = "AUTONOMOUS"
            self.note_length_groupings = self.composer.TERNARY_GROUPINGS

    def register_other_voices(self):
        '''returns the other voices registered in the app'''
        self.other_voices = {}
        for k, v in self.composer.voices.items():
            if v != self:
                self.other_voices[k] = v

    def reload_register(self):
        '''reloads the current register and reapplies its settings

        - in voice
        - in the controller'''
        #print "reloading register: {0}".format(name)
        for k, v in self.register["voice_attrs"].items():
            setattr(self, k, v)
        for k, v in self.register["voice_composer_attrs"].items():
            setattr(self, k, getattr(self.composer, v))
        self.counter = 0

    def make_wavetable(self):
        '''assembles a wavetable

        using the registered wavetable-related params'''
        fun = getattr(wavetables, self.wavetable_generation_type + '_wavetable')
        return fun(self.num_partials, self.partial_pool)


if __name__ == "__main__":
    from composer import Composer
    c = Composer()
    print Voice("", "", c).in_the_middle(45)
