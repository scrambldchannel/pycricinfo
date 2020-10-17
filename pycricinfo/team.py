import json
from functools import cached_property
from typing import Optional

from gazpacho import Soup, get

from pycricinfo import PyCricinfoException


class Team(object):
    """
    Abstraction of a team
    """

    def __init__(
        self,
        team_id: int,
        html_file: str = None,
        json_file: str = None,
        timeout: int = 5,
    ) -> None:

        self.team_id = team_id

        self.url = f"https://www.espncricinfo.com/team/_/id/{self.team_id}/"

        # this doesn't work
        self.json_url = (
            f"https://core.espnuk.org/v2/sports/cricket/teams/{self.team_id}"
        )

        self.html_file = html_file
        self.json_file = json_file

        self.timeout = timeout

    @cached_property
    def html(self) -> str:

        if self.html_file:
            with open(self.html_file, "r") as f:
                return f.read()
        else:
            r = get(self.url)
            return r

    @cached_property
    def json(self) -> dict:

        if self.json_file:
            with open(self.json_file, "r") as f:
                return json.loads(f.read())
        else:
            return get(self.json_url)

    @cached_property
    def soup(self) -> Soup:
        return Soup(self.html)

    @cached_property
    def embedded_json(self) -> Optional[dict]:
        try:
            json_text = self.soup.find("script", attrs={"id": "__NEXT_DATA__"}).text
            return json.loads(json_text)
        except PyCricinfoException:
            return None
