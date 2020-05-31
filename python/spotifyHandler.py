import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

scope = 'user-read-currently-playing'
token = util.prompt_for_user_token(
    'username', scope, redirect_uri='http://localhost:8080')


if token:
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_playing_track()
    albumCover = results['item']['album']['images'].pop()
    print(albumCover)
    currentSongTime = results['progress_ms'] / 1000
    print('currentSong seconds', currentSongTime)
    results = sp.audio_analysis(results['item']['id'])
    print(results['track']['tempo'])
    beatTime = 60 / results['track']['tempo']
else:
    print("Can't get token for", 'username')
