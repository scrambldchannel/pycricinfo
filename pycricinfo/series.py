import json
from functools import cached_property
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

from pycricinfo.exceptions import PyCricinfoException


class Series(object):
    """
    Abstraction of a series
    """

    def __init__(
        self,
        series_id: int,
        html_file: Optional[str] = None,
        json_file: Optional[str] = None,
        timeout: int = 5,
    ) -> None:

        self.series_id = series_id

        self.url = f"https://www.espncricinfo.com/series/_/id/{self.series_id}/"

        self.json_url = (
            f"http://core.espnuk.org/v2/sports/cricket/leagues/{self.series_id}/"
        )

        self.html_file = html_file
        self.json_file = json_file

        self.timeout = timeout

    @cached_property
    def html(self) -> BeautifulSoup:

        if self.html_file:
            with open(self.html_file, "r") as f:
                return BeautifulSoup(f.read(), "html.parser")
        else:
            r = requests.get(self.url, timeout=self.timeout)
            if r.status_code == 404:
                raise PyCricinfoException
            else:
                return BeautifulSoup(r.text, "html.parser")

    @cached_property
    def json(self) -> dict:

        if self.json_file:
            with open(self.json_file, "r") as f:
                return json.loads(f.read())
        else:
            r = requests.get(self.json_url, timeout=self.timeout)
            # need to do something to catch the timeout exception here
            if r.status_code == 404:
                raise PyCricinfoException("Series.json", "404")
            else:
                return r.json()

    @cached_property
    def seasons(self) -> List[int]:
        r = requests.get(f"{self.json_url}seasons/", timeout=self.timeout)

        seasons = []
        for season in r.json().get("items"):
            seasons.append(int(season.get("$ref", "").split("/")[-1]))

        return seasons

    def get_season_matches(self, season: int) -> List[int]:
        r = requests.get(
            f"{self.json_url}seasons/{season}/events/", timeout=self.timeout
        )
        matches = []

        for m in r.json().get("items", []):
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
