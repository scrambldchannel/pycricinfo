import pytest


@pytest.fixture(scope="module")
def matches():
    return [
        1187009,
        1216494,
        1234908,
        356789,
        1152847,
        1152783,
        64976,
        326203,
        67075,
    ]


@pytest.fixture(scope="module")
def players():
    return [
        5600,
        659081,
        54962,
        4188,
        6467,
        53477,
        267192,
        9130,
        30475,
    ]


@pytest.fixture(scope="module")
def grounds():
    return [56293, 56402, 56490, 1170382, 59266, 59269, 468384, 58831]


@pytest.fixture(scope="module")
def teams():
    return [
        30,
        215,
        1145839,
        335977,
        5153,
        1234676,
        233713,
    ]
