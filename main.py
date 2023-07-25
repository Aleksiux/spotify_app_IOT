import json
import requests
from dotenv import dotenv_values

config = dotenv_values(".env")
client_id = config['client_id']
secret_id = config['secret_id']
redirect_uri = config['redirect_uri']
user_id = config['username']
spotify_token = config['spotify_token']
discover_weekly_id = config['discover_weekly_id']

class SaveSongs:
    def __init__(self):
        self.user_id = user_id
        self.spotify_token = spotify_token
        self.discover_weekly_id = discover_weekly_id

    # Loop through playlist tracks, add them to list
    def find_songs(self):
        query = 'https://api.spotify.com/v1/playlists/{}/tracks'.format(discover_weekly_id)
        response = requests.get(query, headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(spotify_token)
        })
        response_json = response.json()
        return response_json
a = SaveSongs()
print(a.find_songs())