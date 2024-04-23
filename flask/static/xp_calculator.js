class Dwarf {
  constructor(type, levels, promotions) {
    this.xp = 0;
    this.level = levels;
    this.promotions = promotions;
    this.totalLevel = 0;
    this.type = type
  }

  calculateClassXP() {
    const levels = {
      1: 0,
      2: 3000,
      3: 7000,
      4: 12000,
      5: 18000,
      6: 25000,
      7: 33000,
      8: 42000,
      9: 52000,
      10: 63000,
      11: 75000,
      12: 88000,
      13: 102000,
      14: 117000,
      15: 132500,
      16: 148500,
      17: 165000,
      18: 182000,
      19: 199500,
      20: 217500,
      21: 236000,
      22: 255000,
      23: 274500,
      24: 294500,
      25: 315000,
    };
    this.xp = levels[this.level] + this.promotions * 315000;
    this.totalLevel = this.level + this.promotions * 25;
  }
}
const xpForm = document.getElementById("xpForm")
function sleep(ms) {
return new Promise(resolve => {
  setTimeout(resolve, ms);
});
}
xpForm.addEventListener("reset", function(event) {
sleep(1).then(() => {
document.getElementById("calcsubmit").click();});
});

xpForm.addEventListener("submit", function(event) {
event.preventDefault();
const hoursInput = document.getElementById("hours");
const engineerPromotionsInput = document.getElementById("engineerPromotions");
const engineerLevelsInput = document.getElementById("engineerLevels");
const scoutPromotionsInput = document.getElementById("scoutPromotions");
const scoutLevelsInput = document.getElementById("scoutLevels");
const drillerPromotionsInput = document.getElementById("drillerPromotions");
const drillerLevelsInput = document.getElementById("drillerLevels");
const gunnerPromotionsInput = document.getElementById("gunnerPromotions");
const gunnerLevelsInput = document.getElementById("gunnerLevels");

const hours = hoursInput.value !== "" ? parseInt(hoursInput.value) : 0;
const engineerPromotions = engineerPromotionsInput.value !== "" ? parseInt(engineerPromotionsInput.value) : 0;
const engineerLevels = engineerLevelsInput.value !== "" ? parseInt(engineerLevelsInput.value) : 1;
const scoutPromotions = scoutPromotionsInput.value !== "" ? parseInt(scoutPromotionsInput.value) : 0;
const scoutLevels = scoutLevelsInput.value !== "" ? parseInt(scoutLevelsInput.value) : 1;
const drillerPromotions = drillerPromotionsInput.value !== "" ? parseInt(drillerPromotionsInput.value) : 0;
const drillerLevels = drillerLevelsInput.value !== "" ? parseInt(drillerLevelsInput.value) : 1;
const gunnerPromotions = gunnerPromotionsInput.value !== "" ? parseInt(gunnerPromotionsInput.value) : 0;
const gunnerLevels = gunnerLevelsInput.value !== "" ? parseInt(gunnerLevelsInput.value) : 1;

const Engineer = new Dwarf('Icon_Character_Engineer', engineerLevels, engineerPromotions);
Engineer.calculateClassXP();

const Scout = new Dwarf('Icon_Character_Scout', scoutLevels, scoutPromotions);
Scout.calculateClassXP();

const Driller = new Dwarf('Icon_Character_Driller', drillerLevels, drillerPromotions);
Driller.calculateClassXP();

const Gunner = new Dwarf('Icon_Character_Gunner', gunnerLevels, gunnerPromotions);
Gunner.calculateClassXP();

const totalPromotions = Engineer.promotions + Scout.promotions + Driller.promotions + Gunner.promotions;
const Badges = (Engineer.totalLevel + Scout.totalLevel + Driller.totalLevel + Gunner.totalLevel) / 3;
const total_xp = Engineer.xp + Scout.xp + Driller.xp + Gunner.xp;
var xp_per_hr = (total_xp / hours)
if (isNaN(xp_per_hr)) {
xp_per_hr = 0;
} else {

}

function getPromoLevel(promoNumber, type) {
  const promos = {
  0: `<div class="mission-hover-zoom"><img class="class-icon" src="/static/class_icons/${type}.png"></div>`,
  1: `<div class="mission-hover-zoom"><img class="class-icon" src="/static/class_icons/${type}_Bronze_1.png"></div>`,
  2: `<div class="mission-hover-zoom"><img class="class-icon"src="/static/class_icons/${type}_Bronze_2.png"></div>`,
  3: `<div class="mission-hover-zoom"><img class="class-icon" src="/static/class_icons/${type}_Bronze_3.png"></div>`,
  4: `<div class="mission-hover-zoom"><img class="class-icon" src="/static/class_icons/${type}_Silver_1.png"></div>`,
  5: `<div class="mission-hover-zoom"><img class="class-icon" src="/static/class_icons/${type}_Silver_2.png"></div>`,
  6: `<div class="mission-hover-zoom"><img class="class-icon" src="/static/class_icons/${type}_Silver_3.png"></div>`,
  7: `<div class="mission-hover-zoom"><img class="class-icon" src="/static/class_icons/${type}_Gold_1.png"></div>`,
  8: `<div class="mission-hover-zoom"><img class="class-icon" src="/static/class_icons/${type}_Gold_2.png"></div>`,
  9: `<div class="mission-hover-zoom"><img class="class-icon" src="/static/class_icons/${type}_Gold_3.png"></div>`,
  10: `<div class="mission-hover-zoom"><img class="class-icon" src="/static/class_icons/${type}_Platinum_1.png"></div>`,
  11: `<div class="mission-hover-zoom"><img class="class-icon" src="/static/class_icons/${type}_Platinum_2.png"></div>`,
  12: `<div class="mission-hover-zoom"><img class="class-icon" src="/static/class_icons/${type}_Platinum_3.png"></div>`,
  13: `<div class="mission-hover-zoom"><img class="class-icon" src="/static/class_icons/${type}_Emerald_1.png"></div>`,
  14: `<div class="mission-hover-zoom"><img class="class-icon" src="/static/class_icons/${type}_Emerald_2.png"></div>`,
  15: `<div class="mission-hover-zoom"><img class="class-icon" src="/static/class_icons/${type}_Emerald_3.png"></div>`,
  16: `<div class="mission-hover-zoom"><img class="class-icon" src="/static/class_icons/${type}_Legendary_1.png"></div>`,
  17: `<div class="mission-hover-zoom"><img class="class-icon" src="/static/class_icons/${type}_Legendary_2.png"></div>`,
  18: `<div class="mission-hover-zoom"><img class="class-icon" src="/static/class_icons/${type}_Legendary_3.png"></div>`
  };
if (promoNumber >= 18) {
  return `<div class="mission-hover-zoom"><img class="class-icon" src="/static/class_icons/${type}_Legendary_3.png"></div>`;
} else {
  return promos[promoNumber];
}
};

document.getElementById('tableEngineerClassRank').innerHTML = `${getPromoLevel(Engineer.promotions, Engineer.type)}`
document.getElementById('tableEngineerClassLevel').innerHTML = `${Engineer.totalLevel.toLocaleString()}`
document.getElementById('tableEngineerClassXP').innerHTML = `<span style="color:red;">${Engineer.xp.toLocaleString()}</span>`

document.getElementById('tableScoutClassRank').innerHTML = `${getPromoLevel(Scout.promotions, Scout.type)}`
document.getElementById('tableScoutClassLevel').innerHTML = `${Scout.totalLevel.toLocaleString()}`
document.getElementById('tableScoutClassXP').innerHTML = `<span style="color:red;">${Scout.xp.toLocaleString()}</span>`

document.getElementById('tableDrillerClassRank').innerHTML = `${getPromoLevel(Driller.promotions, Driller.type)}`
document.getElementById('tableDrillerClassLevel').innerHTML = `${Driller.totalLevel.toLocaleString()}`
document.getElementById('tableDrillerClassXP').innerHTML = `<span style="color:red;">${Driller.xp.toLocaleString()}</span>`

document.getElementById('tableGunnerClassRank').innerHTML = `${getPromoLevel(Gunner.promotions, Gunner.type)}`
document.getElementById('tableGunnerClassLevel').innerHTML = `${Gunner.totalLevel.toLocaleString()}`
document.getElementById('tableGunnerClassXP').innerHTML = `<span style="color:red;">${Gunner.xp.toLocaleString()}</span>`

document.getElementById('results').innerHTML = `
Total XP: <span style="color:red;">${total_xp.toLocaleString()}<br></span>
Total Promotions: ${totalPromotions.toLocaleString()}<br>
<img src="/static/Player_rank_icon.png">${(Badges-0.333).toFixed(2)}<br>
XP Per Hour: ${(xp_per_hr).toLocaleString()}
`;
});

function startsubmit() {
var submitButton = document.getElementById("calcsubmit");
submitButton.click();
};
function onLoad() {
startsubmit();
document.querySelector('p.loading').style.display = 'none';
document.getElementById('scal').classList.toggle('collapsed');  
};

document.addEventListener('DOMContentLoaded', async () => {
  let f = localStorage.getItem('fonts');
  if (f) {
    f = JSON.parse(f);
    for (key in f) {
      let base64data = f[key];
      let font = new FontFace(key, `url(data:font/woff2;base64,${base64data})`);
      await font.load();
      document.fonts.add(font);
    }
  }
  onLoad();
});