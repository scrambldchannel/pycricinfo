from pycricinfo.match import Match


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


def test_match_from_files():
    pass
