from roqba.static import note_length_groupings


def test_analyze_groupings():
    res = note_length_groupings.analyze_grouping([1, 2, 1, 3])
    assert res == [1, 1, 0, 1, 1, 0, 0]


def test_get_grouping():
    assert (note_length_groupings.get_grouping((5, (2, 3)), "heavy") ==
            sum(note_length_groupings.groupings[(5, (2, 3))]["heavy"], []))
    assert note_length_groupings.get_grouping((8, (4, 4)), "heavy") == sum(note_length_groupings.groupings[(8, (4, 4,))]["heavy"], [])


def test_run_doctests():
    import doctest
    doctest.testmod(note_length_groupings)
