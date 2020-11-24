from pathlib import Path

from pycricinfo import Series


def test_series():
    s = Series(8048)
    assert s.id == 8048
    assert s.is_tournament
    assert s.name == "Indian Premier League"


def test_series_to_from_file():

    s = Series(8044)
    s.to_files()

    s2 = Series.from_files(html_file="8044.html", json_file="8044.json")

    assert s.id == s2.id
    assert s.name == s2.name
    assert s.seasons == s2.seasons

    p = Path("8044.html")
    p.unlink(missing_ok=True)
    p = Path("8044.json")
    p.unlink(missing_ok=True)


def test_get_seasons():
    s = Series(8048)
    assert set(s.seasons) == set(
        [2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
    )


def test_get_season_matches():

    s = Series(8048)

    all_2020_games = [
        1216492,
        1216493,
        1216534,
        1216496,
        1216508,
        1216510,
        1216539,
        1216545,
        1216527,
        1216547,
        1216532,
        1216504,
        1216503,
        1216516,
        1216514,
        1216515,
        1216538,
        1216513,
        1216519,
        1216511,
        1216501,
        1216542,
        1216500,
        1216523,
        1216525,
        1216507,
        1216529,
        1216540,
        1216528,
        1216543,
        1216531,
        1216526,
        1216522,
        1216509,
        1216512,
        1216517,
        1216533,
        1216546,
        1216494,
        1216518,
        1216521,
        1216497,
        1216498,
        1216544,
        1216541,
        1216520,
        1216524,
        1216499,
        1216536,
        1216537,
        1216535,
        1216502,
        1216506,
        1216530,
        1216505,
        1216495,
        1237177,
        1237178,
        1237180,
        1237181,
    ]
    assert set(s.get_season_matches(2020)) == set(all_2020_games)
