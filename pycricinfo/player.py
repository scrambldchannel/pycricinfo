import warnings
from functools import cached_property
from typing import Optional

from gazpacho import Soup, get


class Player(object):
    """
    Abstraction of a player
    """

    def __init__(
        self,
        player_id: int,
        html_file: str = None,
        json_file: str = None,
    ) -> None:

        self.player_id = player_id
        self.url = f"https://www.espncricinfo.com/ci/content/player/{player_id}.html"

        self.html_file = html_file
        self.json_file = json_file

    @classmethod
    def from_file(cls, html_file: str):
        with open(html_file, "r") as f:
            # get player_id
            soup = Soup(f.read())
            player_id = int(
                soup.find("link", attrs={"rel": "canonical"})
                .attrs["href"]
                .split("/")[6]
                .split(".")[0]
            )

        return cls(player_id=player_id, html_file=html_file)

    def to_file(self, html_file: str = None) -> None:

        if not html_file:
            html_file = f"{self.player_id}.html"

        with open(html_file, "w") as f:
            f.write(self.soup.html)

    @cached_property
    def html(self) -> str:

        if self.html_file:
            with open(self.html_file, "r") as f:
                return f.read()
        else:
            r = get(self.url)
            return r

    @cached_property
    def soup(self) -> Soup:
        return Soup(self.html)

    @cached_property
    def player_info_soup(self) -> Soup:
        return self.soup.find("p", attrs={"class": "ciPlayerinformationtxt"})

    @cached_property
    def name(self) -> Soup:
        info = self.soup.find("div", attrs={"class": "ciPlayernametxt"}, mode="first")
        return info.find("h1", mode="first").text

    @cached_property
    def full_name(self) -> Optional[str]:
        for i in self.player_info_soup:
            if i.find("b").text == "Full name":
                return i.find("span", mode="first").text

        return None

    @cached_property
    def batting_style(self) -> Optional[str]:
        for i in self.player_info_soup:
            if i.find("b").text == "Batting style":
                return i.find("span", mode="first").text

        return None

    @cached_property
    def bowling_style(self) -> Optional[str]:
        for i in self.player_info_soup:
            if i.find("b").text == "Bowling style":
                return i.find("span", mode="first").text

        return None

    @cached_property
    def player_stats(self) -> dict:
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

                        grade_stats[header_columns[index + 1]] = stat_columns[
                            index + 1
                        ].text

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

                        grade_stats[header_columns[index + 1]] = stat_columns[
                            index + 1
                        ].text

                    bowling[grade] = grade_stats

                stats["bowling"] = bowling
        except Exception:
            warnings.warn("Player stats could not be parsed", RuntimeWarning)

        return stats
