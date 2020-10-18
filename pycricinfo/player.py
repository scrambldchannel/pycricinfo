from functools import cached_property

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
    def full_name(self) -> Soup:
        player_info = self.soup.find(
            "p", attrs={"class": "ciPlayerinformationtxt"}, mode="first"
        )

        return player_info.find("span", mode="first").text

    @cached_property
    def name(self) -> Soup:
        info = self.soup.find("div", attrs={"class": "ciPlayernametxt"}, mode="first")

        return info.find("h1", mode="first").text
