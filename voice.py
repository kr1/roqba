from composer import MOVEMENT_PROBS
from random import choice as sample

class Voice(object):
    def __init__(self, id, target, composer, range = [0, 64], note = None):
        self.target = target
        self.id = id
        range.sort()
        self.range = range
        self.dir = 0
        self.note = note or int((max(self.range) - min(self.range))/2) + min(self.range)
        self.prior_note = None
        self.composer = composer # store the composer
        self.generator = self.voice(target)
        self.generator.next() # get the coroutine to the yield
        composer.add_voice(id, self) # register with the composer

    def __str__(self):
        return str({"note": self.note,
                    "dir": self.dir})

    def __repr__(self):
        return "{0} - {1}".format(self.__class__, self.__str__())
    
    def voice(self, target):
        while True:
            state = (yield)
            #print state, ", possible: ", state.get("possible", [])
            #val = self.desc(state["composer"], sample(state["possible"]))
            val = self.next_note()
            target.send(val)

    def bounce_back(self, dir):
        self.dir = dir   

    def next_note(self):
        if self.dir:
            res = self.note + (self.dir * sample(MOVEMENT_PROBS))
        else:
            res = self.note + sample([-1, 0, 1]) * sample(MOVEMENT_PROBS)
        if self.exceeds(self.note):
            res, self.dir = self.exceeds(self.note)
        if self.in_the_middle(res):
            self.dir = 0
        self.prior_note = self.note
        self.note = res
        return res

    def exceeds(self, note):
        if note > self.range[1]:
            return [self.range[1], -1]
        elif note < self.range[0]:
            return [self.range[0], 1]
        else:
            None
        
    def in_the_middle(self, note):
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
