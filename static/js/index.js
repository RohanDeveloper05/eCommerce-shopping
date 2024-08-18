window.addEventListener("scroll", function() {
    let nav = document.querySelector("nav");
    nav.classList.toggle("sticky", window.scrollY > 0);

    let image = document.getElementById("Account");
    if (window.scrollY > 0) {
        image.src = "{% static 'image/accountblack.png' %}";
        image.style.transition = "0.6s";
    } else {
        image.src = "{% static 'image/accountwhite.png' %}";
    }
});

const cursorDot = document.querySelector("[data-cursor-dot]");
const cursorOutline = document.querySelector("[data-cursor-outline]");
let hideTimeout;

function showCursor() {
    cursorDot.style.opacity = '1';
    cursorOutline.style.opacity = '1';
}

function hideCursor() {
    cursorDot.style.opacity = '0';
    cursorOutline.style.opacity = '0';
}

function updateCursor(e) {
    clearTimeout(hideTimeout);

    const posX = e.clientX;
    const posY = e.clientY;

    cursorDot.style.left = `${posX}px`;
    cursorDot.style.top = `${posY}px`;

    cursorOutline.style.left = `${posX}px`;
    cursorOutline.style.top = `${posY}px`;

    showCursor();

    hideTimeout = setTimeout(hideCursor, 1000);
}

window.addEventListener("mousemove", updateCursor);

hideCursor();

var mySong = document.getElementById("mySong");
var iconSong = document.getElementById("iconSong");

// Attempt to unmute after a short delay (if policy allows)
window.onload = function() {
    setTimeout(() => {
        mySong.muted = false;
    }, 1000); // Unmute after 1 second if possible
};

// Toggle play/pause and icon change on click
iconSong.onclick = function() {
    if (mySong.paused) {
        mySong.play();
        iconSong.src = "{% static 'image/volume-up0.png' %}";
    } else {
        mySong.pause();
        iconSong.src = "{% static 'image/sound-off0.png' %}";
    }
};
