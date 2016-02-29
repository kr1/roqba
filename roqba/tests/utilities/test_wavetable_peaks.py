import pytest

from roqba.utilities import wavetable_peaks

@pytest.fixture
def test_array_long():
    return [1, 2, 3, 4, 5, 4, 3, 4, 5, 6, 7, 6, 5, 4, 5, 6, 7, 8, 7, 6, 7, 8, 9]


@pytest.fixture
def test_array_short():
    return [1, 2, 3, 2, 3, 4, 3, 2, 1]


def test_extract_local_extrema(test_array_long):
    returned = wavetable_peaks.detect_local_extrema(test_array_long)
    expected = {4: 5, 6: 3, 10: 7, 13: 4, 17: 8, 19: 6}
    assert returned == expected


def test_extract_local_extrema_short(test_array_short):
    returned = wavetable_peaks.detect_local_extrema(test_array_short)
    expected = {2: 3, 3: 2, 5: 4}
    assert returned == expected


def test_extract_peak_passages(test_array_short):
    returned = wavetable_peaks.extract_peak_passages(test_array_short)
    expected = {
        'downwards': [{
            'start': (2, 3), 'end': (3, 2)}, {
            'start': (5, 4), 'end': (2, 3)}, {
            'start': (5, 4), 'end': (3, 2)
            }],
        'upwards': [{
            'start': (2, 3), 'end': (5, 4)}, {
            'start': (3, 2), 'end': (2, 3)}, {
            'start': (3, 2), 'end': (5, 4)}
    ]}
    assert returned == expected
