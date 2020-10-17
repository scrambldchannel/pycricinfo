import json
from functools import cached_property

import requests
from bs4 import BeautifulSoup

from pycricinfo.exceptions import PyCricinfoException
from pycricinfo.match import Match


class Player(object):
    """
    Abstraction of a player
    """

    def __init__(
        self,
        player_id: int,
        html_file: str = None,
        json_file: str = None,
        timeout: int = 5,
    ) -> None:

        self.player_id = player_id
        self.url = f"https://www.espncricinfo.com/ci/content/player/{player_id}.html"

        self.json_url = (
            # not working / need to review url
            f"https://core.espnuk.org/v2/sports/cricket/athletes/{player_id}"
        )

        self.html_file = html_file
        self.json_file = json_file

        self.timeout = timeout

    @cached_property
    def html(self) -> BeautifulSoup:

        if self.html_file:
            with open(self.html_file, "r") as f:
                return BeautifulSoup(f.read(), "html.parser")
        else:
            r = requests.get(self.url, timeout=self.timeout)
            if r.status_code == 404:
                raise PyCricinfoException
            else:
                return BeautifulSoup(r.text, "html.parser")

    @cached_property
    def json(self) -> dict:

        if self.json_file:
            with open(self.json_file, "r") as f:
                return json.loads(f.read())
        else:
            r = requests.get(self.json_url, timeout=self.timeout)
            # need to do something to catch the timeout exception here
            if r.status_code == 404:
                raise PyCricinfoException("Team.json", "404")
            else:
                return r.json()

    @cached_property
    def parsed_html(self) -> BeautifulSoup:
        return self.html.find("div", class_="pnl490M")

    @cached_property
    def player_information(self) -> BeautifulSoup:
        return self.parsed_html.find_all("p", class_="ciPlayerinformationtxt")

    @cached_property
    def batting_fielding_averages(self):
        if len(self.parsed_html.findAll("table", class_="engineTable")) == 4:
            headers = [
                "matches",
                "innings",
                "not_out",
                "runs",
                "high_score",
                "batting_average",
                "balls_faced",
                "strike_rate",
                "centuries",
                "fifties",
                "fours",
                "sixes",
                "catches",
                "stumpings",
            ]
            bat_field = [
                td.text.strip()
                for td in self.parsed_html.find("table", class_="engineTable").findAll(
                    "td"
                )
            ]
            num_formats = int(len(bat_field) / 15)
            format_positions = [15 * x for x in range(num_formats)]
            formats = [bat_field[x] for x in format_positions]
            avg_starts = [x + 1 for x in format_positions[:num_formats]]
            avg_finish = [x + 14 for x in avg_starts]
            format_averages = [bat_field[x:y] for x, y in zip(avg_starts, avg_finish)]
            combined = list(zip(formats, format_averages))
            l_not_ambiguous = [{x: dict(zip(headers, y))} for x, y in combined]
            return {k: v for d in l_not_ambiguous for k, v in d.items()}
        else:
            return None

    @cached_property
    def bowling_averages(self):
        if len(self.parsed_html.findAll("table", class_="engineTable")) == 4:
            headers = [
                "matches",
                "innings",
                "balls_delivered",
                "runs",
                "wickets",
                "best_innings",
                "best_match",
                "bowling_average",
                "economy",
                "strike_rate",
                "four_wickets",
                "five_wickets",
                "ten_wickets",
            ]
            bowling = [
                td.text.strip()
                for td in self.parsed_html.findAll("table", class_="engineTable")[
                    1
                ].findAll("td")
            ]
            num_formats = int(len(bowling) / 14)
            format_positions = [14 * x for x in range(num_formats)]
            formats = [bowling[x] for x in format_positions]
            avg_starts = [x + 1 for x in format_positions[:num_formats]]
            avg_finish = [x + 13 for x in avg_starts]
            format_averages = [bowling[x:y] for x, y in zip(avg_starts, avg_finish)]
            combined = list(zip(formats, format_averages))
            l_not_ambiguous = [{x: dict(zip(headers, y))} for x, y in combined]
            return {k: v for d in l_not_ambiguous for k, v in d.items()}
        else:
            return None

    # below is great functionality but should be moved to the match object
    def batting_for_match(self, match_id):
        batting_stats = []
        m = Match(match_id)
        for innings in list(m.full_scorecard["innings"].keys()):
            stats = next(
                (
                    x
                    for x in m.full_scorecard["innings"][innings]["batsmen"]
                    if x["href"] == self.url
                ),
                None,
            )
            if stats:
                batting_stats.append(
                    {
                        "innings": innings,
                        "balls_faced": next(
                            (
                                x["value"]
                                for x in stats["stats"]
                                if x["name"] == "ballsFaced"
                            ),
                            None,
                        ),
                        "minutes": next(
                            (
                                x["value"]
                                for x in stats["stats"]
                                if x["name"] == "minutes"
                            ),
                            None,
                        ),
                        "runs": next(
                            (x["value"] for x in stats["stats"] if x["name"] == "runs"),
                            None,
                        ),
                        "fours": next(
                            (
                                x["value"]
                                for x in stats["stats"]
                                if x["name"] == "fours"
                            ),
                            None,
                        ),
                        "sixes": next(
                            (
                                x["value"]
                                for x in stats["stats"]
                                if x["name"] == "sixes"
                            ),
                            None,
                        ),
                        "strike_rate": next(
                            (
                                x["value"]
                                for x in stats["stats"]
                                if x["name"] == "strikeRate"
                            ),
                            None,
                        ),
                    }
                )
        return batting_stats

    def bowling_for_match(self, match_id):
        bowling_stats = []
        m = Match(match_id)
        for innings in list(m.full_scorecard["innings"].keys()):
            stats = next(
                (
                    x
                    for x in m.full_scorecard["innings"][innings]["bowlers"]
                    if x["href"] == self.url
                ),
                None,
            )
            if stats:
                bowling_stats.append(
                    {
                        "innings": innings,
                        "overs": next(
                            (x["value"] for x in stats["stats"] if x["name"] == "overs")
                        ),
                        "maidens": next(
                            (
                                x["value"]
                                for x in stats["stats"]
                                if x["name"] == "maidens"
                            )
                        ),
                        "conceded": next(
                            (
                                x["value"]
                                for x in stats["stats"]
                                if x["name"] == "conceded"
                            )
                        ),
                        "wickets": next(
                            (
                                x["value"]
                                for x in stats["stats"]
                                if x["name"] == "wickets"
                            )
                        ),
                        "economy_rate": next(
                            (
                                x["value"]
                                for x in stats["stats"]
                                if x["name"] == "economyRate"
                            )
                        ),
                        "dots": next(
                            (x["value"] for x in stats["stats"] if x["name"] == "dots"),
                            None,
                        ),
                        "fours_conceded": next(
                            (
                                x["value"]
                                for x in stats["stats"]
                                if x["name"] == "foursConceded"
                            ),
                            None,
                        ),
                        "sixes_conceded": next(
                            (
                                x["value"]
                                for x in stats["stats"]
                                if x["name"] == "sixesConceded"
                            ),
                            None,
                        ),
                        "wides": next(
                            (
                                x["value"]
                                for x in stats["stats"]
                                if x["name"] == "wides"
                            ),
                            None,
                        ),
                        "no_balls": next(
                            (
                                x["value"]
                                for x in stats["stats"]
                                if x["name"] == "noballs"
                            ),
                            None,
                        ),
                    }
                )
        return bowling_stats
