import pytest
from roqba.static.usualis import safe_next_valid_word, UsualisError

higher = [-1, 0, 1, 2, 8, 9, 10, 11, 12]
lower = [1, 0, -1, -2, -8, -9, -10, -11, -12]
start = range(-11, 11)


@pytest.mark.parametrize('higher', higher)
@pytest.mark.parametrize('lower', lower)
@pytest.mark.parametrize('start_note', start)
def test_next_valid_word(start_note, lower, higher):
    assert safe_next_valid_word(start_note, higher, lower)
