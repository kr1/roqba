from roqba.static import note_length_groupings


def test_analyze_groupings():
    res = note_length_groupings.analyze_grouping([1, 2, 1, 3])
    assert res == [1, 1, 0, 1, 1, 0, 0]


def test_get_grouping():
    assert (note_length_groupings.get_grouping((5, (2, 3)), "heavy") ==
            sum(note_length_groupings.groupings[(5, (2, 3))]["heavy"], []))
    assert note_length_groupings.get_grouping((8, (4, 4)), "heavy") == sum(note_length_groupings.groupings[(8, (4, 4,))]["heavy"], [])


def test_all_groupings_are_well_formed():
    for grouping_id, grouping in list(note_length_groupings.groupings.items()):
        for grouping_type, value in list(grouping.items()):
            # print grouping_id, grouping_type
            assembled = note_length_groupings._assemble(grouping_id, grouping_type)
            bad = note_length_groupings.badly_formeD(grouping_id[0], assembled)
            assert not bad


def test_run_doctests():
    import doctest
    results = doctest.testmod(note_length_groupings)
    assert results.failed == 0
