function isLocalStorageAvailable(){
    var test = 'test';
    try {
        localStorage.setItem(test, test);
        localStorage.removeItem(test);
        return true;
    } catch(e) {
        return false;
    }
}
const isLocalStorageAvailable_ = isLocalStorageAvailable()
function getDomainURL(){
    // var currentDomain = window.location.protocol + "//" + window.location.hostname;
    // if (window.location.port !== "") {
    //     currentDomain += ":" + window.location.port;
    // }
    let base = document.querySelector('base').href
    return base.slice(0, base.length-1);
}

domainURL = getDomainURL();

// caching parameters
var totalImages = 0;
var loadedImages = 0;

var biomeBanners = {
    'Crystalline Caverns': `${domainURL}/static/DeepDive_MissionBar_CrystalCaves.webp`,
    'Glacial Strata' : `${domainURL}/static/DeepDive_MissionBar_GlacialStrata.webp`,
    'Radioactive Exclusion Zone': `${domainURL}/static/DeepDive_MissionBar_Radioactive.webp`,
    'Fungus Bogs': `${domainURL}/static/DeepDive_MissionBar_FungusBogs.webp`,
    'Dense Biozone': `${domainURL}/static/DeepDive_MissionBar_LushDownpour.webp`,
    'Salt Pits': `${domainURL}/static/DeepDive_MissionBar_SaltPits.webp`,
    'Sandblasted Corridors': `${domainURL}/static/DeepDive_MissionBar_Sandblasted.webp`,
    'Magma Core': `${domainURL}/static/DeepDive_MissionBar_MagmaCore.webp`,
    'Azure Weald': `${domainURL}/static/DeepDive_MissionBar_AzureWeald.webp`,
    'Hollow Bough': `${domainURL}/static/DeepDive_MissionBar_HollowBough.webp`
}
totalImages += Object.keys(biomeBanners).length;
var biomeBannersImages = {};
biomeBannersImages.name = 'biomeBanners';

var deepDivesBanners = {
    'dd' : `${domainURL}/static/dd.webp`,
    'edd' : `${domainURL}/static/edd.webp`
};
totalImages += Object.keys(deepDivesBanners).length;
var deepDivesBannersImages = {};
deepDivesBannersImages.name = 'deepDivesBanners';

function setBiomeAndDeepDivesBanners() {
    let minerals = {
        'Crystalline Caverns': 'Abundant: Jadiz; Scarce: Bismor',
        'Glacial Strata' : "Abundant: Magnite; Scarce: Umanite",
        'Radioactive Exclusion Zone': 'Abundant: Umanite; Scarce: Enor Pearl',
        'Fungus Bogs': 'Abundant: Croppa; Scarce: Jadiz',
        'Dense Biozone': 'Abundant: Bismor; Scarce: Umanite',
        'Salt Pits': 'Abundant: Enor Pearl; Scarce: Bismor',
        'Sandblasted Corridors': 'Abundant: Enor Pearl; Scarce: Bismor',
        'Magma Core': 'Abundant: Magnite; Scarce: Croppa',
        'Azure Weald': 'Abundant: Croppa; Scarce: Umanite',
        'Hollow Bough': 'Abundant: Jadiz; Scarce: Bismor'
    }
    for (let biome in minerals) {
        biomeBannersImages[biome].title = minerals[biome];
        biomeBannersImages[biome].classList.add("banner");
        let imgCopy = new Image();
        imgCopy.src = biomeBannersImages[biome].src
        imgCopy.classList.add("banner");
        imgCopy.title = minerals[biome];

        let divs = document.querySelectorAll(`div[biome="${biome}"]`);
        divs[0].prepend(biomeBannersImages[biome]);
        divs[1].prepend(imgCopy)
    }

    for (let deepDive in deepDivesBannersImages) {
        let div = document.querySelector(`div[dd="${deepDive}"]`);
        deepDivesBannersImages[deepDive].classList.add('banner');
        div.prepend(deepDivesBannersImages[deepDive]);
    }
}

var primaryObjs = {
    'Mining Expedition': `${domainURL}/static/img/Mining_expedition_icon.webp`,
    'Egg Hunt': `${domainURL}/static/img/Egg_collection_icon.webp`,
    'On-Site Refining': `${domainURL}/static/img/Refining_icon.webp`,
    'Salvage Operation': `${domainURL}/static/img/Salvage_icon.webp`,
    'Escort Duty': `${domainURL}/static/img/Escort_icon.webp`,
    'Point Extraction': `${domainURL}/static/img/Point_extraction_icon.webp`,
    'Elimination': `${domainURL}/static/img/Elimination_icon.webp`,
    'Industrial Sabotage': `${domainURL}/static/img/Sabotage_icon.webp`,
    'Deep Scan' : `${domainURL}/static/img/Deep_scan_icon.webp`,
};
totalImages += Object.keys(primaryObjs).length;
var primaryObjsImages = {};
primaryObjsImages.name = 'primaryObjsImages';

var primaryObjResources = {
    'hexagon' : `${domainURL}/static/img/hexagon.webp`,
    'Mining Expedition': `${domainURL}/static/img/Morkite_icon.webp`,
    'Egg Hunt': `${domainURL}/static/img/Alien_egg_icon.webp`,
    'On-Site Refining': `${domainURL}/static/img/Icon_PumpingJack_Core_Simplified_Workfile.webp`,
    'Salvage Operation': `${domainURL}/static/img/Icon_Salvage_Mules_Objective.webp`,
    'Escort Duty': `${domainURL}/static/img/Icon_FuelCannister_Simplified.webp`,
    'Point Extraction': `${domainURL}/static/img/Icons_Resources_Outline_Aquarq.webp`,
    'Elimination': `${domainURL}/static/img/Kill_Dreadnought_Objective_icon.webp`,
    'Industrial Sabotage': `${domainURL}/static/img/Icon_Facility_DataRack.webp`,
    'Deep Scan' : `${domainURL}/static/img/Icons_Resources_Detailed_Outline_ResonanceScannerPod.webp`
};
totalImages += Object.keys(primaryObjResources).length;
var primaryObjResourcesImages = {};
primaryObjResourcesImages.name = 'primaryObjResourcesImages';

var secondaryObjs = {
    'ApocaBlooms': `${domainURL}/static/img/ApocaBlooms_icon.webp`,
    'Fossils': `${domainURL}/static/img/Fossils_icon.webp`,
    'Boolo Caps': `${domainURL}/static/img/Boolo_Caps_icon.webp`,
    'Dystrum': `${domainURL}/static/img/Dystrum_icon.webp`,
    'Ebonuts': `${domainURL}/static/img/Ebonuts_icon.webp`,
    'Fester Fleas': `${domainURL}/static/img/Fester_Fleas_icon.webp`,
    'Gunk Seeds': `${domainURL}/static/img/Gunk_Seeds_icon.webp`,
    'Hollomite': `${domainURL}/static/img/Hollomite_icon.webp`,
    'Exterminate Bha Barnacles' : `${domainURL}/static/img/Exterminate_Bha_Barnacles_icon.webp`,
    'Exterminate Glyphid Eggs' : `${domainURL}/static/img/Exterminate_Glyphid_Eggs_icon.webp`,
};
totalImages += Object.keys(secondaryObjs).length;
var secondaryObjsImages = {};
secondaryObjsImages.name = 'secondaryObjsImages';

var complexities = {
    '1': `${domainURL}/static/img/Icons_complexity_1.webp`,
    '2': `${domainURL}/static/img/Icons_complexity_2.webp`,
    '3': `${domainURL}/static/img/Icons_complexity_3.webp`
};
totalImages += Object.keys(complexities).length;
var complexitiesImages = {};
complexitiesImages.name = 'complexitiesImages';

var lengths = {
    '1': `${domainURL}/static/img/Icons_length_1.webp`,
    '2': `${domainURL}/static/img/Icons_length_2.webp`,
    '3': `${domainURL}/static/img/Icons_length_3.webp`
};
totalImages += Object.keys(lengths).length;
var lengthsImages = {};
lengthsImages.name = 'lengthsImages';

var mutators = {
    'Critical Weakness': `${domainURL}/static/img/Mutator_critical_weakness_icon.webp`,
    'Gold Rush': `${domainURL}/static/img/Mutator_gold_rush_icon.webp`,
    'Double XP': `${domainURL}/static/img/Mutator_triple_xp_icon.webp`,
    'Golden Bugs': `${domainURL}/static/img/Mutator_golden_bugs_icon.webp`,
    'Low Gravity': `${domainURL}/static/img/Mutator_no_fall_damage_icon.webp`,
    'Mineral Mania': `${domainURL}/static/img/Mutator_mineral_mania_icon.webp`,
    'Rich Atmosphere': `${domainURL}/static/img/Mutator_rich_atmosphere_icon.webp`,
    'Volatile Guts': `${domainURL}/static/img/Mutator_volatile_guts_icon.webp`,
    'Blood Sugar' : `${domainURL}/static/img/Mutator_blood_sugar_icon.webp`,
    'Secret Secondary' : `${domainURL}/static/img/Mutator_secret_secondary_icon.webp`
};
totalImages += Object.keys(mutators).length;
var mutatorsImages = {};
mutatorsImages.name = 'mutatorsImages';

var warnings = {
    'Cave Leech Cluster': `${domainURL}/static/img/Warning_cave_leech_cluster_icon.webp`,
    'Exploder Infestation': `${domainURL}/static/img/Warning_exploder_infestation_icon.webp`,
    'Haunted Cave': `${domainURL}/static/img/Warning_haunted_cave_icon.webp`,
    'Lethal Enemies': `${domainURL}/static/img/Warning_lethal_enemies_icon.webp`,
    'Low Oxygen': `${domainURL}/static/img/Warning_low_oxygen_icon.webp`,
    'Mactera Plague': `${domainURL}/static/img/Warning_mactera_plague_icon.webp`,
    'Parasites': `${domainURL}/static/img/Warning_parasites_icon.webp`,
    'Regenerative Bugs': `${domainURL}/static/img/Warning_regenerative_bugs_icon.webp`,
    'Shield Disruption': `${domainURL}/static/img/Warning_shield_disruption_icon.webp`,
    'Elite Threat': `${domainURL}/static/img/Warning_elite_threat_icon.webp`,
    'Swarmageddon': `${domainURL}/static/img/Warning_swarmageddon_icon.webp`,
    'Lithophage Outbreak': `${domainURL}/static/img/Warning_lithophage_outbreak_icon.webp`,
    'Rival Presence': `${domainURL}/static/img/Warning_rival_presence_icon.webp`,
    'Duck and Cover': `${domainURL}/static/img/Warning_duck_and_cover_icon.webp`,
    'Ebonite Outbreak' : `${domainURL}/static/img/Warning_ebonite_outbreak_icon.webp`,
};
totalImages += Object.keys(warnings).length;
var warningsImages = {};
warningsImages.name = 'warningsImages';

var secondaryObjsDD = {
    "Repair Minimules": `${domainURL}/static/img/Icon_Salvage_Mules_Objective_DDsecondaryobj.webp`,
    "Eliminate Dreadnought": `${domainURL}/static/img/Kill_Dreadnought_Objective_icon_DDsecondaryobj.webp`,
    "Mine Morkite": `${domainURL}/static/img/Morkite_icon_DDsecondaryobj.webp`,
    "Get Alien Eggs": `${domainURL}/static/img/Alien_egg_icon_DDsecondaryobj.webp`,
    "Black Box": `${domainURL}/static/img/Blackbox_icon_DDsecondaryobj.webp`
};
totalImages += Object.keys(secondaryObjsDD).length;
var secondaryObjsDDImages = {};
secondaryObjsDDImages.name = 'secondaryObjsDDImages';

var biomesDD = {
    'Crystalline Caverns': `${domainURL}/static/img/DeepDive_MissionBar_CrystalCaves.webp`,
    'Glacial Strata': `${domainURL}/static/img/DeepDive_MissionBar_GlacialStrata.webp`,
    'Radioactive Exclusion Zone': `${domainURL}/static/img/DeepDive_MissionBar_Radioactive.webp`,
    'Fungus Bogs': `${domainURL}/static/img/DeepDive_MissionBar_FungusBogs.webp`,
    'Dense Biozone': `${domainURL}/static/img/DeepDive_MissionBar_LushDownpour.webp`,
    'Salt Pits': `${domainURL}/static/img/DeepDive_MissionBar_SaltPits.webp`,
    'Sandblasted Corridors': `${domainURL}/static/img/DeepDive_MissionBar_Sandblasted.webp`,
    'Magma Core': `${domainURL}/static/img/DeepDive_MissionBar_MagmaCore.webp`,
    'Azure Weald': `${domainURL}/static/img/DeepDive_MissionBar_AzureWeald.webp`,
    'Hollow Bough': `${domainURL}/static/img/DeepDive_MissionBar_HollowBough.webp`
};
totalImages += Object.keys(biomesDD).length;
var biomesDDImages = {};
biomesDDImages.name = 'biomesDDImages';

var dailyDealResources = {
    'Bismor': `${domainURL}/static/img/Bismor_icon.webp`,
    'Croppa': `${domainURL}/static/img/Croppa_icon.webp`,
    'Enor Pearl': `${domainURL}/static/img/Enor_pearl_icon.webp`,
    'Jadiz': `${domainURL}/static/img/Jadiz_icon.webp`,
    'Magnite': `${domainURL}/static/img/Magnite_icon.webp`,
    'Umanite': `${domainURL}/static/img/Umanite_icon.webp`,
    'Credits': `${domainURL}/static/img/Credit.webp`,
    'Bubble': `${domainURL}/static/img/Icon_TradeTerminal_SaleBubble.webp`
};
totalImages += Object.keys(dailyDealResources).length;
var dailyDealResourcesImages = {};
dailyDealResourcesImages.name = 'dailyDealResourcesImages';

var fontNamesAndUrls = {
    'CarbonThin-W00-Regular' : `${domainURL}/static/img/CarbonThin-W00-Regular.woff2`,
    'CarbonBold-W00-Regular' : `${domainURL}/static/img/CarbonBold-W00-Regular.woff2`,
    'Bungee-Regular' : `${domainURL}/static/img/Bungee-Regular.woff2`,
    'RiftSoft-Regular' : `${domainURL}/static/img/RiftSoft-Regular.woff2`,
    'BebasNeue' : `${domainURL}/static/img/BebasNeue-Regular.woff2`
};

var base64LocalStoragesImg = {};
var base64LocalStoragesFonts = {};

function arrayBufferToBase64( buffer ) {
    var binary = '';
    var bytes = new Uint8Array( buffer );
    var len = bytes.byteLength;
    for (var i = 0; i < len; i++) {
        binary += String.fromCharCode( bytes[ i ] );
    }
    return window.btoa( binary );
}
function base64ToArrayBuffer(base64_string) {
    return Uint8Array.from(atob(base64_string), c => c.charCodeAt(0)).buffer;
}
async function fetchBinaryData(key, url) {
    const response = await fetch(url);
    const blob = await response.blob();
    const arrayBuffer = await blob.arrayBuffer();
    return [key, arrayBuffer];
   }

async function preloadImages(imageObj, imageCache) {
    let promises = [];
    base64LocalStoragesImg[imageCache.name] = {};

    for (let key in imageObj) {
        let promisedBinary = fetchBinaryData(key, imageObj[key]);
        promises.push(promisedBinary);
    }
    let promisedBinaries = await Promise.all(promises);

    for (let i = 0; i < promisedBinaries.length; i++) {
        let promisedBinary = promisedBinaries[i];
        key = promisedBinary[0];
        let base64Data = arrayBufferToBase64(promisedBinary[1]);
        base64LocalStoragesImg[imageCache.name][key] = base64Data;

        let img = new Image();
        img.src = "data:image/webp;base64," + base64Data;

        imageCache[key] = img;
        loadedImages++;
        let progress = (loadedImages / totalImages) * 100;
        document.querySelector('.loading').textContent = `Loading icons ${progress.toFixed(2)}%`;
    }

    delete imageCache.name;
    // imageObj = undefined;
}
async function loadImgsFromLocalStorageObj(imageObj, imageCache) {
    for (let key in imageObj) {
        let base64Data =  localStorages['img'][imageCache.name][key];

        let img = new Image();
        img.src = "data:image/webp;base64," + base64Data;

        imageCache[key] = img;
        loadedImages++;
        let progress = (loadedImages / totalImages) * 100;
        document.querySelector('.loading').textContent = `${progress.toFixed(2)}%`;
    }

    delete imageCache.name;
    // imageObj = undefined;
}

async function loadImgsFromLocalStorageAll() {
    document.querySelector('.loading').textContent = `Loading icons 0.00%`;
    await Promise.all([
        loadImgsFromLocalStorageObj(primaryObjs, primaryObjsImages),
        loadImgsFromLocalStorageObj(primaryObjResources, primaryObjResourcesImages),
        loadImgsFromLocalStorageObj(secondaryObjs, secondaryObjsImages),
        loadImgsFromLocalStorageObj(complexities, complexitiesImages),
        loadImgsFromLocalStorageObj(lengths, lengthsImages),
        loadImgsFromLocalStorageObj(mutators, mutatorsImages),
        loadImgsFromLocalStorageObj(warnings, warningsImages),
        loadImgsFromLocalStorageObj(secondaryObjsDD, secondaryObjsDDImages),
        loadImgsFromLocalStorageObj(biomesDD, biomesDDImages),
        loadImgsFromLocalStorageObj(biomeBanners, biomeBannersImages),
        loadImgsFromLocalStorageObj(deepDivesBanners, deepDivesBannersImages),
        loadImgsFromLocalStorageObj(dailyDealResources, dailyDealResourcesImages)
    ]);
    base64LocalStoragesImg = undefined;
}

async function preloadFonts(){
    document.querySelector('.loading').textContent = 'Loading fonts'
    let promises = [];
    let fontsBinaries;

    for (let fontName in fontNamesAndUrls) {
        let fontUrl = fontNamesAndUrls[fontName];
        let promisedBinary = fetchBinaryData(fontName, fontUrl);
        promises.push(promisedBinary);
    }

    fontsBinaries = await Promise.all(promises);

    for (let i = 0; i < fontsBinaries.length; i++) {
        let fontName = fontsBinaries[i][0];
        let fontBinaryData = fontsBinaries[i][1];

        base64Data = arrayBufferToBase64(fontBinaryData);
        base64LocalStoragesFonts[fontName] = base64Data;

        let fontFace = new FontFace(fontName, `url(data:font/woff2;base64,${base64Data})`);
        await fontFace.load();
        document.fonts.add(fontFace);
    }

    console.log('New fonts hash:', simpleHash(JSON.stringify(base64LocalStoragesFonts)))
    localStorage.setItem('fonts', JSON.stringify(base64LocalStoragesFonts));

    base64LocalStoragesFonts = undefined;
    fontNamesAndUrls = undefined;
}

async function preloadImagesAll() {
    document.querySelector('.loading').textContent = `Loading icons 0.00%`;
    await Promise.all([
        preloadImages(primaryObjs, primaryObjsImages),
        preloadImages(primaryObjResources, primaryObjResourcesImages),
        preloadImages(secondaryObjs, secondaryObjsImages),
        preloadImages(complexities, complexitiesImages),
        preloadImages(lengths, lengthsImages),
        preloadImages(mutators, mutatorsImages),
        preloadImages(warnings, warningsImages),
        preloadImages(secondaryObjsDD, secondaryObjsDDImages),
        preloadImages(biomesDD, biomesDDImages),
        preloadImages(dailyDealResources, dailyDealResourcesImages),
        preloadImages(biomeBanners, biomeBannersImages),
        preloadImages(deepDivesBanners, deepDivesBannersImages)
    ]);
    if (isLocalStorageAvailable_) {
        console.log('New img hash:', simpleHash(JSON.stringify(base64LocalStoragesImg)))
        localStorage.setItem('img', JSON.stringify(base64LocalStoragesImg));
    }
    base64LocalStoragesImg = undefined;
}

async function preloadHomepageScript() {
    let response = await fetch(`${domainURL}/static/homepage.js`);
    return response.text();
}

async function loadFontsFromLocalStorageObj() {
    for (let key in localStorages['fonts']) {
        let base64Data = localStorages['fonts'][key]
        let font = new FontFace(key, `url(data:font/woff2;base64,${base64Data})`);
        await font.load();
        document.fonts.add(font);
    }
}

async function preloadAll() {
    try {
        return await Promise.all([preloadImagesAll(), preloadFonts()])
    } catch {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                Promise.all([preloadImagesAll(), preloadFonts()])
                    .then(() => resolve())
                    .catch(() => preloadAll().then(() => resolve()));
            }, 2000);
        });
    }
}

function inList(myList, itemToCheck) {
    return myList.indexOf(itemToCheck) !== -1;
}

function replaceCharactersAtIndices(inputString, replacements) {
    let result = inputString;
    replacements.forEach(([index, newCharacter]) => {
        if (index >= 0 && index < inputString.length) {
            result = result.substring(0, index) + newCharacter + result.substring(index + 1);
        }
    });
    return result;
}

function getCurrentDateMidnightUTC() {
    var now = new Date();

    var utcYear = now.getUTCFullYear();
    var utcMonth = ('0' + (now.getUTCMonth() + 1)).slice(-2);
    var utcDay = ('0' + now.getUTCDate()).slice(-2);
    var utcHours = '00';
    var utcMinutes = '00';
    var utcSeconds = '00';

    var formattedUTCDateTime = utcYear + '-' +
                               utcMonth + '-' +
                               utcDay + 'T' +
                               utcHours + ':' +
                               utcMinutes + ':' +
                               utcSeconds + 'Z';
    return formattedUTCDateTime;
}

function getNextDateMidnightUTC(date) {
    let now = new Date(date)
    now.setUTCDate(now.getUTCDate()+1);

    let utcYear = now.getUTCFullYear();
    let utcMonth = ('0' + (now.getUTCMonth() + 1)).slice(-2);
    let utcDay = ('0' + now.getUTCDate()).slice(-2);
    let utcHours = '00';
    let utcMinutes = '00';
    let utcSeconds = '00';

    var formattedUTCDateTime = utcYear + '-' +
        utcMonth + '-' +
        utcDay + 'T' +
        utcHours + ':' +
        utcMinutes + ':' +
        utcSeconds + 'Z';
    return formattedUTCDateTime;
}

function getCurrentDateTimeUTC() {
    var now = new Date();

    var utcYear = now.getUTCFullYear();
    var utcMonth = ('0' + (now.getUTCMonth() + 1)).slice(-2);
    var utcDay = ('0' + now.getUTCDate()).slice(-2);
    var utcHours = ('0' + now.getUTCHours()).slice(-2);
    var utcMinutes = ('0' + now.getUTCMinutes()).slice(-2);
    var utcSeconds = ('0' + now.getUTCSeconds()).slice(-2);

    var formattedUTCDateTime = utcYear + '-' +
                               utcMonth + '-' +
                               utcDay + 'T' +
                               utcHours + ':' +
                               utcMinutes + ':' +
                               utcSeconds + 'Z';
    return formattedUTCDateTime;
}

function incrementTime(direction, datetimeString, numberOfIncrements = 1) {
    if (direction === 'up') {
        for (let i = 0; i < numberOfIncrements; i++) {
            datetimeString = roundTimeUp(datetimeString);
        }
        return datetimeString;
    } else if (direction === 'down') {
        for (let i = 0; i < numberOfIncrements; i++) {
            datetimeString = roundTimeDown(datetimeString);
        }
        return datetimeString;
    } else {
        throw new Error('Invalid direction. Please use "up" or "down".');
    }
}

function roundTimeUpNextUpcoming(datetimestring) {
    return roundTimeUp(roundTimeUp(datetimestring));
}

function roundTimeUp(datetimeString) {
    const currentTime = new Date(datetimeString);
    const currentTimeMinutes = currentTime.getUTCMinutes();

    let lastMark = new Date(currentTime);
    let nextMark = new Date(currentTime);
    let secondsSinceLastMark, secondsToNextMark;

    if (currentTimeMinutes >= 30) {
        lastMark.setUTCMinutes(30);
        nextMark.setUTCMinutes(0);
        nextMark.setUTCHours(nextMark.getUTCHours() + 1);
    } else {
        lastMark.setUTCMinutes(0);
        nextMark.setUTCMinutes(30);
    }

    secondsSinceLastMark = (currentTime - lastMark) / 1000;
    secondsToNextMark = (nextMark - currentTime) / 1000;

    const roundedTime = new Date(currentTime.getTime() + secondsToNextMark * 1000);
    roundedTime.setSeconds(0);
    roundedTime.setMilliseconds(0);
    const roundedTimeStr = roundedTime.toISOString().slice(0,19)+'Z';
    return roundedTimeStr;
}

function getCurrentDateTimeUTC_UNIX() {
    return Math.floor(new Date(getCurrentDateTimeUTC()).getTime() / 1000);
}

function roundTimeDown(datetimeString) {
    var datetimeMinutes = parseInt(datetimeString.slice(14, 16));
    if (datetimeMinutes >= 30) {
        var newDatetime = datetimeString.slice(0, 14) + '30:00Z';
    } else {
        var newDatetime = datetimeString.slice(0, 14) + '00:00Z';
    }
    return newDatetime;
}

function getTomorrowDate(date) {

    var tomorrow = new Date(date);
    tomorrow.setDate(date.getDate() + 1);

    var year = tomorrow.getFullYear();
    var month = tomorrow.getMonth() + 1;
    var day = tomorrow.getDate();

    var formattedTomorrow = year + '-' + (month < 10 ? '0' : '') + month + '-' + (day < 10 ? '0' : '') + day;

    return formattedTomorrow;
}

async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
async function waitRotation() {
    const targetMinutes59 = [29, 59];
    while (true) {
        const currentDate = new Date();
        const currentMinute = currentDate.getMinutes();
        const currentSecond = currentDate.getSeconds() + currentDate.getMilliseconds() / 1000;
        if (currentSecond > 58.50 && inList(targetMinutes59, currentMinute)) {
            await sleep(1500);
            continue
        }
        break
    }
}
function padZero(number) {
    return number.toString().padStart(2, "0");
}
function getMissionsRemainderTimeOnInit(date) {
    let targetTime = new Date(roundTimeUp(date))
    let remainingTime = (targetTime - date)

    let minutes = Math.floor((remainingTime % (1000 * 60 * 60)) / (1000 * 60));
    let seconds = Math.floor((remainingTime % (1000 * 60)) / 1000);

    let formattedTime = padZero(minutes) + ":" + padZero(seconds);
    return formattedTime
}
async function loadJSONnoRetry(filePath) {
    try {
      const response = await fetch(filePath);
      const data = await response.json();
      return data;
    } catch (error) {
      throw error;
    }
}

async function loadJSON(filePath, maxRetries = 3, retryDelay = 5000 ) {
    let retries = 0;
    while (retries < maxRetries) {
        try {
            const response = await fetch(filePath);
            const data = await response.json();
            return data;
        } catch (error) {
            retries++;
            await new Promise(resolve => setTimeout(resolve, retryDelay));
        }
    }
    throw new Error(`Failed to load JSON data from ${filePath} after ${maxRetries} attempts.`);
}

function getPreviousThursdayTimestamp() {
    var currentDate = new Date();

    if (currentDate.getUTCDay() === 4 && currentDate.getUTCHours() < 11) {
        currentDate.setUTCDate(currentDate.getUTCDate() - 7);
    }

    var difference = (currentDate.getUTCDay() + 7 - 4) % 7;
    var previousThursday = new Date(currentDate);
    previousThursday.setUTCDate(previousThursday.getUTCDate() - difference);
    previousThursday.setUTCHours(11, 0, 0, 0);

    var isoTimestamp = previousThursday.toISOString();
    var timestamp = isoTimestamp.slice(0, 19) + "Z";

    return timestamp;
}

function getCurrentMissionData() {
    const datetime = roundTimeDown(getCurrentDateTimeUTC());
    return localStorages['currentDaysJson'][1][datetime];
}
function getUpcomingMissionData() {
    const datetime = roundTimeUp(getCurrentDateTimeUTC());
    return localStorages['currentDaysJson'][1][datetime];
}
function verifyDeepDiveData(data) {
    try {
        for (let deepDive in data['Deep Dives']) {
            let stages = data['Deep Dives'][deepDive]['Stages'];

            for (let i = 0; i < stages.length; i++) {
                let stage = stages[i];
                if (stage['Complexity'] === 'Indefinite' || stage['Length'] === 'Indefinite') {
                    return false;
                }
            }
        }
        return true;
    } catch {
        return false;
    }
}
async function getDeepDiveData() {
    let datetime = getPreviousThursdayTimestamp();
    datetime = replaceCharactersAtIndices(datetime, [[13, '-'], [16,'-']]);
    let data;
    try {
        data = await loadJSONnoRetry(`${domainURL}/static/json/DD_${datetime}.json`);
        if (verifyDeepDiveData(data)) {
            return data;
        } else {
            return undefined;
        }
    } catch {
    }
    return data;
}

function renderMission(m_d) {
    const div = document.createElement('div');
    div.classList.add('mission-hover-zoom');
    div.classList.add('mission');
    div.id = m_d['CodeName'];

    const canvas = document.createElement('canvas');
    canvas.title = m_d["CodeName"];
    canvas.width = 350;
    canvas.height = 300;
    var ctx = canvas.getContext('2d');

    const primaryImg = primaryObjsImages[m_d['PrimaryObjective']];
    ctx.drawImage(primaryImg, 83, 58, primaryImg.width * 0.4, primaryImg.height * 0.4);

    const secondaryImg = secondaryObjsImages[m_d['SecondaryObjective']];
    ctx.drawImage(secondaryImg, -11, -21, secondaryImg.width * 0.6, secondaryImg.height * 0.6);

    if (m_d['MissionWarnings']) {
        let MissionWarnings = [];
        m_d['MissionWarnings'].forEach((warning) => {
            MissionWarnings.push(warning);
        });
        const MISSIONWARNING1 = warningsImages[MissionWarnings[0]];
        const scaledWidth = MISSIONWARNING1.width * 0.38;
        const scaledHeight = MISSIONWARNING1.height * 0.38;
        if (MissionWarnings.length === 1) {
            ctx.drawImage(MISSIONWARNING1, 227, 87, scaledWidth, scaledHeight);
        } else if (MissionWarnings.length === 2) {
            const MISSIONWARNING2 = warningsImages[MissionWarnings[1]];
            ctx.drawImage(MISSIONWARNING1, 227, 42, scaledWidth, scaledHeight);
            ctx.drawImage(MISSIONWARNING2, 227, 142, scaledWidth, scaledHeight);
        }
    }

    if (m_d['MissionMutator']) {
        const mutatorImg = mutatorsImages[m_d['MissionMutator']];
        ctx.drawImage(mutatorImg, 27, 92, mutatorImg.width * 0.38, mutatorImg.height * 0.38);
    }

    const complexityImg = complexitiesImages[m_d['Complexity']];
    ctx.drawImage(complexityImg, 107, 2, complexityImg.width * 0.45, complexityImg.height * 0.45);

    const lengthImg = lengthsImages[m_d['Length']];
    ctx.drawImage(lengthImg, 107, 242, lengthImg.width * 0.45, lengthImg.height * 0.45);

    const values_resource = {
        'Mining Expedition,1,1': '200',
        'Mining Expedition,1,2': '225',
        'Mining Expedition,2,2': '250',
        'Mining Expedition,2,3': '325',
        'Mining Expedition,3,3': '400',
        'Egg Hunt,1': '4',
        'Egg Hunt,2': '6',
        'Egg Hunt,default': '8',
        'Point Extraction,2': '7',
        'Point Extraction,default': '10',
        'Industrial Sabotage,default': '1',
        'On-Site Refining,default': '3',
        'Escort Duty,2': '1',
        'Escort Duty,default': '2',
        'Elimination,2': '2',
        'Elimination,default': '3',
        'Salvage Operation,2': '2',
        'Salvage Operation,default': '3',
        'Deep Scan,2,1' : '3',
        'Deep Scan,3,2' : '5',
    };

    const hexagon = primaryObjResourcesImages['hexagon']
    ctx.drawImage(hexagon, 15, 190, hexagon.width * 0.32, hexagon.height * 0.32);
    drawResource(m_d['PrimaryObjective'], m_d['Complexity'], m_d['Length']);


    function drawResource() {
        const resource = primaryObjResourcesImages[m_d['PrimaryObjective']];
        let scaleFactor;
        if (m_d['PrimaryObjective'] === 'Mining Expedition') scaleFactor = 0.18;
        else if (m_d['PrimaryObjective'] === 'Egg Hunt') scaleFactor = 0.20;
        else scaleFactor = 0.1;

        ctx.drawImage(resource, 38, 205, resource.width * scaleFactor, resource.height * scaleFactor);

        const text = getText(m_d['PrimaryObjective'], m_d['Complexity'], m_d['Length']);
        drawText(text, 'CarbonBold-W00-Regular', '35',  m_d['PrimaryObjective']);
    }

    function getText(primaryObj, complexity, length) {
        return values_resource[`${primaryObj},${length}`] ||
            values_resource[`${primaryObj},${complexity},${length}`] ||
            values_resource[`${primaryObj},${complexity},default`] ||
            values_resource[`${primaryObj},default`];
    }

    function drawText(text, font, fontSize, primaryObj) {
        ctx.font = `${fontSize}px ${font}`;
        ctx.fillStyle = 'white';
        ctx.textAlign = 'center';
        var y = 280
        if (primaryObj == 'Mining Expedition') y -= 5
        ctx.fillText(text, 63, y);
    }
    ctx.save();

    resizeCanvas(div, canvas, 0.35, 0.35)
    div.appendChild(canvas)
    return div;
}

function resizeCanvas(div, canvas, x, y) {
    const newWidth = canvas.width * x;
    const newHeight = canvas.height * y;

    canvas.style.width = `${newWidth.toString()}px`;
    canvas.style.height = `${newHeight.toString()}px`;
    div.style.width = `${newWidth.toString()}px`;
    div.style.height = `${newHeight.toString()}px`;
}

function renderBiomes_(dictionary) {
    let renderedBiomes = {};

    for (var season in dictionary) {
        var Biomes = dictionary[season]['Biomes'];
        renderedBiomes[season] = {};
        renderedBiomes[season]['Biomes'] = {};

        for (let biome in Biomes) {
            let biomeMissions = Biomes[biome];
            let biome1 = [];

            for (let i = 0; i < biomeMissions.length; i++) {
                let mission = biomeMissions[i];
                let mission1 = {};

                mission1['CodeName'] = mission['CodeName'];
                mission1['id'] = mission['id'];

                let mission_icon_canvas_div = renderMission(mission);
                mission1['rendered_mission'] = mission_icon_canvas_div;

                biome1.push(mission1);
            }

            renderedBiomes[season]['Biomes'][biome] = biome1;
        };
    };

    return renderedBiomes;
}
function renderBiomesFlat(dictionary) {
    let renderedBiomes = {};
    var Biomes = dictionary['Biomes'];
    renderedBiomes['Biomes'] = {};
    renderedBiomes['timestamp'] = dictionary['timestamp'];

    for (let biome in Biomes) {
        let biomeMissions = Biomes[biome];
        let biome1 = [];

        for (let i = 0; i < biomeMissions.length; i++) {
            let mission = biomeMissions[i];
            let mission1 = {};

            if (mission.hasOwnProperty('season_modified')) {
                mission1['season_modified'] = {};
                for (let season in mission['season_modified']) {
                    let modifiedMission = mission['season_modified'][season];
                    mission1['season_modified'][season] = {};
                    mission1['season_modified'][season]['CodeName'] = modifiedMission['CodeName'];
                    mission1['season_modified'][season]['id'] = modifiedMission['id'];
                    mission1['season_modified'][season]['season'] = modifiedMission['season'];
                    let mission_icon_canvas_div = renderMission(modifiedMission);
                    mission1['season_modified'][season]['rendered_mission'] = mission_icon_canvas_div;
                }
            }

            mission1['CodeName'] = mission['CodeName'];
            mission1['id'] = mission['id'];
            mission1['season'] = mission['season'];

            let mission_icon_canvas_div = renderMission(mission);
            mission1['rendered_mission'] = mission_icon_canvas_div;

            biome1.push(mission1);
        }
        renderedBiomes['Biomes'][biome] = biome1;
    };
    return renderedBiomes;
}
function renderBiomes(dictionary) {
    let bs;
    if (dictionary.hasOwnProperty('s0')) {
        bs = renderBiomes_(dictionary);
        // console.log(bs['timestamp']);
        return bs;
    } else {
        bs =  renderBiomesFlat(dictionary);
        // console.log(bs['timestamp']);
        return bs;
    }
}

function isMidnightUpcoming(date) {
    return roundTimeDown(date.toISOString()).slice(11, 19) == '23:30:00'
}

async function tempCacheUpcomingBiomes(isMidnightUpcoming_, date) {
    let currentBiomes = biomes[1];
    let upcomingBiomes;

    switch (true) {
        case (isMidnightUpcoming_):
            if (tempCurrentDaysJson) {
                setStorages('currentDaysJson', tempCurrentDaysJson);
                tempCurrentDaysJson = undefined;

            } else {
                await getCurrentDaysJson(date, true);
            }

            upcomingBiomes = renderBiomes(localStorages['currentDaysJson'][1][roundTimeUpNextUpcoming(date.toISOString())]);
            break

        case (roundTimeDown(date.toISOString()).slice(11, 19) == '23:00:00'):
            let nextDay = getNextDateMidnightUTC(date).split('T')[0];
            tempCurrentDaysJson = [nextDay, await loadJSON(`${domainURL}/static/json/bulkmissions/${nextDay}.json`)];
            upcomingBiomes = renderBiomes(tempCurrentDaysJson[1][roundTimeUpNextUpcoming(date.toISOString())]);
            break

        default:
            upcomingBiomes = renderBiomes(localStorages['currentDaysJson'][1][roundTimeUpNextUpcoming(date.toISOString())]);
            break
    }

    tempBiomes = [currentBiomes, upcomingBiomes];
    // console.log('------')
    // console.log(tempBiomes)
    // console.log(date.toISOString())
}

function getBiomesOnInit() {
    let dictionary = getCurrentMissionData(localStorages['currentDaysJson'][1]);
    // console.log(localStorages['currentDaysJson'][1])
    let currentBiomes = renderBiomes(dictionary);
    let dictionary_ = getUpcomingMissionData(localStorages['currentDaysJson'][1]);
    let upcomingBiomes = renderBiomes(dictionary_);
    return [currentBiomes, upcomingBiomes];
}

async function getBiomesMidnightOnInit(date) {
    if (tempBiomes) {
        tempBiomes = undefined;
        tempCurrentDaysJson = undefined;
    }
    let upcomingMidnight = getNextDateMidnightUTC(date);
    let results = await getCurrentDaysJson(date, true);
    // console.log(results)
    let currentBiomes = renderBiomes(results[0][roundTimeDown(date.toISOString().slice(0, 19)+'Z')]);
    let upcomingBiomes = renderBiomes(localStorages['currentDaysJson'][1][upcomingMidnight]);
    return [currentBiomes, upcomingBiomes];
}

function getBiomes() {
    let currentBiomes = tempBiomes[0];
    let upcomingBiomes = tempBiomes[1];
    return [currentBiomes, upcomingBiomes];
}

async function getBiomesMidnight() {
    let currentBiomes = tempBiomes[0];
    if (tempCurrentDaysJson) {
        // console.log(tempCurrentDaysJson)
        setStorages('currentDaysJson', tempCurrentDaysJson);
        tempCurrentDaysJson = undefined;
    }
    let upcomingBiomes = tempBiomes[1];
    return [currentBiomes, upcomingBiomes];
}

function changeSeason(Biomes, season) {
    arrayBiomes(Biomes, season);
    if (document.getElementById('currentButton').textContent == 'Click here to see current missions') {
        document.getElementById('currentButton').click();
    }
    setStorages('seasonSelected', season);
}

function hasMidnightJustBeen(datestring) {
    return datestring.slice(11, 19) === '00:00:00';
}
function rolloverCurrentDaysJsonLink (currentDaysTimestamp) {
    let currentDaysJsonLink = document.getElementById('currentDaysJsonLink');
    currentDaysJsonLink.href = `${domainURL}/static/json/bulkmissions/${currentDaysTimestamp.slice(0, 10)}.json`;

    let tomorrowDaysJsonLink = document.getElementById('tomorrowDaysJsonLink');
    tomorrowDaysJsonLink.href = `${domainURL}/static/json/bulkmissions/${getNextDateMidnightUTC(currentDaysTimestamp).slice(0, 10)}.json`;
}
async function refreshBiomes(isMidnightUpcoming_) {
    let refreshDate = new Date();
    let refreshDateISOString = refreshDate.toISOString().slice(0, 19)+'Z';
    let expectedCurrentTimestamp = roundTimeDown(refreshDateISOString);
    let expectedUpcomingTimestamp = roundTimeUp(refreshDate);

    if (tempBiomes[0]['timestamp'] != expectedCurrentTimestamp || tempBiomes[1]['timestamp'] != expectedUpcomingTimestamp) {
        // console.log('BROWSER TAB INACTIVITY????????????????????????????????');

        isMidnightUpcoming_ = isMidnightUpcoming(refreshDateISOString)
        if (isMidnightUpcoming_) {
            tempBiomes = await getBiomesMidnightOnInit(refreshDate);
            return await refreshBiomes(isMidnightUpcoming_);

        } else if (localStorages['currentDaysJson'][0] != refreshDateISOString.slice(0, 10)) {
            await getCurrentDaysJson(refreshDate);
            tempBiomes = getBiomesOnInit();
            return await refreshBiomes(isMidnightUpcoming_);

        } else {
            tempBiomes = getBiomesOnInit();
            return await refreshBiomes(isMidnightUpcoming_);
        }
    }

    switch (true) {
        case (isMidnightUpcoming_):
            biomes = await getBiomesMidnight();
            break
        default:
            biomes = getBiomes();
            break
    }

    if (hasMidnightJustBeen(expectedCurrentTimestamp)) {
        rolloverCurrentDaysJsonLink(expectedCurrentTimestamp);
    }
    arrayBiomes(biomes, document.getElementById("season").value);
    if (document.getElementById('currentButton').textContent == 'Click here to see current missions') {
        document.getElementById('currentButton').click();
    }

    tempBiomes = undefined;
    // console.log(biomes[0]['timestamp'])
    // console.log(biomes[1]['timestamp'])
}
async function refreshDailyDeal() {
    dailyDeal = await getDailyDealData();
    arrayDailyDeal(dailyDeal);
}
async function refreshDeepDives() {
    deepDiveData = await getDeepDiveData();
    if (deepDiveData) {
        arrayDeepDives(deepDiveData);
        unAvailableDeepDiveDataRetries = 0
    } else {
        await handleUnavailableDeepDiveData();
    }
}
function formatTime(seconds) {
    seconds %= 3600;
    const minutes = Math.floor(seconds / 60);
    seconds %= 60;

    function formatNumber(num) {
        return num.toString().padStart(2, '0');
    }

    return `${formatNumber(minutes)}:${formatNumber(seconds)}`;
}
var unAvailableDeepDiveDataRetries = 0;
async function handleUnavailableDeepDiveData() {
    let deepDiveNormalDiv = document.getElementById('Deep-Dive-Normal');
    while(deepDiveNormalDiv.hasChildNodes()) {
        deepDiveNormalDiv.removeChild(deepDiveNormalDiv.lastChild);
    };

    deepDiveNormalDiv.appendChild(document.createElement("br"));
    let spanElement = document.createElement("span");
    spanElement.className = "scanners";
    spanElement.textContent = "// AWAITING UP TO DATE DATA \\\\";
    deepDiveNormalDiv.appendChild(spanElement);
    deepDiveNormalDiv.appendChild(document.createElement('br'));
    let normalCountdownSpanElement = document.createElement("span");
    normalCountdownSpanElement.className = 'scanners';
    deepDiveNormalDiv.appendChild(normalCountdownSpanElement);

    var deepDiveEliteDiv = document.getElementById('Deep-Dive-Elite');
    while(deepDiveEliteDiv.hasChildNodes()) {
        deepDiveEliteDiv.removeChild(deepDiveEliteDiv.lastChild);
    };

    deepDiveEliteDiv.appendChild(document.createElement("br"));
    spanElement = document.createElement("span");
    spanElement.className = "scanners";
    spanElement.textContent = "// AWAITING UP TO DATE DATA \\\\";
    deepDiveEliteDiv.appendChild(spanElement);
    deepDiveEliteDiv.appendChild(document.createElement('br'));
    let eliteCountdownSpanElement = document.createElement("span");
    eliteCountdownSpanElement.className = 'scanners';
    deepDiveEliteDiv.appendChild(eliteCountdownSpanElement);

    let timeLeft = 30 * (2 ** unAvailableDeepDiveDataRetries);
    let clockString;
    while (timeLeft > 0) {
        clockString = `${formatTime(timeLeft)} until retry, or refresh the page`;
        normalCountdownSpanElement.textContent = clockString;
        eliteCountdownSpanElement.textContent = clockString;
        timeLeft--;
        await sleep(1000);
    }
    unAvailableDeepDiveDataRetries += 1
}

function arrayDailyDeal(dailyDeal) {
    let dailyDealCanvas = renderDailyDeal(dailyDeal);
    let dailyDealDiv = document.getElementById('DailyDeal');

    while(dailyDealDiv.hasChildNodes()) {
        dailyDealDiv.removeChild(dailyDealDiv.lastChild);
    };

    dailyDealDiv.appendChild(dailyDealCanvas);
}

function arrayBiomes_(Biomes, season) { // deprecated, may need for debugging come season 5
    var currentBiomes = Biomes[0][season]['Biomes'];
    var nextBiomes = Biomes[1][season]['Biomes'];

    let biomes_ = ['Crystalline Caverns', 'Glacial Strata', 'Radioactive Exclusion Zone', 'Fungus Bogs', 'Dense Biozone', 'Salt Pits', 'Sandblasted Corridors', 'Magma Core', 'Azure Weald', 'Hollow Bough'];
    for (var i_ = 0; i_ < biomes_.length; i_++) {
        var biome = biomes_[i_];

        var biomeDiv = document.getElementById(biome);
        while(biomeDiv.hasChildNodes()) {
            biomeDiv.removeChild(biomeDiv.lastChild);
        };
        if (!(biome in currentBiomes)) {
            var spanElement = document.createElement("span");
            spanElement.className = "scanners";
            spanElement.textContent = "// SCANNERS OUT OF RANGE \\\\";
            biomeDiv.appendChild(spanElement)
        } else {
            var biomeMissions = currentBiomes[biome];
            for (var i = 0; i < biomeMissions.length; i++) {
                var mission = biomeMissions[i];
                biomeDiv.appendChild(mission['rendered_mission']);
            };
        };

        biomeDiv = document.getElementById(`next${biome}`);
        while(biomeDiv.hasChildNodes()) {
            biomeDiv.removeChild(biomeDiv.lastChild);
        };
        if (!(biome in nextBiomes)) {
            var spanElement = document.createElement("span");
            spanElement.className = "scanners";
            spanElement.textContent = "// SCANNERS OUT OF RANGE \\\\";
            biomeDiv.appendChild(spanElement)
        } else {
            var biomeMissions = nextBiomes[biome];
            for (var i = 0; i < biomeMissions.length; i++) {
                var mission = biomeMissions[i];
                biomeDiv.appendChild(mission['rendered_mission']);
            };
        };
    };
    equalizeGridItems();
}

// array as a verb
function arrayBiomes(Biomes, season) { // may need for debugging
    // if (Biomes[0].hasOwnProperty('s0')) {
    //     arrayBiomes_(Biomes, season);
    // } else {
        arrayBiomesFlat(Biomes, season);
    // }
}
function arrayBiomesFlat(Biomes, season) {
    let currentBiomes = Biomes[0]['Biomes'];
    let nextBiomes = Biomes[1]['Biomes'];
    let biomeMissions;
    let isS0 = season === 's0';

    let biomes_ = ['Crystalline Caverns', 'Glacial Strata', 'Radioactive Exclusion Zone', 'Fungus Bogs', 'Dense Biozone', 'Salt Pits', 'Sandblasted Corridors', 'Magma Core', 'Azure Weald', 'Hollow Bough'];
    for (let i_ = 0; i_ < biomes_.length; i_++) {
        let biome = biomes_[i_];

        let biomeDiv = document.getElementById(biome);
        while(biomeDiv.hasChildNodes()) {
            biomeDiv.removeChild(biomeDiv.lastChild);
        };
        let nextBiomeDiv = document.getElementById(`next${biome}`)
        while(nextBiomeDiv.hasChildNodes()) {
            nextBiomeDiv.removeChild(nextBiomeDiv.lastChild);
        };

        if (!(biome in currentBiomes)) {
            let spanElement = document.createElement("span");
            spanElement.className = "scanners";
            spanElement.textContent = "// SCANNERS OUT OF RANGE \\\\";
            biomeDiv.appendChild(spanElement);
        } else {
            biomeMissions = currentBiomes[biome];
            for (let i = 0; i < biomeMissions.length; i++) {
                let mission = biomeMissions[i];

                if (isS0 && mission['season'] != season) {
                    continue
                }
                if (mission.hasOwnProperty('season_modified') && !isS0) {
                    mission = mission['season_modified'][season];
                }
                if (!isS0 && mission['season'] != season && mission['season'] != 's0'){
                    continue
                }

                biomeDiv.appendChild(mission['rendered_mission']);
            }
        }

        if (!(biome in nextBiomes)) {
            let spanElement = document.createElement("span");
            spanElement.className = "scanners";
            spanElement.textContent = "// SCANNERS OUT OF RANGE \\\\";
            nextBiomeDiv.appendChild(spanElement);
        } else {
            biomeMissions = nextBiomes[biome];
            for (let i = 0; i < biomeMissions.length; i++) {
                let mission = biomeMissions[i];

                if (isS0 && mission['season'] != season) {
                    continue
                }
                if (mission.hasOwnProperty('season_modified') && !isS0) {
                    mission = mission['season_modified'][season];
                }
                if (!isS0 && mission['season'] != season && mission['season'] != 's0'){
                    continue
                }

                nextBiomeDiv.appendChild(mission['rendered_mission']);
            }
        }
    };
    equalizeGridItems();
}

function addShadowedTextToImage(canvas, texts, fontSize) {
    function getTextMetrics(context, text, font) {
        context.font = font;
        return context.measureText(text);
    }
    function drawText(text, x, y, fillStyle, fontSize, fontName) {
        tempCtx.font = `${fontSize}px ${fontName}`;
        tempCtx.fillStyle = fillStyle;
        tempCtx.fillText(text, x, y);
    }
    function shadowText(text, x, y, shadowColor, fontSize, fontName) {
        tempCtx.font = `${fontSize}px ${fontName}`;
        tempCtx.shadowColor = shadowColor;
        tempCtx.shadowBlur = 7;
        tempCtx.lineWidth = 5;
        tempCtx.strokeStyle = 'black';
        tempCtx.strokeText(text, x, y);
        tempCtx.shadowBlur = 0
    }
    const x = canvas.width / 2;
    const y = canvas.height / 2;

    const descriptorText = texts[0];
    const codename = texts[1];

    var descriptorFontName = `RiftSoft-Regular`;
    var mainFontName = `BebasNeue`;


    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = canvas.width;
    tempCanvas.height = canvas.height;

    const tempCtx = tempCanvas.getContext('2d');

    const descriptorWidth = getTextMetrics(tempCtx, descriptorText, `${fontSize}px ${descriptorFontName}`).width;
    const codenameWidth = getTextMetrics(tempCtx, codename, `${fontSize}px ${mainFontName}`).width;
    const totalWidth = descriptorWidth + codenameWidth;

    const combinedX = x - (totalWidth / 2);

    shadowText(descriptorText, combinedX, y+15, 'black', fontSize, descriptorFontName);
    drawText(descriptorText, combinedX, y+15, 'white', fontSize, descriptorFontName);

    const codenameX = combinedX + descriptorWidth;

    shadowText(codename, codenameX, y+15, 'black', fontSize, mainFontName);
    drawText(codename, codenameX, y+15, 'white', fontSize, mainFontName);

    canvas.getContext('2d').drawImage(tempCanvas, 0, 0);
}

function renderDeepDiveBiomeCodename(biome, codename) {
    const texts = ['CODENAME: ', codename];
    const fontSize = 45;
    const canvas = document.createElement('canvas');
    canvas.classList.add('dd-biome');
    const ctx = canvas.getContext('2d');
    for (let biomeName in biomesDD) {
        if (biomeName == biome) {
            const img = biomesDDImages[biomeName];
            canvas.width = img.width;
            canvas.height = img.height;
            ctx.drawImage(img, 0, 0);
            addShadowedTextToImage(canvas, texts, fontSize);
            break
        }
    }
    return canvas;
}

function renderDeepDiveStage(m_d, stageCount) {
    const div = document.createElement('div');
    div.classList.add('mission-hover-zoom');
    div.classList.add('mission');
    div.id = m_d['CodeName'];

    const canvas = document.createElement('canvas');
    canvas.title = `Stage ${stageCount.toString()}`;
    canvas.width = 350;
    canvas.height = 300;
    var ctx = canvas.getContext('2d');

    const primaryImg = primaryObjsImages[m_d['PrimaryObjective']];
    ctx.drawImage(primaryImg, 83, 58, primaryImg.width * 0.4, primaryImg.height * 0.4);

    const secondaryImg = secondaryObjsDDImages[m_d['SecondaryObjective']];
    ctx.drawImage(secondaryImg, -11, -21, secondaryImg.width * 0.6, secondaryImg.height * 0.6);

    if (m_d['MissionWarnings']) {
        let MissionWarnings = [];
        m_d['MissionWarnings'].forEach((warning) => {
            MissionWarnings.push(warning);
        });
        const MISSIONWARNING1 = warningsImages[MissionWarnings[0]];
        const scaledWidth = MISSIONWARNING1.width * 0.38;
        const scaledHeight = MISSIONWARNING1.height * 0.38;
        if (MissionWarnings.length === 1) {
            ctx.drawImage(MISSIONWARNING1, 227, 87, scaledWidth, scaledHeight);
        } else if (MissionWarnings.length === 2) {
            const MISSIONWARNING2 = warningsImages[MissionWarnings[1]];
            ctx.drawImage(MISSIONWARNING1, 227, 42, scaledWidth, scaledHeight);
            ctx.drawImage(MISSIONWARNING2, 227, 142, scaledWidth, scaledHeight);
        }
    }

    if (m_d['MissionMutator']) {
        const mutatorImg = mutatorsImages[m_d['MissionMutator']];
        ctx.drawImage(mutatorImg, 27, 92, mutatorImg.width * 0.38, mutatorImg.height * 0.38);
    }

    const complexityImg = complexitiesImages[m_d['Complexity']];
    ctx.drawImage(complexityImg, 107, 2, complexityImg.width * 0.45, complexityImg.height * 0.45);

    const lengthImg = lengthsImages[m_d['Length']];
    ctx.drawImage(lengthImg, 107, 242, lengthImg.width * 0.45, lengthImg.height * 0.45);

    const values_resource = {
        'Mining Expedition,1,1': '200',
        'Mining Expedition,1,2': '225',
        'Mining Expedition,2,2': '250',
        'Mining Expedition,2,3': '325',
        'Mining Expedition,3,3': '400',
        'Egg Hunt,1': '4',
        'Egg Hunt,2': '6',
        'Egg Hunt,default': '8',
        'Point Extraction,2': '7',
        'Point Extraction,default': '10',
        'Industrial Sabotage,default': '1',
        'On-Site Refining,default': '3',
        'Escort Duty,2': '1',
        'Escort Duty,default': '2',
        'Elimination,2': '2',
        'Elimination,default': '3',
        'Salvage Operation,2': '2',
        'Salvage Operation,default': '3',
        'Deep Scan,2,1' : '3',
        'Deep Scan,3,2' : '5'
    };

    const hexagon = primaryObjResourcesImages['hexagon'];
    ctx.drawImage(hexagon, 15, 190, hexagon.width * 0.32, hexagon.height * 0.32);
    drawResource(m_d['PrimaryObjective'], m_d['Complexity'], m_d['Length']);

    function drawResource() {
        const resource = primaryObjResourcesImages[m_d['PrimaryObjective']];
        let scaleFactor;
        if (m_d['PrimaryObjective'] === 'Mining Expedition') scaleFactor = 0.18;
        else if (m_d['PrimaryObjective'] === 'Egg Hunt') scaleFactor = 0.20;
        else scaleFactor = 0.1;

        ctx.drawImage(resource, 38, 205, resource.width * scaleFactor, resource.height * scaleFactor);

        const text = getText(m_d['PrimaryObjective'], m_d['Complexity'], m_d['Length']);
        drawText(text, 'CarbonBold-W00-Regular', '35',  m_d['PrimaryObjective']);
    }

    function getText(primaryObj, complexity, length) {
        return values_resource[`${primaryObj},${length}`] ||
            values_resource[`${primaryObj},${complexity},${length}`] ||
            values_resource[`${primaryObj},${complexity},default`] ||
            values_resource[`${primaryObj},default`];
    }

    function drawText(text, font, fontSize, primaryObj) {
        ctx.font = `${fontSize}px ${font}`;
        ctx.fillStyle = 'white';
        ctx.textAlign = 'center';
        var y = 280;
        if (primaryObj == 'Mining Expedition') y -= 5;
        ctx.fillText(text, 63, y);
    }
    ctx.save();
    resizeCanvas(div, canvas, 0.35, 0.35);
    div.appendChild(canvas);
    return div;
}

function sortDeepDiveStages(stages) {
    let hasId999 = false;
    let hasId0 = false;
    for (let i = 0; i < stages.length; i++) {
        let stage = stages[i]
        if (stage['id'] === 999) {
            hasId999 = true;
        }
        if (stage['id'] === 0) {
            hasId0 = true;
        }
    }
    for (let i = 0; i < stages.length; i++) {
        let stage = stages[i];
        if (hasId999 && hasId0) {
            if (stage['id'] === 999) {
                stage['id'] = -1;
            }
        }
    }
    return stages.slice().sort((a, b) => b['id'] - a['id']);
}

async function arrayDeepDives(deepDiveData) {
    try {
        var deepDiveNormal = deepDiveData["Deep Dives"]["Deep Dive Normal"];
        var deepDiveElite = deepDiveData["Deep Dives"]["Deep Dive Elite"];
        var deepDiveNormalDiv = document.getElementById('Deep-Dive-Normal');
        var deepDiveEliteDiv = document.getElementById('Deep-Dive-Elite');

        var deepDiveNormalBiome = renderDeepDiveBiomeCodename(deepDiveNormal['Biome'], deepDiveNormal['CodeName']);
        while(deepDiveNormalDiv.hasChildNodes()) {
            deepDiveNormalDiv.removeChild(deepDiveNormalDiv.lastChild);
        };
        deepDiveNormalDiv.appendChild(deepDiveNormalBiome);
        deepDiveNormalDiv.appendChild(document.createElement("br"));


        var deepDiveEliteBiome = renderDeepDiveBiomeCodename(deepDiveElite['Biome'], deepDiveElite['CodeName']);
        while(deepDiveEliteDiv.hasChildNodes()) {
            deepDiveEliteDiv.removeChild(deepDiveEliteDiv.lastChild);
        };
        deepDiveEliteDiv.appendChild(deepDiveEliteBiome);
        deepDiveEliteDiv.appendChild(document.createElement("br"));

        var normalStages = sortDeepDiveStages(deepDiveNormal["Stages"]);
        var stageCount = 0;
        for (var i = 0; i < normalStages.length; i++) {
            stage = normalStages[i];
            stageCount += 1;
            stageDiv = renderDeepDiveStage(stage, stageCount);
            deepDiveNormalDiv.appendChild(stageDiv);
        };

        var eliteStages = sortDeepDiveStages(deepDiveElite["Stages"]);
        stageCount = 0;
        for (var i = 0; i < eliteStages.length; i++) {
            stage = eliteStages[i];
            stageCount += 1;
            stageDiv = renderDeepDiveStage(stage, stageCount);
            deepDiveEliteDiv.appendChild(stageDiv);
        };
    } catch {
        // deepDiveData is undefined
    }
}

function getDailyDealData(isMidnightUpcoming=false) {
    if (isMidnightUpcoming) {
        return tempDailyDeal;
    }
    return localStorages['currentDaysJson'][1]['dailyDeal'];
}

function scaleImage(ctx, image, scale) {
    var newWidth = image.width * scale;
    var newHeight = image.height * scale;
    ctx.drawImage(image, 0, 0, newWidth, newHeight);
}

function resizeImage(img, desiredWidth, desiredHeight) {
    var tempCanvas = document.createElement('canvas');
    var tempCtx = tempCanvas.getContext('2d');

    tempCanvas.width = desiredWidth;
    tempCanvas.height = desiredHeight;

    tempCtx.drawImage(img, 0, 0, desiredWidth, desiredHeight);

    return tempCanvas;
  }

function renderDailyDeal(dealDict) {
    function drawText(text, x, y, fillStyle, fontSize, fontName) {
        ctx.font = `${fontSize}px ${fontName}`;
        ctx.fillStyle = fillStyle;
        ctx.fillText(text, x, y);
        }

    var canvas = document.createElement('canvas');
    var div = document.createElement('div')
    canvas.height = 635;
    canvas.width = 400;
    var ctx = canvas.getContext('2d');

    var buyOrGet = {
        'Buy': 'Pay',
        'Sell': 'Get',
    };
    var saveProfit = {
        'Buy':'Savings!',
        'Sell':'Profit!',
    };
    var resourceAmount = dealDict['ResourceAmount'];
    var resource = dealDict['Resource'];

    ctx.fillStyle = 'rgba(0, 44, 81, 255)';
    ctx.fillRect(0, 0, 400, 635);
    ctx.fillStyle = 'rgba(57, 148, 136, 255)';
    ctx.fillRect(0, 0, 400, 120);
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    var text = "TODAY'S OFFER:";
    drawText(text, 200, 30, 'black', 45, 'CarbonBold-W00-Regular');
    drawText(resource, 200, 75, 'black', 60, 'Bungee-Regular');

    var resourceImg = dailyDealResourcesImages[resource];
    var text = resourceAmount.toString();
    var fontName = 'Bungee-Regular';
    ctx.font = `75px ${fontName}`;
    var textWidth = ctx.measureText(text).width;
    drawText(text, 200, 200, 'white', 75, fontName);

    var resourceImage = resizeImage(resourceImg, resourceImg.width*0.3, resourceImg.height*0.3);
    var x = ((canvas.width / 2) - textWidth) / 2;

    ctx.drawImage(resourceImage, x+25, 150);
    ctx.save();

    ctx.translate(canvas.width, 0);
    ctx.scale(-1, 1);
    ctx.drawImage(resourceImage, x+25, 150);
    ctx.restore();

    drawText(dealDict['DealType'], 200, 152, 'white', 35, 'Bungee-Regular');
    drawText(buyOrGet[dealDict['DealType']], 200, 290, 'white', 35, 'Bungee-Regular');

    var creditsImage = dailyDealResourcesImages['Credits'];
    creditsImage = resizeImage(creditsImage, creditsImage.width*0.4, creditsImage.height*0.4);

    text = dealDict['Credits'].toString();
    drawText(text, 200, 337, 'white', 75, 'Bungee-Regular');
    if (text.length < 5) {
        ctx.drawImage(creditsImage, 34, 312);
        ctx.drawImage(creditsImage, canvas.width - creditsImage.width - 34, 312);
    } else {
        ctx.drawImage(creditsImage, 20, 315);
        ctx.drawImage(creditsImage, canvas.width - creditsImage.width - 20, 315);
    }

    var bubbleImage = dailyDealResourcesImages['Bubble'];
    bubbleImage = resizeImage(bubbleImage, bubbleImage.width*0.8, bubbleImage.height*0.8);
    ctx.save();
    ctx.rotate(20 * Math.PI / 180);
    ctx.drawImage(bubbleImage, 105, 337);

    text = Math.round(dealDict['ChangePercent']).toString();
    if (text.length == 2) {
        text = text.split('');
        let digit1 = text[0];
        drawText(digit1, 248, 433, 'black', 75, 'Bungee-Regular');
        let digit2 = text[1]+'%';
        drawText(digit2, 340, 433, 'black', 75, 'Bungee-Regular');

    } else {
        text += '%';
        drawText(text, 321, 433, 'black', 75, 'Bungee-Regular');
    }

    text = saveProfit[dealDict['DealType']];
    drawText(text, 310, 480, 'black', 30, 'Bungee-Regular');
    ctx.restore();

    resizeCanvas(div, canvas, 0.5, 0.5);
    canvas.classList.add('daily_trade');
    div.appendChild(canvas);
    return div;
}
function isElementVisible(el) {
    return (el.offsetParent !== null);
}
function setupIdleVideoPause(videoElementId, idleTimeThreshold) {
    let idleTimer;
    let isPausedByIdle = false;
    let isPausedByBlur = false;
    const videoElement = document.getElementById(videoElementId);

    function resetIdleTimer() {
        clearTimeout(idleTimer);
        idleTimer = setTimeout(function() {
            if (!isPausedByBlur) {
                videoElement.pause();
                isPausedByIdle = true;
            }
        }, idleTimeThreshold);
    }

    function handleUserActivity() {
        resetIdleTimer();
        if (!isPausedByBlur && isPausedByIdle && videoElement.style.display != 'none') {
            videoElement.play();
            isPausedByIdle = false;
        }

    }

    document.addEventListener("mousemove", handleUserActivity);
    document.addEventListener("keypress", handleUserActivity);
    document.addEventListener("click", handleUserActivity);

    window.addEventListener('blur', function() {
        if (!isPausedByIdle && videoElement.style.display != 'none') {
            videoElement.pause();
            isPausedByBlur = true;
        }


    });
    window.addEventListener('focus', function() {
        if (isPausedByBlur && videoElement.style.display != 'none') {
            videoElement.play();
            isPausedByBlur = false;
        }
    });

    document.addEventListener('visibilitychange', function() {
        if (document.hidden) {
            if (!isPausedByIdle && videoElement.style.display != 'none') {
                videoElement.pause();
                isPausedByBlur = true;
            }
        } else {
            if (isPausedByBlur && videoElement.style.display != 'none') {
                videoElement.play();
                isPausedByBlur = false;
            }
        }
    });

    resetIdleTimer();
}

function mostCommonNumber(arr) {
    const filteredArr = arr.filter(num => num !== 0);
    const countMap = filteredArr.reduce((map, num) => (map.set(num, (map.get(num) || 0) + 1), map), new Map());
    return [...countMap.entries()].reduce((a, b) => b[1] > a[1] ? b : a, [0, 0])[0];
}
function checkOverflowAndFixScanners(containers) {
    let overflowing_containers = [];
    let scanners = [];
    let heights = [];

    containers.forEach(container => {
        if (Array.from(container.children).some(child =>
            child.tagName.toLowerCase() === 'div' && child.children.length === 1)) {
            scanners.push(container);
        }
    });
    containers.forEach(container => {
        container.style.height = "auto";
        let height = container.offsetHeight;
        if (height != 0) {
            container.style.height = `${height-10}px`;
            if (!(inList(scanners, container))) {
                heights.push(height);
            }
        }
    });
    if (window.matchMedia("(min-width: 1440px)").matches) {
        scanners.forEach(container => {
            container.style.height = `${mostCommonNumber(heights)-10}px`;
        });
    } else {
        scanners.forEach(container => {
            container.style.height = `auto`;
        });
    }

    containers.forEach(container => {
      if (container.scrollHeight > container.clientHeight+10) {
        overflowing_containers.push(container);
      }
    });
    if (overflowing_containers.length != 0) {
        overflowing_containers.forEach(container => {
            container.style.height = "auto";
        });
    }
}
function equalizeGridItems() {
    const gridItems = document.querySelectorAll('.biome-container');
    checkOverflowAndFixScanners(gridItems);
}

function toggleBackground() {
    var video = document.getElementById("background-video");
    var backgroundbutton = document.getElementById('backgroundButton');
    var overlay = document.querySelector(".overlay");
    if (video.style.display === "none" && overlay.style.display === "none") {
        video.style.display = "block";
        overlay.style.display = "block";
        backgroundbutton.textContent = "Hide background";
        if (initialized) {
            video.play();
        }
        setStorages('isBackgroundHidden', false);
    } else {
        video.style.display = "none";
        overlay.style.display = "none";
        backgroundbutton.textContent = "Show background";
        video.pause();
        setStorages('isBackgroundHidden', true);
    }
};

function handleStorageChange(event) {
    function handleCase(key) {
        localStorages[key] = JSON.parse(event.newValue);
        dispatchConfigEvent(key, localStorages[key]);
    }

    for (const key in localStorages) {
        if (key === event.key) {
            handleCase(key);
            break;
        }
    }
}
function dispatchConfigEvent(key, value) {
    const configEvent = new Event('configEvent');
    configEvent.key = key;
    configEvent.newValue = {};
    configEvent.newValue[key] = value;
    window.dispatchEvent(configEvent);
}
window.addEventListener('storage', handleStorageChange);
window.addEventListener('configEvent', (event) => {
    switch (event.key) {
        case 'isBackgroundHidden':
            if (event.newValue[event.key] !== localStorages['isBackgroundHidden']) {
                localStorages['isBackgroundHidden'] = event.newValue[event.key];
            }
            break;
        case 'areButtonsHidden':
            if (event.newValue[event.key] !== localStorages['areButtonsHidden']) {
                localStorages['areButtonsHidden'] = event.newValue[event.key];
            }
            break;
        default:
            break;
    }
});
function toggleButtons() {
    let buttonDiv = document.getElementById('buttonDiv');
    let buttonsButton = document.getElementById('buttonsButton');

    if (buttonDiv.style.display === "none") {
        buttonDiv.style.display = 'block';
        // for (let i = 0; i < buttonDiv.parentElement.childNodes.length; i++) {
            // node = buttonDiv.parentElement.childNodes[i]
            // if (node.nodeName === 'BR') {
                // console.log(node)
                // console.log(i)

            // }
            // if (buttonDiv.parentElement.childNodes[9] == currentButtonLineBreak) {
                buttonDiv.parentElement.removeChild(currentButtonLineBreak)
            // }
        // }
        // slideToggle('missionsCountdown', 'missionRotationSlideButton', ['Show Countdown', 'Hide Countdown']);
        document.getElementById('dailyDealButton').textContent = 'Click here to see Daily Deal';
        buttonsButton.textContent = "x";
        setStorages('areButtonsHidden', false);
    } else {
        buttonDiv.style.display = "none";
        buttonDiv.parentElement.insertBefore(currentButtonLineBreak, document.getElementById('currentButton'))
        // slideToggle('missionsCountdown', 'missionRotationSlideButton', ['Show Countdown', 'Hide Countdown'])
        slideToggle('dailyDealMaster', 'dailyDealButton', ['Click here to see Daily Deal', 'Hide Daily Deal'])
        buttonsButton.textContent = "+";
        setStorages('areButtonsHidden', true);
    }
};
async function slideToggle(elementId, buttonId, buttonTexts) {
    let element = document.getElementById(elementId);
    let button = document.getElementById(buttonId)
    let currentHeight = element.clientHeight;
    let contentHeight = element.scrollHeight;

    if (currentHeight === 0) {
        element.style.height = contentHeight + "px";
        button.textContent = buttonTexts[1];
    } else {
        element.style.height = 0;
        button.textContent = buttonTexts[0];
    }
}
window.addEventListener('resize', function(event) {
    if (initialized) {
        equalizeGridItems();
    }
});
async function initialize(date) {
    let biomes_;
    let dailyDeal_;

    if (isMidnightUpcoming(date)) {
        biomes_ = await getBiomesMidnightOnInit(date);
        dailyDeal_ = getDailyDealData(true);
        // console.log('------');
        // console.log(biomes_);
        // console.log(biomes_[0]['timestamp']);
        // console.log(biomes_[1]['timestamp']);

    } else {
        await getCurrentDaysJson(date);
        biomes_ = getBiomesOnInit();
        dailyDeal_ = getDailyDealData();
        // console.log('------');
        // console.log(biomes_);
        // console.log(biomes_[0]['timestamp']);
        // console.log(biomes_[1]['timestamp']);
    }

    let currentDatetime = date.toISOString().slice(0, 10);
    let currentDateTimeHREF = `${domainURL}/static/json/bulkmissions/${currentDatetime}.json`;

    let nextDatetime = getNextDateMidnightUTC(date).slice(0, 10);
    let nextDateTimeHREF = `${domainURL}/static/json/bulkmissions/${nextDatetime}.json`;

    let ddDatetime = getPreviousThursdayTimestamp();
    ddDatetime = replaceCharactersAtIndices(ddDatetime, [[13, '-'], [16,'-']]);
    let ddDatetimeHREF = `${domainURL}/static/json/DD_${ddDatetime}.json`;

    let html = `
    <div id="current">
    <div class="grid-container">

    <h2>
    <div class="biome-container" biome="Glacial Strata">
    <br><div id="Glacial Strata" class="missions">
    </div>
    </div>
    </h2>

    <h2>
    <div class="biome-container" biome="Crystalline Caverns">
    <br><div id="Crystalline Caverns" class="missions">
    </div>
    </div>
    </h2>

    <h2>
    <div class="biome-container" biome="Salt Pits">
    <br><div id="Salt Pits">
    </div>
    </div>
    </h2>

    <h2>
    <div class="biome-container" biome="Magma Core">
    <br><div id="Magma Core" class="missions">
    </div>
    </div>
    </h2>

    <h2>
    <div class ="biome-container" biome="Azure Weald">
    <br><div id="Azure Weald" class="missions">
    </div>
    </div>
    </h2>

    <h2>
    <div class="biome-container" biome="Sandblasted Corridors">
    <br><div id="Sandblasted Corridors" class="missions">
    </div>
    </div>
    </h2>

    <h2>
    <div class="biome-container" biome="Fungus Bogs">
    <br><div id="Fungus Bogs" class="missions">
    </div>
    </div>
    </h2>

    <h2>
    <div class="biome-container" biome="Radioactive Exclusion Zone">
    <br><div id="Radioactive Exclusion Zone" class="missions">
    </div>
    </div>
    </h2>

    <h2>
    <div class="biome-container" biome="Dense Biozone">
    <br><div id="Dense Biozone" class="missions">
    </div>
    </div>
    </h2>

    <h2>
    <div class="biome-container" biome="Hollow Bough">
    <br><div id="Hollow Bough" class="missions">
    </div>
    </div>
    </h2>

    </div>
    </div>


    <div id="upcoming" style="visibility: hidden;">
    <div class="grid-container">

    <h2>
    <div class="biome-container" biome="Glacial Strata">
    <br><div id="nextGlacial Strata" class="missions">
    </div>

    </div>
    </h2>

    <h2>
    <div class="biome-container" biome="Crystalline Caverns">
    <br><div id="nextCrystalline Caverns" class="missions">
    </div>
    </div>
    </h2>

    <h2>
    <div class="biome-container" biome="Salt Pits">
    <br><div id="nextSalt Pits" class="missions">
    </div>
    </div>
    </h2>

    <h2>
    <div class="biome-container" biome="Magma Core">
    <br><div id="nextMagma Core" class="missions">
    </div>
    </div>
    </h2>

    <h2>
    <div class ="biome-container" biome="Azure Weald">
    <br><div id="nextAzure Weald" class="missions">
    </div>

    </div>
    </h2>

    <h2>
    <div class="biome-container" biome="Sandblasted Corridors">
    <br><div id="nextSandblasted Corridors">
    </div>
    </h2>

    <h2>
    <div class="biome-container" biome="Fungus Bogs">
    <br><div id="nextFungus Bogs" class="missions">
    </div>
    </div>
    </h2>

    <h2>
    <div class="biome-container" biome="Radioactive Exclusion Zone">
    <br><div id="nextRadioactive Exclusion Zone" class="missions">
    </div>
    </div>
    </h2>

    <h2>
    <div class="biome-container" biome="Dense Biozone">
    <br><div id="nextDense Biozone" class="missions">
    </div>
    </div>
    </h2>

    <h2>
    <div class="biome-container" biome="Hollow Bough">
    <br><div id="nextHollow Bough" class="missions">
    </div>
    </div>
    </h2>

    </div>
    </div>


    <div class="grid-container">

    <h2>
    <div class="dd-container" dd="dd">
    <div id="Deep-Dive-Normal" class="dd-missions">
    </div>
    </div>
    </h2>

    <h2>
    <div class="dd-container" dd="edd">
    <div id="Deep-Dive-Elite" class="dd-missions">
    </div>
    </div>
    </h2>

    </div>

    <div>

    <div class="deepDiveCountdownHead">NEW DEEP DIVES IN</div>
    <span id="deepDiveCountdown"></span>
    <hr>
    </div>

    <div class="jsonc">
    <div class="jsonlinks"><span style="color: white;font-size: 30px;font-family: BebasNeue, sans-serif;"> <a id="currentDaysJsonLink" class="jsonlink" href="${currentDateTimeHREF}">TODAY'S DATA</a> | <a id="tomorrowDaysJsonLink" class="jsonlink" href="${nextDateTimeHREF}">TOMORROW'S DATA</a> | <a class="jsonlink" href="${ddDatetimeHREF}">CURRENT DEEP DIVE DATA</a> | <a class="jsonlink" href="/static/xp_calculator.html">CLASS XP CALCULATOR</a> | <a class="jsonlink" href="https://github.com/rolfosian/drgmissions/">GITHUB</a></span> </div>
    <span class="credits">Send credits (eth): 0xb9c8591A80A3158f7cFFf96EC3c7eA9adB7818E7</span>
    </div>
    <p class='gsgdisclaimer'><i>This website is a third-party platform and is not affiliated, endorsed, or sponsored by Ghost Ship Games. The use of Deep Rock Galactic's in-game assets on this website is solely for illustrative purposes and does not imply any ownership or association with the game or its developers. All copyrights and trademarks belong to their respective owners. For official information about Deep Rock Galactic, please visit the official Ghost Ship Games website.</i></p></div>
    `;

    let mainContent = document.getElementById('mainContent');
    mainContent.innerHTML = html;
    setBiomeAndDeepDivesBanners();

    return [biomes_, dailyDeal_]
}

async function getCurrentDaysJson(date, isMidnightUpcoming_=false) {
    document.querySelector('.loading').textContent = `Loading today's data...`;
    let cdj;
    const todaysDate = date.toISOString().slice(0, 10);

    if (localStorages['currentDaysJson']) {
        cdj = localStorages['currentDaysJson'];
        if (isMidnightUpcoming_) {
            const tomorrowsDate = getNextDateMidnightUTC(date).slice(0, 10);

            if (cdj[0] == todaysDate) {
                let cdjMidnight = [tomorrowsDate, await loadJSON(`${domainURL}/static/json/bulkmissions/${tomorrowsDate}.json`)];
                tempDailyDeal = cdj[1]['dailyDeal'];
                setStorages('currentDaysJson', cdjMidnight);
                return [cdj[1], cdjMidnight[1]];
            } else {
                let cdjs = await Promise.all([
                    loadJSON(`${domainURL}/static/json/bulkmissions/${todaysDate}.json`),
                    loadJSON(`${domainURL}/static/json/bulkmissions/${tomorrowsDate}.json`)
                ]);
                tempDailyDeal = cdjs[0]['dailyDeal'];
                setStorages('currentDaysJson', [tomorrowsDate, cdjs[1]]);
                return [cdjs[0], cdjs[1]];
            }

        } else if (cdj[0] === todaysDate) {
            return cdj[1];
        }

    } else if (isMidnightUpcoming_ && !localStorages['currentDaysJson']) {
        const tomorrowsDate = getNextDateMidnightUTC(date).slice(0, 10);
        let cdjs = await Promise.all([
            loadJSON(`${domainURL}/static/json/bulkmissions/${todaysDate}.json`),
            loadJSON(`${domainURL}/static/json/bulkmissions/${tomorrowsDate}.json`)
        ]);
        tempDailyDeal = cdjs[0]['dailyDeal'];
        let cdjMidnight = [tomorrowsDate, cdjs[1]];
        setStorages('currentDaysJson', cdjMidnight);
        return [cdjs[0], cdjs[1]];

    } else {
        cdj = [todaysDate, await loadJSON(`${domainURL}/static/json/bulkmissions/${todaysDate}.json`)];
        setStorages('currentDaysJson', cdj);
        return cdj[1];
    }
}

function simpleHash(input) {
    let hash = 0;
    for (let i = 0; i < input.length; i++) {
        const charCode = input.charCodeAt(i);
        hash = (hash << 5) - hash + charCode;
        hash |= 0;
    }
    return hash;
}

async function verifyStorages(date) {
    for (let key in localStorages) {
        let v;
        // try {

            // if (key == 'img') {
            //     setStorages(key, null)
            //     continue
            // }

            // if (key == 'fonts') {
            //     setStorages(key, null)
            //     continue
            // }

            // if (key == 'currentDaysJson') {
            //     setStorages(key, null)
            //     continue
            // }

            // if (key == 'homepageScript') {
            //     setStorages(key, null)
            //     continue
            // }


            if (isLocalStorageAvailable_) {
                v = localStorage.getItem(key);
            }
            if (v) {
                if (localStoragesHashes.hasOwnProperty(key)) {
                    if (simpleHash(v) === localStoragesHashes[key]) {
                        localStorages[key] = JSON.parse(v);
                    } else {
                        console.log(`Old hash of ${key}:`, simpleHash(v));
                        setStorages(key, null);
                    }

                } else if (key === 'currentDaysJson') {
                    let data = JSON.parse(v);
                    if (data[0] != date.toISOString().slice(0, 10)) {
                        setStorages(key, null);
                    } else {
                        localStorages[key] = data;
                    }
                } else {
                    localStorages[key] = JSON.parse(v);
                }

            } else {
                setStorages(key, localStorages[key]);
            }
        // } catch (error) {
        //     console.log(key, error)
        // }

        // console.log(key, localStorages[key]);
    }
    if (!localStorages['homepageScript'] || localStorages['homepageScript'] == 'null') {
        let s = await preloadHomepageScript()
        console.log('New homepageScript hash:', simpleHash(JSON.stringify(s)))
        setStorages('homepageScript', s);
    }
    // console.log(localStorages['homepageScript'])
}

function setStorages(key, value, storages=localStorages) {
    storages[key] = value;
    if (isLocalStorageAvailable_) {
        if (value === null) {
            localStorage.removeItem(key);
        } else {
            localStorage.setItem(key, JSON.stringify(value));
        }
    }
}
var localStorages = {
    'isBackgroundHidden' : false,
    'areButtonsHidden' : false,
    'seasonSelected' : 's0',
    'currentDaysJson' : null,
    'img' : null,
    'fonts' : null,
    'homepageScript' : null,
};
var localStoragesHashes = {
    'img' : 1012099637,
    'fonts' : 906557479,
    'homepageScript' : 1068821741,
};

var cacheActive = false;
var isRefreshing = false;
var tempBiomes;
var tempCurrentDaysJson;

var biomes;
var dailyDeal;
var tempDailyDeal;

var deepDiveData;

var currentButtonLineBreak = document.createElement('br');
currentButtonLineBreak.id = 'currentButtonLineBreak'

var initialized = false;

function resetGlobalVars() {
    biomeBannersImages = {};
    biomeBannersImages.name = 'biomeBanners';
    deepDivesBannersImages = {};
    deepDivesBannersImages.name = 'deepDivesBanners';
    primaryObjsImages = {};
    primaryObjsImages.name = 'primaryObjsImages';
    primaryObjResourcesImages = {};
    primaryObjResourcesImages.name = 'primaryObjResourcesImages';
    secondaryObjsImages = {};
    secondaryObjsImages.name = 'secondaryObjsImages';
    complexitiesImages = {};
    complexitiesImages.name = 'complexitiesImages';
    lengthsImages = {};
    lengthsImages.name = 'lengthsImages';
    mutatorsImages = {};
    mutatorsImages.name = 'mutatorsImages';
    warningsImages = {};
    warningsImages.name = 'warningsImages';
    secondaryObjsDDImages = {};
    secondaryObjsDDImages.name = 'secondaryObjsDDImages';
    biomesDDImages = {};
    biomesDDImages.name = 'biomesDDImages';
    dailyDealResourcesImages = {};
    dailyDealResourcesImages.name = 'dailyDealResourcesImages';
    base64LocalStoragesImg = {};
    base64LocalStoragesFonts = {};

    localStorages = {
        'isBackgroundHidden' : false,
        'areButtonsHidden' : false,
        'seasonSelected' : 's0',
        'currentDaysJson' : null,
        'img' : null,
        'fonts' : null,
        'homepageScript' : null,
    };

    cacheActive = false;
    isRefreshing = false;
    tempBiomes = undefined;
    tempCurrentDaysJson = undefined;

    biomes = undefined;
    dailyDeal = undefined;
    tempDailyDeal = undefined;

    deepDiveData = undefined;

    initialized = false;
}

document.addEventListener('DOMContentLoaded', async function() {
    let initTries = 0
    while (true) {
        let date = new Date();
        try {
            await waitRotation();
            await verifyStorages(date);

            if (localStorages['isBackgroundHidden']) {
                toggleBackground();
            } else {
                document.getElementById('background-video').play();
            }
            if (localStorages['areButtonsHidden']) {
                toggleButtons();
            }

            let seasonBoxValues = {
                's0' : 'Unseasoned/Drilling Deeper',
                's1' : 'Rival Incursion/Escalation',
            //     's1': 'Rival Incursion',
            //     's2': 'Rival Escalation',
                's3' : 'Plaguefall/Critical Corruption',
            //     's3': 'Plaguefall',
            //     's4': 'Critical Corruption',
            //     's5': 'Drilling Deeper'
            };
            let seasonBox = document.getElementById('season')
            for (let season in seasonBoxValues) {
                let option = document.createElement('option');
                option.value = season;
                option.textContent = seasonBoxValues[season];
                seasonBox.appendChild(option);
            }
            seasonBox.value = seasonBoxValues[localStorages['seasonSelected']];
            seasonBox.selectedIndex = Object.keys(seasonBoxValues).indexOf(localStorages['seasonSelected']);

            if (!localStorages['fonts']) {
                await preloadFonts();
            } else {
                await loadFontsFromLocalStorageObj();
            }
            if (!localStorages['img']) {
                await preloadImagesAll();
            } else {
                await loadImgsFromLocalStorageAll();
            }

            var breakfast = await initialize(date);
            biomes = breakfast[0];
            dailyDeal = breakfast[1];
            breakfast = undefined;

        } catch (error) {
            // likely localStorages hashing is broken
            console.log(error);
            localStorage.clear();
            // resetGlobalVars();

            initTries += 1;
            if (initTries > 2) {
                let loadingElement = document.getElementById('loading');
                document.querySelector('.overlay').style.display = 'none';
                document.getElementById('background-video').style.display = 'none';
                document.getElementById('background-video').pause();
                loadingElement.style.top = '50%';
                loadingElement.style.fontSize = '35px';
                loadingElement.style.width = 'auto';
                loadingElement.innerHTML = `An error occurred. Please try clearing your cache and restarting the browser. If this message persists, consider opening an issue on the <a style="color: #1E90FF;" href="https://github.com/rolfosian/drgmissions/">Github</a> and include the stack trace:<br><br><em>${error.stack}</em>`;
                break
            }
            continue
        }
            document.getElementById('missionsCountdown').textContent = getMissionsRemainderTimeOnInit(date)
            var homepageScript = document.createElement('script');
            homepageScript.textContent = localStorages['homepageScript']
            document.head.appendChild(homepageScript);
            await onLoad();
            break
            // await homepageScript.onload();


            // homepageScript.src = "/static/homepage.js"
            // homepageScript.onload = async function () {
            //    await onLoad(); // bottom of homepage.js
            // };
    }
});
