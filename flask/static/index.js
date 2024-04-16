//img caching parameters
var primaryObjs = {
    'Mining Expedition': '/static/img/Mining_expedition_icon.png',
    'Egg Hunt': '/static/img/Egg_collection_icon.png',
    'On-Site Refining': '/static/img/Refining_icon.png',
    'Salvage Operation': '/static/img/Salvage_icon.png',
    'Escort Duty': '/static/img/Escort_icon.png',
    'Point Extraction': '/static/img/Point_extraction_icon.png',
    'Elimination': '/static/img/Elimination_icon.png',
    'Industrial Sabotage': '/static/img/Sabotage_icon.png'
};
var primaryObjsImages = {};

var primaryObjResources = {
    'hexagon' : '/static/img/hexagon.png',
    'Mining Expedition': '/static/img/Morkite_icon.png',
    'Egg Hunt': '/static/img/Alien_egg_icon.png',
    'On-Site Refining': '/static/img/Icon_PumpingJack_Core_Simplified_Workfile.png',
    'Salvage Operation': '/static/img/Icon_Salvage_Mules_Objective.png',
    'Escort Duty': '/static/img/Icon_FuelCannister_Simplified.png',
    'Point Extraction': '/static/img/Icons_Resources_Outline_Aquarq.png',
    'Elimination': '/static/img/Kill_Dreadnought_Objective_icon.png',
    'Industrial Sabotage': '/static/img/Icon_Facility_DataRack.png'
};
var primaryObjResourcesImages = {};

var secondaryObjs = {
    'ApocaBlooms': '/static/img/Apoca_bloom_icon.png',
    'Fossils': '/static/img/Fossil_icon.png',
    'Boolo Caps': '/static/img/Boolo_cap_icon.png',
    'Dystrum': '/static/img/Dystrum_icon.png',
    'Ebonuts': '/static/img/Ebonut_icon.png',
    'Fester Fleas': '/static/img/Fleas_icon.png',
    'Gunk Seeds': '/static/img/Gunk_seed_icon.png',
    'Hollomite': '/static/img/Hollomite_icon.png'
};
var secondaryObjsImages = {};

var complexities = {
    '1': '/static/img/Icons_complexity_1.png',
    '2': '/static/img/Icons_complexity_2.png',
    '3': '/static/img/Icons_complexity_3.png'
};
var complexitiesImages = {};

var lengths = {
    '1': '/static/img/Icons_length_1.png',
    '2': '/static/img/Icons_length_2.png',
    '3': '/static/img/Icons_length_3.png'
};
var lengthsImages = {};

var mutators = {
    'Critical Weakness': '/static/img/Mutator_critical_weakness_icon.png',
    'Gold Rush': '/static/img/Mutator_gold_rush_icon.png',
    'Double XP': '/static/img/Mutator_triple_xp_icon.png',
    'Golden Bugs': '/static/img/Mutator_golden_bugs_icon.png',
    'Low Gravity': '/static/img/Mutator_no_fall_damage_icon.png',
    'Mineral Mania': '/static/img/Mutator_mineral_mania_icon.png',
    'Rich Atmosphere': '/static/img/Mutator_rich_atmosphere_icon.png',
    'Volatile Guts': '/static/img/Mutator_volatile_guts_icon.png'
};
var mutatorsImages = {};

var warnings = {
    'Cave Leech Cluster': '/static/img/Warning_cave_leech_cluster_icon.png',
    'Exploder Infestation': '/static/img/Warning_exploder_infestation_icon.png',
    'Haunted Cave': '/static/img/Warning_haunted_cave_icon.png',
    'Lethal Enemies': '/static/img/Warning_lethal_enemies_icon.png',
    'Low Oxygen': '/static/img/Warning_low_oxygen_icon.png',
    'Mactera Plague': '/static/img/Warning_mactera_plague_icon.png',
    'Parasites': '/static/img/Warning_parasites_icon.png',
    'Regenerative Bugs': '/static/img/Warning_regenerative_bugs_icon.png',
    'Shield Disruption': '/static/img/Warning_shield_disruption_icon.png',
    'Elite Threat': '/static/img/Warning_elite_threat_icon.png',
    'Swarmageddon': '/static/img/Warning_swarmageddon_icon.png',
    'Lithophage Outbreak': '/static/img/Warning_lithophage_outbreak_icon.png',
    'Rival Presence': '/static/img/Warning_rival_presence_icon.png'
};
var warningsImages = {};

var secondaryObjsDD = {
    "Repair Minimules": "/static/img/Icon_Salvage_Mules_Objective_DDsecondaryobj.png",
    "Eliminate Dreadnought": "/static/img/Kill_Dreadnought_Objective_icon_DDsecondaryobj.png",
    "Mine Morkite": "/static/img/Morkite_icon_DDsecondaryobj.png",
    "Get Alien Eggs": "/static/img/Alien_egg_icon_DDsecondaryobj.png",
    "Black Box": "/static/img/Blackbox_icon_DDsecondaryobj.png"
};
var secondaryObjsDDImages = {};

var biomesDD = {
    'Crystalline Caverns': '/static/img/DeepDive_MissionBar_CrystalCaves.png',
    'Glacial Strata': '/static/img/DeepDive_MissionBar_GlacialStrata.png',
    'Radioactive Exclusion Zone': '/static/img/DeepDive_MissionBar_Radioactive.png',
    'Fungus Bogs': '/static/img/DeepDive_MissionBar_FungusBogs.png',
    'Dense Biozone': '/static/img/DeepDive_MissionBar_LushDownpour.png',
    'Salt Pits': '/static/img/DeepDive_MissionBar_SaltPits.png',
    'Sandblasted Corridors': '/static/img/DeepDive_MissionBar_Sandblasted.png',
    'Magma Core': '/static/img/DeepDive_MissionBar_MagmaCore.png',
    'Azure Weald': '/static/img/DeepDive_MissionBar_AzureWeald.png',
    'Hollow Bough': '/static/img/DeepDive_MissionBar_HollowBough.png'
};
var biomesDDImages = {};

var dailyDealResources = {
    'Bismor': '/static/img/Bismor_icon.png',
    'Croppa': '/static/img/Croppa_icon.png',
    'Enor Pearl': '/static/img/Enor_pearl_icon.png',
    'Jadiz': '/static/img/Jadiz_icon.png',
    'Magnite': '/static/img/Magnite_icon.png',
    'Umanite': '/static/img/Umanite_icon.png',
    'Credits': '/static/img/Credit.png',
    'Bubble': '/static/img/Icon_TradeTerminal_SaleBubble.png'
};
var dailyDealResourcesImages = {};

var fontNamesAndUrls = {
    'HammerBro101MovieBold-Regular' : '/static/img/HammerBro101MovieBold-Regular.ttf',
    'HammerBro101MovieThin-Regular' : '/static/HammerBro101MovieThin-Regular.woff',
    'Bungee-Regular' : '/static/img/Bungee-Regular.ttf',
    'RiftSoft-Regular' : '/static/img/RiftSoft-Regular.ttf',
    'BebasNeue' : '/static/img/BebasNeue-Regular.woff2'
};

async function preloadImages(imageObj, imageCache) {
    let promises = [];
    for (let key in imageObj) {
        let img = new Image();
        img.src = imageObj[key];
        let promise = new Promise((resolve, reject) => {
            img.onload = () => resolve();
            img.onerror = () => reject();
        });
        promises.push(promise);
        imageCache[key] = img;
    }
    await Promise.all(promises);
}
async function preloadImagesAll() {
    await Promise.all([
        preloadImages(primaryObjs, primaryObjsImages),
        preloadImages(primaryObjResources, primaryObjResourcesImages),
        preloadImages(secondaryObjs, secondaryObjsImages),
        preloadImages(complexities, complexitiesImages),
        preloadImages(lengths, lengthsImages),
        preloadImages(mutators, mutatorsImages),
        preloadImages(warnings, warningsImages),
        preloadImages(secondaryObjsDD, secondaryObjsDDImages),
        // preloadImages(biomesDD, biomesDDImages),
        preloadImages(dailyDealResources, dailyDealResourcesImages)
    ]);
}

async function preloadFonts(){
    let promises = [];
    let fonts = [];
    for (let fontName in fontNamesAndUrls) {
        let fontUrl = fontNamesAndUrls[fontName];
        let font = new FontFace(fontName, `url(${fontUrl})`);
        let promise = font.load();
        promises.push(promise);
        fonts.push(font);
    }
    await Promise.all(promises);
    for (let i = 0; i < fonts.length; i++) {
        document.fonts.add(fonts[i]);
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

function getNextDateMidnightUTC() {
    let now = new Date();
    let sysYear = now.getFullYear()
    let sysMonth = now.getMonth()
    let sysDate = now.getDate()
    let nows = new Date(Date.UTC(sysYear, sysMonth,  sysDate, 0, 0, 0, 0))
    nows.setUTCDate(nows.getUTCDate()+1);

    let utcYear = nows.getUTCFullYear();
    let utcMonth = ('0' + (nows.getUTCMonth() + 1)).slice(-2);
    let utcDay = ('0' + nows.getUTCDate()).slice(-2);
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

// function roundTimeUpNextUpcoming(datetimeString) {
//     var datetimeMinutes = parseInt(datetimeString.slice(14, 16));
//     var datetime_unix = getCurrentDateTimeUTC_UNIX();
//     var nextHour = datetime_unix - (datetime_unix % 3600) + 3600;

//     var nextHourDate = new Date(nextHour * 1000);
    
//     var newYear = nextHourDate.getUTCFullYear();
//     var newMonth = ('0' + (nextHourDate.getUTCMonth() + 1)).slice(-2);
//     var newDay = ('0' + nextHourDate.getUTCDate()).slice(-2);
//     var newHour = ('0' + nextHourDate.getUTCHours()).slice(-2);
//     var newMinutes = ':00:00Z'

//     if (datetimeMinutes >= 30) {
//         newMinutes = ':30:00Z'
//     }

//     var newDatetime = newYear + '-' + 
//                       newMonth + '-' + 
//                       newDay + 'T' +
//                       newHour + newMinutes;

//     return newDatetime;
// }

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

// function roundTimeUp(datetimeString) {
//     var datetimeMinutes = parseInt(datetimeString.slice(14, 16));
//     if (datetimeMinutes >= 30) {
//         var datetime_unix = getCurrentDateTimeUTC_UNIX();
//         var nextHour = datetime_unix - (datetime_unix % 3600) + 3600;
    
//         var nextHourDate = new Date(nextHour * 1000);
        
//         var newYear = nextHourDate.getUTCFullYear();
//         var newMonth = ('0' + (nextHourDate.getUTCMonth() + 1)).slice(-2);
//         var newDay = ('0' + nextHourDate.getUTCDate()).slice(-2);
//         var newHour = ('0' + nextHourDate.getUTCHours()).slice(-2);
    
//         var newDatetime = newYear + '-' + 
//                           newMonth + '-' + 
//                           newDay + 'T' +
//                           newHour + ':00:00Z';
//     } else {
//         var newDatetime = datetimeString.slice(0, 14) + '30:00Z';
//     }
//     return newDatetime;
// }

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
    while (true) {
        const targetMinutes59 = [29, 59];
        const currentDate = new Date();
        const currentMinute = currentDate.getMinutes();
        const currentSecond = currentDate.getSeconds() + currentDate.getMilliseconds() / 1000;
        if (currentSecond > 58.50 && inList(targetMinutes59, currentMinute)) {
            await sleep(1500)
            continue
        }
        break
    }
}

// async function loadJSON(filePath) {
//     try {
//       const response = await fetch(filePath);
//       const data = await response.json();
//       return data;
//     } catch (error) {
//       throw error;
//     }
// }

async function loadJSON(filePath, maxRetries = 3, retryDelay = 2000) {
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

function getDomainURL(){
    var currentDomain = window.location.protocol + "//" + window.location.hostname;
    if (window.location.port !== "") {
        currentDomain += ":" + window.location.port;
    }
    return currentDomain
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

async function getCurrentDaysJson() {
    const currentDate = getCurrentDateTimeUTC().split('T')[0];
    return await loadJSON(getDomainURL()+`/static/json/bulkmissions/${currentDate}.json`)
}
function getCurrentMissionData() {
    const datetime = roundTimeDown(getCurrentDateTimeUTC())
    return currentDaysJson[datetime]
}
function getUpcomingMissionData() {
    const datetime = roundTimeUp(getCurrentDateTimeUTC())
    return currentDaysJson[datetime]
}
function getNextUpcomingMissionData() {
    const datetime = roundTimeUp(getCurrentDateTimeUTC())
}

async function getDeepDiveData() {
    let datetime = getPreviousThursdayTimestamp()
    datetime = replaceCharactersAtIndices(datetime, [[13, '-'], [16,'-']])
    let data;
    try {
        data = await loadJSON(getDomainURL()+`/static/json/DD_${datetime}.json`)
    } catch {
    }
    return data
}

function renderMission(m_d) {
    const div = document.createElement('div');
    div.classList.add('mission-hover-zoom')
    div.classList.add('mission')
    div.id = m_d['CodeName']

    const canvas = document.createElement('canvas');
    canvas.title = m_d["CodeName"]
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
        'Salvage Operation,default': '3'
    };

    const hexagon = primaryObjResourcesImages['hexagon']
    ctx.drawImage(hexagon, 21, 190, hexagon.width * 0.32, hexagon.height * 0.32);
    drawResource(m_d['PrimaryObjective'], m_d['Complexity'], m_d['Length']);


    function drawResource() {
        const resource = primaryObjResourcesImages[m_d['PrimaryObjective']];
        let scaleFactor;
        if (m_d['PrimaryObjective'] === 'Mining Expedition') scaleFactor = 0.18;
        else if (m_d['PrimaryObjective'] === 'Egg Hunt') scaleFactor = 0.20;
        else scaleFactor = 0.1;

        ctx.drawImage(resource, 44, 205, resource.width * scaleFactor, resource.height * scaleFactor);

        const text = getText(m_d['PrimaryObjective'], m_d['Complexity'], m_d['Length']);
        drawText(text, 'HammerBro101MovieBold-Regular', '35',  m_d['PrimaryObjective']);
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
        ctx.fillText(text, 69, y);
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
        var Biomes = dictionary[season]['Biomes']
        renderedBiomes[season] = {}
        renderedBiomes[season]['Biomes'] = {}

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
    var Biomes = dictionary['Biomes']
    renderedBiomes['Biomes'] = {}
    renderedBiomes['timestamp'] = dictionary['timestamp']

    for (let biome in Biomes) {
        let biomeMissions = Biomes[biome];
        let biome1 = [];

        for (let i = 0; i < biomeMissions.length; i++) {
            let mission = biomeMissions[i];
            let mission1 = {}

            if (mission.hasOwnProperty('season_modified')) {
                mission1['season_modified'] = {}
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
            // mission_icon_canvas_div.name = biome+mission1['CodeName']+mission1['season']

            let mission_icon_canvas_div = renderMission(mission);
            mission1['rendered_mission'] = mission_icon_canvas_div;

            // biome1[mission_icon_canvas_div.name] = mission1
            biome1.push(mission1);
        }
        renderedBiomes['Biomes'][biome] = biome1;
    };
    return renderedBiomes;
}
function renderBiomes(dictionary) {
    let bs;
    if (dictionary.hasOwnProperty('s0')) {
        bs = renderBiomes_(dictionary)
        // console.log(bs['timestamp'])
        return bs
    } else {
        bs =  renderBiomesFlat(dictionary)
        // console.log(bs['timestamp'])
        return bs
    }
}

function isMidnightUpcoming(date) {
    return roundTimeDown(date.toISOString()).slice(11, 19) == '23:30:00'
}

// async function getBiomesMidnight(date) {
//     let upcomingMidnight = getNextDateMidnightUTC();
//     let nextDay = upcomingMidnight.split('T')[0];

//     if (biomes) {
//         let currentBiomes = biomes[1];
//         currentDaysJson = await loadJSON(getDomainURL()+`/static/json/bulkmissions/${nextDay}.json`);
//         let upcomingBiomes = renderBiomes(currentDaysJson[upcomingMidnight]);
//         return [currentBiomes, upcomingBiomes];
//     } else {
//         let results = await Promise.all([
//             getCurrentDaysJson(),
//             loadJSON(getDomainURL()+`/static/json/bulkmissions/${nextDay}.json`)
//         ])
//         let currentBiomes = renderBiomes(results[0][roundTimeDown(date.toISOString())]);
//         currentDaysJson = results[1];
//         let upcomingBiomes = renderBiomes(currentDaysJson[upcomingMidnight]);
//         return [currentBiomes, upcomingBiomes];
//     }   
// }
async function tempCacheUpcomingBiomes(isMidnightUpcoming_, date) {
    let currentBiomes = biomes[1];
    let upcomingBiomes;
    if (isMidnightUpcoming_) {
        let upcomingMidnight = getNextDateMidnightUTC();
        let nextDay = upcomingMidnight.split('T')[0];
        if (tempCurrentDaysJson) {
            currentDaysJson = tempCurrentDaysJson;
            tempCurrentDaysJson = undefined
        } else {
            currentDaysJson = await loadJSON(getDomainURL()+`/static/json/bulkmissions/${nextDay}.json`);
        }
        upcomingBiomes = renderBiomes(currentDaysJson[roundTimeUpNextUpcoming(date.toISOString())]);
        tempBiomes = [currentBiomes, upcomingBiomes]
        console.log(tempBiomes)
    } else {
        if (roundTimeDown(date.toISOString()).split('T')[1] == '23:00:00Z') {
            let upcomingMidnight = getNextDateMidnightUTC();
            let nextDay = upcomingMidnight.split('T')[0];
            tempCurrentDaysJson = await loadJSON(getDomainURL()+`/static/json/bulkmissions/${nextDay}.json`);
            upcomingBiomes = renderBiomes(tempCurrentDaysJson[roundTimeUpNextUpcoming(date.toISOString())]);
        } else {
            upcomingBiomes = renderBiomes(currentDaysJson[roundTimeUpNextUpcoming(date.toISOString())]);
        }
        tempBiomes = [currentBiomes, upcomingBiomes]
        console.log(tempBiomes)
        // console.log(tempBiomes)
    }
}

function getBiomesOnInit() {
    let dictionary = getCurrentMissionData(currentDaysJson);
    let currentBiomes = renderBiomes(dictionary);
    let dictionary_ = getUpcomingMissionData(currentDaysJson);
    let upcomingBiomes = renderBiomes(dictionary_);
    return [currentBiomes, upcomingBiomes];
}

async function getBiomesMidnightOnInit(date) {
    let upcomingMidnight = getNextDateMidnightUTC();
    let nextDay = upcomingMidnight.split('T')[0];
    let results = await Promise.all([
        getCurrentDaysJson(),
        loadJSON(getDomainURL()+`/static/json/bulkmissions/${nextDay}.json`)
    ]);
    let currentBiomes = renderBiomes(results[0][roundTimeDown(date.toISOString())]);
    currentDaysJson = results[1];
    tempCurrentDaysJson = currentDaysJson;
    let upcomingBiomes = renderBiomes(currentDaysJson[upcomingMidnight]);
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
        currentDaysJson = tempCurrentDaysJson;
    }
    let upcomingBiomes = tempBiomes[1];
    return [currentBiomes, upcomingBiomes];
}

function changeSeason(Biomes, season) {
    arrayBiomes(Biomes, season);
    if (document.getElementById('currentButton').textContent == 'Click here to see current missions') {
        document.getElementById('currentButton').click();
    }
}

function toggleSeason4(Biomes, bool) {
    if (bool) {
        document.getElementById("season").value = 's4'
        arrayBiomes(Biomes, 's4');
    } else {
        document.getElementById("season").value = 's0'
        arrayBiomes(Biomes, 's0');
    }
}

async function refreshBiomes(isMidnightUpcoming_) {
    if (isMidnightUpcoming_) { // this could probably be consolidated into one block but im not going to fix what isnt broken for now
        biomes = await getBiomesMidnight();
        tempBiomes = undefined;
    } else {
        biomes = getBiomes();
        tempBiomes = undefined;
    }
    arrayBiomes(biomes, document.getElementById("season").value);
    if (document.getElementById('currentButton').textContent == 'Click here to see current missions') {
        document.getElementById('currentButton').click();
    }
    console.log(biomes[0]['timestamp'])
    console.log(biomes[1]['timestamp'])
}
async function refreshDailyDeal() {
    dailyDeal = await getDailyDealData();
    arrayDailyDeal(dailyDeal)
}
async function refreshDeepDives() {
    ddData = await getDeepDiveData();
    if (ddData) {
        arrayDeepDives(ddData)
    } else {
        let deepDiveNormalDiv = document.getElementById('Deep Dive Normal');
        while(deepDiveNormalDiv.hasChildNodes()) {
            deepDiveNormalDiv.removeChild(deepDiveNormalDiv.lastChild);
        };
        deepDiveNormalDiv.appendChild(document.createElement("br"));
        let spanElement = document.createElement("span");
        spanElement.className = "scanners";
        spanElement.textContent = "// AWAITING UP TO DATE DATA \\\\";
        deepDiveNormalDiv.appendChild(spanElement)

        var deepDiveEliteDiv = document.getElementById('Deep Dive Elite');
        while(deepDiveEliteDiv.hasChildNodes()) {
            deepDiveEliteDiv.removeChild(deepDiveEliteDiv.lastChild);
        };
        deepDiveEliteDiv.appendChild(document.createElement("br"));
        spanElement = document.createElement("span");
        spanElement.className = "scanners";
        spanElement.textContent = "// AWAITING UP TO DATE DATA \\\\";
        deepDiveEliteDiv.appendChild(spanElement)
    } 
}

function arrayDailyDeal(dailyDeal) {
    let dailyDealCanvas = renderDailyDeal(dailyDeal)
    let dailyDealDiv = document.getElementById('DailyDeal')
    while(dailyDealDiv.hasChildNodes()) {
        dailyDealDiv.removeChild(dailyDealDiv.lastChild);
    };
    dailyDealDiv.appendChild(dailyDealCanvas)
}

function arrayBiomes_(Biomes, season) { // deprecated, may need for debugging come season 5
    var currentBiomes = Biomes[0][season]['Biomes']
    var nextBiomes = Biomes[1][season]['Biomes']
    
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
                biomeDiv.appendChild(mission['rendered_mission'])
            };
        };

        biomeDiv = document.getElementById(`next${biome}`)
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
                biomeDiv.appendChild(mission['rendered_mission'])
            };
        };
    };
    equalizeGridItems()
}

function arrayBiomes(Biomes, season) { // may need for debugging
    if (Biomes[0].hasOwnProperty('s0')) {
        arrayBiomes_(Biomes, season)
    } else {
        arrayBiomesFlat(Biomes, season)
    }
}
function arrayBiomesFlat(Biomes, season) {
    let currentBiomes = Biomes[0]['Biomes']
    let nextBiomes = Biomes[1]['Biomes']
    let biomeMissions;
    let isS0 = season === 's0'
    
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
            biomeDiv.appendChild(spanElement)
        } else {
            biomeMissions = currentBiomes[biome];
            for (let i = 0; i < biomeMissions.length; i++) {
                let mission = biomeMissions[i];
                if (isS0 && mission['season'] != season) {
                    continue
                }
                if (mission.hasOwnProperty('season_modified') && !isS0) {
                    mission = mission['season_modified'][season]
                }
                biomeDiv.appendChild(mission['rendered_mission']);
            }
        }

        if (!(biome in nextBiomes)) {
            let spanElement = document.createElement("span");
            spanElement.className = "scanners";
            spanElement.textContent = "// SCANNERS OUT OF RANGE \\\\";
            nextBiomeDiv.appendChild(spanElement)
        } else {
            biomeMissions = nextBiomes[biome];
            for (let i = 0; i < biomeMissions.length; i++) {
                let mission = biomeMissions[i];
                if (isS0 && mission['season'] != season) {
                    continue
                }
                if (mission.hasOwnProperty('season_modified') && !isS0) {
                    mission = mission['season_modified'][season]
                }
                nextBiomeDiv.appendChild(mission['rendered_mission']);
            }
        }
    };
    equalizeGridItems()
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
        tempCtx.strokeStyle = 'black'
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

    shadowText(codename, codenameX, y+15, 'black', fontSize, mainFontName)
    drawText(codename, codenameX, y+15, 'white', fontSize, mainFontName)

    canvas.getContext('2d').drawImage(tempCanvas, 0, 0)
}

function renderDeepDiveBiomeCodename(biome, codename) {
    const texts = ['CODENAME: ', codename];
    const fontSize = 45;
    const canvas = document.createElement('canvas');
    canvas.classList.add('dd-biome')
    const ctx = canvas.getContext('2d');
    for (let biomeName in biomesDD) {
        if (biomeName == biome) {
            const img = new Image()
            img.src = biomesDD[biomeName]
            img.onload = () => {
                canvas.width = img.width;
                canvas.height = img.height;
                ctx.drawImage(img, 0, 0);
                addShadowedTextToImage(canvas, texts, fontSize);
            }
            break
        }
    }
    // const img = biomesDDImages[biome];
    return canvas;
}

function renderDeepDiveStage(m_d, stageCount) {
    const div = document.createElement('div');
    div.classList.add('mission-hover-zoom')
    div.classList.add('mission')
    div.id = m_d['CodeName']

    const canvas = document.createElement('canvas');
    canvas.title = `Stage ${stageCount.toString()}`
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
        'Salvage Operation,default': '3'
    };

    const hexagon = primaryObjResourcesImages['hexagon']
    ctx.drawImage(hexagon, 21, 190, hexagon.width * 0.32, hexagon.height * 0.32);
    drawResource(m_d['PrimaryObjective'], m_d['Complexity'], m_d['Length']);

    function drawResource() {
        const resource = primaryObjResourcesImages[m_d['PrimaryObjective']];
        let scaleFactor;
        if (m_d['PrimaryObjective'] === 'Mining Expedition') scaleFactor = 0.18;
        else if (m_d['PrimaryObjective'] === 'Egg Hunt') scaleFactor = 0.20;
        else scaleFactor = 0.1;

        ctx.drawImage(resource, 44, 205, resource.width * scaleFactor, resource.height * scaleFactor);

        const text = getText(m_d['PrimaryObjective'], m_d['Complexity'], m_d['Length']);
        drawText(text, 'HammerBro101MovieBold-Regular', '35',  m_d['PrimaryObjective']);
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
        ctx.fillText(text, 69, y);
    }
    ctx.save();
    resizeCanvas(div, canvas, 0.35, 0.35)
    div.appendChild(canvas)
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
        let stage = stages[i]
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
        var deepDiveNormalDiv = document.getElementById('Deep Dive Normal');
        var deepDiveEliteDiv = document.getElementById('Deep Dive Elite');
    
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
            stage = normalStages[i]
            stageCount += 1;
            stageDiv = renderDeepDiveStage(stage, stageCount);
            deepDiveNormalDiv.appendChild(stageDiv);
        };
    
        var eliteStages = sortDeepDiveStages(deepDiveElite["Stages"]);
        stageCount = 0;
        for (var i = 0; i < eliteStages.length; i++) {
            stage = eliteStages[i]
            stageCount += 1;
            stageDiv = renderDeepDiveStage(stage, stageCount);
            deepDiveEliteDiv.appendChild(stageDiv);
        };
    } catch (error) {
        // deepDiveData is undefined
    }
}

async function getDailyDealData() {
    var datetime = getCurrentDateMidnightUTC()
    datetime = replaceCharactersAtIndices(datetime, [[13, '-'], [16,'-']])
    var data = await loadJSON(getDomainURL()+`/static/json/dailydeals/${datetime}.json`)
    return data
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
    var resourceAmount = dealDict['ResourceAmount']
    var resource = dealDict['Resource']

    ctx.fillStyle = 'rgba(0, 44, 81, 255)';
    ctx.fillRect(0, 0, 400, 635);
    ctx.fillStyle = 'rgba(57, 148, 136, 255)';
    ctx.fillRect(0, 0, 400, 120);
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    var text = "TODAY'S OFFER:";
    var fillStyle = 'black';
    drawText(text, 200, 30, 'black', 45, 'HammerBro101MovieBold-Regular');
    drawText(resource, 200, 75, 'black', 60, 'Bungee-Regular')

    var resourceImg = dailyDealResourcesImages[resource];
    var text = resourceAmount.toString();
    var fontName = 'Bungee-Regular';
    ctx.font = `75px ${fontName}`
    var textWidth = ctx.measureText(text).width
    drawText(text, 200, 200, 'white', 75, fontName)

    var resourceImage = resizeImage(resourceImg, resourceImg.width*0.3, resourceImg.height*0.3)
    var x = ((canvas.width / 2) - textWidth) / 2;

    ctx.drawImage(resourceImage, x+25, 150);
    ctx.save()

    ctx.translate(canvas.width, 0);
    ctx.scale(-1, 1);
    ctx.drawImage(resourceImage, x+25, 150);
    ctx.restore();

    drawText(dealDict['DealType'], 200, 152, 'white', 35, 'Bungee-Regular');
    drawText(buyOrGet[dealDict['DealType']], 200, 290, 'white', 35, 'Bungee-Regular');

    var creditsImage = dailyDealResourcesImages['Credits'];
    creditsImage = resizeImage(creditsImage, creditsImage.width*0.4, creditsImage.height*0.4)

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
    
    text = Math.round(dealDict['ChangePercent']).toString()
    if (text.length == 2) {
        text = text.split('')
        let digit1 = text[0];
        drawText(digit1, 248, 433, 'black', 75, 'Bungee-Regular')
        let digit2 = text[1]+'%';
        drawText(digit2, 340, 433, 'black', 75, 'Bungee-Regular')
        
    } else {
        text += '%'
        drawText(text, 321, 433, 'black', 75, 'Bungee-Regular')
    }

    text = saveProfit[dealDict['DealType']]
    drawText(text, 310, 480, 'black', 30, 'Bungee-Regular')
    ctx.restore()

    resizeCanvas(div, canvas, 0.5, 0.5)
    canvas.classList.add('daily_trade')
    div.appendChild(canvas)
    return div
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
        let children_ = container.children;
        for (var i = 0; i < children_.length; i++) {
            if (children_[i].tagName.toLowerCase() === 'div') {
                if (children_[i].children.length == 1) {
                    scanners.push(container);
                }
            }
        }
    });
    containers.forEach(container => {
        container.style.height = "auto"
        let height = container.offsetHeight
        if (height != 0) {
            container.style.height = `${height-10}px`
            if (!(inList(scanners, container))) {
                heights.push(height)
            }
        }
    });
    if (window.matchMedia("(min-width: 1440px)").matches) {
        scanners.forEach(container => {
            container.style.height = `${mostCommonNumber(heights)-10}px`
        })
    } else {
        scanners.forEach(container => {
            container.style.height = `auto`
        })
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
    checkOverflowAndFixScanners(gridItems)
}
window.addEventListener('resize', function(event) {
    if (initialized) {
        equalizeGridItems()
    }
});
async function initialize() {
    let biomes_;
    let ddData_;
    let dailyDeal_;
    await waitRotation()

    let date = new Date();
    if (isMidnightUpcoming(date)) {
        let results = await Promise.all([
            getBiomesMidnightOnInit(date),
            getDeepDiveData(),
            getDailyDealData()
        ])
        biomes_ = results[0];
        console.log(biomes_)
        console.log(biomes_[0]['timestamp'])
        console.log(biomes_[1]['timestamp'])
        ddData_ = results[1];
        dailyDeal_ = results[2]
        // for (let i = 0; i < results.length; i++) {
        //     let result = results[i]
        //     if (Array.isArray(result)) {
        //         biomes_ = result[0];
        //     } else if ('Deep Dives' in result) {
        //         ddData_ = result;
        //     } else {
        //         dailyDeal_ = result;
        //     }
        // }
    } else {
        currentDaysJson = await getCurrentDaysJson();
        let results = await Promise.all([
            getDeepDiveData(),
            getDailyDealData()
        ]);
        biomes_ = getBiomesOnInit();
        console.log(biomes_)
        console.log(biomes_[0]['timestamp'])
        console.log(biomes_[1]['timestamp'])
        ddData_ = results[0];
        dailyDeal_ = results[1]
        // for (let i = 0; i < results.length; i++) {
        //     let result = results[i]
        //     if (Array.isArray(result)) {
        //         biomes_ = result;
        //     } else if ('Deep Dives' in result) {
        //         ddData_ = result;
        //     } else {
        //         dailyDeal_ = result;
        //     }
        // }
    }
    


    let currentDatetime = date.toISOString().slice(0, 10);
    // currentDatetime = replaceCharactersAtIndices(currentDatetime, [[13, '-'], [16,'-']]);
    let currentDateTimeHREF = getDomainURL()+'/static/json/bulkmissions/'+currentDatetime+'.json';

    let nextDatetime = getNextDateMidnightUTC().split('T')[0];
    // nextDatetime = replaceCharactersAtIndices(nextDatetime, [[13, '-'], [16,'-']]);
    let nextDateTimeHREF = getDomainURL()+'/static/json/bulkmissions/'+nextDatetime+'.json';

    let ddDatetime = getPreviousThursdayTimestamp();
    ddDatetime = replaceCharactersAtIndices(ddDatetime, [[13, '-'], [16,'-']]);
    let ddDatetimeHREF = getDomainURL()+'/static/json/DD_'+ddDatetime+'.json';

    let dailyDealDatetime = getCurrentDateMidnightUTC();
    dailyDealDatetime = replaceCharactersAtIndices(dailyDealDatetime, [[13, '-'], [16,'-']]);
    let dailyDealHREF = getDomainURL()+`/static/json/dailydeals/${dailyDealDatetime}.json`;


    let html = `
    <div id="countdowncontainer">
    <button id="backgroundButton">Hide background</button><button id="buttonsbutton">x</button><br>
    <div id=DAILYDEAL><div id="dailydealhead">NEW DAILY DEAL IN<br><span id="DailyDealcountdown"></span></div><div id="DailyDeal" class="daily_deal_container"></div></div>
    <button id="dailydealbutton">Click here to see Daily Deal</button><br>
    <div id="missionscountdown">NEW MISSIONS IN<br>
    <span id="countdown"></span></div><button id="slideButton">Hide countdown</button><br>
    <button id="currentButton">Click here to see upcoming missions</button>
    <br>
    <div id="seasonSelect" class="seasonselect">
    <button id="seasonClick" class="seasonBox">Season 4 Toggle</button>
    <input type="checkbox" id="season" class="seasonBox" value="s0" disabled>
    <!-- <select id="season" name="season" class="seasonBox" disabled></select> -->
    </div>
    </div>
    
    
    <div id="current">
    <div class="grid-container">
    
    <h2>
    <div class="biome-container">
    <img title="Abundant: Magnite; Scarce: Umanite" class="image-container" src="/static/DeepDive_MissionBar_GlacialStrata.png">
    <br><div id="Glacial Strata" class="missions">
    </div>
    </div>
    </h2>
    
    <h2>
    <div class="biome-container">
    <img title="Abundant: Jadiz; Scarce: Bismor" class="image-container" src="/static/DeepDive_MissionBar_CrystalCaves.png">
    <br><div id="Crystalline Caverns" class="missions">
    </div>
    </div>
    </h2>
    
    <h2>
    <div class="biome-container">
    <img title="Abundant: Enor Pearl; Scarce: Bismor" class="image-container" src="/static/DeepDive_MissionBar_SaltPits.png">
    <br><div id="Salt Pits">
    </div>
    </div>
    </h2>
    
    <h2>
    <div class="biome-container">
    <img title="Abundant: Magnite; Scarce: Croppa" class="image-container" src="/static/DeepDive_MissionBar_MagmaCore.png">
    <br><div id="Magma Core" class="missions">
    </div>
    </div>
    </h2>
    
    <h2>
    <div class ="biome-container">
    <img title="Abundant: Croppa; Scarce: Umanite" class="image-container" src="/static/DeepDive_MissionBar_AzureWeald.png">
    <br><div id="Azure Weald" class="missions">
    </div>
    </div>
    </h2>
    
    <h2>
    <div class="biome-container">
    <img title="Abundant: Enor Pearl; Scarce: Bismor" class="image-container" src="/static/DeepDive_MissionBar_Sandblasted.png">
    <br><div id="Sandblasted Corridors" class="missions">
    </div>
    </div>
    </h2>
    
    <h2>
    <div class="biome-container">
    <img title="Abundant: Croppa; Scarce: Jadiz" class="image-container" src="/static/DeepDive_MissionBar_FungusBogs.png">
    <br><div id="Fungus Bogs" class="missions">
    </div>
    </div>
    </h2>
    
    <h2>
    <div class="biome-container">
    <img title="Abundant: Umanite; Scarce: Enor Pearl" class="image-container" src="/static/DeepDive_MissionBar_Radioactive.png">
    <br><div id="Radioactive Exclusion Zone" class="missions">
    </div>
    </div>
    </h2>
    
    <h2>
    <div class="biome-container">
    <img title="Abundant: Bismor; Scarce: Umanite" class="image-container" src="/static/DeepDive_MissionBar_LushDownpour.png">
    <br><div id="Dense Biozone" class="missions">
    </div>
    </div>
    </h2>
    
    <h2>
    <div class="biome-container">
    <img title="Abundant: Jadiz; Scarce: Bismor" class="image-container" src="/static/DeepDive_MissionBar_HollowBough.png">
    <br><div id="Hollow Bough" class="missions">
    </div>
    </div>
    </h2>
    
    </div>
    </div>
    

    <div id="upcoming" style="visibility: hidden;">
    <div class="grid-container">
    
    <h2>
    <div class="biome-container">
    <img title="Abundant: Magnite; Scarce: Umanite" class="image-container" src="/static/DeepDive_MissionBar_GlacialStrata.png">
    <br><div id="nextGlacial Strata" class="missions">
    </div>
    
    </div>
    </h2>
    
    <h2>
    <div class="biome-container">
    <img title="Abundant: Jadiz; Scarce: Bismor" class="image-container" src="/static/DeepDive_MissionBar_CrystalCaves.png">
    <br><div id="nextCrystalline Caverns" class="missions">
    </div>
    </div>
    </h2>
    
    <h2>
    <div class="biome-container">
    <img title="Abundant: Enor Pearl; Scarce: Bismor" class="image-container" src="/static/DeepDive_MissionBar_SaltPits.png">
    <br><div id="nextSalt Pits" class="missions">
    </div>
    </div>
    </h2>
    
    <h2>
    <div class="biome-container">
    <img title="Abundant: Magnite; Scarce: Croppa" class="image-container" src="/static/DeepDive_MissionBar_MagmaCore.png">
    <br><div id="nextMagma Core" class="missions">
    </div>
    </div>
    </h2>
    
    <h2>
    <div class ="biome-container">
    <img title="Abundant: Croppa; Scarce: Umanite" class="image-container" src="/static/DeepDive_MissionBar_AzureWeald.png">
    <br><div id="nextAzure Weald" class="missions">
    </div>
    
    </div>
    </h2>
    
    <h2>
    <div class="biome-container">
    <img title="Abundant: Enor Pearl; Scarce: Bismor" class="image-container" src="/static/DeepDive_MissionBar_Sandblasted.png">
    <br><div id="nextSandblasted Corridors">
    </div>
    </h2>
    
    <h2>
    <div class="biome-container">
    <img title="Abundant: Croppa; Scarce: Jadiz" class="image-container" src="/static/DeepDive_MissionBar_FungusBogs.png">
    <br><div id="nextFungus Bogs" class="missions">
    </div>
    </div>
    </h2>
    
    <h2>
    <div class="biome-container">
    <img title="Abundant: Umanite; Scarce: Enor Pearl" class="image-container" src="/static/DeepDive_MissionBar_Radioactive.png">
    <br><div id="nextRadioactive Exclusion Zone" class="missions">
    </div>
    </div>
    </h2>
    
    <h2>
    <div class="biome-container">
    <img title="Abundant: Bismor; Scarce: Umanite" class="image-container" src="/static/DeepDive_MissionBar_LushDownpour.png">
    <br><div id="nextDense Biozone" class="missions">
    </div>
    </div>
    </h2>
    
    <h2>
    <div class="biome-container">
    <img title="Abundant: Jadiz; Scarce: Bismor" class="image-container" src="/static/DeepDive_MissionBar_HollowBough.png">
    <br><div id="nextHollow Bough" class="missions">
    </div>
    </div>
    </h2>

    </div>
    </div>
    
    
    <div class="grid-container">

    <div class="dd-container">
    <h2>
    <img class="image-container" src="/static/dd.png">
    <div id="Deep Dive Normal" class="dd-missions">
    </div>
    </h2>
    </div>

    <div class="dd-container">
    <h2>
    <img class="image-container" src="/static/edd.png">
    <div id="Deep Dive Elite" class="dd-missions">
    </div>
    </h2>
    </div>

    </div>
    
    <div>
    
    <div class="ddscountdown">NEW DEEP DIVES IN</div>
    <span id="ddcountdown"></span>
    <hr>
    </div>

    <div class="jsonc">
    <div class="jsonlinks"><span style="color: white;font-size: 30px;font-family: BebasNeue, sans-serif;"> <a class="jsonlink" href="${currentDateTimeHREF}">TODAY'S MISSION DATA</a> | <a class="jsonlink" href="${nextDateTimeHREF}">TOMORROW'S MISSION DATA</a> | <a class="jsonlink" href="${ddDatetimeHREF}">CURRENT DEEP DIVE DATA</a> | <a class="jsonlink" href="${dailyDealHREF}">CURRENT DAILY DEAL DATA</a> | <a class="jsonlink" href="/static/xp_calculator.html">CLASS XP CALCULATOR</a> | <a class="jsonlink" href="https://github.com/rolfosian/drgmissions/">GITHUB</a></span> </div>
    <span class="credits">Send credits (eth): 0xb9c8591A80A3158f7cFFf96EC3c7eA9adB7818E7</span>
    </div>
    <p class='gsgdisclaimer'><i>This website is a third-party platform and is not affiliated, endorsed, or sponsored by Ghost Ship Games. The use of Deep Rock Galactic's in-game assets on this website is solely for illustrative purposes and does not imply any ownership or association with the game or its developers. All copyrights and trademarks belong to their respective owners. For official information about Deep Rock Galactic, please visit the official Ghost Ship Games website.</i></p></div>
    `

    let mainContent = document.getElementById('mainContent')
    mainContent.innerHTML = html

    // let seasonBoxValues = {
    //     's0' : 'No Season',
    //     's1': 'Season 1',
    //     's2': 'Season 2', 
    //     's3': 'Season 3', 
    //     's4': 'Season 4', 
    //     's5': 'Season 5'
    // }
    // let seasonBox = document.getElementById('season')
    // for (let season in seasonBoxValues) {
    //     if (season in biomes_[0]) {
    //         let option = document.createElement('option');
    //         option.value = season;
    //         option.textContent = seasonBoxValues[season];
    //         seasonBox.appendChild(option);
    //     }
    // }

    return [biomes_, dailyDeal_, ddData_]
}

// document.addEventListener('upcomingBiomesCachingEvent', (event) => {
//     let cache
// })

var tempBiomes;
var tempCurrentDaysJson;
var currentDaysJson;
var biomes;
var dailyDeal;
var ddData;
var initialized = false;
var cacheActive = false;
document.addEventListener('DOMContentLoaded', async function() {
    // try {
        await preloadFonts()
        await preloadImagesAll()
        var imgs = await initialize();
        biomes = imgs[0];
        dailyDeal = imgs[1];
        ddData = imgs[2];

        var jqueryScript = document.createElement('script');
        jqueryScript.src = "/static/jquery.min.js";
        document.head.appendChild(jqueryScript);
        jqueryScript.onload = function() {
            var homepageScript = document.createElement('script');
            homepageScript.src = "/static/homepage.js";
            document.head.appendChild(homepageScript);
            homepageScript.onload = function (){
                onLoad(); // bottom of homepage.js
            };
        };
    // } catch (error) {
    //     alert(error);
    //     location.reload();
    // }
});