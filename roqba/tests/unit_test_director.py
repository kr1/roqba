"""unit tests for the composer module

"""
import unittest2 as unittest
from mock import Mock
from roqba.voice import Voice
from roqba.composer import Composer
from roqba.director import Director
from roqba.static.scales_and_harmonies import SCALES
from roqba.main import settings, behaviour

DIATONIC = SCALES["DIATONIC"]


class UnitTestDirector(unittest.TestCase):
    """a test class for the Composer class"""
    def setUp(self):
        """
        set up data used and mock objects/methods in the tests.

        this method is called before each test function execution.
#        """
        gw = Mock()
        self.composer = Composer(gw, settings, behaviour, num_voices=2)
        v = Voice(1, self.composer)
        v = Voice(2, self.composer)
        self.composer.add_voice(v.id, v)
        self.composer.add_voice(v.id, v)
        self.composer.gateway.hub = Mock()
        state = {"weight": 1,
                 "speed": 0.4,
                 "cycle_pos": 2}
        self.director = Director(self.composer, state, behaviour, settings)

    def test_new_transition_speed(self):
        '''test that new speed values comply with specs'''
        self.director.speed_change = 'transition'
        trans = [self.director.new_speed() for n in xrange(666)]
        deltas = [abs(trans[n] - trans[n + 1]) for n in xrange(len(trans) - 1)]
        self.assertTrue(max(deltas) < 0.04)

    def test_new_leap_speed(self):
        '''test that new leap speed values comply with specs'''
        self.director.speed_change = 'leap'
        leaps = [self.director.new_speed() for n in xrange(666)]
        average = sum(leaps) / float(len(leaps))
        max_ = self.director.MAX_SPEED
        min_ = self.director.MIN_SPEED
        center = min_ + (max_ - min_) * self.director.speed_target
        self.assertTrue(abs(average - center) < 0.07)
        for r in [0.000001, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6,
                  0.7, 0.8, 0.9, 0.9999999]:
            self.director.speed_target = r
            res = [self.director.new_speed() for n in xrange(666)]
            average = sum(res) / float(len(res))
            calc_target = min_ + ((max_ - min_) * r)
            #print r, average, calc_target
            self.assertTrue(abs(average - calc_target) < 0.15)


def suite():
    """make the test suite"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(UnitTestDirector))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
