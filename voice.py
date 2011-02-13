
from random import choice as sample

from movement_probabilities import DEFAULT_MOVEMENT_PROBS
from movement_probabilities import MIDDLE_VOICES_MOVEMENT_PROBS
from movement_probabilities import BASS_MOVEMENT_PROBS
from note_length_groupings import DEFAULT_NOTE_LENGTH_GROUPINGS as GROUPINGS
from note_length_groupings import  analyze_grouping
from metronome import HEAVY, MEDIUM, LIGHT


class Voice(object):
    def __init__(self, id,
                       composer,
                       range=[24, 48],
                       note=None,
                       real_note=None,
                       note_length_grouping=sample(GROUPINGS)):
        self.id = id
        range.sort()
        self.range = range
        self.dir = 0
        self.note = note or int((max(self.range)
                                 - min(self.range)) / 2) + min(self.range)
        self.real_note = real_note or int((max(self.range)
                                 - min(self.range)) / 2) + min(self.range)
        self.note_length_grouping = note_length_grouping
        self.weight = MEDIUM
        self.prior_note = None
        self.note_delta = None
        # behaviour
        self.change_rhythm_after_times = 1
        self.movement_probs = DEFAULT_MOVEMENT_PROBS

        self.note_change = True
        self.counter = 0
        self.composer = composer  # store the composer
        self.scale = composer.scale
        self.generator = self.voice()
        self.generator.next()  # set the coroutine to the yield-point
        composer.add_voice(id, self)  # register with the composer

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
            #print state, ", possible: ", state.get("possible", [])
            #val = self.desc(state["composer"], sample(state["possible"]))
            self.note_change = self.on_off_pattern[state['cycle_pos']]
            self.weight = state["weight"]
            if self.note_change:
                self.prior_note = self.note
                self.note = self.next_note()
                self.note_delta = self.note - self.prior_note
                self.real_note = self.composer.scale_walker(self.scale,
                                                            self.real_note,
                                                            self.note_delta)

    def next_note(self):
        """the next is calculated from here"""
        if self.dir:
            move = (self.dir * sample(self.movement_probs))
        else:
            move = sample([-1, 0, 1]) * sample(self.movement_probs)
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

    def exceeds(self, note):
        """returns min/max limits and a bounce back direction coefficient

        if incomint int exceeds limits, returns False otherwise"""
        if note > self.range[1]:
            return (self.range[1], -1)
        elif note < self.range[0]:
            return (self.range[0], 1)
        else:
            False

    def set_rhythm_grouping(self, grouping):
        """setter method which creates also the on/off pattern"""
        if self.counter % self.change_rhythm_after_times == 0:
            self.note_length_grouping = grouping
            self.on_off_pattern = analyze_grouping(grouping)
        self.counter += 1

    def in_the_middle(self, note):
        """returns true is int is in the center area of the range"""
        range_span = self.range[1] - self.range[0]
        lower_thresh = self.range[0] + (range_span * 0.333)
        upper_thresh = self.range[0] + (range_span * 0.666)
        return note > lower_thresh and note < upper_thresh

    def desc(self, c, val):
        return val - 1

    def set_state(self, name):
        if name == "BASS":
            self.change_rhythm_after_times = 8
            self.movement_probs = BASS_MOVEMENT_PROBS
            self.range = [18, 36]
        elif name == "MID":
            self.change_rhythm_after_times = 4
            self.movement_probs = MIDDLE_VOICES_MOVEMENT_PROBS
            self.range = [30, 45]
        elif name == "HIGH":
            self.change_rhythm_after_times = 1
            self.movement_probs = DEFAULT_MOVEMENT_PROBS
            self.range = [35, 50]


if __name__ == "__main__":
    from composer import Composer
    c = Composer()
    print Voice("", "", c).in_the_middle(45)
