import json
import warnings
from datetime import datetime
from functools import cached_property
from typing import List, Optional

from gazpacho import Soup, get
from gazpacho.utils import HTTPError

from pycricinfo.base import BaseCricinfoPage
from pycricinfo.exceptions import PageNotFoundException, PyCricinfoException


class Match(BaseCricinfoPage):
    """
    Object that abstracts the information avialable about a match
    """

    def __init__(
        self,
        id: int,
        html_file: Optional[str] = None,
        json_file: Optional[str] = None,
        **kwargs,
    ) -> None:

        self.id = id

        self.url = f"https://www.espncricinfo.com/matches/engine/match/{id}.html"
        self.json_url = f"https://www.espncricinfo.com/matches/engine/match/{id}.json"

        self.html_file = html_file
        self.json_file = json_file

    @classmethod
    def from_files(cls, html_file: str, json_file: str):
        with open(html_file, "r") as f:
            # get match id
            soup = Soup(f.read())
            id = int(
                soup.find("link", attrs={"rel": "canonical"})
                .attrs["href"]
                .split("/")[6]
            )

        return cls(id=id, html_file=html_file, json_file=json_file)

    def to_files(self, html_file: str = None, json_file: str = None) -> None:

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
                        f"Match {self.id} not found. Check that the id is correct.",
                    )
                raise PyCricinfoException(e.code, e.message)

    @cached_property
    def embedded_json(self) -> Optional[dict]:
        try:
            json_text = self.soup.find(
                "script", attrs={"id": "__NEXT_DATA__"}, mode="first"
            ).text
            return json.loads(json_text)
        except Exception:
            warnings.warn(
                f"Embedded JSON not found for match {self.id}", RuntimeWarning
            )
            return None

    @cached_property
    def name(self) -> Optional[str]:
        try:
            return self.json.get("description")
        except Exception:
            warnings.warn("Property not found in page", RuntimeWarning)
            return None

    @cached_property
    def short_name(self) -> Optional[str]:
        try:
            return self.json.get("description")
        except Exception:
            warnings.warn("Property not found in page", RuntimeWarning)
            return None

    @cached_property
    def date(self) -> Optional[datetime]:
        try:
            date_str = self.json["match"]["start_datetime_local"]
            return datetime.fromisoformat(date_str)
        except Exception:
            warnings.warn("Property not found in page", RuntimeWarning)
            return None

    @cached_property
    def format(self) -> Optional[dict]:
        try:
            if self.json["match"].get("international_valid") != "1":
                return {
                    "id": int(self.json["match"].get("general_class_id", -1)),
                    "name": self.json["match"]["general_class_card"]
                    if self.json["match"]["general_class_card"] != ""
                    else self.json["match"]["general_class_name"],
                }
            else:
                return {
                    "id": int(self.json["match"].get("general_class_id", -1)),
                    "name": self.json["match"]["international_class_card"],
                }

        except Exception:
            warnings.warn("Property not found in page", RuntimeWarning)
            return None

    @cached_property
    def series(self) -> Optional[dict]:
        try:
            series = {
                "id": int(self.json["series"][0]["core_recreation_id"]),
                "name": self.json["series"][0]["series_name"],
            }
            return series
        except Exception:
            warnings.warn("Property not found in page", RuntimeWarning)
            return None

    @cached_property
    def season(self) -> Optional[dict]:
        try:
            return {
                "id": int(self.json["match"]["season"].split("/")[0]),
                "name": self.json["match"]["season"],
            }
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
    def ground(self) -> Optional[dict]:
        try:
            return {
                "id": int(self.json["match"]["ground_id"]),
                "name": self.json["match"]["ground_name"],
            }
        except Exception:
            warnings.warn("Property not found in page", RuntimeWarning)
            return None

    @cached_property
    def teams(self) -> List[dict]:
        try:
            teams = []
            for index, team in enumerate(self.json["team"]):
                players = []
                for p in self.json["team"][index]["player"]:
                    players.append(
                        {
                            "id": p["object_id"],
                            "name": p["known_as"],
                        }
                    )
                teams.append(
                    {
                        "id": int(self.json["team"][index]["team_id"]),
                        "name": self.json["team"][index]["team_name"],
                        "players": players,
                    }
                )

            return teams

        except Exception:
            warnings.warn("Property not found in page", RuntimeWarning)
            return [{}, {}]

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
    def team_1_innings(self) -> list:
        try:
            innings = []
            for i in self.json["innings"]:
                if i["batting_team_id"] == self.teams[0]["id"]:
                    innings.append(i)
            return i
        except Exception:
            warnings.warn("Property not found in page", RuntimeWarning)
            return []

    @cached_property
    def team_2_innings(self):
        try:
            innings = []
            for i in self.json["innings"]:
                if i["batting_team_id"] == self.teams[1]["id"]:
                    innings.append(i)
            return i
        except Exception:
            warnings.warn("Property not found in page", RuntimeWarning)
            return None
