"""unit tests for the director module"""

import pytest

from mock import Mock
from roqba.voice import Voice
from roqba.composers.baroq import Composer
from roqba.director import Director
from roqba.static.scales_and_harmonies import SCALES
from roqba.main import settings, behaviour

DIATONIC = SCALES["DIATONIC"]


@pytest.fixture
def director():
    gateway = Mock()
    settings['gui'] = False
    settings["number_of_voices"] = 4
    composer = Composer(gateway, settings, behaviour)
    composer.gateway.hub = Mock()
    state = {
        "weight": 1,
        "speed": 0.4,
        "cycle_pos": 2
    }
    director = Director(gateway, behaviour, settings)
    return director


def test_new_transition_speed(director):
    '''test that new speed values comply with specs'''
    director.speed_change = 'transition'
    trans = [director.new_speed() for n in xrange(666)]
    deltas = [abs(trans[n] - trans[n + 1]) for n in xrange(len(trans) - 1)]
    assert max(deltas) < 0.04


def test_new_leap_speed(director):
    '''test that new leap speed values comply with specs'''
    director.speed_change = 'leap'
    min_ = director.behaviour['min_speed'] = 0.1
    max_ = director.behaviour['max_speed'] = 0.2
    center = min_ + (max_ - min_) * director.speed_target
    leaps = [director.new_speed() for n in xrange(666)]
    average = sum(leaps) / float(len(leaps))
    assert abs(average - center) < 0.07
    for r in [0.000001, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6,
              0.7, 0.8, 0.9, 0.9999999]:
        director.speed_target = r
        res = [director.new_speed() for n in xrange(666)]
        average = sum(res) / float(len(res))
        calc_target = min_ + ((max_ - min_) * r)
        assert abs(average - calc_target) < 0.15
