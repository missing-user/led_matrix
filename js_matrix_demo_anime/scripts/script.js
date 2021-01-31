var grid = document.getElementById("grid")
var grid_elements = []
const offColor = '#36383c';

window.onresize = recalc_grid_height;
document.addEventListener('DOMContentLoaded', () => {
    recalc_grid_height()
    anime({
        startDelay: 1000,
        targets: grid_elements,
        backgroundColor: { value: "#FFF", easing: 'easeInOutQuad', duration: 250 },
        delay: anime.stagger(40, { grid: [16, 16], axis: 'y' }),
    });
}, false);

function recalc_grid_height() {
    grid.style.height = anime.get(grid, 'width', 'px');
}

var c = document.createDocumentFragment();
for (i = 0; i < 16 * 16; i++) {
    var e = document.createElement("div");
    e.className = "grid-item";
    c.appendChild(e);
    grid_elements.push(e)
}
grid.appendChild(c); //append all the grid elements to the container
grid_elements = document.getElementsByClassName("grid-item")


//add click listeners to all elements
for (let index = 0; index < grid_elements.length; index++) {
    const el = grid_elements[index];
    el.addEventListener("click", e => {
        anime({
            targets: grid_elements,
            backgroundColor: [
                { value: "#FFF", easing: 'easeInOutQuad', duration: 120 },
                { value: "#36383c", easing: 'easeInOutQuad', duration: 300 }
            ],
            delay: anime.stagger(50, { grid: [16, 16], from: index })
        });
    });
}

var currentMode

function rainbow() {
    //why isn't this simpler
    anime.set(grid_elements, { backgroundColor: function (el, i) { return 'hsl(' + (i - i % 16 + 360) + ', 100%, 50%)'; } })

    anime.timeline({
        targets: grid_elements,
        loop: true,
        autoplay: true,
        easing: 'linear',
        duration: 250,
    }).add({
        backgroundColor: function (el, i) { return 'hsl(' + (i - i % 16 + 20) + ', 100%, 50%)'; }
    }).add({
        backgroundColor: function (el, i) { return 'hsl(' + (i - i % 16 + 40) + ', 100%, 50%)'; }
    }).add({
        backgroundColor: function (el, i) { return 'hsl(' + (i - i % 16 + 60) + ', 100%, 50%)'; }
    }).add({
        backgroundColor: function (el, i) { return 'hsl(' + (i - i % 16 + 80) + ', 100%, 50%)'; }
    }).add({
        backgroundColor: function (el, i) { return 'hsl(' + (i - i % 16 + 100) + ', 100%, 50%)'; }
    }).add({
        backgroundColor: function (el, i) { return 'hsl(' + (i - i % 16 + 120) + ', 100%, 50%)'; }
    }).add({
        backgroundColor: function (el, i) { return 'hsl(' + (i - i % 16 + 140) + ', 100%, 50%)'; }
    }).add({
        backgroundColor: function (el, i) { return 'hsl(' + (i - i % 16 + 160) + ', 100%, 50%)'; }
    }).add({
        backgroundColor: function (el, i) { return 'hsl(' + (i - i % 16 + 180) + ', 100%, 50%)'; }
    }).add({
        backgroundColor: function (el, i) { return 'hsl(' + (i - i % 16 + 200) + ', 100%, 50%)'; }
    }).add({
        backgroundColor: function (el, i) { return 'hsl(' + (i - i % 16 + 220) + ', 100%, 50%)'; }
    }).add({
        backgroundColor: function (el, i) { return 'hsl(' + (i - i % 16 + 240) + ', 100%, 50%)'; }
    }).add({
        backgroundColor: function (el, i) { return 'hsl(' + (i - i % 16 + 260) + ', 100%, 50%)'; }
    }).add({
        backgroundColor: function (el, i) { return 'hsl(' + (i - i % 16 + 280) + ', 100%, 50%)'; }
    }).add({
        backgroundColor: function (el, i) { return 'hsl(' + (i - i % 16 + 300) + ', 100%, 50%)'; }
    }).add({
        backgroundColor: function (el, i) { return 'hsl(' + (i - i % 16 + 320) + ', 100%, 50%)'; }
    }).add({
        backgroundColor: function (el, i) { return 'hsl(' + (i - i % 16 + 340) + ', 100%, 50%)'; }
    }).add({
        backgroundColor: function (el, i) { return 'hsl(' + (i - i % 16 + 360) + ', 100%, 50%)'; }
    })

}


function twinkle() {
    for (let index = 0; index < 128; index++) {
        randomValues()
    }
}

function pulses() {
    if (currentMode == pulses) {
        anime({
            targets: grid_elements,
            backgroundColor: [
                { value: "#FFF", easing: 'easeInOutQuad', duration: 120 },
                { value: "#36383c", easing: 'easeInOutQuad', duration: 300 }
            ],
            delay: anime.stagger(50, { grid: [16, 16], from: anime.random(0, 255) }),
            complete: pulses
        });
    }
}


function wipes() {
    if (currentMode == wipes) {
        anime({
            targets: grid_elements,
            backgroundColor: { value: 'hsl(' + anime.random(0, 360) + ', 90%, 50%)', easing: 'easeInOutQuad', duration: 500 },
            delay: anime.stagger(70, { grid: [16, 16], axis: 'x' }),
            complete: wipes
        });
    }
}
function off() {
    anime({
        targets: grid_elements,
        backgroundColor: offColor,
        easing: 'easeInOutQuad',
        duration: 200
    });
}

function randomValues() {
    if (currentMode == twinkle) {
        const el = grid_elements[anime.random(0, grid_elements.length - 1)]
        currentAnimation = anime({
            targets: el,
            backgroundColor:
                function () {
                    return ['hsl(' + Math.floor((anime.random(0, 40) + Date.now() / 100) % 360) + ', 100%, 50%)',
                        offColor];
                },
            easing: 'easeInOutQuad',
            duration: 1200,
            delay: anime.random(0, 1200),
            complete: randomValues
        });
    }
}

function setAnim(targetMode) {
    if (currentMode != targetMode) {
        for (const anim of anime.running) {
            anim.pause()
            anim.reset()
        }
        currentMode = targetMode
    }
    currentMode()
}
