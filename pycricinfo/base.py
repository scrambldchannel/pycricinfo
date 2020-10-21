from functools import cached_property

from gazpacho import Soup, get
from gazpacho.utils import HTTPError

from pycricinfo.exceptions import PageNotFoundException


class BaseCricinfoPage:
    """
    Base class for all pycricinfo objects
    """

    def __init__(self, id):
        """
        Class constructor
        """
        self.id: int = id

        self.url = None
        self.json_url = None
        self.html = None
        self.json = None
        self.html_file = None
        self.json_file = None
        self.soup = None

    @cached_property
    def html(self) -> str:
        """
        Caches the html from the page associate with the object
        """
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
        """
        Caches the Soup object derived from the html
        """
        return Soup(self.html)

    def to_file(self, html_file: str = None) -> None:
        """
        Write the page html from the object to a file. Default, is "./{id}.html"
        """
        if not html_file:
            html_file = f"{self.id}.html"

        with open(html_file, "w") as f:
            f.write(self.soup.html)

    def to_json_file(self, json_file: str = None) -> None:
        """
        Write the page json from the object to a file. Default, is "./{id}.json"
        """

        if self.json:
            if not json_file:
                json_file = f"{self.id}.json"

            with open(json_file, "w") as f:
                f.write(self.json)

    @staticmethod
    def safe_int(int_string: str = "0") -> int:
        """
        Cast various string representations of zero to int safely
        """
        int_things = [None, "", "-", "0"]

        if int_string in int_things:
            return 0
        else:
            return int(int_string)

    @staticmethod
    def safe_float(float_string: str = "0.0") -> float:
        """
        Cast various string representations of zero to float safely
        """
        float_things = [None, "", "-", "0"]

        if float_string in float_things:
            return 0.0
        else:
            return float(float_string)
