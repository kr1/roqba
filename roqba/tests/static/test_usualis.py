import pytest
from roqba.static.usualis import next_valid_word, UsualisError

higher = [-1, 0, 1, 2, 8, 9, 10, 11, 12]
lower = [1, 0, -1, -2, -8, -9, -10, -11, -12]
start = range(-7, 7)


@pytest.mark.parametrize('higher', higher)
@pytest.mark.parametrize('lower', lower)
@pytest.mark.parametrize('start_note', start)
def test_next_valid_word(start_note, lower, higher):
    if ((higher < 0 or lower > 0 or (lower == higher == 0) or
            higher < 0 and lower > 0) or 
            start_note > higher or start_note < lower):
        with pytest.raises(UsualisError):
            next_word = next_valid_word(start_note, higher, lower)
            assert next_word
    else:
        assert next_valid_word(start_note, higher, lower)
