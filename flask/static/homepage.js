function scrollToTop() {
    window.scrollTo(0, 0);
    }
$(document).ready(function() {
$('img').on('load', function() {
    scrollToTop();
});
scrollToTop();
});

function deepDiveCountDown() {
    let targetDay = 4;
    let targetHour = 11;
    let targetTime = new Date();
    let countdownTimer;
    
    function startCountdown(interval) {
        targetTime.setUTCHours(targetHour, 0, 0, 0);
        if (targetTime.getUTCDay() === targetDay && Date.now() > targetTime.getTime()) {
            targetTime.setUTCDate(targetTime.getUTCDate() + 7);
        }
        while (targetTime.getUTCDay() !== targetDay) {
            targetTime.setUTCDate(targetTime.getUTCDate() + 1);
        }
        countdownTimer = setInterval(updateCountdown, interval)
    }
    function updateCountdown() {
        let now;
        let remainingTime;
        if (initialized && !ddData) {
            remainingTime = 0;
            document.getElementById("ddcountdown").classList.add('glow-text');
        } else {
            now = Date.now();
            remainingTime = targetTime.getTime() - now;
            document.getElementById("ddcountdown").classList.remove('glow-text');
        }
        if (remainingTime <= 0) {
            clearInterval(countdownTimer);
            document.getElementById("ddcountdown").innerHTML = "0D 00:00:00";
            if (initialized) {
                refreshDeepDives().then(() => {
                    startCountdown(30000);
                });
            } else {
                startCountdown(1000);
            }
        } else {(0)
            let days = Math.floor(remainingTime / (1000 * 60 * 60 * 24));
            let hours = Math.floor((remainingTime % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            let minutes = Math.floor((remainingTime % (1000 * 60 * 60)) / (1000 * 60));
            let seconds = Math.floor((remainingTime % (1000 * 60)) / 1000);
            let formattedTime = formatTime(days, hours, minutes, seconds);
            document.getElementById("ddcountdown").innerHTML = formattedTime;
        }
    }
    function formatTime(days, hours, minutes, seconds) {
        return `${days}:${formatNumber(hours)}:${formatNumber(minutes)}:${formatNumber(seconds)}`;
    }

    function formatNumber(number) {
        return number.toString().padStart(2, "0");
    }
    startCountdown(1000);
}

function topMissionsCountdown() {
    let countdownElement = document.getElementById('countdown');
    let countdownTimer;
    let targetTime = new Date();
    
    function startCountdown() {
        targetTime.setSeconds(0);
        targetTime.setMilliseconds(0);
        if (targetTime.getMinutes() < 30) {
            targetTime.setMinutes(30);
        } else {
            targetTime.setMinutes(0);
            targetTime.setHours(targetTime.getHours() + 1);
        }
        countdownTimer = setInterval(updateCountdown, 1000);
    }
    function updateCountdown() {
        let remainingTime = Math.floor(((targetTime - new Date() + 2) / 1000));
        if (remainingTime < 0) {
            clearInterval(countdownTimer);
            if (initialized) {
                let loading = document.querySelector('p.loading')
                loading.style.display = 'inline-block';
                $(".biome-container").each(function() {
                    $(this).css("opacity", "0");
                    });
                refreshBiomes().then(startCountdown);
                $(".biome-container").each(function() {
                    $(this).css("opacity", "1");
                    });
                loading.style.display = 'none';
            } else {
                startCountdown();
            };
        } else if (remainingTime >= 0) {
            let minutes = Math.floor(remainingTime / 60);
            let seconds = remainingTime % 60;
            let countdownString = `${minutes.toString().padStart(2, '0')} : ${seconds.toString().padStart(2, '0')}`;
            countdownElement.textContent = countdownString;
        }
    }
    startCountdown();
};
function topDailyDealCountdown() {
    let targetHour = 0;
    let targetTime = new Date();
    let countdownTimer;

    function startCountdown() {
        targetTime.setUTCHours(targetHour, 0, 0, 0);
        targetTime.setUTCDate(targetTime.getUTCDate() + 1);
        countdownTimer = setInterval(updateCountdown, 1000)
    }
    function updateCountdown() {
        let now = Date.now();
        let remainingTime = targetTime.getTime() - now;
        if (remainingTime <= 0) {
            clearInterval(countdownTimer);
            if (initialized) {
                refreshDailyDeal().then(startCountdown);
            } else {
                startCountdown();
            }
        } else {
            let hours = Math.floor((remainingTime % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            let minutes = Math.floor((remainingTime % (1000 * 60 * 60)) / (1000 * 60));
            let seconds = Math.floor((remainingTime % (1000 * 60)) / 1000);
            let formattedTime = padZero(hours) + ":" + padZero(minutes) + ":" + padZero(seconds);
            document.getElementById("DailyDealcountdown").innerHTML = formattedTime;
        }
    }
    function padZero(number) {
        return number.toString().padStart(2, "0");
    }
    startCountdown();
};
window.addEventListener('blur', function() {
    document.querySelector('#background-video').pause();
    ;
    });
window.addEventListener('focus', function() {
document.querySelector('#background-video').play();
});

$(document).ready(function() {
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
    maxHeight = Math.max(maxHeight, item.offsetHeight) - 2;
    });
    gridItems.forEach(item => {
    item.style.height = `${maxHeight}px`;
    });
}
};

function toggleButtons() {
    let buttonsbutton = document.getElementById('buttonsbutton');
    let backgroundbutton = document.getElementById('backgroundButton');
    let slideButton = document.getElementById('slideButton');
    let currentButton = document.getElementById('currentButton');
    let missionscountdown = document.getElementById('missionscountdown');
    let DAILYDEAL = document.getElementById('DAILYDEAL');
    let dailydealbutton = document.getElementById('dailydealbutton');
    let seasonBox = document.getElementById('season')

    if (slideButton.style.display === "none") {
        backgroundbutton.style.display = "inline-block";
        slideButton.style.display = "inline-block";
        currentButton.style.display = "inline-block";
        dailydealbutton.style.display = "inline-block";
        dailydealbutton.textContent = "Click here to see Daily Deal";
        DAILYDEAL.style.display = "none";
        seasonBox.style.display = "inline-block";
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
        seasonBox.style.display = "none";
        buttonsbutton.textContent = "+";
    }
};

function onLoad() {
    arrayBiomes(biomes, 's0');
    arrayDailyDeal(dailyDeal);
    arrayDeepDives(ddData);
    initialized = true

    document.querySelector('p.loading').style.display = 'none';
    equalizeGridItems();
    document.getElementById("current").classList.toggle("collapsed");
    toggleCollapse();
    document.getElementById("upcoming").style.visibility = 'visible';

    topDailyDealCountdown()
    topMissionsCountdown()
    deepDiveCountDown()

    $(".biome-container").each(function() {
    $(this).css("opacity", "1");
    });
    $("#missionscountdown").slideToggle();

    document.getElementById('buttonsbutton').setAttribute('onclick', 'toggleButtons()');
    document.getElementById('season').setAttribute('onchange', 'changeSeason(biomes, this.value)');
    document.getElementById('currentButton').setAttribute('onclick', 'toggleCollapse()');
    document.getElementById('backgroundButton').setAttribute('onclick', 'toggleBackground()');
};