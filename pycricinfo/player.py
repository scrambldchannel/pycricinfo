import warnings
from functools import cached_property
from typing import Optional

from gazpacho import Soup

from pycricinfo.base import BaseCricinfoPage


class Player(BaseCricinfoPage):
    """
    Abstraction of a player
    """

    def __init__(
        self,
        id: int,
        html_file: str = None,
    ) -> None:

        self.id = id
        self.url = f"https://www.espncricinfo.com/ci/content/player/{id}.html"

        self.html_file = html_file

    @classmethod
    def from_file(cls, html_file: str):
        """
        Load the player html from a previously saved file
        """
        with open(html_file, "r") as f:
            # get player id
            soup = Soup(f.read())
            id = int(
                soup.find("link", attrs={"rel": "canonical"})
                .attrs["href"]
                .split("/")[6]
                .split(".")[0]
            )
        return cls(id=id, html_file=html_file)

    @cached_property
    def player_info_soup(self) -> Soup:
        """
        The player html as a Soup object
        """
        return self.soup.find("p", attrs={"class": "ciPlayerinformationtxt"})

    @cached_property
    def name(self) -> str:
        """
        The player's name
        """
        info = self.soup.find("div", attrs={"class": "ciPlayernametxt"}, mode="first")
        return info.find("h1", mode="first").text

    @cached_property
    def full_name(self) -> Optional[str]:
        """
        The player's long name
        """
        for i in self.player_info_soup:
            if i.find("b").text == "Full name":
                return i.find("span", mode="first").text
        return None

    @cached_property
    def batting_style(self) -> Optional[str]:
        """
        The player's batting style eg Right-hand bat
        """

        for i in self.player_info_soup:
            if i.find("b").text == "Batting style":
                return i.find("span", mode="first").text
        return None

    @cached_property
    def bowling_style(self) -> Optional[str]:
        """
        The player's bowling style(s) eg 'Right-arm offbreak'. Note, may return several, comma separated
        """

        for i in self.player_info_soup:
            if i.find("b").text == "Bowling style":
                return i.find("span", mode="first").text
        return None

    @cached_property
    def player_stats(self) -> dict:
        """
        The player's stats as a dict
        """

        stats = {}

        try:
            etables = self.soup.find(
                "table", attrs={"class": "engineTable"}, mode="all"
            )

            if len(etables) >= 2:

                # this will hopefully be batting
                batting_table = etables[0]
                batting = {}
                header_columns = []
                for th in (
                    batting_table.find("thead", mode="first")
                    .find("tr", mode="first")
                    .find("th", mode="all")
                ):
                    header_columns.append(th.attrs["title"])

                for tr in batting_table.find("tbody", mode="first").find(
                    "tr", mode="all"
                ):

                    grade_stats = {}

                    stat_columns = tr.find("td", mode="all")

                    grade = stat_columns[0].text

                    for index, col in enumerate(stat_columns[1:]):

                        stat = header_columns[index + 1]

                        val = stat_columns[index + 1].text
                        # hack to do type conversion

                        stat, val = self._format_stat(stat, val)
                        # hack to do type conversion

                        grade_stats[stat] = val

                    batting[grade] = grade_stats

                stats["batting"] = batting

                bowling_table = etables[1]

                bowling = {}

                header_columns = []
                for th in (
                    bowling_table.find("thead", mode="first")
                    .find("tr", mode="first")
                    .find("th", mode="all")
                ):
                    header_columns.append(th.attrs["title"])

                for tr in bowling_table.find("tbody", mode="first").find(
                    "tr", mode="all"
                ):

                    grade_stats = {}

                    stat_columns = tr.find("td", mode="all")

                    grade = stat_columns[0].text

                    for index, col in enumerate(stat_columns[1:]):
                        stat = header_columns[index + 1]

                        val = stat_columns[index + 1].text
                        # hack to do type conversion

                        stat, val = self._format_stat(stat, val)
                        grade_stats[stat] = val

                    bowling[grade] = grade_stats

                stats["bowling"] = bowling
        except Exception as e:
            raise e
            warnings.warn("Player stats could not be parsed", RuntimeWarning)

        return stats

    def _format_stat(self, stat: str, val: str):
        """
        Helper method to map stats to names and types. Needs improvement
        """
        to_int_stats = {
            "wickets taken": "wickets",
            "five wkts in an inns": "five wickets",
            "balls bowled": "balls",
            "ten wkts in a match": "ten wickets",
            "runs conceded": "runs",
            "four wkts in an inns": "four wickets",
            "matches played": "matches",
            "innings batted": "innings",
            "not outs": "not outs",
            "runs scored": "runs",
            "balls faced": "balls",
            "hundreds scored": "100s",
            "fifties scored": "50s",
            "boundary fours": "fours",
            "boundary sixes": "sixes",
            "catches taken": "catches",
            "stumpings made": "stumpings",
            "innings bowled in": "innings bowled",
        }
        to_float_stats = {
            "batting average": "average",
            "batting strike rate": "sr",
            "bowling average": "average",
            "bowling strike rate": "sr",
            "economy rate": "er",
        }
        to_str_stats = {
            "highest inns score": "hs",
            "best innings bowling": "best bowling innings",
            "best match bowling": "best bowling match",
        }

        if stat in to_int_stats.keys():
            stat = to_int_stats[stat]
            return stat, BaseCricinfoPage.safe_float(val)

        elif stat in to_float_stats.keys():
            stat = to_float_stats[stat]
            return stat, BaseCricinfoPage.safe_float(val)
        else:
            stat = to_str_stats.get(stat, stat)
            return stat, val
