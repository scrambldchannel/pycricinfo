from gazpacho import Soup

from pycricinfo.base import BaseCricinfoPage


class Ground(BaseCricinfoPage):
    """
    Abstraction of a team
    """

    def __init__(
        self,
        id: int,
        html_file: str = None,
    ) -> None:

        self.id = id

        self.url = f"https://www.espncricinfo.com/ci/content/ground/{self.id}.html"

        self.html_file = html_file

    @classmethod
    def from_file(cls, html_file: str):
        with open(html_file, "r") as f:
            # get id
            soup = Soup(f.read())
            id = int(
                soup.find("link", attrs={"rel": "canonical"})
                .attrs["href"]
                .split("/")[6]
                .split(".")[0]
            )

        return cls(id=id, html_file=html_file)
