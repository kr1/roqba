from composer import DEFAULT_MOVEMENT_PROBS as MOVEMENT_PROBS
from note_length_groupings import DEFAULT_NOTE_LENGTH_GROUPINGS as GROUPINGS
from note_length_groupings import  analyze_grouping 
from random import choice as sample
from metronome import HEAVY, MEDIUM, LIGHT

class Voice(object):
    def __init__(self, id, 
                       target, 
                       composer, 
                       range = [0, 64], 
                       note = None, 
                       note_length_grouping = sample(GROUPINGS)):
        self.target = target
        self.id = id
        range.sort()
        self.range = range
        self.dir = 0
        self.note = note or int((max(self.range) - min(self.range))/2) + min(self.range)
        self.note_length_grouping = note_length_grouping 
        self.prior_note = None
        self.note_change = True
        self.composer = composer # store the composer
        self.generator = self.voice(target)
        self.generator.next() # get the coroutine to the yield
        composer.add_voice(id, self) # register with the composer

    def __str__(self):
        return str({"note": self.note,
                    "dir": self.dir})

    def __repr__(self):
        return "{0} - {1}".format(self.__class__, self.__str__())
    
    def voice(self):
        """the generator method of the Voice-class"""
        while True:
            state = (yield)
            #print state, ", possible: ", state.get("possible", [])
            #val = self.desc(state["composer"], sample(state["possible"]))
            self.note_change =  self.on_off_pattern[state['cycle_pos']]
            if self.note_change:
                self.prior_note = self.note
                self.note = self.next_note()

    def next_note(self):
        """the next is calculated from here""" 
        if self.dir:
            res = self.note + (self.dir * sample(MOVEMENT_PROBS))
        else:
            res = self.note + sample([-1, 0, 1]) * sample(MOVEMENT_PROBS)
        exceed = self.exceeds(res)
        if exceed:
            print "exceed"
            res, self.dir = exceed
        if self.in_the_middle(res):
            self.dir = 0
        if self.exceeds(res):
            raise RuntimeError, "diabolus in musica: {0} is too low/high, dir:{1}".format(res,self.dir)
        return res

    def exceeds(self, note):
        """returns min/max limits and a bounce back direction coefficient if incomint int exceeds limits
        
        returns False otherwise"""
        if note > self.range[1]:
            return (self.range[1], -1)
        elif note < self.range[0]:
            return (self.range[0], 1)
        else:
            False

    def set_rhythm_grouping(self, grouping):
        """setter method which creates also the on/off pattern"""
        self.note_length_grouping = grouping
        self.on_off_pattern = analyze_grouping(grouping)
        
    def in_the_middle(self, note):
        """returns true is the incoming int is in the center area of the range"""
        range_span = self.range[1] - self.range[0]
        lower_thresh = self.range[0] + (range_span * 0.333)
        upper_thresh = self.range[0] + (range_span * 0.666)
        return note > lower_thresh and note < upper_thresh

    def desc(self, c, val):
        return val - 1


if __name__ == "__main__":
    from composer import Composer
    c = Composer()
    print Voice("","",c).in_the_middle(45)
