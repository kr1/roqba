import pytest

from roqba.utilities import wavetable_peaks

@pytest.fixture
def test_array_long():
    return [0.1, 0.2, 0.3, 0.4, 0.5, 0.4, 0.3, 0.4, 0.5, 0.6, 0.7, 0.6,
            0.5, 0.4, 0.5, 0.6, 0.7, 0.8, 0.7, 0.6, 0.7, 0.8, 0.9, 0.8, 0.9, 0.99, 0.98, 1.0]


@pytest.fixture
def test_array_short():
    return [0.1, 0.5, 0.9, 0.5, 0.9, 1.0, 0.9, 0.5, 0.1]


@pytest.fixture
def test_array():
    return [0.01, 0.4, 0.99, 0.3, 0.2, 0.98, 0.4]


@pytest.fixture
def test_array_shortest():
    return [0.01, 0.4, 0.3, 0.5]


def test_extract_local_extrema(test_array_long):
    returned = wavetable_peaks.detect_local_extrema(test_array_long)
    expected = {4: 0.5, 6: 0.3, 10: 0.7, 13: 0.4, 17: 0.8,
                19: 0.6, 22: 0.9, 23: 0.8, 25: 0.99, 26: 0.98}
    assert returned == expected


def test_extract_local_extrema_short(test_array_short):
    returned = wavetable_peaks.detect_local_extrema(test_array_short)
    expected = {2: 0.9, 3: 0.5, 5: 1.0}
    assert returned == expected

def test_extract_local_extrema_shortest(test_array_shortest):
    returned = wavetable_peaks.detect_local_extrema(test_array_shortest)
    expected = {2: 0.9, 3: 0.5, 5: 1.0}
    assert returned == expected

def test_extract_peak_passages(test_array_short):
    returned = wavetable_peaks.extract_peak_passages(test_array_short)
    expected = {
        'downwards': [{
            'start': (2, 0.9), 'end': (3, 0.5), 'in_between': [], 'deviation': 1}, {
            'start': (5, 1.0), 'end': (2, 0.9), 'in_between': [(3, 0.5)],
                'deviation': 0.5 / (1.0 - 0.9)}, {
            'start': (5, 1.0), 'end': (3, 0.5), 'in_between': [], 'deviation': 1
            }],
        'upwards': [{
            'start': (2, 0.9), 'end': (5, 1.0), 'in_between': [(3, 0.5)],
                'deviation': 0.5 / (1.0 - 0.9)}, {
            'start': (3, 0.5), 'end': (2, 0.9), 'in_between': [], 'deviation': 1}, {
            'start': (3, 0.5), 'end': (5, 1.0), 'in_between': [], 'deviation': 1}
    ]}
    assert returned == expected


def test_extract_peak_passages2(test_array):
    returned = wavetable_peaks.extract_peak_passages(test_array)
    print sorted(returned['upwards'], key=lambda res: res['deviation'])
