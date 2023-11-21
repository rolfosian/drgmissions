function scrollToTop() {
    window.scrollTo(0, 0);
    }
    $(document).ready(function() {
    $('img').on('load', function() {
        scrollToTop();
    });
    scrollToTop();
    });

document.addEventListener("DOMContentLoaded", function () {
    const targetDay = 4;
    const targetHour = 11;
    let targetTime = new Date();
    targetTime.setUTCHours(targetHour, 0, 0, 0);
    if (targetTime.getUTCDay() === targetDay && Date.now() > targetTime.getTime()) {
        targetTime.setUTCDate(targetTime.getUTCDate() + 7);
    }
    while (targetTime.getUTCDay() !== targetDay) {
        targetTime.setUTCDate(targetTime.getUTCDate() + 1);
    }
    const countdownTimer = setInterval(() => {
        const now = Date.now();
        const remainingTime = targetTime.getTime() - now;
        if (remainingTime <= 0) {
            clearInterval(countdownTimer);
            document.getElementById("ddcountdown").innerHTML = "0D 00:00:00";
        } else {(0)
            const days = Math.floor(remainingTime / (1000 * 60 * 60 * 24));
            const hours = Math.floor((remainingTime % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((remainingTime % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((remainingTime % (1000 * 60)) / 1000);
            const formattedTime = formatTime(days, hours, minutes, seconds);
            document.getElementById("ddcountdown").innerHTML = formattedTime;
        }
    }, 1000);

function formatTime(days, hours, minutes, seconds) {
    return `${days}:${formatNumber(hours)}:${formatNumber(minutes)}:${formatNumber(seconds)}`;
}

function formatNumber(number) {
    return number.toString().padStart(2, "0");
}
});

document.addEventListener("DOMContentLoaded", function() {
    const targetTime1 = new Date();
    targetTime1.setSeconds(0);
    targetTime1.setMilliseconds(0);
    if (targetTime1.getMinutes() < 30) {
        targetTime1.setMinutes(30);
    } else {
        targetTime1.setMinutes(0);
        targetTime1.setHours(targetTime1.getHours() + 1);
    }
    const countdownElement1 = document.getElementById('countdown');
    let isReloading = false;
    let isWindowFocused = true; 
    const countdownTimer1 = setInterval(updateCountdown1, 1000);
    window.addEventListener('focus', function() {
        isWindowFocused = true;
    });
    window.addEventListener('blur', function() {
        isWindowFocused = false;
    });
    function updateCountdown1() {
        const remainingTime1 = Math.floor(((targetTime1 - new Date() + 2) / 1000));
        if (remainingTime1 < 0 && !isReloading && isWindowFocused) {
            clearInterval(countdownTimer1);
            isReloading = true;
            location.reload();
        } else if (remainingTime1 >= 0) {
            const minutes1 = Math.floor(remainingTime1 / 60);
            const seconds1 = remainingTime1 % 60;
            const countdownString1 = `${minutes1.toString().padStart(2, '0')} : ${seconds1.toString().padStart(2, '0')}`;
            countdownElement1.textContent = countdownString1;
        }
    }
});
document.addEventListener("DOMContentLoaded", function () {
    const targetHour = 0;
    let targetTime = new Date();
    targetTime.setUTCHours(targetHour, 0, 0, 0);
    targetTime.setUTCDate(targetTime.getUTCDate() + 1);
    const countdownTimer = setInterval(() => {
        const now = Date.now();
        const remainingTime = targetTime.getTime() - now;
        if (remainingTime <= 0) {
            clearInterval(countdownTimer);
            document.getElementById("DailyDealcountdown").innerHTML = "00:00:00";
        } else {
            const hours = Math.floor((remainingTime % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((remainingTime % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((remainingTime % (1000 * 60)) / 1000);
            const formattedTime = padZero(hours) + ":" + padZero(minutes) + ":" + padZero(seconds);
            document.getElementById("DailyDealcountdown").innerHTML = formattedTime;
        }
    }, 1000);
    function padZero(number) {
        return number.toString().padStart(2, "0");
    }
});
window.addEventListener('blur', function() {
    const video = document.querySelector('#background-video');
    video.pause();
    });
window.addEventListener('focus', function() {
const video = document.querySelector('#background-video');
video.play();
});

$(document).ready(function() {
$("#missionscountdown").hide();
$("#slideButton").click(function() {
    $("#missionscountdown").slideToggle(function() {
    if ($("#missionscountdown").is(":hidden")) {
        $("#slideButton").text("Show countdown");
    } else {
        $("#slideButton").text("Hide countdown");
    }
    });
});
});

$(document).ready(function() {
$("#DAILYDEAL").hide();
$("#dailydealbutton").click(function() {
    $("#DAILYDEAL").slideToggle(700, function() {
    if ($("#DAILYDEAL").is(":hidden")) {
        $("#dailydealbutton").text("Click here to see Daily Deal");
    } else {
        $("#dailydealbutton").text("Hide Daily Deal");
    }
    });
});
});

function toggleCollapse() {
    var current = document.getElementById("current");
    var upcoming = document.getElementById("upcoming");
    var currentButton = document.getElementById("currentButton");
    current.classList.toggle("collapsed");
    upcoming.classList.toggle("collapsed");
    if (current.classList.contains("collapsed")) {
        currentButton.textContent = "Click here to see current missions";
        document.title = "Upcoming Missions from the Hoxxes IV Mission Terminal";
    } else {
        currentButton.textContent = "Click here to see upcoming missions";
        document.title = "Current Missions from the Hoxxes IV Mission Terminal";
    }
};

function toggleBackground() {
    var video = document.getElementById("background-video");
    var backgroundbutton = document.getElementById('backgroundButton');
    var overlay = document.querySelector(".overlay");
    if (video.style.display === "none" && overlay.style.display === "none") {
        video.style.display = "block";
        overlay.style.display = "block";
        backgroundbutton.textContent = "Hide background";
        video.play();
    } else {
        video.style.display = "none";
        overlay.style.display = "none";
        backgroundbutton.textContent = "Show background";
        video.pause();
    }
};

function equalizeGridItems() {
if (window.matchMedia("(min-width: 1440px)").matches) {
    const gridItems = document.querySelectorAll('.biome-container');
    let maxHeight = 0;
    gridItems.forEach(item => {
    maxHeight = Math.max(maxHeight, item.offsetHeight);
    });
    gridItems.forEach(item => {
    item.style.height = `${maxHeight}px`;
    });
}
};

function toggleButtons() {
    var buttonsbutton = document.getElementById('buttonsbutton');
    var backgroundbutton = document.getElementById('backgroundButton');
    var slideButton = document.getElementById('slideButton');
    var currentButton = document.getElementById('currentButton');
    var missionscountdown = document.getElementById('missionscountdown');
    var DAILYDEAL = document.getElementById('DAILYDEAL');
    var dailydealbutton = document.getElementById('dailydealbutton');
    var DailyDealImg = document.getElementById('DailyDeal');
    if (slideButton.style.display === "none") {
        backgroundbutton.style.display = "inline-block";
        slideButton.style.display = "inline-block";
        currentButton.style.display = "inline-block";
        dailydealbutton.style.display = "inline-block";
        dailydealbutton.textContent = "Click here to see Daily Deal";
        DAILYDEAL.style.display = "none";
        missionscountdown.style.display = "none";
        buttonsbutton.textContent = " x ";
        $("#missionscountdown").slideToggle();
        $("#slideButton").text("Hide countdown");
    } else {
        missionscountdown.style.display = "none";
        backgroundbutton.style.display = "none";
        DAILYDEAL.style.display = "none";
        dailydealbutton.style.display = "none";
        slideButton.style.display = "none";
        currentButton.style.display = "none";
        buttonsbutton.textContent = "+";
    }
};

function onLoad() {
    const loadingElement = document.querySelector('p.loading');
    if (loadingElement) {
    loadingElement.style.display = 'none';
    }
    equalizeGridItems();
    var current = document.getElementById("current");
    current.classList.toggle("collapsed");
    toggleCollapse();
    $("#missionscountdown").slideToggle();
    var buttonsbutton = document.getElementById('buttonsbutton');
    buttonsbutton.setAttribute('onclick', 'toggleButtons()');
    var currentbutton = document.getElementById('currentButton');
    currentbutton.setAttribute('onclick', 'toggleCollapse()');
    var backgroundbutton = document.getElementById('backgroundButton');
    backgroundbutton.setAttribute('onclick', 'toggleBackground()');
};

window.addEventListener('load', function() {
    var upcoming = document.getElementById("upcoming");
    var current = document.getElementById('current');
    upcoming.style.visibility = 'visible';
    $(".biome-container").each(function() {
    $(this).css("opacity", "1");
    });
});
window.onload = onLoad;