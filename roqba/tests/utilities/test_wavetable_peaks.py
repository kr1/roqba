import pytest

from roqba.utilities import wavetable_peaks

@pytest.fixture
def test_array():
    return [1, 2, 3, 4, 5, 4, 3, 4, 5, 6, 7, 6, 5, 4, 5, 6, 7, 8, 7, 6, 7, 8, 9]


def test_extract_local_extrema(test_array):
    returned = wavetable_peaks.detect_local_extrema(test_array)
    expected = {4: 5, 6: 3, 10: 7, 13: 4, 17: 8, 19: 6}
    assert returned == expected
