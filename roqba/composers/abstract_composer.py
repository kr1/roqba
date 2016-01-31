import sys
from abc import ABCMeta, abstractmethod


class AbstractComposer(object):
    __metaclass__ = ABCMeta

    def __repr__(self):
        return "<Composer-Inst with {0}>".format(self.harm)

    def report(self):
        '''utility function that prints info on  harmonies and single voices'''
        sys.stderr.write("harmonies: {0}\n".format(self.harm))
        sys.stderr.write("voices: {0}\nnotes:{1}\n".format(self.voices,
                         map(lambda x: x.note, self.voices.values())))

    @abstractmethod
    def set_meter(self, meter):
        pass

    @abstractmethod
    def generate(self):
        pass

    @abstractmethod
    def set_scale(self, scale):
        pass

    @abstractmethod
    def choose_rhythm(self):
        pass

    @abstractmethod
    def set_binaural_diffs(self):
        pass
