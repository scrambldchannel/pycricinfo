from pathlib import Path

from pycricinfo import Team


def test_team():
    t = Team(387)
    assert t.id == 387
    assert t.html is not None


def test_team_to_from_file():

    t = Team(387)
    t.to_file()

    t2 = Team.from_file("387.html")

    assert t.id == t2.id
    assert t2.html is not None

    p = Path("387.html")
    p.unlink(missing_ok=True)
