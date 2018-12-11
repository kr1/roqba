"""unit tests for the BehaviourDict

"""
import pytest


from mock import Mock
from roqba.utilities.behaviour_dict import BehaviourDict


@pytest.fixture()
def behaviour_dict(request):
    """
    set up data used and mock objects/methods in the tests.
    """
    behaviour_dict = BehaviourDict({
        11: 2, 13: 4,
        'per_voice': {
            1: {
                11: 3
            }
        }
    })
    return behaviour_dict


def test_voice_get_should_return_voice_behaviour_if_set(behaviour_dict):
    '''should return a set behaviour for a voice'''
    assert behaviour_dict.voice_get(1, 11) == 3


def test_voice_get_should_return_default_behaviour_if_not_set_for_voice(behaviour_dict):
    '''should return default if no behaviour for a voice'''
    assert behaviour_dict.voice_get(1, 13) == 4


def test_voice_get_should_raise_runtime_error_for_no_voice(behaviour_dict):
    '''should raise RuntimeError if called for non-existant voice'''
    with pytest.raises(RuntimeError):
        behaviour_dict.voice_get(2,'any')


def test_voice_get_should_raise_runtime_error_for_wrong_key(behaviour_dict):
    '''should raise RuntimeError for wrong key'''
    with pytest.raises(RuntimeError):
        behaviour_dict.voice_get(1,'any')
