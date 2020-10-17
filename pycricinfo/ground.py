import json
from functools import cached_property
from typing import Optional

from gazpacho import Soup, get

from pycricinfo import PyCricinfoException


class Ground(object):
    """
    Abstraction of a team
    """

    def __init__(
        self,
        ground_id: int,
        html_file: str = None,
        json_file: str = None,
        timeout: int = 5,
    ) -> None:

        self.ground_id = ground_id

        self.url = (
            f"https://www.espncricinfo.com/ci/content/ground/{self.ground_id}.html"
        )

        # this doesn't work
        self.json_url = (
            f"https://core.espnuk.org/v2/sports/cricket/ground/{self.ground_id}"
        )

        self.html_file = html_file
        self.json_file = json_file

        self.timeout = timeout

    @cached_property
    def html(self):
        if self.html_file:
            with open(self.html_file, "r") as f:
                return f.read
        else:
            r = get(self.url)
            return r

    @cached_property
    def json(self):

        if self.json_file:
            with open(self.json_file, "r") as f:
                return json.loads(f.read())
        else:
            return get(self.json_url)

    @cached_property
    def soup(self) -> Soup:
        return Soup(self.html, "html.parser")

    @cached_property
    def embedded_json(self) -> Optional[dict]:
        try:
            json_text = self.soup.find("script", attrs={"id": "__NEXT_DATA__"}).text
            return json.loads(json_text)
        except PyCricinfoException:
            return None
