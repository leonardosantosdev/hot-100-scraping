import requests
from bs4 import BeautifulSoup
from difflib import SequenceMatcher as sm


class Hot100Scraping:
    def __init__(self, user_id, hot_100_url, sp) -> None:
        self.user_id = user_id
        self.hot_100_url = hot_100_url
        self.sp = sp
        self.hot_100_list = []

    def create_hot_100_playist(self):
        playlist_name = self._create_playlist()
        self._scrape_hot_100_url()
        self.hot_100_list = [
            {j: k.lower() for j, k in i.items()} for i in self.hot_100_list
        ]
        tracks_id = self._get_track_id()
        self.sp.user_playlist_add_tracks(
            self.user_id, self._get_playlist_id(playlist_name), tracks_id
        )

    def _create_playlist(self):
        playlist_name = "Billboard Hot 100"
        self.sp.user_playlist_create(self.user_id, name=playlist_name)
        return playlist_name

    def _scrape_hot_100_url(self):
        try:
            r = requests.get(self.hot_100_url)

            soup = BeautifulSoup(r.content, features="html.parser")

            songs_list = soup.find_all(class_="o-chart-results-list-row-container")
            for s in songs_list:
                song = (
                    s.find(
                        class_=(
                            "lrv-a-unstyle-list lrv-u-flex lrv-u-height-100p lrv-u-flex-direction"
                            + "-column@mobile-max"
                        )
                    )
                    .find("h3")
                    .get_text()
                    .strip()
                )
                artist = (
                    s.find(
                        class_=(
                            "lrv-a-unstyle-list lrv-u-flex lrv-u-height-100p lrv-u-flex-direction"
                            + "-column@mobile-max"
                        )
                    )
                    .find("span")
                    .get_text()
                    .strip()
                )
                self.hot_100_list.append({"song": song, "artist": artist})
        except Exception as e:
            raise e

    def _get_track_id(self):
        track_ids = []
        for i in range(len(self.hot_100_list)):
            if " featuring " in self.hot_100_list[i]["artist"]:
                self.hot_100_list[i]["artist"] = self.hot_100_list[i]["artist"].split(
                    "featuring"
                )[0]

            if " with" in self.hot_100_list[i]["artist"]:
                self.hot_100_list[i]["artist"] = self.hot_100_list[i]["artist"].split(
                    "with"
                )[0]

            if " & " in self.hot_100_list[i]["artist"]:
                self.hot_100_list[i]["artist"] = self.hot_100_list[i]["artist"].split(
                    "&"
                )[0]

            if " and " in self.hot_100_list[i]["artist"]:
                self.hot_100_list[i]["artist"] = self.hot_100_list[i]["artist"].split(
                    "and"
                )[0]

            if ", " in self.hot_100_list[i]["artist"]:
                self.hot_100_list[i]["artist"] = self.hot_100_list[i]["artist"].split(
                    ", "
                )[0]

            if " x " in self.hot_100_list[i]["artist"]:
                self.hot_100_list[i]["artist"] = self.hot_100_list[i]["artist"].split(
                    " x "
                )[0]

            if "[from" in self.hot_100_list[i]["song"]:
                self.hot_100_list[i]["song"] = self.hot_100_list[i]["song"].split(
                    "[from"
                )[0]

            if " (" in self.hot_100_list[i]["song"]:
                self.hot_100_list[i]["song"] = self.hot_100_list[i]["song"].split(" (")[
                    0
                ]

            results = self.sp.search(
                q=f"{self.hot_100_list[i]['song']} {self.hot_100_list[i]['artist']} ",
                limit=5,
                type="track",
            )

            if results["tracks"]["total"] == 0:
                continue
            else:
                for j in range(len(results["tracks"]["items"])):
                    aux_artist_a = results["tracks"]["items"][j]["artists"][0]["name"]
                    aux_artist_b = self.hot_100_list[i]["artist"]
                    aux_song_a = results["tracks"]["items"][j]["name"]
                    aux_song_b = self.hot_100_list[i]["song"]

                    aux_artist_a = aux_artist_a.lower()
                    aux_song_a = aux_song_a.lower()

                    if "(from" in aux_song_a:
                        aux_song_a = aux_song_a.split("(from")[0].strip()

                    if "[from" in aux_song_a:
                        aux_song_a = aux_song_a.split("[from")[0].strip()

                    if "- from" in aux_song_a:
                        aux_song_a = aux_song_a.split("- from")[0].strip()

                    if "(feat" in aux_song_a:
                        aux_song_a = aux_song_a.split("(feat")[0].strip()

                    if "(with" in aux_song_a:
                        aux_song_a = aux_song_a.split("(with")[0].strip()

                    if " with" in aux_song_a:
                        aux_song_a = aux_song_a.split(" with")[0].strip()

                    if " - en" in aux_song_a:
                        aux_song_a = aux_song_a.split(" - en")[0].strip()

                    if "- remix" in aux_song_a:
                        aux_song_a = aux_song_a.split("- remix")[0].strip()

                    if " (" in aux_song_a:
                        aux_song_a = aux_song_a.split(" (")[0].strip()

                    if ", " in aux_artist_a:
                        aux_artist_a = aux_artist_a.split(", ")[0].strip()

                    if (
                        round(sm(None, aux_artist_a, aux_artist_b).ratio(), 1) >= 0.8
                    ) and (round(sm(None, aux_song_a, aux_song_b).ratio(), 1) >= 0.8):
                        track_ids.append(results["tracks"]["items"][j]["id"])
                        break

                    else:
                        print("position {}".format(i))
                        print("NOT FOUND")
                        print(j)
                        print(aux_artist_a + " | " + aux_artist_b)
                        print(aux_song_a + " | " + aux_song_b)

                        print(round(sm(None, aux_artist_a, aux_artist_b).ratio(), 1))
                        print(
                            round(
                                sm(
                                    None, aux_song_a.lower(), aux_song_b.lower()
                                ).ratio(),
                                1,
                            )
                        )
                        print()

        return track_ids

    def _get_playlist_id(self, playlist_name):
        playlist_id = ""
        playlists = self.sp.user_playlists(self.user_id)
        for playlist in playlists["items"]:
            if playlist["name"] == playlist_name:
                playlist_id = playlist["id"]
        return playlist_id
