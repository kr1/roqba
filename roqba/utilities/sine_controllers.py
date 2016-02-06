"""this module provides objects that produce controller sine-waves

for given frequencies.
they use elapsed time to calculate the value
for any given moment in which the get_value-methods are called"""
from math import sin, pi
from time import time


class Sine(object):
    """a single frequency sine-wave controller object"""
    def __init__(self, freq, range=[-1, 1]):
        self.start = time()
        self.freq = 1.0 / freq

    def get_value(self):
        """returns the controller value at the moment it is called"""
        delta = time() - self.start
        offset = delta % self.freq
        #print "offset: {0} - offset/freq: {1}".format(offset,
        #                                              offset/self.freq)
        #print "time:{0} - delta:{1}".format(time(), delta)
        pos = (offset / self.freq) * (pi * 2)
        val = sin(pos)
        return val

    def set_freq(self, freq):
        self.freq = 1.0 / freq


class MultiSine(object):
    """a controller object for multiple overlaid sine-waves"""
    def __init__(self, freqs, equal_power=True):
        self.start = time()
        if type(freqs) != type([]):
            raise RuntimeError("freqs must be a list")
        self.freqs = freqs
        self.equal_power = equal_power
        if equal_power:
            self.coeff = 1
        else:
            self.coeff = 1.0 / sum([1.0 / (n + 1) for n in xrange(len(freqs))])
        self.assemble_funnel()

    def get_value(self):
        """returns the combined (added) value of the

        multiple sine controllers"""
        tmp = [get_value() for get_value in self.funnel]
        if self.equal_power:
            return sum(tmp) / float(len(self.funnel))
        else:
            ## each value gets scaled according to its position in the array
            tmp = [tmp[pos] / (pos + 1.0) for pos in xrange(len(tmp))]
            return sum(tmp) * self.coeff

    def get_value_as_factor(self, variation):
        """returns scaled value oscillating around one"""
        return 1 + (self.get_value() * variation)

    def assemble_funnel(self):
        """assembles a list of get_value function objects"""
        funnel = []
        for freq in self.freqs:
            funnel.append(Sine(freq).get_value)
        self.funnel = funnel

    def set_freqs(self, freqs):
        """set new frequencies for the controller

        (note that the number of frequencies must be equal to
        the original number if frequencies)"""
        if len(freqs) != len(self.freqs):
            raise RuntimeError('''update-frequencies must be of same
                                  length as original frequencies''')
        self.freqs = freqs
        self.assemble_funnel()
