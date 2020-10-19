from functools import cached_property

from gazpacho import Soup, get


class BaseCricinfoPage:
    """
    Base class for all pycricinfo objects
    """

    def __init__(self, id):
        self.id = id

        self.url = None
        self.json_url = None
        self.html = None
        self.json = None
        self.html_file = None
        self.json_file = None
        self.soup = None

    @cached_property
    def html(self) -> str:

        if self.html_file:
            with open(self.html_file, "r") as f:
                return f.read()
        else:
            return get(self.url)

    @cached_property
    def soup(self) -> Soup:
        return Soup(self.html)

    def to_file(self, html_file: str = None) -> None:

        if not html_file:
            html_file = f"{self.id}.html"

        with open(html_file, "w") as f:
            f.write(self.soup.html)

    def to_json_file(self, json_file: str = None) -> None:

        if self.json:
            if not json_file:
                json_file = f"{self.id}.json"

            with open(json_file, "w") as f:
                f.write(self.json)
