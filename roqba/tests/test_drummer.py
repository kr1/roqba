"""unit tests for the drummer module"""
import pytest

from mock import Mock
from roqba.drummer import Drummer


@pytest.fixture
def drum():
    comp = Mock()
    return Drummer(comp, [2, 0, 1, 0, 1, 0, 1, 0])

def test_push_value(drum):
    '''pushed values should end up appended to the pattern'''
    drum.empty_pattern()
    drum.push_value(1)
    assert drum.pattern["low"] == [1]
    drum.push_value(111)
    assert drum.pattern["cont"] == [1, 111]

def test_create_pattern_without_specifing_a_pattern(drum):
    '''creating a pattern without specifying a reference

    should lead to the a pattern based on the meter'''
    drum.create_pattern()
    assert drum.pattern["cont"] == [1, 1, 1, 1, 1, 1, 1, 1]
    assert drum.pattern["low"] == [1, 0, 0, 0, 0, 0, 0, 0]
    assert drum.pattern["high"] == [0, 0, 1, 0, 1, 0, 1, 0]

def test_create_pattern(drum):
    '''creating a pattern specifying a simple reference'''

    drum.create_pattern([1, 0, 1, 1, 0, 1, 0])
    assert drum.pattern["cont"] == [1, 1, 1, 1, 1, 1, 1]
    assert drum.pattern["low"] ==  [1, 0, 0, 1, 0, 0, 0]
    assert drum.pattern["high"] == [0, 0, 1, 0, 0, 1, 0]

def test_create_high_low_pattern(drum):
    '''control the mapping between full pattern and high-low version'''

    drum.create_pattern([1, 0, 1, 1, 0, 1, 0])
    assert drum.pattern["low"] == [1, 0, 0, 1, 0, 0, 0]
    assert drum.pattern["high"] == [0, 0, 1, 0, 0, 1, 0]
    assert drum.high_low_pattern == [-1, 0, 1, -1, 0, 1, 0]
