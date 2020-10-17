from pycricinfo.series import Series


def test_series():
    s = Series(8048)
    assert s.series_id == 8048
    assert s.is_tournament
    assert s.name == "Indian Premier League"
