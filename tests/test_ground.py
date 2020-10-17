from pathlib import Path

from pycricinfo import Ground


def test_ground():
    g = Ground(59269)
    assert g.ground_id == 59269


def test_ground_from_file():

    html_file = Path(__file__).parent.joinpath(
        "serialised_objects/ground/", "59269.html"
    )

    g = Ground(52812, html_file=html_file, json_file=None)
    assert g.ground_id == 52812
