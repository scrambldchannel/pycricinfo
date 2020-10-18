import json
from functools import cached_property
from typing import List, Optional

from gazpacho import Soup, get


class Series(object):
    """
    Abstraction of a series
    """

    def __init__(
        self,
        series_id: int,
        html_file: Optional[str] = None,
        json_file: Optional[str] = None,
    ) -> None:

        self.series_id = series_id

        self.url = f"https://www.espncricinfo.com/series/_/id/{self.series_id}/"

        self.json_url = (
            f"http://core.espnuk.org/v2/sports/cricket/leagues/{self.series_id}/"
        )

        self.html_file = html_file
        self.json_file = json_file

    def to_files(self, html_file: str = None, json_file: str = None) -> None:

        if not html_file:
            html_file = f"{self.series_id}.html"
        if not json_file:
            json_file = f"{self.series_id}.json"

        with open(html_file, "w") as f:
            f.write(self.html)
        with open(json_file, "w") as f:
            f.write(json.dumps(self.json, indent=4))

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
    def seasons(self) -> List[int]:
        r = get(f"{self.json_url}seasons/")

        seasons = []
        for season in r.get("items"):
            seasons.append(int(season.get("$ref", "").split("/")[-1]))

        return seasons

    def get_season_matches(self, season: int) -> List[int]:
        r = get(f"{self.json_url}seasons/{season}/events/")
        matches = []

        for m in r.get("items", []):
            matches.append(int(m.get("$ref", "").split("/")[-1]))

        return matches

    @cached_property
    def all_matches(self) -> List[int]:
        matches = []
        for season in self.seasons:
            for match in self.get_season_matches(season):
                matches.append(match)
        return matches

    @cached_property
    def is_tournament(self) -> bool:
        return self.json.get("isTournament", False)

    @cached_property
    def name(self) -> Optional[str]:
        return self.json.get("name")

    @cached_property
    def short_name(self) -> Optional[str]:
        return self.json.get("shortName")

    @cached_property
    def abbreviation(self) -> Optional[str]:
        return self.json.get("abbreviation")

    @cached_property
    def slug(self) -> Optional[str]:
        return self.json.get("slug")
