import json

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

scope = 'user-read-currently-playing'
token = util.prompt_for_user_token(
    'username', scope, redirect_uri='http://localhost:8080')


def time_to_beats(time_seconds):
    for i, beat in enumerate(results['beats']):
        if time_seconds > beat['start']:
            return i + (time_seconds - beat['start']) / beat['duration']
    return 0


if token:
    sp = spotipy.Spotify(auth=token)
    currentTrack = sp.current_user_playing_track()
    if not currentTrack:
        print('no currently playing song found, exiting')
        exit()
    album_cover = currentTrack['item']['album']['images'].pop()
    currentSongTime = currentTrack['progress_ms'] / 1000
    print('currentSong seconds', currentSongTime)
    results = sp.audio_analysis(currentTrack['item']['id'])
    print('BPM:', results['track']['tempo'])
    beatTime = 60 / results['track']['tempo']
    print()
    print(currentTrack['item']['name'], '    by   ',
          currentTrack['item']['artists'][0]['name'])
    print(json.dumps(sp.audio_features(
        currentTrack['item']['id']), indent=2))
    print()
else:
    print("Can't get token for", 'username')
