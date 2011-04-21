"""unit tests for the drummer module

"""
import unittest2 as unittest
from mock import Mock
from drummer import Drummer

class UnitTestDrummer(unittest.TestCase):
    """a test class for the Drummer class"""
    def setUp(self):
        """
        set up data used and mock objects/methods in the tests.

        this method is called before each test function execution.
        """
        comp = Mock()
        self.drum = Drummer(comp, [2, 0, 1, 0, 1, 0, 1, 0])

    def test_push_value(self):
        '''pushed values should end up appended to the pattern'''
        self.drum.empty_pattern()
        self.drum.push_value(1)
        self.assertEqual(self.drum.pattern["low"], [1])
        self.drum.push_value(111)
        self.assertEqual(self.drum.pattern["cont"], [1,111])

    def test_create_pattern_without_specifing_a_pattern(self):
        '''creating a pattern without specifying a reference

        should lead to the a pattern based on the meter'''
        self.drum.create_pattern()
        self.assertEqual(self.drum.pattern["cont"], [1, 1, 1, 1, 1, 1, 1, 1])
        self.assertEqual(self.drum.pattern["low"], [1, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(self.drum.pattern["high"], [0, 0, 1, 0, 1, 0, 1, 0])

    def test_create_pattern(self):
        '''creating a pattern specifying a simple reference'''

        self.drum.create_pattern([1, 0, 1, 1, 0, 1, 0])
        self.assertEqual(self.drum.pattern["cont"], [1, 1, 1, 1, 1, 1, 1])
        self.assertEqual(self.drum.pattern["low"],  [1, 0, 0, 1, 0, 0, 0])
        self.assertEqual(self.drum.pattern["high"], [0, 0, 1, 0, 0, 1, 0])

    def test_create_high_low_pattern(self):
        '''control the mapping between full pattern and high-low version'''

        self.drum.create_pattern([1, 0, 1, 1, 0, 1, 0])
        self.assertEqual(self.drum.pattern["low"],  [1, 0, 0, 1, 0, 0, 0])
        self.assertEqual(self.drum.pattern["high"], [0, 0, 1, 0, 0, 1, 0])
        self.assertEqual(self.drum.high_low_pattern,[-1, 0, 1, -1, 0, 1, 0])


def suite():
    """make the test suite"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(UnitTestDrummer))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
