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
    ) -> None:

        self.team_id = team_id

        self.url = f"https://www.espncricinfo.com/team/_/id/{self.team_id}/"

        self.json_url = None

        self.html_file = html_file
        self.json_file = json_file

    @cached_property
    def html(self) -> str:

        if self.html_file:
            with open(self.html_file, "r") as f:
                return f.read()
        else:
            r = get(self.url)
            return r

    @cached_property
    def soup(self) -> Soup:
        return Soup(self.html)

    @cached_property
    def embedded_json(self) -> Optional[dict]:
        try:
            json_text = self.soup.find(
                "script", attrs={"id": "__NEXT_DATA__"}, mode="first"
            ).text
            return json.loads(json_text)
        except:
            raise PyCricinfoException("Team.embedded_json", "Embedded JSON not found")
