from pycricinfo import LiveScores


def test_livescores():
    ls = LiveScores()
    assert isinstance(ls.html, str)
    assert isinstance(ls.live_matches, list)
    assert isinstance(ls.embedded_json, dict)
