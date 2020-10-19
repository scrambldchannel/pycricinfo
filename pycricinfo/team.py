import json
import warnings
from functools import cached_property
from typing import Optional

from gazpacho import Soup

from pycricinfo.base import BaseCricinfoPage


class Team(BaseCricinfoPage):
    """
    Abstraction of a team
    """

    def __init__(
        self,
        id: int,
        html_file: str = None,
    ) -> None:

        self.id = id
        self.url = f"https://www.espncricinfo.com/team/_/id/{self.id}/"

        self.html_file = html_file

    @classmethod
    def from_file(cls, html_file: str):
        with open(html_file, "r") as f:
            # get team_id
            soup = Soup(f.read())
            id = int(
                soup.find("link", attrs={"rel": "canonical"})
                .attrs["href"]
                .split("/")[6]
            )

        return cls(id=id, html_file=html_file)

    @cached_property
    def embedded_json(self) -> Optional[dict]:
        try:
            json_text = self.soup.find(
                "script", attrs={"id": "__NEXT_DATA__"}, mode="first"
            ).text
            return json.loads(json_text)
        except Exception:
            warnings.warn("Embedded JSON not found", RuntimeWarning)
            return {}
