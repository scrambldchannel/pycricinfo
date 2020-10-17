import requests
from bs4 import BeautifulSoup

from pycricinfo.exceptions import PyCricinfoException


class Team(object):
    """
    Abstraction of a team
    """

    def __init__(
        self, team_id: int, html_file: str = None, json_file: str = None
    ) -> None:

        self.team_id = team_id
        # this almost certainly isn't right but seems to get re-directed to the right place
        self.url = f"https://www.espncricinfo.com/team/_/id/{self.team_id}/"

        # not working / need to review url
        self.json_url = (
            f"https://core.espnuk.org/v2/sports/cricket/teams/{self.team_id}"
        )

        if html_file:
            self.html = self.get_html_from_file(f"{html_file}")
        else:
            self.html = self.get_html()

    def get_html(self) -> BeautifulSoup:
        r = requests.get(self.url)
        if r.status_code == 404:
            raise PyCricinfoException
        else:
            return BeautifulSoup(r.text, "html.parser")

    def get_html_from_file(self, file: str) -> BeautifulSoup:
        with open(file, "r") as f:
            return BeautifulSoup(f.read(), "html.parser")

    # not working with any url I can locate
    def get_json(self) -> dict:
        r = requests.get(self.json_url)
        # how to handle rejection here?
        if r.status_code == 404:
            raise PyCricinfoException
        return r.json()
