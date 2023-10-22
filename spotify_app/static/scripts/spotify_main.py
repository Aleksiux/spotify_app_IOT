import requests
from dotenv import dotenv_values, load_dotenv
from .refresh import Refresh

config = dotenv_values(".env")
redirect_uri = config['redirect_uri']
user_id = config['username']
discover_weekly_id = config['discover_weekly_id']


# device_id = config['device_id']


class SaveSongs:
    def __init__(self):
        with open(
                r'C:\Users\Aleksas\PycharmProjects\spotify_api\spotify_app_IOT\spotify_app\static\scripts\devices.txt',
                'r') as f:
            device = f.read()
        self.user_id = user_id
        self.spotify_token = ''
        self.discover_weekly_id = discover_weekly_id
        self.tracks = []
        self.available_devices = []
        self.device_id = device

    # Loop through playlist tracks, add them to list
    def find_songs(self):
        query = 'https://api.spotify.com/v1/playlists/{}/tracks'.format(discover_weekly_id)
        response = requests.get(query, headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.spotify_token)
        })
        response_json = response.json()
        for i in response_json['items']:
            self.tracks.append(i['track']['uri'])
        return self.tracks

    def find_album_songs(self, album_id):
        query = f"https://api.spotify.com/v1/albums/{album_id}"
        response = requests.get(query, headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.spotify_token)
        })
        return response.json()

    def get_available_devices(self):
        query = 'https://api.spotify.com/v1/me/player/devices'
        response = requests.get(query, headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.spotify_token)
        })
        response_json = response.json().values()
        for _ in response_json:
            for devices in _:
                device = {
                    'id': devices['id'],
                    'name': devices['name'],
                    'type': devices['type'],
                    'volume_percent': devices['volume_percent']
                }
                self.available_devices.append(device)

        return self.available_devices

    def play_song_on_device(self, track=''):
        query = 'https://api.spotify.com/v1/me/player/play'
        querystring = {"device_id": f"{self.device_id}"}

        payload = {
            "uris": [f"{track}"],
            "position_ms": 1,
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.spotify_token)
        }

        play = requests.request("PUT", query, json=payload, headers=headers, params=querystring)
        return play

    def pause_song_on_device(self):
        query = 'https://api.spotify.com/v1/me/player/pause'
        querystring = {"device_id": f"{self.device_id}"}
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.spotify_token)
        }

        pause = requests.request("PUT", query, headers=headers, params=querystring)
        return pause

    def play_track(self):
        query = 'https://api.spotify.com/v1/me/player/play'
        querystring = {"device_id": f"{self.device_id}"}
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.spotify_token)
        }

        pause = requests.request("PUT", query, headers=headers, params=querystring)
        return pause

    def search_track(self, search_query):
        query = 'https://api.spotify.com/v1/search'
        querystring = {"q": search_query, "type": "track"}
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.spotify_token)
        }
        searched = requests.request("GET", query, headers=headers, params=querystring)
        return searched.json()

    def call_refresh(self):
        refresh_caller = Refresh()
        self.spotify_token = refresh_caller.refresh()

    def get_playback_state(self):
        query = 'https://api.spotify.com/v1/me/player/currently-playing'
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.spotify_token)
        }
        playback_state = requests.request("GET", query, headers=headers)
        return playback_state.json()

    def skip_next(self):
        query = 'https://api.spotify.com/v1/me/player/next'
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.spotify_token)
        }
        skip = requests.request("POST", query, headers=headers)
        return skip

    def prev_track(self):
        query = 'https://api.spotify.com/v1/me/player/previous'
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.spotify_token)
        }
        prev = requests.request("POST", query, headers=headers)
        return prev

    def set_playback_volume(self, volume):
        query = 'https://api.spotify.com/v1/me/player/volume'
        querystring = {"volume_percent": volume}
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.spotify_token)
        }
        volume_data = requests.request("PUT", query, headers=headers, params=querystring)
        return volume_data
