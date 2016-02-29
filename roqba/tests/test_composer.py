"""unit tests for the composer module """
import pytest
from mock import Mock

from roqba.voice import Voice
from roqba.composers.baroq import Composer
from roqba.static.scales_and_harmonies import SCALES
from roqba.main import settings, behaviour

DIATONIC = SCALES["DIATONIC"]


@pytest.fixture()
def composer():
    """
    set up data used and mock objects/methods in the tests.

    this method is called before each test function execution."""
    composer = Composer(Mock(), settings, behaviour)
    composer.gateway.hub = Mock()
    return composer

@pytest.fixture()
def test_chord():
    test_chord = [30, 25, 28, 40]
    return test_chord

def test_40_scale_walker(composer):
    """hard-coded test to check the correctness of the scale-walker method

    by comparing to expected results on the DIATONIC scale"""
    sw = composer.scale_walker
    # simple up
    assert sw(DIATONIC, 0, 2) == 4
    assert sw(DIATONIC, 2, 2) == 5
    #  wrap-around up
    assert sw(DIATONIC, 11, 3) == 16
    # simple down
    assert sw(DIATONIC, 35, -3) == 29
    assert sw(DIATONIC, 29, -1) == 28
    # wrap-around down
    assert sw(DIATONIC, 36, -1) == 35
    assert sw(DIATONIC, 36, -2) == 33

def test_flatten_chord(composer, test_chord):
    '''test flattening of a chord'''
    res = composer.flatten_chord(test_chord)
    assert res == [2, 4, 0, 5]

def test_get_deltas(composer, test_chord):
    '''should create reliable deltas of harmonies'''
    res = composer.get_deltas(test_chord)
    assert res == [3, 5, 15]

def test_acceptable_harm_for_length(composer):
    '''harmonic watchdog: test harmonies pass'''
    fun = composer.acceptable_harm_for_length
    assert fun([], 0) == True
    assert fun([1], 1) == True
    assert fun([1, 3], 2) == True
    assert fun([1, 3, 5], 3) == True
    assert fun([1, 3, 5, 7], 4) == True

def test_inacceptable_harm_for_length(composer):
    '''harmonic watchdog: test disharmonies do not pass'''
    fun = composer.acceptable_harm_for_length
    assert fun([1, 2], 2) == False
    assert fun([1, 3, 4], 3) == False
    assert fun([1, 3, 5, 6], 4) == False
