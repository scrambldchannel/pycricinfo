import json
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
        **kwargs,
    ) -> None:

        self.match_id = match_id

        self.match_url = (
            f"https://www.espncricinfo.com/matches/engine/match/{match_id}.html"
        )
        self.json_url = (
            f"https://www.espncricinfo.com/matches/engine/match/{match_id}.json"
        )

        if html_file:
            self.html = self.get_html_from_file(f"{html_file}")
        else:
            self.hmtl = self.get_html()

        if json_file:
            self.json = self.get_json_from_file(f"{json_file}")
        else:
            self.json = self.get_json()

        # this isn't the best name, maybe change to something that implies it's coming from the html (I think)
        self.comms_json = self.get_comms_json()

        if self.json:
            # leaving this here for now as they seem to all work for the matches I'm interested in
            # review this pattern in future though and create something more lightweight

            self.season = self._season()
            self.description = self._description()
            self.series = self._series()
            self.series_id = self._series_id()
            self.date = self._date()
            self.match_title = self._match_title()
            self.scheduled_overs = self._scheduled_overs()
            self.innings_list = self._innings_list()
            self.innings = self._innings()
            self.team_1 = self._team_1()
            self.team_1_id = self._team_1_id()
            self.team_1_abbreviation = self._team_1_abbreviation()
            self.team_1_players = self._team_1_players()
            self.team_1_innings = self._team_1_innings()
            self.team_2 = self._team_2()
            self.team_2_id = self._team_2_id()
            self.team_2_abbreviation = self._team_2_abbreviation()
            self.team_2_players = self._team_2_players()
            self.team_2_innings = self._team_2_innings()

            self.espn_api_url = self._espn_api_url()
            # from comms_json
            self.rosters = self._rosters()
            self.all_innings = self._all_innings()
            self.close_of_play = self._close_of_play()

    def get_json(self) -> dict:
        r = requests.get(self.json_url)
        if r.status_code == 404:
            raise PyCricinfoException
        elif "Scorecard not yet available" in r.text:
            raise PyCricinfoException
        else:
            return r.json()

    def get_json_from_file(self, file):

        with open(file, "r") as f:
            j = json.loads(f.read())
            return j

    def get_html(self) -> BeautifulSoup:
        r = requests.get(self.match_url)
        if r.status_code == 404:
            raise PyCricinfoException
        else:
            return BeautifulSoup(r.text, "html.parser")

    def get_html_from_file(self, file: str) -> BeautifulSoup:
        with open(file, "r") as f:
            return BeautifulSoup(f.read(), "html.parser")

    def get_comms_json(self) -> Optional[dict]:
        try:
            text = self.html.find_all("script")[15].string
            return json.loads(text)
        except:
            return None

    def _espn_api_url(self) -> str:
        # what is this? Move to constructor if useful
        return f"https://site.api.espn.com/apis/site/v2/sports/cricket/{self.series_id}/summary?event={self.match_id}"

    # as above
    def _details_url(self, page=1, number=1000):
        return (
            self.event_url
            + f"/competitions/{self.match_id}/details?page_size={number}&page={page}"
        )

    def _season(self):
        return self.json["match"]["season"]

    def _description(self):
        return self.json["description"]

    def _series(self):
        return self.json["series"]

    def _series_id(self):
        return self.json["series"][-1]["core_recreation_id"]

    def _date(self):
        return self.json["match"]["start_date_raw"]

    def _match_title(self):
        return self.json["match"]["cms_match_title"]

    def _result(self):
        return self.json["live"]["status"]

    def _ground_id(self):
        return self.json["match"]["ground_id"]

    def _ground_name(self):
        return self.json["match"]["ground_name"]

    def _scheduled_overs(self):
        try:
            return int(self.json["match"]["scheduled_overs"])
        except:
            return None

    def _innings_list(self):
        try:
            return self.json["centre"]["common"]["innings_list"]
        except:
            return None

    def _innings(self):
        return self.json["innings"]

    def _team_1(self):
        return self.json["team"][0]

    def _team_1_id(self):
        return self._team_1()["team_id"]

    def _team_1_abbreviation(self):
        return self._team_1()["team_abbreviation"]

    def _team_1_players(self):
        return self._team_1().get("player", [])

    def _team_1_innings(self):
        try:
            return [
                inn
                for inn in self.json["innings"]
                if inn["batting_team_id"] == self._team_1_id()
            ][0]
        except:
            return None

    def _team_2(self):
        return self.json["team"][1]

    def _team_2_id(self):
        return self._team_2()["team_id"]

    def _team_2_abbreviation(self):
        return self._team_2()["team_abbreviation"]

    def _team_2_players(self):
        return self._team_2().get("player", [])

    def _team_2_innings(self):
        try:
            return [
                inn
                for inn in self.json["innings"]
                if inn["batting_team_id"] == self._team_2_id()
            ][0]
        except:
            return None

    # comms_json methods

    def _rosters(self):
        try:
            return self.comms_json["props"]["pageProps"]["data"]["content"]["teams"]
        except:
            return None

    def _all_innings(self):
        try:
            return self.comms_json["props"]["pageProps"]["data"]["content"]["innings"]
        except:
            return None

    def _close_of_play(self):
        try:
            return self.comms_json["props"]["pageProps"]["data"]["content"]["closePlay"]
        except:
            return None
