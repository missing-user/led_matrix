const LOCALSTORAGE_ACCESS_TOKEN_KEY = "spotify-led-matrix-token";
const LOCALSTORAGE_ACCESS_TOKEN_EXPIRY_KEY =
	"spotify-led-matrix-token-expires-in";
const accessToken = localStorage.getItem(LOCALSTORAGE_ACCESS_TOKEN_KEY);
var spotifyApi = new SpotifyWebApi();
var currentSongMs = 0;
var songAnaysis;
spotifyApi.setAccessToken(localStorage.getItem(LOCALSTORAGE_ACCESS_TOKEN_KEY));
//gets the current playing song, saves analysis

var currentTrack;
var results;

function getCurrSongInfo() {
	spotifyApi
		.getMyCurrentPlayingTrack()
		.then(
			function(data) {
				console.log("current song", data);
				document.getElementById("track_name").textContent = data.item.name;
				if (data) {
					currentTrack = data;
					total_song_time = data.item.duration_ms / 1000;
					current_song_time = data.progress_ms / 1000;
					console.log(data, "at time", current_song_time);
					return data.item.id;
				}

				return null;
			},
			function(err) {
				console.error(err);
			}
		)
		.then(getSongAnalysis);
}
function getSongAnalysis(songId) {
	spotifyApi.getAudioAnalysisForTrack(songId).then(r => {
		results = r;
		console.log(r);
	});
}

getCurrSongInfo();
