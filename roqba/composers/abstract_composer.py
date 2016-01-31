import sys
import logging
from abc import ABCMeta, abstractmethod

from roqba.voice import Voice
from roqba.notator import Notator
from roqba.drummer import Drummer
import roqba.static.note_length_groupings as note_length_groupings
from roqba.static.meters import METERS
from roqba.static.scales_and_harmonies import (ALL_STRICT_HARMONIES,
                                               BASE_HARMONIES,
                                               FOLLOWINGS,
                                               HARMONIC_INTERVALS,
                                               HARMONIES,
                                               NOTES_PER_SCALE,
                                               SCALES)


class AbstractComposer(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.comp_logger = logging.getLogger("composer")
        self.note_logger = logging.getLogger("transcriber")
        self.musical_logger = logging.getLogger("musical")
        # change INFO to DEBUG for debugging output
        self.musical_logger.setLevel(logging.INFO)
        self.meter = self.behaviour['meter']
        self.applied_meter = METERS[self.meter]['applied']
        self._update_groupings(self.meter)
        self.drummer = Drummer(self)
        self.comment = None
        self.voices = {}
        for voice_idx in range(self.num_voices):
            id_ = voice_idx + 1
            self.voices[id_] = Voice(
                id_, self,
                note_length_grouping=self.behaviour["meter"][1],
                register=self.settings["voice_registers"][voice_idx],
                behaviour=self.settings['voice_behaviours'][voice_idx])
        [voice.register_other_voices() for voice in self.voices.values()]
        self.set_meter(self.meter)
        self.notator = Notator(self.num_voices)

    def __repr__(self):
        return "<Composer-Inst with {0}>".format(self.harm)

    def _update_groupings(self, meter):
        self.TERNARY_GROUPINGS = note_length_groupings.get_grouping(meter,
                                                                    "terns")
        self.HEAVY_GROUPINGS = note_length_groupings.get_grouping(meter,
                                                                  "heavy")
        self.DEFAULT_GROUPINGS = note_length_groupings.get_grouping(meter,
                                                                    "default")
        self.FAST_GROUPINGS = note_length_groupings.get_grouping(meter,
                                                                 "first")

    def report(self):
        '''utility function that prints info on  harmonies and single voices'''
        sys.stderr.write("harmonies: {0}\n".format(self.harm))
        sys.stderr.write("voices: {0}\nnotes:{1}\n".format(self.voices,
                         map(lambda x: x.note, self.voices.values())))

    def set_meter(self, meter):
        '''modifies composer-attributes for the specified meter.

        calls reload_register method of the voices and creates and
        sets the new meter also for the drummer-instance'''
        self.meter = meter
        for v in self.voices.values():
            v.reload_register()
        self.drummer.create_pattern(METERS[meter]["applied"])
        pass

    @abstractmethod
    def generate(self):
        pass

    @abstractmethod
    def choose_rhythm(self):
        pass

    @abstractmethod
    def set_binaural_diffs(self):
        pass

    def set_scale(self, name, min=0, max=128):
        '''sets the specified scale and generates a new real scale'''
        self.scale = name
        self.generate_real_scale(min, max)

    @staticmethod
    def assemble_real_scale(scale, min=0, max=128):
        '''extends the one-octave scale over the specified range'''
        real_scale = []
        value = 0
        for n in xrange(min, max):
            value += 1
            index = n % len(scale)
            if scale[index]:
                real_scale.append(value)
        return real_scale

    def generate_real_scale(self, min=0, max=128):
        '''extends the one-octave scale over the specified range'''
        scale = SCALES[self.scale]
        self.real_scale = self.assemble_real_scale(scale, min, max)

