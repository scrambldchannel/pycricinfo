import random
from datetime import datetime
from pathlib import Path

import pytest

from pycricinfo import Match, PageNotFoundException, Player


def test_test_match():
    m = Match(63438)
    assert m.id == 63438
    assert (
        m.name
        == "Australia tour of India, 1st Test: India v Australia at Chennai, Sep 18-22, 1986"
    )

    assert m.status == "complete"


def test_ipl():
    m = Match(734043)
    assert m.id == 734043
    assert (
        m.name
        == "Pepsi Indian Premier League, Qualifier 1: Kolkata Knight Riders v Kings XI Punjab at Kolkata, May 27-28, 2014"
    )
    assert m.status == "complete"


def test_date():
    m = Match(1175356)
    assert isinstance(m.date, datetime)

    m2 = Match(1226908)
    assert isinstance(m.date, datetime)

    assert m2.date > m.date


def test_format():
    m = Match(1227897)
    assert m.format["id"] == 6
    assert m.format["name"] == "Twenty20"

    m2 = Match(215010)
    assert m2.format["id"] == 4
    assert m2.format["name"] == "Test"

    m3 = Match(65117)
    assert m3.format["id"] == 5
    assert m3.format["name"] == "ODI"

    m4 = Match(1226905)
    assert m4.format["id"] == 13
    assert m4.format["name"] == "Other Twenty20 matches"


def test_season():
    m = Match(65117)

    assert m.season["id"] == 1987
    assert m.season["name"] == "1987/88"

    m2 = Match(734043)

    assert m2.season["id"] == 2014
    assert m2.season["name"] == "2014"


def test_series():
    m = Match(1233446)
    assert isinstance(m.series, dict)
    assert m.series["id"] == 8043
    assert m.series["name"] == "Sheffield Shield"


def test_status(matches):
    m = Match(random.choice(matches))
    assert m.status in ["forthcoming", "current", "complete"]


def test_ground():
    m = Match(62396)
    assert isinstance(m.series, dict)
    assert m.ground["id"] == 56441
    assert m.ground["name"] == "Melbourne Cricket Ground"


def test_teams(matches):
    m = Match(62396)

    assert len(m.teams) == 2
    assert len(m.teams[0]["players"]) == 11
    assert len(m.teams[1]["players"]) == 11

    # get a random player from each team and check the id is valid
    for t in m.teams:
        random_player = t["players"][random.randint(0, 10)]

        p = Player(random_player["id"])

        assert p.name == random_player["name"]

    m2 = Match(1152847)
    assert len(m2.teams) == 2
    assert len(m2.teams[0]["players"]) == 11
    # concussion sub
    assert len(m2.teams[1]["players"]) == 12

    # get a random player from each team and check the id is valid
    for t in m2.teams:
        random_player = t["players"][random.randint(0, 10)]

        p = Player(random_player["id"])

        assert p.name == random_player["name"]

    m3 = Match(random.choice(matches))
    assert len(m3.teams) == 2
    # get a random player from each team and check the id is valid
    for t in m3.teams:
        if t.get("players"):

            random_player = t["players"][random.randint(0, 10)]

            p = Player(random_player["id"])

            assert p.name == random_player["name"]


def test_match_to_from_file(matches):

    m = Match(random.choice(matches))
    m.to_files()

    m2 = Match.from_files(html_file=f"{m.id}.html", json_file=f"{m.id}.json")

    assert m.id == m2.id
    assert m.name == m2.name
    assert m.format == m2.format
    assert m.series == m2.series
    assert m.season == m2.season
    assert m.date == m2.date
    assert m.ground == m2.ground

    p = Path(f"{m.id}.html")
    p.unlink(missing_ok=True)
    p = Path(f"{m.id}.json")
    p.unlink(missing_ok=True)


def test_embedded_json():

    m = Match(1210428)

    assert (
        m.embedded_json["props"]["pageProps"]["data"]["meta"]["leagueName"]
        == "Australia tour of Scotland"
    )


def test_missing_match():

    with pytest.raises(PageNotFoundException):
        m = Match(123)
        print(m.html)


def test_no_embedded_json():

    with pytest.warns(RuntimeWarning):
        m = Match(123)
        print(m.embedded_json)


def test_match_stats():

    # more needed
    m = Match(63438)

    stats = m.match_stats

    assert isinstance(stats, dict)
    assert m.match_stats["all_innings"][1]["batting"][1]["name"] == "Kris Srikkanth"
    assert m.match_stats["all_innings"][0]["batting"][2]["runs"] == 210

    assert m.match_stats["all_innings"][3]["bowling"][2]["runs"] == 146
    assert m.match_stats["all_innings"][3]["bowling"][2]["wickets"] == 5

    assert m.match_stats["all_innings"][2]["bowling"][0]["wides"] == 0


def test_all_innings():

    # more needed
    m = Match(1216509)

    assert m._all_innings[0]["bowling"][0]["name"] == "Tushar Deshpande"
    assert m._all_innings[0]["bowling"][2]["wickets"] == 0
    assert m._all_innings[0]["bowling"][5]["name"] == "Marcus Stoinis"
    assert m._all_innings[0]["bowling"][1]["sixes"] == 2
    assert m._all_innings[0]["bowling"][3]["overs"] == 4.0
    assert m._all_innings[0]["bowling"][3]["overs"] == 4
