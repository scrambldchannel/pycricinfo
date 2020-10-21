from functools import cached_property

from gazpacho import Soup, get
from gazpacho.utils import HTTPError

from pycricinfo.exceptions import PageNotFoundException


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
            try:
                return get(self.url)
            except HTTPError as e:
                if e.code == 404:
                    raise PageNotFoundException(
                        e.code,
                        f"Object {self.id} not found. Check that the id is correct.",
                    )
                return ""

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

    @staticmethod
    def safe_int(int_string: str = "0") -> int:
        # bit of a hack to deal with None, '-', '', ' '
        int_things = [None, "", "-", "0"]

        if int_string in int_things:
            return 0
        else:
            return int(int_string)

    @staticmethod
    def safe_float(float_string: str = "0.0") -> float:
        # bit of a hack to deal with None, '-', '', ' '
        float_things = [None, "", "-", "0"]

        if float_string in float_things:
            return 0.0
        else:
            return float(float_string)
