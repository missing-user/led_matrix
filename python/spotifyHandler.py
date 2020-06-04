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


if token:
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_playing_track()
    if not results:
        print('no currently playing song found, exiting')
        exit()
    albumCover = results['item']['album']['images'].pop()
    print(albumCover)
    currentSongTime = results['progress_ms'] / 1000
    print('currentSong seconds', currentSongTime)
    results = sp.audio_analysis(results['item']['id'])
    print('BPM:', results['track']['tempo'])
    beatTime = 60 / results['track']['tempo']

    segments = results['segments']
    bars = results['bars']
    sections = results['sections']
else:
    print("Can't get token for", 'username')
