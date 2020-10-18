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

    def to_file(self, html_file: str = None) -> None:

        if not html_file:
            html_file = f"{self.player_id}.html"

        with open(html_file, "w") as f:
            f.write(self.html)

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
    def player_stats(self) -> Optional[dict]:
        stats = {}

        etables = self.soup.find("table", attrs={"class": "engineTable"}, mode="all")

        if len(etables) >= 2:
            batting = {}
            # this will hopefully be batting
            for tr in etables[0].find("tr", attrs={"class": "data1"}, mode="all"):

                for td in tr.find("td", attrs={"title": "record rank:"}, mode="all"):
                    grade = td.find("b", mode="first").text

                    grade_stats = {}
                    stat_list = tr.find("td", attrs={"nowrap": "nowrap"}, mode="all")
                    # assuming this order is fixed
                    grade_stats["matches"] = stat_list[1].text
                    grade_stats["innings"] = stat_list[2].text
                    grade_stats["not out"] = stat_list[3].text
                    grade_stats["runs"] = stat_list[4].text
                    grade_stats["hs"] = stat_list[5].text
                    grade_stats["average"] = stat_list[6].text
                    grade_stats["sr"] = stat_list[7].text
                    grade_stats["balls"] = stat_list[8].text
                    grade_stats["100s"] = stat_list[9].text
                    grade_stats["50s"] = stat_list[10].text
                    grade_stats["6s"] = stat_list[11].text
                    grade_stats["catches"] = stat_list[12].text
                    grade_stats["stumpings"] = stat_list[13].text

                    batting[grade] = grade_stats

            stats["batting"] = batting

            bowling = {}
            # this will hopefully be bowling
            for tr in etables[1].find("tr", attrs={"class": "data1"}, mode="all"):

                for td in tr.find("td", attrs={"title": "record rank:"}, mode="all"):
                    grade = td.find("b", mode="first").text
                    grade_stats = {}
                    stat_list = tr.find("td", attrs={"nowrap": "nowrap"}, mode="all")
                    # assuming this order is fixed
                    grade_stats["matches"] = stat_list[1].text
                    grade_stats["innings"] = stat_list[2].text
                    grade_stats["balls"] = stat_list[3].text
                    grade_stats["runs"] = stat_list[4].text
                    grade_stats["wickets"] = stat_list[5].text
                    grade_stats["best innings"] = stat_list[6].text
                    grade_stats["best match"] = stat_list[7].text
                    grade_stats["average"] = stat_list[8].text
                    grade_stats["er"] = stat_list[9].text
                    grade_stats["6s"] = stat_list[10].text
                    grade_stats["4s"] = stat_list[11].text
                    grade_stats["5s"] = stat_list[12].text
                    grade_stats["10s"] = stat_list[13].text

                    bowling[grade] = grade_stats
            stats["bowling"] = bowling

        return stats
