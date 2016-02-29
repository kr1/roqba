from roqba.utilities import project_scale


def test_project_scale_basic():
    scaled = project_scale(0.3, 0.1, 0.9, 10, 20)
    assert scaled == 12.5


def test_project_scale_reversed():
    scaled = project_scale(0.3, 0.1, 0.9, 20, 10)
    assert scaled == 17.5


def test_project_scale_zero_cross():
    scaled = project_scale(-0.1, 0.1, -0.4, 70, 10)
    assert scaled == 46


def test_project_scale_zero_cross_reversed():
    scaled = project_scale(-0.1, 0.1, -0.4, 10, 70)
    assert scaled == 34
