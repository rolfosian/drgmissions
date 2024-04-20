function scrollToTop() {
    window.scrollTo(0, 0);
    }
$(document).ready(function() {
$('img').on('load', function() {
    scrollToTop();
});
scrollToTop();
});

async function deepDiveCountDown() {
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
        if (!deepDiveData) {
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
            refreshDeepDives().then(() => {
                startCountdown(30000);
            });
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
    let isMidnightUpcoming_;

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

    function dispatchCacheEvent(isMidnightUpcoming_, date_) {
        let upcomingBiomeCacheEvent = new Event('upcomingBiomeCache');
        let date__ = new Date(date_)
        upcomingBiomeCacheEvent.isMidnightUpcoming = isMidnightUpcoming_;
        upcomingBiomeCacheEvent.date = date__;
        document.dispatchEvent(upcomingBiomeCacheEvent);
    }

    function updateCountdown() {
        let date_ = new Date();
        let remainingTime = Math.floor(((targetTime - date_ + 2) / 1000));
        if (remainingTime >= 0){
            isMidnightUpcoming_ = isMidnightUpcoming(date_);
        }
        if (remainingTime < 60 && !cacheActive && remainingTime > 0) {
            cacheActive = true;
            dispatchCacheEvent(isMidnightUpcoming_, date_)
        }
        if (remainingTime < 0 && !isRefreshing) {
            isRefreshing = true
            if (!cacheActive) {
                cacheActive = true;
                dispatchCacheEvent(isMidnightUpcoming_, date_)
            }
            clearInterval(countdownTimer);
            let refreshBiomesEvent = new Event('refreshBiomes');
            refreshBiomesEvent.isMidnightUpcoming = isMidnightUpcoming_;
            document.dispatchEvent(refreshBiomesEvent);
        } else if (remainingTime >= 0) {
            let minutes = Math.floor(remainingTime / 60);
            let seconds = remainingTime % 60;
            let countdownString = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
            countdownElement.textContent = countdownString;
        }
    }

    document.addEventListener('upcomingBiomeCache', async function(event) {
        tempCacheUpcomingBiomes(event.isMidnightUpcoming, event.date)
    });
    
    document.addEventListener('refreshBiomes', async function(event) {
        while (!tempBiomes) {
            await sleep(1);
        }
        startCountdown();
        await refreshBiomes(event.isMidnightUpcoming)
        cacheActive = false;
        isRefreshing = false;
    });

    startCountdown();
}

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
        let date = new Date()
        let now = date.getTime();
        let remainingTime = targetTime.getTime() - now;
        if (remainingTime <= 0) {
            clearInterval(countdownTimer);
            let event = new Event('refreshDailyDeal')
            event.dateString = date.toISOString().slice(0, 10)
            document.dispatchEvent(event)
        }
            let hours = Math.floor((remainingTime % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            let minutes = Math.floor((remainingTime % (1000 * 60 * 60)) / (1000 * 60));
            let seconds = Math.floor((remainingTime % (1000 * 60)) / 1000);
            let formattedTime = padZero(hours) + ":" + padZero(minutes) + ":" + padZero(seconds);
            document.getElementById("DailyDealcountdown").innerHTML = formattedTime;
        }
    
    function padZero(number) {
        return number.toString().padStart(2, "0");
    }

    document.addEventListener('refreshDailyDeal', async function(event) {
        while (localStorages['currentDaysJson'][0] != event.dateString) {
            await sleep(1);
        }
        await refreshDailyDeal();
        startCountdown();
    });


    startCountdown();
};

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
    equalizeGridItems()
};

async function onLoad() {
    arrayBiomes(biomes, localStorages['seasonSelected']);
    if (tempDailyDeal) {
        arrayDailyDeal(tempDailyDeal);
        tempDailyDeal = undefined;
    } else {
        arrayDailyDeal(dailyDeal);
    }

    document.querySelector('p.loading').style.display = 'none';
    document.getElementById("current").classList.toggle("collapsed");
    toggleCollapse();
    document.getElementById("upcoming").style.visibility = 'visible';
    initialized = true

    setupIdleVideoPause('background-video', 180000)
    topDailyDealCountdown()
    topMissionsCountdown()
    deepDiveCountDown()

    // let season = document.getElementById('season');
    // season.setAttribute('onchange', 'changeSeason(biomes, this.value)');
    // season.disabled = false;
    season.setAttribute('onchange', "toggleSeason4(biomes, this.checked)");
    season.disabled = false;
    seasonClick = document.getElementById('seasonClick')
    seasonClick.setAttribute('onclick', "document.getElementById('season').click()");
    seasonClick.disabled = false;

    $(".biome-container").each(function() {
    $(this).css("opacity", "1");
    });
    if (!localStorages['areButtonsHidden']) {
        $("#missionscountdown").slideToggle();
    }

    let buttonsButton = document.getElementById('buttonsbutton');
    buttonsButton.setAttribute('onclick', 'toggleButtons()');
    buttonsButton.disabled = false;
    
    currentButton = document.getElementById('currentButton');
    currentButton.setAttribute('onclick', 'toggleCollapse()');
    currentButton.disabled = false;

    backgroundButton = document.getElementById('backgroundButton');
    backgroundButton.setAttribute('onclick', 'toggleBackground()');
    backgroundButton.disabled = false;
    // document.getElementById('loading').textContent = 'An error occured, please refresh the page.'

    try {
        deepDiveData = await getDeepDiveData()
        arrayDeepDives(deepDiveData);
    } catch {
        handleUnavailableDeepDiveData()
    }
    $(".dd-missions").each(function() {
        $(this).css("opacity", "1");
        });
};