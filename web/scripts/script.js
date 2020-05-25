const LOCALSTORAGE_ACCESS_TOKEN_KEY = "spotify-audio-analysis-playback-token";
const LOCALSTORAGE_ACCESS_TOKEN_EXPIRY_KEY =
	"spotify-audio-analysis-playback-token-expires-in";
const accessToken = localStorage.getItem(LOCALSTORAGE_ACCESS_TOKEN_KEY);

fetch("https://api.spotify.com/v1/me/player/currently-playing", {
	method: "GET",
	headers: {
		Authorization: `Bearer ${accessToken}`
	}
})
	.then(response => response.json())
	.then(json => {
		console.log(json);
		document.getElementById("track_name").textContent = json.item.name;
		var image = json.item.album.images.pop() || {
			height: 256,
			url: "https://via.placeholder.com/256",
			width: 256
		};
		console.log(image);
		ResizeImage(image.url);
	});

var track_id = "6EJiVf7U0p1BBfs0qqeb1f";
fetch("https://api.spotify.com/v1/audio-analysis/" + track_id, {
	method: "GET",
	headers: {
		Authorization: `Bearer ${accessToken}`
	}
})
	.then(response => response.json())
	.then(json => {
		console.log(json);
		/*json.beats.forEach((beat, index) => {
			console.log(`Beat ${index} starts at ${beat.start}`);
		});*/
	});

/*function getCurrentlyPlaying() {
  fetch("https://api.spotify.com/v1/me/player/currently-playing" -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer {TOKEN}")
}*/

var img = new Image();
var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");

function ResizeImage(url) {
	img.crossOrigin = "anonymous";
	img.src = url;
	img.onload = function() {
		canvas.height = img.height * 4;
		canvas.width = img.width * 4;
		ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
		setTimeout(pixelate, 250);
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
