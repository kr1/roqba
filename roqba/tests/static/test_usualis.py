import pytest
from roqba.static.usualis import next_valid_word, UsualisError

higher = [-1, 0, 1, 2, 8, 9, 10, 11, 12]
lower = [1, 0, -1, -2, -8, -9, -10, -11, -12]


@pytest.mark.parametrize('higher', higher)
@pytest.mark.parametrize('lower', lower)
@pytest.mark.parametrize('start_note', higher + lower)
def test_next_valid_word(start_note, lower, higher):
    if higher < 0 or lower > 0 or (lower == higher == 0):
        with pytest.raises(UsualisError):
            assert next_valid_word(start_note, higher, lower)
    else:
        assert next_valid_word(start_note, higher, lower)
