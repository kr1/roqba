"""unit tests for the BehaviourDict

"""
import unittest2 as unittest

from mock import Mock
from roqba.utilities import behaviour_dict


class UnitTestBehaviourDict(unittest.TestCase):
    """a test class for the BehaviourDict class"""
    def setUp(self):
        """
        set up data used and mock objects/methods in the tests.
        """
        self.bd = behaviour_dict.BehaviourDict({11:2, 13:4, 
                                                'per_voice':{1: {11:3}
                                               }})

    def test_voice_get_should_return_voice_behaviour_if_set(self):
        '''should return a set behaviour for a voice'''
        self.assertEqual(self.bd.voice_get(1, 11), 3)
   
    def test_voice_get_should_return_default_behaviour_if_not_set_for_voice(self):
        '''should return default if no behaviour for a voice'''
        self.assertEqual(self.bd.voice_get(1, 13), 4)
   
    def test_voice_get_should_raise_runtime_error_for_no_voice(self):
        '''should raise RuntimeError if called for non-existant voice'''
        self.assertRaises(RuntimeError, self.bd.voice_get, 2,'any')

    def test_voice_get_should_raise_runtime_error_for_wrong_key(self):
        '''should raise RuntimeError for wrong key'''
        self.assertRaises(RuntimeError, self.bd.voice_get, 1,'any')

def suite():
    """make the test suite"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(UnitTestBehaviourDict))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
