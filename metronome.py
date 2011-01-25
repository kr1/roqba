from itertools import cycle

HEAVY = 2
MEDIUM = 1
LIGHT = 0

class Metronome(object):
    def __init__(self, meter = [2, 0, 1, 0]):
        self.meter = meter
        self.metronome = cycle(meter)

    def beat(self):
        return self.metronome.next()
