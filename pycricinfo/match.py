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

        self.html_file = html_file
        self.json_file = json_file

        if self.html_file:
            self.html = self.get_html_from_file(f"{html_file}")
        else:
            self.html = self.get_html()

        if self.json_file:
            self.json = self.get_json_from_file(f"{json_file}")
        else:
            self.json = self.get_json()

        if self.html:
            self.comms_json = self.get_comms_json()
            # from comms_json which is a part of the
            self.rosters = self.get_rosters()
            self.all_innings = self.get_all_innings()
            self.close_of_play = self.get_close_of_play()

        if self.json:
            # leaving this here for now as they seem to all work for the matches I'm interested in
            # review this pattern in future though and create something more lightweight

            self.description = self.get_description()
            self.match_title = self.get_match_title()
            self.date = self.get_date()

            self.ground_id = self.get_ground_id()
            #            self.get_ground_name = self.get_ground_name()

            self.season = self.get_season()
            self.series = self.get_series()
            self.series_id = self.get_series_id()

            #            self.team_1 = self.get_team_1()
            self.team_1_id = self.get_team_1_id()
            self.team_1_abbreviation = self.get_team_1_abbreviation()
            self.team_1_players = self.get_team_1_players()
            self.team_1_innings = self.get_team_1_innings()
            self.team_2 = self.get_team_2()
            self.team_2_id = self.get_team_2_id()
            self.team_2_abbreviation = self.get_team_2_abbreviation()
            self.team_2_players = self.get_team_2_players()
            self.team_2_innings = self.get_team_2_innings()

            # what are these three urls?
            self.espn_api_url = f"https://site.api.espn.com/apis/site/v2/sports/cricket/{self.series_id}/summary?event={self.match_id}"
            self.event_url = "https://core.espnuk.org/v2/sports/cricket/leagues/{0}/events/{1}".format(
                str(self.series_id), str(match_id)
            )
            page, number = 1, 1000
            self.details_url = (
                self.event_url
                + f"/competitions/{self.match_id}/details?page_size={number}&page={page}"
            )

    def get_json(self) -> dict:
        r = requests.get(self.json_url)
        if r.status_code == 404:
            raise PyCricinfoException("Match.get_json", message="404")
        elif "Scorecard not yet available" in r.text:
            raise PyCricinfoException("Match.get_json", message="Not yet available")
        else:
            return r.json()

    def get_json_from_file(self, file):

        with open(file, "r") as f:
            return json.loads(f.read())

    def get_html(self) -> BeautifulSoup:
        r = requests.get(self.match_url)
        if r.status_code == 404:
            raise PyCricinfoException("Match.get_html", "404")
        else:
            return BeautifulSoup(r.text, "html.parser")

    def get_html_from_file(self, file: str) -> BeautifulSoup:
        with open(file, "r") as f:
            return BeautifulSoup(f.read(), "html.parser")

    def get_comms_json(self) -> Optional[dict]:
        try:
            text = self.html.find_all("script")[15].string
            return json.loads(text)
        except PyCricinfoException:
            return None

    def get_season(self):
        return self.json.get("Match", {}).get("season")

    def get_description(self):
        return self.json.get("description")

    def get_series(self):
        return self.json.get("series")

    def get_series_id(self):
        return self.json["series"][-1]["core_recreation_id"]

    def get_date(self):
        return self.json["match"]["start_date_raw"]

    def get_match_title(self):
        return self.json["match"]["cms_match_title"]

    def get_result(self):
        return self.json["live"]["status"]

    def get_ground_id(self):
        return self.json["match"]["ground_id"]

    def get_ground_name(self):
        return self.json["match"]["ground_name"]

    def get_innings_list(self):
        try:
            return self.json["centre"]["common"]["innings_list"]
        except:
            return None

    def get_innings(self):
        return self.json["innings"]

    def get_team_1(self):
        return self.json["team"][0]

    def get_team_1_id(self):
        return self.get_team_1()["team_id"]

    def get_team_1_abbreviation(self):
        return self.get_team_1()["team_abbreviation"]

    def get_team_1_players(self):
        return self.get_team_1().get("player", [])

    def get_team_1_innings(self):
        try:
            return [
                inn
                for inn in self.json["innings"]
                if inn["batting_team_id"] == self.get_team_1_id()
            ][0]
        except:
            return None

    def get_team_2(self):
        return self.json["team"][1]

    def get_team_2_id(self):
        return self.get_team_2()["team_id"]

    def get_team_2_abbreviation(self):
        return self.get_team_2()["team_abbreviation"]

    def get_team_2_players(self):
        return self.get_team_2().get("player", [])

    def get_team_2_innings(self):
        try:
            return [
                inn
                for inn in self.json["innings"]
                if inn["batting_team_id"] == self.get_team_2_id()
            ][0]
        except:
            return None

    # comms_json methods

    def get_rosters(self):
        try:
            return self.comms_json["props"]["pageProps"]["data"]["content"]["teams"]
        except:
            return None

    def get_all_innings(self):
        try:
            return self.comms_json["props"]["pageProps"]["data"]["content"]["innings"]
        except:
            return None

    def get_close_of_play(self):
        try:
            return self.comms_json["props"]["pageProps"]["data"]["content"]["closePlay"]
        except:
            return None
