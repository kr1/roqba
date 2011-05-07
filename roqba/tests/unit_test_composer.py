"""unit tests for the composer module

"""
import unittest2 as unittest
from mock import Mock
from roqba.voice import Voice
from roqba.composer import Composer
from roqba.scales_and_harmonies import SCALES

DIATONIC = SCALES["DIATONIC"]


class UnitTestComposer(unittest.TestCase):
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
        self.test_chord = [30, 25, 28, 40]

    def test_40_scale_walker(self):
        """hard-coded test to check the correctness of the scale-walker method

        by comparing to expected results on the DIATONIC scale"""
        sw = self.composer.scale_walker
        # simple up
        self.assertEqual(sw(DIATONIC, 0, 2), 4)
        self.assertEqual(sw(DIATONIC, 2, 2), 5)
        #  wrap-around up
        self.assertEqual(sw(DIATONIC, 11, 3), 16)
        # simple down
        self.assertEqual(sw(DIATONIC, 35, -3), 29)
        self.assertEqual(sw(DIATONIC, 29, -1), 28)
        # wrap-around down
        self.assertEqual(sw(DIATONIC, 36, -1), 35)
        self.assertEqual(sw(DIATONIC, 36, -2), 33)

    def test_flatten_chord(self):
        '''test flattening of a chord'''
        res = self.composer.flatten_chord(self.test_chord)
        self.assertEqual(res, [2, 4, 0, 5])

    def test_get_deltas(self):
        '''should create reliable deltas of harmonies'''
        res = self.composer.get_deltas(self.test_chord)
        self.assertEqual(res, [3, 5, 15])

    def test_acceptable_harm_for_length(self):
        '''harmonic watchdog: test harmonies pass'''
        fun = self.composer.acceptable_harm_for_length
        self.assertEqual(fun([], 0), True)
        self.assertEqual(fun([1], 1), True)
        self.assertEqual(fun([1, 3], 2), True)
        self.assertEqual(fun([1, 3, 5], 3), True)
        self.assertEqual(fun([1, 3, 5, 7], 4), True)

    def test_inacceptable_harm_for_length(self):
        '''harmonic watchdog: test disharmonies do not pass'''
        fun = self.composer.acceptable_harm_for_length
        self.assertEqual(fun([1, 2], 2), False)
        self.assertEqual(fun([1, 3, 4], 3), False)
        self.assertEqual(fun([1, 3, 5, 6], 4), False)


def suite():
    """make the test suite"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(UnitTestComposer))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
