from pathlib import Path

from pycricinfo.player import Player


def test_player():
    p = Player(6044)
    assert p.player_id == 6044


def test_player_from_file():

    html_file = Path(__file__).parent.joinpath(
        "serialised_objects/player/", "52812.html"
    )

    # json not available
    json_file = None

    p = Player(52812, html_file=html_file, json_file=json_file)
    assert p.player_id == 52812
