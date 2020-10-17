import json
from functools import cached_property
from typing import Optional

import requests
from bs4 import BeautifulSoup

from pycricinfo.exceptions import PyCricinfoException


class Match(object):
    """
    Object that abstracts the information avialable about a match
    """

    def __init__(
        self,
        match_id: int,
        html_file: Optional[str] = None,
        json_file: Optional[str] = None,
        timeout: int = 5,
        **kwargs,
    ) -> None:

        self.match_id = match_id

        self.url = f"https://www.espncricinfo.com/matches/engine/match/{match_id}.html"
        self.json_url = (
            f"https://www.espncricinfo.com/matches/engine/match/{match_id}.json"
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
    def comms_json(self) -> Optional[dict]:
        try:
            text = self.html.find_all("script")[15].string
            return json.loads(text)
        except PyCricinfoException:
            return None

    @cached_property
    def season(self):
        return self.json.get("Match", {}).get("season")

    @cached_property
    def description(self) -> Optional[str]:
        return self.json.get("description")

    @cached_property
    def series(self):
        return self.json.get("series")

    @cached_property
    def series_id(self):
        return self.json["series"][-1]["core_recreation_id"]

    @cached_property
    def date(self):
        return self.json["match"]["start_date_raw"]

    @cached_property
    def match_title(self):
        return self.json["match"]["cms_match_title"]

    @cached_property
    def result(self):
        return self.json["live"]["status"]

    @cached_property
    def ground_id(self):
        return self.json["match"]["ground_id"]

    @cached_property
    def ground_name(self):
        return self.json["match"]["ground_name"]

    @cached_property
    def innings_list(self):
        try:
            return self.json["centre"]["common"]["innings_list"]
        except:
            return None

    @cached_property
    def innings(self):
        return self.json["innings"]

    @cached_property
    def team_1(self):
        return self.json["team"][0]

    @cached_property
    def team_1_id(self):
        return self.get_team_1()["team_id"]

    @cached_property
    def team_1_abbreviation(self):
        return self.get_team_1()["team_abbreviation"]

    @cached_property
    def team_1_players(self):
        return self.get_team_1().get("player", [])

    @cached_property
    def team_1_innings(self):
        try:
            return [
                inn
                for inn in self.json["innings"]
                if inn["batting_team_id"] == self.get_team_1_id()
            ][0]
        except:
            return None

    @cached_property
    def team_2(self):
        return self.json["team"][1]

    @cached_property
    def team_2_id(self):
        return self.get_team_2()["team_id"]

    @cached_property
    def team_2_abbreviation(self):
        return self.get_team_2()["team_abbreviation"]

    @cached_property
    def team_2_players(self):
        return self.get_team_2().get("player", [])

    @cached_property
    def team_2_innings(self):
        try:
            return [
                inn
                for inn in self.json["innings"]
                if inn["batting_team_id"] == self.get_team_2_id()
            ][0]
        except:
            return None

    # comms_json methods

    @cached_property
    def rosters(self):
        try:
            return self.comms_json["props"]["pageProps"]["data"]["content"]["teams"]
        except:
            return None

    @cached_property
    def all_innings(self):
        try:
            return self.comms_json["props"]["pageProps"]["data"]["content"]["innings"]
        except:
            return None

    @cached_property
    def close_of_play(self):
        try:
            return self.comms_json["props"]["pageProps"]["data"]["content"]["closePlay"]
        except:
            return None
