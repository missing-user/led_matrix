const LOCALSTORAGE_ACCESS_TOKEN_KEY = "spotify-led-matrix-token";
const LOCALSTORAGE_ACCESS_TOKEN_EXPIRY_KEY =
	"spotify-led-matrix-token-expires-in";
const accessToken = localStorage.getItem(LOCALSTORAGE_ACCESS_TOKEN_KEY);
var spotifyApi = new SpotifyWebApi();
var currentSongMs = 0;
var timeouts = [];
var songAnaysis;
spotifyApi.setAccessToken(localStorage.getItem(LOCALSTORAGE_ACCESS_TOKEN_KEY));
//gets the current playing song, shows title and pixelated image
function getCurrSongInfo() {
	for (var t of timeouts) clearTimeout(t);
	timeouts = [];
	spotifyApi
		.getMyCurrentPlayingTrack()
		.then(
			function(data) {
				console.log("current song", data);
				if (data) {
					document.getElementById("track_name").textContent = data.item.name;
					//get the last (lowest resolution) image from the album images list
					var image = data.item.album.images.pop();
					pixelateAndDisplay(image.url);
					currentSongMs = data.progress_ms;
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
	spotifyApi.getAudioAnalysisForTrack(songId).then(
		//do something with json
		displayAnalysis
	);
}
var effect = 0;

function displayAnalysis(data) {
	songAnaysis = data;
	for (var sct of data.sections) setupSection(sct);
	for (var beat of data.beats) setupBeat(beat);
	for (var bar of data.bars) setupBar(bar);
}

function setupSection(section) {
	startTime = section.start * 1000 - currentSongMs;
	timeouts.push(
		setTimeout(() => {
			console.log("SECTION");
			//set the description text for this section
			document.getElementById(
				"sectionInfo"
			).textContent = `duration: ${section.duration}, time signature: ${section.time_signature}, loudness: ${section.loudness}, bpm: ${songAnaysis.track.tempo}`;
			//CurrentMusic.time_signature = section.time_signature;
			if (songAnaysis.track.tempo > 100) CurrentMusic.time_signature = 1;
			else CurrentMusic.time_signature = 2;

			effect = ~~(Math.random() * 15);
			//animate the small section visualizer
		}, startTime)
	);
}

function setupBeat(beat) {
	startTime = beat.start * 1000 - currentSongMs;
	if (startTime > 0)
		timeouts.push(
			setTimeout(() => {
				CurrentMusic.startDate = Date.now();
				CurrentMusic.duration = beat.duration * 1000;
			}, startTime)
		);
}
var color = 1;
function setupBar(bar) {
	startTime = bar.start * 1000 - currentSongMs;
	if (startTime > 0)
		timeouts.push(
			setTimeout(() => {
				console.log("BAR");
				rotation++;
				if (color == 1) fillColor(0, 0, 1);
				else if (color == 2) fillColor(0, 1, 0);
				else if (color == 3) fillColor(1, 0, 0);
				else fillColor(1, 1, 1);
				color++;
				color = color % 4;
			}, startTime)
		);
}
getCurrSongInfo();
//image pixelization stuff
var img = new Image();
var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");

function pixelateAndDisplay(url) {
	img.crossOrigin = "anonymous";
	img.src = url;
	img.onload = function() {
		canvas.height = img.height * 4;
		canvas.width = img.width * 4;
		ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
		pixelate();
	};
}

function pixelate() {
	//dynamically adjust canvas size to the size of the uploaded image
	canvas.height = img.height * 4;
	canvas.width = img.width * 4;
	/// cache scaled width and height
	(w = 16), (h = 16);
	/// draw original image to the scaled size
	ctx.drawImage(img, 0, 0, w, h);
	ctx.mozImageSmoothingEnabled = false;
	ctx.imageSmoothingEnabled = false;
	ctx.drawImage(canvas, 0, 0, w, h, 0, 0, canvas.width, canvas.height);
}
// DEBUG: this is just for local testing
setTimeout(displayAnalysis, 500, testdata);
