const LOCALSTORAGE_ACCESS_TOKEN_KEY = "spotify-led-matrix-token";
const LOCALSTORAGE_ACCESS_TOKEN_EXPIRY_KEY =
	"spotify-led-matrix-token-expires-in";
const jssdkscopes = [
	"streaming",
	"user-read-birthdate",
	"user-read-email",
	"user-read-private",
	"user-modify-playback-state"
];

function parseHash(hash) {
	return hash
		.substring(1)
		.split("&")
		.reduce(function(initial, item) {
			if (item) {
				var parts = item.split("=");
				initial[parts[0]] = decodeURIComponent(parts[1]);
			}
			return initial;
		}, {});
}

document.addEventListener("DOMContentLoaded", () => {
	if (
		localStorage.getItem(LOCALSTORAGE_ACCESS_TOKEN_KEY) &&
		parseInt(
			parseInt(localStorage.getItem(LOCALSTORAGE_ACCESS_TOKEN_EXPIRY_KEY))
		) > Date.now()
	) {
		window.location = "/web/main.html";
	} else {
		if (window.location.hash) {
			const hash = parseHash(window.location.hash);
			if (hash["access_token"] && hash["expires_in"]) {
				localStorage.setItem(
					LOCALSTORAGE_ACCESS_TOKEN_KEY,
					hash["access_token"]
				);
				localStorage.setItem(
					LOCALSTORAGE_ACCESS_TOKEN_EXPIRY_KEY,
					Date.now() + 990 * parseInt(hash["expires_in"])
				);
				window.location = "/web/main.html";
			}
		}
		document
			.getElementById("spotifyBtn")
			.addEventListener("click", function(e) {
				e.preventDefault();
				fetch("https://accounts.spotify.com/authorize?", {
					client_id: "052c0d00a1cb4a7e8f63037443b7aee1",
					response_type: "token",
					scope: jssdkscopes.join(" "),
					redirect_uri: "https://missing-user.github.io/led_matrix/",
					show_dialog: true
				})
					.then(e => e.json())
					.then(data => {
						window.location = data.redirectUri;
					})
					.catch(error => {
						alert("Failed to prepare for Spotify Authentication");
					});
			});
	}
});
