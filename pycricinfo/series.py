import requests


class Series(object):
    """
    Abstraction of a series
    """

    def __init__(self, series_id: int) -> None:

        self.series_id = series_id

        self.json_url = (
            f"http://core.espnuk.org/v2/sports/cricket/leagues/{self.series_id}/"
        )
        # need to think about naming here - what is at this url?
        self.events_url = (
            f"http://core.espnuk.org/v2/sports/cricket/leagues/{self.series_id}/events"
        )

        self.seasons_url = (
            f"http://core.espnuk.org/v2/sports/cricket/leagues/{self.series_id}/seasons"
        )

        self.json = self.get_json()

        # parsing json
        if self.json:
            self.name = self.json["name"]
            self.short_name = self.json["shortName"]
            self.abbreviation = self.json["abbreviation"]
            self.slug = self.json["slug"]
            self.is_tournament = self.json["isTournament"]
            self.url = self.json["links"][0]["href"]

    def get_json(self):

        r = requests.get(self.json_url)
        if r.status_code == 404:
            raise "Not Found"
        else:
            return r.json()

    # again, need to look into what is a series vs season
    def get_events_for_season(self, season):
        responses = []
        season_events = []
        season_events_url = self.seasons_url + "/{0}/events".format(str(season))
        season_events_json = self.get_json(season_events_url)
        if season_events_json:
            rs = (requests.get(event["$ref"]) for event in season_events_json["items"])
            responses = requests.map(rs)
            for response in responses:
                event_json = response.json()
                venue_json = self.get_json(event_json["venues"][0]["$ref"])
                season_events.append(
                    {
                        "url": event_json["$ref"],
                        "match_id": event_json["id"],
                        "class": event_json["competitions"][0]["class"][
                            "generalClassCard"
                        ],
                        "date": event_json["date"],
                        "description": event_json["shortDescription"],
                        "venue_url": event_json["venues"][0]["$ref"],
                        "venue": venue_json["fullName"],
                    }
                )
            return season_events
        else:
            return None
