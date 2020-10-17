import json
from functools import cached_property
from typing import Optional

from gazpacho import Soup, get

from pycricinfo.exceptions import PyCricinfoException


class LiveScores(object):
    """
    Object used to scrape basic information about live games
    """

    def __init__(
        self,
        **kwargs,
    ) -> None:

        self.url = "https://www.espncricinfo.com/scores"

    @cached_property
    def html(self):
        r = get(self.url)
        return r

    @cached_property
    def soup(self):
        return Soup(self.html)

    @cached_property
    def embedded_json(self) -> Optional[dict]:
        try:
            json_text = self.soup.find("script", attrs={"id": "__NEXT_DATA__"}).text
            return json.loads(json_text)
        except:
            raise PyCricinfoException(
                "LiveScores.embedded_json", "Embedded JSON not found"
            )

    @cached_property
    def get_live_matches(self):
        matches = [
            x["id"]
            for x in self.embedded_json()["props"]["pageProps"]["data"]["content"][
                "leagueEvents"
            ][0]["matchEvents"]
        ]
        return matches
