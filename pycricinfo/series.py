import json
from functools import cached_property
from typing import List, Optional

from gazpacho import Soup

from pycricinfo.base import BaseCricinfoPage, get


class Series(BaseCricinfoPage):
    """
    Abstraction of a series
    """

    def __init__(
        self,
        id: int,
        html_file: Optional[str] = None,
        json_file: Optional[str] = None,
    ) -> None:

        self.id = id

        self.url = f"https://www.espncricinfo.com/series/_/id/{self.id}/"

        self.json_url = f"http://core.espnuk.org/v2/sports/cricket/leagues/{self.id}/"

        self.html_file = html_file
        self.json_file = json_file

    @classmethod
    def from_files(cls, html_file: str, json_file: str):
        """
        Create series object from offline files
        """
        with open(html_file, "r") as f:
            # get series_id
            soup = Soup(f.read())
            id = int(
                soup.find("link", attrs={"rel": "canonical"})
                .attrs["href"]
                .split("/")[6]
            )

        return cls(id=id, html_file=html_file, json_file=json_file)

    def to_files(self, html_file: str = None, json_file: str = None) -> None:
        """
        Save the json and html for the series to files
        """

        if not html_file:
            html_file = f"{self.id}.html"
        if not json_file:
            json_file = f"{self.id}.json"

        with open(html_file, "w") as f:
            f.write(self.soup.html)
        with open(json_file, "w") as f:
            f.write(json.dumps(self.json, indent=4))

    @cached_property
    def json(self) -> dict:
        """
        The JSON feed for this series
        """

        if self.json_file:
            with open(self.json_file, "r") as f:
                return json.loads(f.read())
        else:
            return get(self.json_url)

    # need to think about whether these belong here or somewhere else
    @cached_property
    def seasons(self) -> List[int]:
        """
        Get all the seasons for this series
        """
        r = get(f"{self.json_url}seasons/")

        seasons = []
        for season in r.get("items"):
            seasons.append(int(season.get("$ref", "").split("/")[-1]))

        return seasons

    def get_season_matches(self, season: int) -> List[int]:
        """
        Get all match ids that formed part of a specific season for this series
        """
        r = get(f"{self.json_url}seasons/{season}/events/")
        matches = []

        for m in r.get("items", []):
            matches.append(int(m.get("$ref", "").split("/")[-1]))

        return matches

    @cached_property
    def all_matches(self) -> List[int]:
        """
        Iterate through all seasons of this series and return a list of all match ids
        """

        matches = []
        for season in self.seasons:
            for match in self.get_season_matches(season):
                matches.append(match)
        return matches

    @cached_property
    def is_tournament(self) -> bool:
        """
        Simple flag to indicate whether series is a tournament
        """

        return self.json.get("isTournament", False)

    @cached_property
    def name(self) -> Optional[str]:
        """
        The name of the series eg "Indian Premier League"
        """

        return self.json.get("name")

    @cached_property
    def short_name(self) -> Optional[str]:
        return self.json.get("shortName")

    @cached_property
    def abbreviation(self) -> Optional[str]:
        return self.json.get("abbreviation")
