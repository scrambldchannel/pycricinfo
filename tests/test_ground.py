from pathlib import Path

from pycricinfo import Ground


def test_ground():
    g = Ground(59269)
    assert g.id == 59269


def test_ground_to_from_file():
    g = Ground(57129)
    g.to_file()
    g2 = Ground.from_file(html_file="57129.html")
    g.id = g2.id

    p = Path("57129.html")
    p.unlink(missing_ok=True)
