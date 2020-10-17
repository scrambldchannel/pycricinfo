import json
from functools import cached_property
from typing import List

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

    # caching the results for now, this might need to be reviewed for this object

    @cached_property
    def html(self) -> str:
        r = get(self.url)
        return r

    @cached_property
    def soup(self) -> Soup:
        return Soup(self.html)

    @cached_property
    def embedded_json(self) -> dict:
        try:
            json_text = self.soup.find(
                "script", attrs={"id": "__NEXT_DATA__"}, mode="first"
            ).text
            return json.loads(json_text)
        except:
            raise PyCricinfoException(
                "LiveScores.embedded_json", "Embedded JSON not found"
            )

    @cached_property
    def live_matches(self) -> List[int]:
        match_ids = []
        for match in self.embedded_json["props"]["pageProps"]["data"]["content"][
            "leagueEvents"
        ][0]["matchEvents"]:

            match_ids.append(int(match["id"]))

        return match_ids
