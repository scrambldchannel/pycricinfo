from pycricinfo.player import Player


def test_player():
    p = Player(6044)
    assert p.player_id == 6044


def test_player_from_file():
    pass
