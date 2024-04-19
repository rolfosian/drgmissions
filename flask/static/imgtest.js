function replaceCharactersAtIndices(inputString, replacements) {
    let result = inputString;
    replacements.forEach(([index, newCharacter]) => {
        if (index >= 0 && index < inputString.length) {
            result = result.substring(0, index) + newCharacter + result.substring(index + 1);
        }
    });
    return result;
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

function getCurrentDateTimeUTC_UNIX() {
    return Math.floor(new Date(getCurrentDateTimeUTC()).getTime() / 1000);
}

function roundTimeUp(datetimeString) {
    var datetimeMinutes = parseInt(datetimeString.slice(14, 16));
    if (datetimeMinutes >= 30) {
        var datetime_unix = getCurrentDateTimeUTC_UNIX();
        var nextHour = datetime_unix - (datetime_unix % 3600) + 3600;
    
        var nextHourDate = new Date(nextHour * 1000);
        
        var newYear = nextHourDate.getUTCFullYear();
        var newMonth = ('0' + (nextHourDate.getUTCMonth() + 1)).slice(-2);
        var newDay = ('0' + nextHourDate.getUTCDate()).slice(-2);
        var newHour = ('0' + nextHourDate.getUTCHours()).slice(-2);
    
        var newDatetime = newYear + '-' + 
                          newMonth + '-' + 
                          newDay + 'T' +
                          newHour + ':00:00Z';
    } else {
        var newDatetime = datetimeString.slice(0, 14) + '30:00Z';
    }
    return newDatetime;
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

async function loadJSON(filePath) {
    try {
      const response = await fetch(filePath);
      const data = await response.json();
      return data;
    } catch (error) {
      throw error;
    }
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

async function getCurrentMissionData() {
    var datetime = roundTimeDown(getCurrentDateTimeUTC())
    datetime = replaceCharactersAtIndices(datetime, [[13, '-'], [16,'-']])
    datetime = 'drgmissions' // dev
    var data = await loadJSON(getDomainURL()+`/static/json/${datetime}.json`)
    return data
}
async function getUpcomingMissionData() {
    var datetime = roundTimeUp(getCurrentDateTimeUTC())
    datetime = replaceCharactersAtIndices(datetime, [[13, '-'], [16,'-']])
    datetime = 'drgmissionsupcoming' // dev
    var data = await loadJSON(getDomainURL()+`/static/json/${datetime}.json`)
    return data
}
function resizeCanvas(div, canvas, x, y) {
    const newWidth = canvas.width * x;
    const newHeight = canvas.height * y;

    canvas.style.width = `${newWidth.toString()}px`;
    canvas.style.height = `${newHeight.toString()}px`;
    div.style.width = `${newWidth.toString()}px`;
    div.style.height = `${newHeight.toString()}px`;
}

async function getDailyDealData() {
    var datetime = getCurrentDateMidnightUTC()
    datetime = replaceCharactersAtIndices(datetime, [[13, '-'], [16,'-']])
    var data = await loadJSON(getDomainURL()+`/static/json/dailydeals/${datetime}.json`)
    return data
}

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
    "Repair Minimules": "./static/img/Icon_Salvage_Mules_Objective_DDsecondaryobj.png",
    "Eliminate Dreadnought": "./static/img/Kill_Dreadnought_Objective_icon_DDsecondaryobj.png",
    "Mine Morkite": "./static//img/Morkite_icon_DDsecondaryobj.png",
    "Get Alien Eggs": "./static/img/Alien_egg_icon_DDsecondaryobj.png",
    "Black Box": "./static/img/Blackbox_icon_DDsecondaryobj.png"
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
        preloadImages(biomesDD, biomesDDImages),
        preloadImages(dailyDealResources, dailyDealResourcesImages)
    ]);
}

var fontNamesAndUrls = {
    'CarbonBold-W00-Regular' : '/static/img/CarbonBold-W00-Regular.ttf',
    'Bungee-Regular' : '/static/img/Bungee-Regular.ttf',
    'RiftSoft-Regular' : '/static/img/RiftSoft-Regular.ttf',
    'BebasNeue' : '/static/img/BebasNeue-Regular.woff2'
};

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

function renderMission(m_d, six) {
    const div = document.createElement('div');
    div.classList.add('mission-hover-zoom')
    div.classList.add('mission')
    div.id = m_d['CodeName']
    // Create a new canvas element
    const canvas = document.createElement('canvas');
    canvas.title = m_d["CodeName"]
    canvas.width = 350;
    canvas.height = 300;
    var ctx = canvas.getContext('2d');

    // Draw background
    ctx.fillStyle = 'rgba(0, 0, 0, 0)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw primary objective
    const primaryImg = primaryObjsImages[m_d['PrimaryObjective']];
    ctx.drawImage(primaryImg, 83, 58, primaryImg.width * 0.4, primaryImg.height * 0.4);

    // Draw secondary objective
    const secondaryImg = secondaryObjsImages[m_d['SecondaryObjective']];
    ctx.drawImage(secondaryImg, -11, -21, secondaryImg.width * 0.6, secondaryImg.height * 0.6);

    // Draw mission warnings if available
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

    // Draw mission mutator if available
    if (m_d['MissionMutator']) {
        const mutatorImg = mutatorsImages[m_d['MissionMutator']];
        ctx.drawImage(mutatorImg, 27, 92, mutatorImg.width * 0.38, mutatorImg.height * 0.38);
    }

    // Draw complexity and length icons
    const complexityImg = complexitiesImages[m_d['Complexity']];
    ctx.drawImage(complexityImg, 107, 2, complexityImg.width * 0.45, complexityImg.height * 0.45);

    const lengthImg = lengthsImages[m_d['Length']];
    ctx.drawImage(lengthImg, 107, 242, lengthImg.width * 0.45, lengthImg.height * 0.45);

    // Draw primary objective resource
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
        ctx.fillText(text, 69, y);
    }
    ctx.save();

    resizeCanvas(div, ctx, canvas, 0.35, 0.35)
    div.appendChild(canvas)
    return div;
}

function renderDeepDiveStage(m_d, stageCount) {
    const div = document.createElement('div');
    div.classList.add('mission-hover-zoom')
    div.classList.add('mission')
    div.id = m_d['CodeName']
    // Create a new canvas element
    const canvas = document.createElement('canvas');
    canvas.title = `Stage ${stageCount.toString()}`
    canvas.width = 350;
    canvas.height = 300;
    var ctx = canvas.getContext('2d');

    // Draw background
    ctx.fillStyle = 'rgba(0, 0, 0, 0)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw primary objective
    const primaryImg = primaryObjsImages[m_d['PrimaryObjective']];
    ctx.drawImage(primaryImg, 83, 58, primaryImg.width * 0.4, primaryImg.height * 0.4);

    // Draw secondary objective
    const secondaryImg = secondaryObjsDDImages[m_d['SecondaryObjective']];
    ctx.drawImage(secondaryImg, -11, -21, secondaryImg.width * 0.6, secondaryImg.height * 0.6);

    // Draw mission warnings if available
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

    // Draw mission mutator if available
    if (m_d['MissionMutator']) {
        const mutatorImg = mutatorsImages[m_d['MissionMutator']];
        ctx.drawImage(mutatorImg, 27, 92, mutatorImg.width * 0.38, mutatorImg.height * 0.38);
    }

    // Draw complexity and length icons
    const complexityImg = complexitiesImages[m_d['Complexity']];
    ctx.drawImage(complexityImg, 107, 2, complexityImg.width * 0.45, complexityImg.height * 0.45);

    const lengthImg = lengthsImages[m_d['Length']];
    ctx.drawImage(lengthImg, 107, 242, lengthImg.width * 0.45, lengthImg.height * 0.45);
    // Draw primary objective resource        
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
        ctx.fillText(text, 69, y);
    }
    ctx.save();
    resizeCanvas(div, ctx, canvas, 0.35, 0.35)
    div.appendChild(canvas)
    return div;
}

async function getBiomes() {
    var dictionary = await getCurrentMissionData();
    // var currentBiomes = await renderBiomes(dictionary);
    // var dictionary_ = await getUpcomingMissionData();
    // var upcomingBiomes = await renderBiomes(dictionary_);

    return [dictionary];
}
async function renderBiomes(dictionary) {
    let renderedBiomes = {};

    for (var season in dictionary) {
        var Biomes = dictionary[season]['Biomes']
        renderedBiomes[season] = {}
        renderedBiomes[season]['Biomes'] = {}

        for (let biome in Biomes) {
            let biomeMissions = Biomes[biome];
            let biome1 = [];

            let six = biomeMissions.length > 5;

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
    drawText(text, 200, 30, 'black', 45, 'CarbonBold-W00-Regular');
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

function resizeImage(img, desiredWidth, desiredHeight) {
    var tempCanvas = document.createElement('canvas');
    var tempCtx = tempCanvas.getContext('2d');
  
    tempCanvas.width = desiredWidth;
    tempCanvas.height = desiredHeight;
  
    tempCtx.drawImage(img, 0, 0, desiredWidth, desiredHeight);
  
    return tempCanvas;
}

function renderDeepDiveBiomeCodename(biome, codename) {
    const img = biomesDDImages[biome];
    const canvas = document.createElement('canvas');
    canvas.classList.add('dd-biome')
    canvas.width = img.width;
    canvas.height = img.height;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(img, 0, 0);

    const texts = ['CODENAME: ', codename];

    const textColor = 'white';
    const shadowColor = '#000000';
    const fontSize = 45;
    
    addShadowedTextToImage(canvas, texts, fontSize);
    return canvas;
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

var biomes;
var dailyDealData;
document.addEventListener('DOMContentLoaded', async function() {
    await preloadImagesAll();
    await preloadFonts();
    dailyDealData = await getDailyDealData()
    document.getElementById('canvascontainer').appendChild(renderDeepDiveBiomeCodename('Magma Core', 'Distant Summit'))
    // biomes =  await getBiomes();
    // biomes = biomes[0]
    // biomes = await renderBiomes(biomes)
    // console.log(biomes)
    // for (let season in biomes) {
    //     console.log(season)
    //     for (let biome in biomes[season]['Biomes']) {
    //         let biomeMissions = biomes[season]['Biomes'][biome]
    //         for (let i = 0; i < biomeMissions.length; i++) {
    //             let mission = biomeMissions[i]
    //             console.log(mission['CodeName'])
    //             document.getElementById('canvascontainer').appendChild(mission['rendered_mission'])
    //         }
    //     }
    // }

});
