from pathlib import Path

from pycricinfo import Player


def test_player():
    p = Player(6044)
    assert p.player_id == 6044
    assert p.name == "Dean Jones"
    assert p.full_name == "Dean Mervyn Jones"
    assert p.batting_style == "Right-hand bat"
    assert p.bowling_style == "Right-arm offbreak"
    assert p.player_stats["batting"]["Tests"]["balls faced"] == "7427"
    assert p.player_stats["batting"]["Tests"]["catches taken"] == "34"
    assert p.player_stats["batting"]["ODIs"]["matches played"] == "164"
    assert p.player_stats["batting"]["Tests"]["stumpings made"] == "0"


def test_player_to_from_file():

    p = Player(52812)
    p.to_file()

    p2 = Player.from_file("52812.html")

    assert p2.player_id == 52812
    assert len(p2.html) > 0
    assert isinstance(p2.html, str)
    assert p2.name == "Sir Viv Richards"
    assert p2.full_name == "Isaac Vivian Alexander Richards"
    assert p2.batting_style == "Right-hand bat"
    assert p2.bowling_style == "Right-arm slow, Right-arm offbreak"
    assert p2.player_stats["batting"]["Tests"]["highest inns score"] == "291"

    p = Path("52812.html")
    p.unlink(missing_ok=True)


def test_player_stats():
    p = Player(7924)
    assert p.player_stats["batting"]["Tests"]["highest inns score"] == "334*"
    assert p.player_stats["bowling"]["First-class"]["wickets taken"] == "2"
    assert p.player_stats["bowling"]["Tests"]["wickets taken"] == "1"
    assert p.player_stats["bowling"]["Tests"]["wickets taken"] == "1"
    assert p.player_stats["bowling"]["First-class"]["five wkts in an inns"] == "0"
    assert p.player_stats["batting"]["List A"]["stumpings made"] == "0"
    assert p.player_stats["bowling"]["Tests"]["wickets taken"] == "1"
    assert p.player_stats["bowling"]["Tests"]["five wkts in an inns"] == "0"
