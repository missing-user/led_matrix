const staggerVisualizerEl = document.getElementById("stagger-visualizer");
const staggerVisualizerEl2 = document.getElementById("stagger-visualizer2");
const staggerVisualizerEl3 = document.getElementById("stagger-visualizer3");
const fragment = document.createDocumentFragment();
const grid = [16, 16];
const col = grid[0];
const row = grid[1];
const numberOfElements = col * row;

for (let i = 0; i < numberOfElements; i++) {
	fragment.appendChild(document.createElement("div"));
}
staggerVisualizerEl.appendChild(fragment);
for (let i = 0; i < numberOfElements; i++) {
	fragment.appendChild(document.createElement("div"));
}
staggerVisualizerEl2.appendChild(fragment);
for (let i = 0; i < numberOfElements; i++) {
	fragment.appendChild(document.createElement("div"));
}
staggerVisualizerEl3.appendChild(fragment);

function animateBeat(duration) {
	anime({
		targets: "#stagger-visualizer2 div",
		easing: "easeInOutSine",
		loop: false,
		autoplay: true,
		delay: anime.stagger(duration / row / 2, {
			grid: grid,
			from: "center"
		}),
		scale: [
			{
				value: 0.1,
				easing: "easeOutSine",
				duration: duration / 4
			},
			{
				value: 1,
				easing: "easeInOutQuad",
				duration: duration / 2
			}
		]
	});
}
function animateBar(duration) {
	anime({
		targets: "#stagger-visualizer div",
		easing: "easeInOutSine",
		loop: false,
		autoplay: true,
		delay: anime.stagger(duration / row / 2, {
			grid: grid,
			from: "first",
			axis: "x"
		}),
		scale: [
			{
				value: 0.1,
				easing: "easeOutSine",
				duration: duration / 4
			},
			{
				value: 1,
				easing: "easeInOutQuad",
				duration: duration / 4
			}
		]
	});
}
function animateSection(duration, loudness) {
	anime({
		targets: "#stagger-visualizer3 div",
		easing: "easeInOutSine",
		loop: false,
		autoplay: true,
		delay: anime.stagger(duration / row / 2, {
			grid: grid,
			from: "first"
		}),
		scale: [
			{
				value: 0.1,
				easing: "easeOutSine",
				duration: duration / 4
			},
			{
				value: 1,
				easing: "easeInOutQuad",
				duration: duration / 4
			}
		],
		background: "hsl(" + ~~loudness + ", 84%, 73%)"
	});
}

//drawing the canvas matrix
var canvasMatrix = document.getElementById("canvasMatrix");
var ctx2 = canvasMatrix.getContext("2d");
let leds = [];
let rotation = 0;

for (var i = 0; i < row * col; i++) {
	leds.push({ r: 1, g: 1, b: 1, v: 1 });
}

function fromXY(x, y) {
	return y * row + x;
}
function XY(index) {
	return {
		x: index % row,
		y: ~~(index / row)
	};
}
function rotateMatrix90(count) {
	count = (count + 4) % 4;
	let rotated_leds = [...leds];
	switch (count) {
		case 1:
			for (var i = 0; i < leds.length; i++) {
				//rotate 90 deg
				rotated_leds[fromXY(XY(i).y, row - 1 - XY(i).x)] = leds[i];
			}
			break;
		case 2:
			for (var i = 0; i < leds.length; i++) {
				//rotate 90 deg
				rotated_leds[fromXY(row - 1 - XY(i).x, col - 1 - XY(i).y)] = leds[i];
			}
			break;
		case 3:
			for (var i = 0; i < leds.length; i++) {
				//rotate 90 deg
				rotated_leds[i] = leds[fromXY(XY(i).y, row - 1 - XY(i).x)];
			}
			break;
		default:
		case 0:
			return leds;
	}
	return rotated_leds;
}
Math.clamp = function(number, min = 0, max = 1) {
	return Math.max(min, Math.min(number, max));
};

setInterval(function() {
	timePercent =
		((Date.now() - CurrentMusic.startDate) / CurrentMusic.duration) % 1;
	if (even) Effects.arrow(timePercent, CurrentMusic.time_signature);
	else Effects.wave(timePercent, CurrentMusic.time_signature);

	leds = rotateMatrix90(rotation);
	drawCanvasMatrix();
}, 10);

function drawCanvasMatrix() {
	size = 50;
	margin = 10;
	ctx2.fillStyle = "white";
	ctx2.clearRect(0, 0, canvasMatrix.width, canvasMatrix.height);
	for (var i = 0; i < leds.length; i++) {
		offset = (size * leds[i].v) / 2;

		ctx2.fillStyle = [
			"rgb(",
			~~(leds[i].r * 255),
			", ",
			~~(leds[i].g * 255),
			", ",
			~~(leds[i].b * 255),
			")"
		].join("");
		//create centered, scaled square grid with a 10px margin
		ctx2.fillRect(
			(XY(i).x + 0.5) * (size + margin) - offset,
			(XY(i).y + 0.5) * (size + margin) - offset,
			size * leds[i].v,
			size * leds[i].v
		);
	}
}

Effects = {
	arrow: (timePercent, iterations = 1, ease = EasingFunctions.gaussianFit) => {
		for (var i = 0; i < numberOfElements / 2; i++) {
			eval =
				timePercent * (iterations + 1.5) - 1.5 + XY(i).x / row + XY(i).y / col;
			leds[i].v = ease(Math.clamp(eval > iterations ? eval : eval % 1));
		}
		for (var i = numberOfElements / 2; i < numberOfElements; i++) {
			eval =
				timePercent * (iterations + 1.5) +
				XY(i).x / row -
				1.5 +
				(col - 1 - XY(i).y) / col;
			leds[i].v = ease(Math.clamp(eval > iterations ? eval : eval % 1));
		}
	},
	wave: (timePercent, iterations = 1, ease = EasingFunctions.gaussianFit) => {
		for (var i = 0; i < leds.length; i++) {
			eval = timePercent * (iterations + 1) - 1 + XY(i).x / row;
			leds[i].v = ease(Math.clamp(eval > iterations ? eval : eval % 1));
		}
	}
};

CurrentMusic = {
	startDate: Date.now(),
	time_signature: 1,
	duration: 1000
};

EasingFunctions = {
	// no easing, no acceleration
	linear: t => t,
	// accelerating from zero velocity
	easeInQuad: t => t * t,
	// decelerating to zero velocity
	easeOutQuad: t => t * (2 - t),
	// acceleration until halfway, then deceleration
	easeInOutQuad: t => (t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t),
	// accelerating from zero velocity
	easeInCubic: t => t * t * t,
	// decelerating to zero velocity
	easeOutCubic: t => --t * t * t + 1,
	// acceleration until halfway, then deceleration
	easeInOutCubic: t =>
		t < 0.5 ? 4 * t * t * t : (t - 1) * (2 * t - 2) * (2 * t - 2) + 1,
	// accelerating from zero velocity
	easeInQuart: t => t * t * t * t,
	// decelerating to zero velocity
	easeOutQuart: t => 1 - --t * t * t * t,
	// acceleration until halfway, then deceleration
	easeInOutQuart: t => (t < 0.5 ? 8 * t * t * t * t : 1 - 8 * --t * t * t * t),
	// accelerating from zero velocity
	easeInQuint: t => t * t * t * t * t,
	// decelerating to zero velocity
	easeOutQuint: t => 1 + --t * t * t * t * t,
	// acceleration until halfway, then deceleration
	easeInOutQuint: t =>
		t < 0.5 ? 16 * t * t * t * t * t : 1 + 16 * --t * t * t * t * t,
	gaussianFit: t =>
		0.257 * t + 14.717 * t * t - 29.947 * t * t * t + 14.973 * t * t * t * t
};
