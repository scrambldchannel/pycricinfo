import json
from functools import cached_property

import requests
from bs4 import BeautifulSoup

from pycricinfo.exceptions import PyCricinfoException


class Ground(object):
    """
    Abstraction of a team
    """

    def __init__(
        self,
        ground_id: int,
        html_file: str = None,
        json_file: str = None,
        timeout: int = 5,
    ) -> None:

        self.ground_id = ground_id

        self.url = (
            f"https://www.espncricinfo.com/ci/content/ground/{self.ground_id}.html"
        )

        # this doesn't work
        self.json_url = (
            f"https://core.espnuk.org/v2/sports/cricket/ground/{self.ground_id}"
        )

        self.html_file = html_file
        self.json_file = json_file

        self.timeout = timeout

    @cached_property
    def html(self):
        if self.html_file:
            with open(self.html_file, "r") as f:
                return f.read
        else:
            r = requests.get(self.url, timeout=self.timeout)
            if r.status_code == 404:
                raise PyCricinfoException("Ground.html", "404")
            else:
                return r.text

    @cached_property
    def json(self):

        if self.json_file:
            with open(self.json_file, "r") as f:
                return json.loads(f.read())
        else:
            r = requests.get(self.json_url, timeout=self.timeout)
            # need to do something to catch the timeout exception here
            if r.status_code == 404:
                raise PyCricinfoException("Team.json", "404")
            else:
                return r.json()

    @cached_property
    def soup(self) -> BeautifulSoup:
        return BeautifulSoup(self.html, "html.parser")
