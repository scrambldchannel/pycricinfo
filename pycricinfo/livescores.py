import json

import requests
from bs4 import BeautifulSoup

from pycricinfo.exceptions import PyCricinfoException


class Summary(object):
    def __init__(self) -> None:
        self.url = "https://www.espncricinfo.com/scores"
        self.html = self.get_html()
        self.match_ids = self._match_ids()

    def get_html(self):
        r = requests.get(self.url)
        if r.status_code == 404:
            raise PyCricinfoException
        else:
            return BeautifulSoup(r.text, "html.parser")

    def summary_json(self):
        try:
            text = self.html.find_all("script")[15].contents[0]
            return json.loads(text)
        except:
            return None

    # replace this with
    def _match_ids(self):
        matches = [
            x["id"]
            for x in self.summary_json()["props"]["pageProps"]["data"]["content"][
                "leagueEvents"
            ][0]["matchEvents"]
        ]
        return matches
