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
		easing: 'easeInOutSine',
		loop: false,
		autoplay: true,
		delay: anime.stagger(duration / row / 2, {
			grid: grid,
			from: 'center'
		}),
		scale: [{
			value: .1,
			easing: 'easeOutSine',
			duration: duration / 4
		}, {
			value: 1,
			easing: 'easeInOutQuad',
			duration: duration / 2
		}],
	})
}

function animateBar(duration) {
	anime({
		targets: "#stagger-visualizer div",
		easing: 'easeInOutSine',
		loop: false,
		autoplay: true,
		delay: anime.stagger(duration / row / 2, {
			grid: grid,
			from: 'first',
			axis: 'x'
		}),
		scale: [{
			value: .1,
			easing: 'easeOutSine',
			duration: duration / 4
		}, {
			value: 1,
			easing: 'easeInOutQuad',
			duration: duration / 4
		}],
	})
}

function animateSection(duration, loudness) {
	anime({
		targets: "#stagger-visualizer3 div",
		easing: 'easeInOutSine',
		loop: false,
		autoplay: true,
		delay: anime.stagger(duration / row / 2, {
			grid: grid,
			from: 'first'
		}),
		scale: [{
			value: .1,
			easing: 'easeOutSine',
			duration: duration / 4
		}, {
			value: 1,
			easing: 'easeInOutQuad',
			duration: duration / 4
		}],
		background: 'hsl(' + ~~(loudness) + ', 84%, 73%)'
	})
}