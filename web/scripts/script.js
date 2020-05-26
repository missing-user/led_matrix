const LOCALSTORAGE_ACCESS_TOKEN_KEY = "spotify-led-matrix-token";
const LOCALSTORAGE_ACCESS_TOKEN_EXPIRY_KEY =
	"spotify-led-matrix-token-expires-in";
const accessToken = localStorage.getItem(LOCALSTORAGE_ACCESS_TOKEN_KEY);

var spotifyApi = new SpotifyWebApi();
spotifyApi.setAccessToken(localStorage.getItem(LOCALSTORAGE_ACCESS_TOKEN_KEY));

spotifyApi.getMyCurrentPlayingTrack({}, response => {
	console.log("response", response);
	response.json().then(json => {
		console.log(json);
		document.getElementById("track_name").textContent = json.item.name;
		var image = json.item.album.images.pop() || {
			height: 128,
			url: "https://via.placeholder.com/128",
			width: 128
		};
		console.log(image);
		ResizeImage(image.url);
	});
});

/*
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
			height: 128,
			url: "https://via.placeholder.com/128",
			width: 128
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

	});

/*function getCurrentlyPlaying() {
  fetch("https://api.spotify.com/v1/me/player/currently-playing" -H "Accept: application/json" -H "Content-Type: application/json" -H "Authorization: Bearer BQDroIxFLAaZuwdNf52kr2lISRNhJYZ2k_iOr8dzDxhmYIP66nijRd4faw7LImykeoQeb1NfVtJ-jf8VnvaPa1yWfwmH2Z3w_Y5QcaaeMRsXr08voNz2rsN-dDUTRmb1I3Izm7OaiOJgv9sp5t-LILsM8UZ4v7M3qVMJnm5AKWwFCiyy5iXWnQ")
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
