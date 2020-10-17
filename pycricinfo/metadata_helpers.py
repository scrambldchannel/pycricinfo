import BeautifulSoup
import requests


def get_recent_matches(date=None):
    if date:
        url = (
            "https://www.espncricinfo.com/ci/engine/match/index.html?date=%sview=week"
            % date
        )
    else:
        url = "https://www.espncricinfo.com/ci/engine/match/index.html?view=week"

    r = requests.get(url)
    # is there a source for this that doesn't use BS?
    soup = BeautifulSoup(r.text, "html.parser")
    return [
        x["href"].split("/", 4)[4].split(".")[0]
        for x in soup.findAll("a", href=True, text="Scorecard")
    ]


# https://www.espncricinfo.com/ci/content/match/fixtures_futures.html
