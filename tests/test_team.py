from pathlib import Path

from pycricinfo.team import Team


def test_team():
    t = Team(387)
    assert t.team_id == 387
    assert t.html is not None


def test_team_from_file():

    html_file = Path(__file__).parent.joinpath("serialised_objects/team/", "387.html")

    # json not available
    json_file = None

    t = Team(387, html_file=html_file, json_file=json_file)
    assert t.team_id == 387
    assert t.html is not None
