import json
import warnings
from functools import cached_property
from typing import List

from gazpacho import Soup, get


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
        """
        The html from this page
        """
        r = get(self.url)
        return r

    @cached_property
    def soup(self) -> Soup:
        """
        The object for the livescores page
        """
        return Soup(self.html)

    @cached_property
    def embedded_json(self) -> dict:
        """
        Try to locate the embedded json inside the html
        """
        try:
            json_text = self.soup.find(
                "script", attrs={"id": "__NEXT_DATA__"}, mode="first"
            ).text
            return json.loads(json_text)
        except Exception:
            warnings.warn(
                "Unable to obtain embedded JSON in live scores page", RuntimeWarning
            )
            return {}

    @cached_property
    def live_matches(self) -> List[int]:
        """
        Return a list of all live matches
        """
        match_ids = []
        for match in self.embedded_json["props"]["pageProps"]["data"]["content"][
            "leagueEvents"
        ][0]["matchEvents"]:

            match_ids.append(int(match["id"]))

        return match_ids
