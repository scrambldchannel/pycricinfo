import json
import warnings
from functools import cached_property
from typing import Optional

from gazpacho import Soup, get
from gazpacho.utils import HTTPError

from pycricinfo.exceptions import PageNotFoundException, PyCricinfoException


class Match(object):
    """
    Object that abstracts the information avialable about a match
    """

    def __init__(
        self,
        match_id: int,
        html_file: Optional[str] = None,
        json_file: Optional[str] = None,
        **kwargs,
    ) -> None:

        self.match_id = match_id

        self.url = f"https://www.espncricinfo.com/matches/engine/match/{match_id}.html"
        self.json_url = (
            f"https://www.espncricinfo.com/matches/engine/match/{match_id}.json"
        )

        self.html_file = html_file
        self.json_file = json_file

    @classmethod
    def from_files(cls, html_file: str, json_file: str):
        with open(html_file, "r") as f:
            # get match_id
            soup = Soup(f.read())
            match_id = int(
                soup.find("link", attrs={"rel": "canonical"})
                .attrs["href"]
                .split("/")[6]
            )

        return cls(match_id=match_id, html_file=html_file, json_file=json_file)

    def to_files(self, html_file: str = None, json_file: str = None) -> None:

        if not html_file:
            html_file = f"{self.match_id}.html"
        if not json_file:
            json_file = f"{self.match_id}.json"

        with open(html_file, "w") as f:
            f.write(self.soup.html)
        with open(json_file, "w") as f:
            f.write(json.dumps(self.json, indent=4))

    @cached_property
    def html(self) -> str:

        if self.html_file:
            with open(self.html_file, "r") as f:
                return f.read()
        else:
            try:
                return get(self.url)
            except HTTPError as e:
                if e.code == 404:
                    raise PageNotFoundException(
                        e.code,
                        f"Match {self.match_id} not found. Check that the id is correct.",
                    )
                return ""

    @cached_property
    def json(self) -> dict:
        if self.json_file:
            with open(self.json_file, "r") as f:
                return json.loads(f.read())
        else:
            try:
                return get(self.json_url)
            except HTTPError as e:
                if e.code == 404:
                    raise PageNotFoundException(
                        e.code,
                        f"Match {self.match_id} not found. Check that the id is correct.",
                    )
                raise PyCricinfoException(e.code, e.message)

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
        except Exception:
            warnings.warn(
                f"Embedded JSON not found for match {self.match_id}", RuntimeWarning
            )
            return None

    @cached_property
    def season(self):
        try:
            return self.json["Match"]["season"]
        except Exception:
            warnings.warn("Property not found in page", RuntimeWarning)
            return None

    @cached_property
    def description(self) -> Optional[str]:
        try:
            return self.json.get("description")
        except Exception:
            warnings.warn("Property not found in page", RuntimeWarning)
            return None

    @cached_property
    def series(self):
        try:
            return self.json.get("series")
        except Exception:
            warnings.warn("Property not found in page", RuntimeWarning)
            return None

    @cached_property
    def series_id(self):
        try:
            return self.json["series"][-1]["core_recreation_id"]
        except Exception:
            warnings.warn("Property not found in page", RuntimeWarning)
            return None

    @cached_property
    def date(self):
        try:
            return self.json["match"]["start_date_raw"]
        except Exception:
            warnings.warn("Property not found in page", RuntimeWarning)
            return None

    @cached_property
    def result(self):
        try:
            return self.json["live"]["status"]
        except Exception:
            warnings.warn("Property not found in page", RuntimeWarning)
            return None

    @cached_property
    def ground_id(self):
        try:
            return self.json["match"]["ground_id"]
        except Exception:
            warnings.warn("Property not found in page", RuntimeWarning)
            return None

    @cached_property
    def ground_name(self):
        try:
            return self.json["match"]["ground_name"]
        except Exception:
            warnings.warn("Property not found in page", RuntimeWarning)
            return None

    @cached_property
    def innings_list(self):
        try:
            return self.json["centre"]["common"]["innings_list"]
        except Exception:
            warnings.warn("Property not found in page", RuntimeWarning)
            return None

    @cached_property
    def innings(self):
        try:
            return self.json["innings"]
        except Exception:
            warnings.warn("Property not found in page", RuntimeWarning)
            return None

    @cached_property
    def team_1(self):
        try:
            return self.json["team"][0]
        except Exception:
            warnings.warn("Property not found in page", RuntimeWarning)
            return None

    @cached_property
    def team_1_id(self):
        try:
            return self.team_1["team_id"]
        except Exception:
            warnings.warn("Property not found in page", RuntimeWarning)
            return None

    @cached_property
    def team_1_abbreviation(self):
        try:
            return self.team_1["team_abbreviation"]
        except Exception:
            warnings.warn("Property not found in page", RuntimeWarning)
            return None

    @cached_property
    def team_1_players(self):
        try:
            return self.team_1.get("player", [])
        except Exception:
            warnings.warn("Property not found in page", RuntimeWarning)
            return None

    @cached_property
    def team_1_innings(self):
        try:
            return [
                inn
                for inn in self.json["innings"]
                if inn["batting_team_id"] == self.get_team_1_id()
            ][0]
        except Exception:
            warnings.warn("Property not found in page", RuntimeWarning)
            return None

    @cached_property
    def team_2(self):
        try:
            return self.json["team"][1]
        except Exception:
            warnings.warn("Property not found in page", RuntimeWarning)
            return None

    @cached_property
    def team_2_id(self):
        try:
            return self.team_2["team_id"]
        except Exception:
            warnings.warn("Property not found in page", RuntimeWarning)
            return None

    @cached_property
    def team_2_abbreviation(self):
        try:
            return self.team_2["team_abbreviation"]
        except Exception:
            warnings.warn("Property not found in page", RuntimeWarning)
            return None

    @cached_property
    def team_2_players(self):
        try:
            return self.team_2.get("player", [])
        except Exception:
            warnings.warn("Property not found in page", RuntimeWarning)
            return None

    @cached_property
    def team_2_innings(self):
        try:
            return [
                inn
                for inn in self.json["innings"]
                if inn["batting_team_id"] == self.get_team_2_id()
            ][0]
        except Exception:
            warnings.warn("Property not found in page", RuntimeWarning)
            return None

    # embedded_json methods

    @cached_property
    def rosters(self):
        try:
            return self.embedded_json["props"]["pageProps"]["data"]["content"]["teams"]
        except Exception:
            warnings.warn("Property not found in page", RuntimeWarning)
            return None

    @cached_property
    def all_innings(self):
        try:
            return self.embedded_json["props"]["pageProps"]["data"]["content"][
                "innings"
            ]
        except Exception:
            warnings.warn("Property not found in page", RuntimeWarning)
            return None
