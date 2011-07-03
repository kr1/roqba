import random
from Queue import deque
from random import choice as sample

from static.movement_probabilities import DEFAULT_MOVEMENT_PROBS
from static.note_length_groupings import DEFAULT_NOTE_LENGTH_GROUPINGS as GROUPINGS
from static.note_length_groupings import  analyze_grouping
from metronome import MEDIUM, HEAVY


class Voice(object):
    def __init__(self, id,
                       composer,
                       note_range=[24, 48],
                       register=None,
                       behaviour=None,
                       note=None,
                       real_note=None,
                       note_length_grouping=sample(GROUPINGS)):
        # AFFILIATION
        self.composer = composer  # store the composer
        composer.add_voice(id, self)  # register with the composer
        # IDENTITY
        self.id = id
        self.register = (self.composer.registers[register]
                      if register else
                  composer.registers[sample(self.composer.registers.keys())])
        # TECH
        self.track_me = False
        self.queue = deque([], composer.settings['track_voices_length'])
        # STARTUP
        note_range.sort()
        self.pan_position = composer.behaviour.voice_get(self.id, "default_pan_position")
        self.range = note_range
        self.dir = 0
        self.prior_note = None
        self.note_change = True
        self.generator = self.voice()
        self.generator.next()  # set the coroutine to the yield-point
        self.counter = 0
        self.scale = composer.scale
        self.do_embellish = False
        self.note_delta = None
        self.weight = MEDIUM
        self.note = note or int((max(self.range)
                                 - min(self.range)) / 2) + min(self.range)
        self.real_note = real_note or int((max(self.range)
                                 - min(self.range)) / 2) + min(self.range)

        # BEHAVIOUR
        if behaviour:
            self.behaviour = behaviour[0]
            self.followed_voice_id = behaviour[1]
            self.following_counter = 0
            self.follow_limit = sample(range(3, 9))
        else:
            self.behaviour = composer.behaviour["default_behaviour"]
        self.should_play_a_melody = composer.behaviour.voice_get(id, 'should_play_a_melody')
        mel = self.should_play_a_melody
        if mel:
            self.melody = mel[1]
            self.melody_starts_on = mel[0]
        self.playing_a_melody = False 
        self.duration_in_msec = 0
        self.change_rhythm_after_times = 1
        self.note_length_grouping = note_length_grouping
        self.set_rhythm_grouping(note_length_grouping)
        self.note_duration_steps = 1
        self.pause_prob = composer.behaviour.voice_get(id, 'default_pause_prob')
        self.legato_prob = 0.1  # to-do: really implement it
        # probability to have an embellishment-ornament during the current note
        self.embellishment_prob = composer.behaviour['default_embellishment_prob']
        self.movement_probs = DEFAULT_MOVEMENT_PROBS
        self.slide = composer.behaviour.voice_get(id, "automate_slide")
        self.slide_duration_prop = composer.behaviour.voice_get(id, 'default_slide_duration_prop')
        self.next_pat_length = None
        self.note_duration_prop = composer.behaviour['default_note_duration_prop']
        self.set_state(register)

    def __str__(self):
        return str({"note": self.note,
                    "dir": self.dir,
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
                    self.note_duration_steps = 1
                self.prior_note = self.note
                if random.random() < self.pause_prob:
                    self.note = 0
                else:
                    self.note = self.next_note(meter_pos)
                    self.note_delta = self.note - self.prior_note
                if self.track_me:
                    self.queue.append(self.note)
                if random.random() < self.embellishment_prob:
                    self.do_embellish = True

    def next_note(self, meter_pos):
        """the next note is calculated/read here"""
        move = sample([-1, 1]) * sample(self.movement_probs)
        if self.dir:
            move = (self.dir * sample(self.movement_probs))
        elif self.playing_a_melody:
            try:
                move = self.manage_melody_note(meter_pos)
                print "move {0} ".format(move)
            except StopIteration:
                self.playing_a_melody = False
        else:
            if self.should_play_a_melody and self.note != 0:
                if (self.melody_starts_on == (self.note % 7) and
                    self.weight in [HEAVY, MEDIUM]):
                    print "starting the melody"
                    # regarding the on-off pattern we try a minimum invasive strategy
                    # by modifying only those indexes of the pattern covered by the 
                    # current note and the start of the following note 
                    self.melody_iterator = iter(self.melody)
                    move = self.manage_melody_note(meter_pos)
                    self.playing_a_melody = True
        res = self.note + move
        exceed = self.exceeds(res)
        if exceed:
            #print "exceed"
            res, self.dir = exceed
        if self.in_the_middle(res):
            self.dir = 0
        if self.exceeds(res):
            raise RuntimeError('''diabolus in musica: {0} is too low/high,
                         dir:{1}'''.format(res, self.dir))
        return res

    def manage_melody_note(self, meter_pos):
        """retrieves next note-delta and length belonging to the melody.

        sets the following 'bits' of the off-on-pattern according to the 
        specified length of the note.
        returns the pitch-related move (delta)"""
        move, length = self.melody_iterator.next()
        oop = self.on_off_pattern
        oop[meter_pos] = 1
        remaining = len(oop) - meter_pos
        if remaining < length:
            this_pat_length = remaining
            self.next_pat_length = length - remaining
            self.apply_overhanging_notes()
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
        if len(self.on_off_pattern) > self.next_pat_length:
            for idx in range(self.next_pat_length):
                self.on_off_pattern[idx] = 0
            self.on_off_pattern[idx + 1] = 1
            self.next_pat_length = None
        else:
            self.next_pat_length -= self.on_off_pattern

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
        self.others = self.other_voices()
        if change_master:
            if type(change_master) == int:
                self.followed_voice_id = change_master
            else:
                self.followed_voice_id = sample(self.others.keys())
        follow = self.others[self.followed_voice_id]
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

    def other_voices(self):
        '''returns the other voices registered in the app'''
        res = {}
        for k, v in self.composer.voices.items():
            if v != self:
                res[k] = v
        #print res
        return res

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

if __name__ == "__main__":
    from composer import Composer
    c = Composer()
    print Voice("", "", c).in_the_middle(45)
