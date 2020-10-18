from pathlib import Path

from pycricinfo import Match


def test_test_match():
    m = Match(63438)
    assert m.match_id == 63438
    assert (
        m.description
        == "Australia tour of India, 1st Test: India v Australia at Chennai, Sep 18-22, 1986"
    )


def test_ipl():
    m = Match(734043)
    assert m.match_id == 734043
    assert (
        m.description
        == "Pepsi Indian Premier League, Qualifier 1: Kings XI Punjab v Kolkata Knight Riders at Kolkata, May 27-28, 2014"
    )


def test_match_t_from_file():

    m = Match(1216499)
    m.to_files()

    m2 = Match.from_files(html_file="1216499.html", json_file="1216499.json")

    assert m.match_id == m2.match_id
    assert m.description == m2.description

    p = Path("1216499.html")
    p.unlink(missing_ok=True)
    p = Path("1216499.json")
    p.unlink(missing_ok=True)


def test_embedded_json():

    m = Match(1210428)

    assert (
        m.embedded_json["props"]["pageProps"]["data"]["meta"]["leagueName"]
        == "Australia tour of Scotland"
    )
