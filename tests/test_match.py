from datetime import datetime
from pathlib import Path

import pytest

from pycricinfo import Match, PageNotFoundException


def test_test_match():
    m = Match(63438)
    assert m.id == 63438
    assert (
        m.description
        == "Australia tour of India, 1st Test: India v Australia at Chennai, Sep 18-22, 1986"
    )


def test_ipl():
    m = Match(734043)
    assert m.id == 734043
    assert (
        m.description
        == "Pepsi Indian Premier League, Qualifier 1: Kings XI Punjab v Kolkata Knight Riders at Kolkata, May 27-28, 2014"
    )


def test_date():
    m = Match(1175356)
    assert isinstance(m.date, datetime)

    m2 = Match(1226908)
    assert isinstance(m.date, datetime)

    assert m2.date > m.date


def test_format():
    m = Match(1227897)
    assert m.format == "Twenty20"

    m2 = Match(215010)
    assert m2.format == "Test"


def test_series():
    m = Match(1233446)
    assert isinstance(m.series, dict)
    assert m.series["id"] == 8043
    assert m.series["name"] == "Sheffield Shield"


def test_match_t_from_file():

    m = Match(1216499)
    m.to_files()

    m2 = Match.from_files(html_file="1216499.html", json_file="1216499.json")

    assert m.id == m2.id
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


def test_missing_match():

    with pytest.raises(PageNotFoundException):
        m = Match(123)
        print(m.html)


def test_no_embedded_json():

    with pytest.warns(RuntimeWarning):
        m = Match(123)
        print(m.embedded_json)
