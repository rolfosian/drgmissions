function scrollToTop() {
    window.scrollTo(0, 0);
    }
document.querySelectorAll('img').forEach((element)=> {
    element.style.opacity = "1";
});

async function deepDiveCountDown() {
    let targetDay = 4;
    let targetHour = 11;
    let targetTime = new Date();
    let countdownTimer;
    
    function startCountdown() {
        targetTime.setUTCHours(targetHour, 0, 0, 0);
        if (targetTime.getUTCDay() === targetDay && Date.now() > targetTime.getTime()) {
            targetTime.setUTCDate(targetTime.getUTCDate() + 7);
        }
        while (targetTime.getUTCDay() !== targetDay) {
            targetTime.setUTCDate(targetTime.getUTCDate() + 1);
        }
        countdownTimer = setInterval(updateCountdown)
    }

    function updateCountdown() {
        let now;
        let remainingTime;
        if (!deepDiveData) {
            remainingTime = 0;
            document.getElementById("ddCountdown").classList.add('glow-text-red-white');
        } else {
            now = Date.now();
            remainingTime = targetTime.getTime() - now;
            document.getElementById("ddCountdown").classList.remove('glow-text-red-white');
        }
        if (remainingTime <= 0) {
            clearInterval(countdownTimer);
            document.getElementById("ddCountdown").innerHTML = "0:00:00:00";
            refreshDeepDives().then(() => {
                startCountdown();
            });
        } else {(0)
            let days = Math.floor(remainingTime / (1000 * 60 * 60 * 24));
            let hours = Math.floor((remainingTime % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            let minutes = Math.floor((remainingTime % (1000 * 60 * 60)) / (1000 * 60));
            let seconds = Math.floor((remainingTime % (1000 * 60)) / 1000);
            let formattedTime = formatTime(days, hours, minutes, seconds);
            document.getElementById("ddCountdown").innerHTML = formattedTime;
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
    let countdownElement = document.getElementById('missionsCountdown');
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
        upcomingBiomeCacheEvent.isMidnightUpcoming = isMidnightUpcoming_;
        upcomingBiomeCacheEvent.date = date_;
        document.dispatchEvent(upcomingBiomeCacheEvent);
    }

    function updateCountdown() {
        let date_ = new Date();
        let remainingTime = Math.floor(((targetTime - date_ + 2) / 1000));
        if (remainingTime >= 0){
            isMidnightUpcoming_ = isMidnightUpcoming(date_);
        }
        if (remainingTime < 102 && !cacheActive && remainingTime > 0) {
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
    let isDailyDealRefreshing;

    function startCountdown() {
        targetTime.setUTCHours(targetHour, 0, 0, 0);
        targetTime.setUTCDate(targetTime.getUTCDate() + 1);
        countdownTimer = setInterval(updateCountdown, 1000)
    }
    function updateCountdown() {
        let date = new Date()
        let now = date.getTime();
        let remainingTime = targetTime.getTime() - now;
        if (remainingTime < 0 && !isDailyDealRefreshing) {
            isDailyDealRefreshing = true;
            clearInterval(countdownTimer);
            let event = new Event('refreshDailyDeal')
            event.dateString = date.toISOString().slice(0, 10)
            document.dispatchEvent(event)
        }
            let hours = Math.floor((remainingTime % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            let minutes = Math.floor((remainingTime % (1000 * 60 * 60)) / (1000 * 60));
            let seconds = Math.floor((remainingTime % (1000 * 60)) / 1000);
            let formattedTime = padZero(hours) + ":" + padZero(minutes) + ":" + padZero(seconds);
            document.getElementById("dailyDealCountdown").innerHTML = formattedTime;
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
        isDailyDealRefreshing = false;
    });

    startCountdown();
};

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

    setupIdleVideoPause('background-video', 10000)
    topDailyDealCountdown()
    topMissionsCountdown()

    // let season = document.getElementById('season');
    // season.setAttribute('onchange', 'changeSeason(biomes, this.value)');
    // season.disabled = false;
    season.setAttribute('onchange', "toggleSeason4(biomes, this.checked)");
    season.disabled = false;
    seasonClick = document.getElementById('seasonClick')
    seasonClick.setAttribute('onclick', "document.getElementById('season').click()");
    seasonClick.disabled = false;

    document.querySelectorAll('.biome-container').forEach((element)=> {
        element.style.opacity = "1";
    });

    let dailyDealButton = document.getElementById('dailyDealButton')
    dailyDealButton.setAttribute('onclick', "slideToggle('dailyDealMaster', 'dailyDealButton', ['Click here to see Daily Deal', 'Hide Daily Deal'])");
    slideToggle('dailyDealMaster', 'dailyDealButton', ['Click here to see Daily Deal', 'Hide Daily Deal'])
    dailyDealButton.disabled = false

    // setupMissionRotationCountdownSlideToggle = async () => {
    //     let missionRotationCountDownButton = document.getElementById('missionRotationSlideButton');
    //     missionRotationCountDownButton.setAttribute('onclick', `slideToggle('missionsCountdownMaster', 'missionRotationSlideButton', ['Show Countdown', 'Hide Countdown'])`);
    //     slideToggle('missionsCountdownMaster', 'missionRotationSlideButton', ['Show Countdown', 'Hide Countdown'])
    //     while (document.getElementById('missionsCountdown').textContent === '') {
    //         await sleep(1);
    //     }
    //     slideToggle('missionsCountdownMaster', 'missionRotationSlideButton', ['Show Countdown', 'Hide Countdown'])
    //     missionRotationCountDownButton.disabled = false;
    // }
    // setupMissionRotationCountdownSlideToggle().then(() => {
        let buttonsButton = document.getElementById('buttonsButton');
        buttonsButton.setAttribute('onclick', 'toggleButtons()');
        buttonsButton.disabled = false;
    // });
    
    currentButton = document.getElementById('currentButton');
    currentButton.setAttribute('onclick', 'toggleCollapse()');
    currentButton.disabled = false;

    backgroundButton = document.getElementById('backgroundButton');
    backgroundButton.setAttribute('onclick', 'toggleBackground()');
    backgroundButton.disabled = false;

    deepDiveData = await getDeepDiveData()
    if (deepDiveData) {
        arrayDeepDives(deepDiveData);
        document.querySelectorAll('.dd-missions').forEach((element)=> {
            element.style.opacity = "1";
        });
    } else {
        let deepDiveCountdownElement = document.getElementById("ddCountdown");
        deepDiveCountdownElement.classList.add('glow-text-red-white');
        deepDiveCountdownElement.innerHTML = "0:00:00:00";
        document.querySelectorAll('.dd-missions').forEach((element)=> {
            element.style.opacity = "1";
        });
        await handleUnavailableDeepDiveData();
    };
    deepDiveCountDown()
}