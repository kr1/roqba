"""unit tests for the composer module

"""
import unittest2 as unittest
from mock import Mock
from voice import Voice
from composer import Composer
from director import Director
from scales_and_harmonies import SCALES

DIATONIC = SCALES["DIATONIC"]


class UnitTestDirector(unittest.TestCase):
    """a test class for the Composer class"""
    def setUp(self):
        """
        set up data used and mock objects/methods in the tests.

        this method is called before each test function execution.
#        """
        gw = Mock()
        self.composer = Composer(gateway=gw, num_voices=2)
        v = Voice(1, self.composer)
        v = Voice(2, self.composer)
        self.composer.add_voice(v.id, v)
        self.composer.add_voice(v.id, v)
        self.composer.gateway.hub = Mock()
        state = {"weight" : 1,
                 "speed" : 0.4,
                 "cycle_pos":2}
        self.director = Director(self.composer, state)

    def test_new_transition_speed(self):
        '''test that new speed values comply with specs'''
        self.director.speed_change = 'transition'
        trans = [self.director.new_speed() for n in xrange(666)]
        deltas = [abs(trans[n] - trans[n+1]) for n in xrange(len(trans) - 1) ]
        self.assertTrue(max(deltas) < 0.04)

    def test_new_leap_speed(self):
        '''test that new leap speed values comply with specs'''
        self.director.speed_change = 'leap'
        leaps = [self.director.new_speed() for n in xrange(666)]
        average = sum(leaps) / float(len(leaps))
        max_ =  self.director.MAX_SPEED
        min_ =  self.director.MIN_SPEED
        center = min_ + (max_ - min_) / 2
        self.assertTrue(abs(average - center) < 0.05)

def suite():
    """make the test suite"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(UnitTestDirector))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
