from roqba.static import note_length_groupings, meters


def test_all_meters_have_groupings():
    for meter in meters.METERS:
        note_length_groupings.get_grouping(meter, "default")
