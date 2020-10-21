import random
from pathlib import Path

from pycricinfo import Ground


def test_ground(grounds):
    g_id = random.choice(grounds)

    g = Ground(g_id)

    assert g.id == g_id
    assert isinstance(g.html, str)


def test_ground_to_from_file(grounds):

    g_id = random.choice(grounds)

    g = Ground(g_id)

    assert isinstance(g.html, str)

    g.to_file(html_file=f"{g_id}.html")

    g2 = Ground.from_file(html_file=f"{g_id}.html")

    assert g.id == g2.id
    assert isinstance(g2.html, str)

    p = Path(f"{g_id}.html")
    p.unlink(missing_ok=True)
