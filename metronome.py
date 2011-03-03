from itertools import cycle

HEAVY = 2
MEDIUM = 1
LIGHT = 0


class Metronome(object):
    def __init__(self, meter=[2, 0, 1, 0]):
        self.meter = meter
        self.metronome = cycle(meter)
        self.cycle_pos = cycle(xrange(len(meter)))

    def beat(self):
        return [self.cycle_pos.next(), self.metronome.next()]

    def reset(self):
        self.metronome = cycle(self.meter)
        self.cycle_pos = cycle(xrange(len(self.meter)))

    def set_meter(self, meter):
        self.meter = meter
        self.metronome = cycle(meter)
        self.cycle_pos = cycle(xrange(len(meter)))
