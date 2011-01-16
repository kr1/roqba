
from random import choice as sample

class Voice(object):
    def __init__(self, id, target, composer):
        self.target = target
        self.id = id
        self.composer = composer
        self.gen = self.voice(target)
        self.gen.next() # get the coroutine to the yield
        composer.add_voice(id, self.gen)
    
    def voice(self, target):
        while True:
            state = (yield)
            print state, ", possible: ", state.get("possible", [])
            val = self.desc(state["composer"], sample(state["possible"]))
            state["composer"].harm.update({self.id:val})
            target.send(val)

    def desc(self, c, val):
        return val - 1
