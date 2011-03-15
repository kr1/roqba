
"""integration test for the composer module

"""
import unittest2 as unittest
from mock import Mock
from voice import Voice
from composer import Composer
from scales_and_harmonies import SCALES
from note_length_groupings import groupings

DIATONIC = SCALES["DIATONIC"]

class UnitTestComposer(unittest.TestCase):
    """a test class for the Composer class"""
    def setUp(self):
        """
        set up data used and mock objects/methods in the tests.

        this method is called before each test function execution.
#        """
        gw = Mock()
        self.composer = Composer(gateway=gw, num_voices = 2)
        self.v1 = Voice(1, self.composer)
        self.v2 = Voice(2, self.composer)
        self.composer.add_voice(self.v1.id, self.v1)
        self.composer.add_voice(self.v2.id, self.v2)
        self.composer.gateway.hub = Mock()

    def test_meter_setting(self):
        '''test method raises non exception'''
        for meter in groupings.keys():
            self.composer.set_meter(meter)

    def test_generate(self):
        state = {"weight" : 1,
                 "speed" : 0.4,
                 "cycle_pos":2}
        self.composer.generate(state)
    
    def test_stream_analyzer(self):
        '''test caesura detection'''
        self.composer.stream_analyzer()
        self.assertEqual(self.composer.comment, 'normal')
        self.v1.note = 21
        self.v1.note_change = 1
        self.v2.note = 23
        self.v2.note_change = 1
        self.composer.stream_analyzer()
        self.assertEqual(self.composer.comment, 'caesura')

def suite():
    """make the test suite"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(UnitTestComposer))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
