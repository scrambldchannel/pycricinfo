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


def test_match_from_file():

    html_file = Path(__file__).parent.joinpath(
        "serialised_objects/match/", "1216499.html"
    )
    json_file = Path(__file__).parent.joinpath(
        "serialised_objects/match/", "1216499.json"
    )

    m = Match(1216499, html_file=html_file, json_file=json_file)
    assert m.match_id == 1216499
    assert (
        m.description
        == "Indian Premier League, 48th Match: Mumbai Indians v Royal Challengers Bangalore at Abu Dhabi, Oct 28, 2020"
    )


def test_embedded_json():

    m = Match(1210428)

    assert (
        m.embedded_json["props"]["pageProps"]["data"]["meta"]["leagueName"]
        == "Australia tour of Scotland"
    )
