"""integration test for the composer module"""

import pytest
from mock import Mock

from roqba.voice import Voice
from roqba.composers.baroq import Composer
from roqba.static.scales_and_harmonies import SCALES
from roqba.static.note_length_groupings import groupings
from roqba.main import settings, behaviour

DIATONIC = SCALES["DIATONIC"]


@pytest.fixture
def composer():
    gateway = Mock()
    settings["number_of_voices"] = 2
    composer = Composer(gateway, settings, behaviour)
    return composer


def test_meter_setting(composer):
    '''test method raises non exception'''
    for meter in groupings.keys():
        composer.set_meter(meter)


def test_generate(composer):
    '''test the main function of the module'''
    state = {"weight": 1,
             "speed": 0.4,
             "comp": composer,
             "cycle_pos": 2}
    composer.generate(state)


def test_stream_analyzer(composer):
    '''test caesura detection'''
    composer.stream_analyzer()
    assert composer.comment == 'normal'
    v1 = composer.voices[1]
    v1.note = 21
    v1.note_change = 1
    v2 = composer.voices[2]
    v2.note = 23
    v2.note_change = 1
    composer.stream_analyzer()
    assert composer.comment == 'caesura'


def test_generate_real_scale(composer):
    '''test real scale generation from scale patterns'''
    for scale in SCALES:
        composer.generate_real_scale()


def test_generate_real_scale_greek_chromatic(composer):
    '''test real scale generation from scale patterns'''
    composer.scale = 'GREEK_ENHARMONIC'
    real_scale = composer.generate_real_scale()
    assert composer.real_scale[:7] == [0, 0.5, 1, 5, 7, 7.5, 8]
