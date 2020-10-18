from pathlib import Path

from pycricinfo import Player


def test_player():
    p = Player(6044)
    assert p.player_id == 6044
    assert p.name == "Dean Jones"
    assert p.full_name == "Dean Mervyn Jones"
    assert p.batting_style == "Right-hand bat"
    assert p.bowling_style == "Right-arm offbreak"
    assert p.player_stats["batting"]["Tests"]["balls"] == "7427"
    assert p.player_stats["batting"]["Tests"]["catches"] == "34"
    assert p.player_stats["batting"]["Tests"]["matches"] == "52"
    assert p.player_stats["batting"]["Tests"]["stumpings"] == "0"


def test_player_from_file():

    html_file = Path(__file__).parent.joinpath(
        "serialised_objects/player/", "52812.html"
    )

    # json not available
    json_file = None

    p = Player(52812, html_file=html_file, json_file=json_file)
    assert p.player_id == 52812
    assert len(p.html) > 0
    assert isinstance(p.html, str)
    assert p.name == "Sir Viv Richards"
    assert p.full_name == "Isaac Vivian Alexander Richards"
    assert p.batting_style == "Right-hand bat"
    assert p.bowling_style == "Right-arm slow, Right-arm offbreak"

    assert p.player_stats["batting"]["Tests"]["hs"] == "291"


def test_player_stats():
    p = Player(7924)
    assert p.player_stats["batting"]["Tests"]["hs"] == "334*"
    assert p.player_stats["bowling"]["First-class"]["wickets"] == "2"
