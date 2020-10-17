from functools import cached_property

from gazpacho import Soup, get


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

        self.json_url = None

        self.html_file = html_file
        self.json_file = json_file

    @cached_property
    def html(self):
        if self.html_file:
            with open(self.html_file, "r") as f:
                return f.read
        else:
            r = get(self.url)
            return r

    @cached_property
    def soup(self) -> Soup:
        return Soup(self.html)