from typing import List

import requests

from pycricinfo.exceptions import PyCricinfoException


class Series(object):
    """
    Abstraction of a series
    """

    def __init__(self, series_id: int) -> None:

        self.series_id = series_id

        self.json_url = (
            f"http://core.espnuk.org/v2/sports/cricket/leagues/{self.series_id}/"
        )

        self.json = self.get_json()

        # parsing json
        if self.json:
            # need to drill into what this is
            self.name = self.json["name"]
            self.short_name = self.json["shortName"]
            self.abbreviation = self.json["abbreviation"]
            self.slug = self.json["slug"]
            self.is_tournament = self.json["isTournament"]
            self.url = self.json["links"][0]["href"]

    def get_json(self) -> dict:

        r = requests.get(self.json_url)
        # proper exception handling needed

        if r.status_code == 404:
            raise PyCricinfoException
        else:
            return r.json()

    def get_seasons(self) -> List[int]:
        r = requests.get(
            f"http://core.espnuk.org/v2/sports/cricket/leagues/{self.series_id}/seasons/"
        )
        seasons = []
        for season in r.json().get("items"):
            seasons.append(int(season.get("$ref", "").split("/")[-1]))

        return seasons

    def get_season_matches(self, season: int) -> List[int]:
        r = requests.get(
            f"http://core.espnuk.org/v2/sports/cricket/leagues/{self.series_id}/seasons/{season}/events/"
        )
        matches = []
        for m in r.json().get("items"):
            matches.append(int(m.get("$ref", "").split("/")[-1]))

        return matches

    def get_all_matches(self) -> List[int]:
        matches = []
        for season in self.get_seasons():
            for match in self.get_season_matches(season):
                matches.append(match)
        return matches
