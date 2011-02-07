"""unit tests for the composer module

"""
import unittest2 as unittest
from mock import Mock
from composer import Composer, DIATONIC


class UnitTestComposer(unittest.TestCase):
    """a test class for the Composer class"""
    def setUp(self):
        """
        set up data used and mock objects/methods in the tests.

        this method is called before each test function execution.
#        """
        gw = Mock()
        self.composer = Composer(gateway=gw)
        self.composer.gateway.hub = Mock()

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


def suite():
    """make the test suite"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(UnitTestComposer))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
