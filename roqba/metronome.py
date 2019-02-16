from itertools import cycle

HEAVY = 2
MEDIUM = 1
LIGHT = 0


class Metronome(object):
    def __init__(self, meter=[2, 0, 1, 0]):
        self.meter = meter
        self.metronome = cycle(meter)
        self.cycle_pos = cycle(range(len(meter)))

    def beat(self):
        '''return the weight of the current beat'''
        return [next(self.cycle_pos), next(self.metronome)]

    def reset(self):
        '''resets the internal counter to zero'''
        self.metronome = cycle(self.meter)
        self.cycle_pos = cycle(range(len(self.meter)))

    def set_meter(self, meter):
        '''sets the meter and resets the internal counter'''
        self.meter = meter
        self.metronome = cycle(meter)
        self.cycle_pos = cycle(range(len(meter)))
