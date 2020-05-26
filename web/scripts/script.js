const LOCALSTORAGE_ACCESS_TOKEN_KEY = "spotify-led-matrix-token";
const LOCALSTORAGE_ACCESS_TOKEN_EXPIRY_KEY = "spotify-led-matrix-token-expires-in";
const accessToken = localStorage.getItem(LOCALSTORAGE_ACCESS_TOKEN_KEY);
var spotifyApi = new SpotifyWebApi();
var currentSongMs = 0;
var timeouts = [];
var songAnaysis;
spotifyApi.setAccessToken(localStorage.getItem(LOCALSTORAGE_ACCESS_TOKEN_KEY));
//gets the current playing song, shows title and pixelated image
function getCurrSongInfo() {
	for (var t of timeouts) clearTimeout(t);
	timeouts = []
	spotifyApi.getMyCurrentPlayingTrack()
		.then(function (data) {
			console.log("current song", data);
			if (data) {
				document.getElementById("track_name")
					.textContent = data.item.name;
				//get the last (lowest resolution) image from the album images list
				var image = data.item.album.images.pop();
				pixelateAndDisplay(image.url);
				currentSongMs = data.progress_ms;
				return data.item.id;
			}
			return null;
		}, function (err) {
			console.error(err);
		})
		.then(getSongAnalysis);
}

function getSongAnalysis(songId) {
	spotifyApi.getAudioAnalysisForTrack(songId)
		.then(
			//do something with json
			testDisplayAnalysis);
}
var even = true,
	even2 = true;

function testDisplayAnalysis(data) {
	songAnaysis = data;
	for (var sct of data.sections) setupSection(sct);
	for (var beat of data.beats) setupBeat(beat);
	for (var bar of data.bars) setupBar(bar);
}

function setupSection(section) {
	timeouts.push(setTimeout(() => {
		document.getElementById("sectionInfo")
			.textContent = `duration: ${section.duration},\n time signature: ${section.time_signature},\n loudness: ${section.loudness}`;
		animateSection(section.duration * 1000, Math.exp(section.loudness) * 30000)
	}, section.start * 1000 - currentSongMs));
}

function setupBeat(beat) {
	timeouts.push(setTimeout(() => {
		animateBeat(beat.duration * 1000)
	}, beat.start * 1000 - currentSongMs));
}

function setupBar(bar) {
	timeouts.push(setTimeout(() => {
		animateBar(bar.duration * 1000)
	}, bar.start * 1000 - currentSongMs));
}
getCurrSongInfo();
//image pixelization stuff
var img = new Image();
var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");

function pixelateAndDisplay(url) {
	img.crossOrigin = "anonymous";
	img.src = url;
	img.onload = function () {
		canvas.height = img.height * 4;
		canvas.width = img.width * 4;
		ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
		setTimeout(pixelate, 750);
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