class Dwarf {
  constructor() {
    this.xp = 0;
    this.level = 0;
    this.promotions = 0;
    this.total_level = 0;
    this.type = null
  }

  calculate_class_xp() {
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
    this.total_level = this.level + this.promotions * 25;
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

const Engineer = new Dwarf();
Engineer.type = 'Icon_Character_Engineer'
Engineer.level = engineerLevels;
Engineer.promotions = engineerPromotions;
Engineer.calculate_class_xp();

const Scout = new Dwarf();
Scout.type = 'Icon_Character_Scout'
Scout.level = scoutLevels;
Scout.promotions = scoutPromotions;
Scout.calculate_class_xp();

const Driller = new Dwarf();
Driller.type = 'Icon_Character_Driller'
Driller.level = drillerLevels;
Driller.promotions = drillerPromotions;
Driller.calculate_class_xp();

const Gunner = new Dwarf();
Gunner.type = 'Icon_Character_Gunner'
Gunner.level = gunnerLevels;
Gunner.promotions = gunnerPromotions;
Gunner.calculate_class_xp();

const total_promotions = Engineer.promotions + Scout.promotions + Driller.promotions + Gunner.promotions;

const Badges = (Engineer.total_level + Scout.total_level + Driller.total_level + Gunner.total_level) / 3;

const total_xp = Engineer.xp + Scout.xp + Driller.xp + Gunner.xp;
var xp_per_hr = (total_xp / hours)
if (isNaN(xp_per_hr)) {
xp_per_hr = 0;
} else {

}

function getPromoLevel(promoNumber, type) {
  const promos = {
  0: `<div class="mission-hover-zoom"><img class="class-icon" src="/files/class_icons/${type}.png"></div>`,
  1: `<div class="mission-hover-zoom"><img class="class-icon" src="/files/class_icons/${type}_Bronze_1.png"></div>`,
  2: `<div class="mission-hover-zoom"><img class="class-icon"src="/files/class_icons/${type}_Bronze_2.png"></div>`,
  3: `<div class="mission-hover-zoom"><img class="class-icon" src="/files/class_icons/${type}_Bronze_3.png"></div>`,
  4: `<div class="mission-hover-zoom"><img class="class-icon" src="/files/class_icons/${type}_Silver_1.png"></div>`,
  5: `<div class="mission-hover-zoom"><img class="class-icon" src="/files/class_icons/${type}_Silver_2.png"></div>`,
  6: `<div class="mission-hover-zoom"><img class="class-icon" src="/files/class_icons/${type}_Silver_3.png"></div>`,
  7: `<div class="mission-hover-zoom"><img class="class-icon" src="/files/class_icons/${type}_Gold_1.png"></div>`,
  8: `<div class="mission-hover-zoom"><img class="class-icon" src="/files/class_icons/${type}_Gold_2.png"></div>`,
  9: `<div class="mission-hover-zoom"><img class="class-icon" src="/files/class_icons/${type}_Gold_3.png"></div>`,
  10: `<div class="mission-hover-zoom"><img class="class-icon" src="/files/class_icons/${type}_Platinum_1.png"></div>`,
  11: `<div class="mission-hover-zoom"><img class="class-icon" src="/files/class_icons/${type}_Platinum_2.png"></div>`,
  12: `<div class="mission-hover-zoom"><img class="class-icon" src="/files/class_icons/${type}_Platinum_3.png"></div>`,
  13: `<div class="mission-hover-zoom"><img class="class-icon" src="/files/class_icons/${type}_Emerald_1.png"></div>`,
  14: `<div class="mission-hover-zoom"><img class="class-icon" src="/files/class_icons/${type}_Emerald_2.png"></div>`,
  15: `<div class="mission-hover-zoom"><img class="class-icon" src="/files/class_icons/${type}_Emerald_3.png"></div>`,
  16: `<div class="mission-hover-zoom"><img class="class-icon" src="/files/class_icons/${type}_Legendary_1.png"></div>`,
  17: `<div class="mission-hover-zoom"><img class="class-icon" src="/files/class_icons/${type}_Legendary_2.png"></div>`,
  18: `<div class="mission-hover-zoom"><img class="class-icon" src="/files/class_icons/${type}_Legendary_3.png"></div>`
  };
if (promoNumber >= 18) {
  return `<div class="mission-hover-zoom"><img class="class-icon" src="/files/class_icons/${type}_Legendary_3.png"></div>`;
} else {
  return promos[promoNumber];
}
};

const tableContent = `
<style>
table {
  border-collapse: collapse;
  width: auto;
}

th, td {
  padding: 8px;
  text-align: center;
  border-bottom: 1px solid #ddd;
}
tr {
  height: 75px;
}
</style>
<table id="outputTable" class="collapsed">
<tr>
  <!-- <th>Class</th> -->
  <th>Rank</th>
  <th>XP</th>
  
</tr>
<tr>
  <!-- <td><span style="color:#9f2c14;">Engineer</span></td> -->
  <td style="height:50px;">${getPromoLevel(Engineer.promotions, Engineer.type)}</td>
  <td><span style="color:red;">${Engineer.xp.toLocaleString()}</span></td>
</tr>
<tr>
  <!-- <td><span style="color:#3062b1;">Scout</span></td> -->
  <td style="height:50px;">${getPromoLevel(Scout.promotions, Scout.type)}</td>
  <td><span style="color:red;">${Scout.xp.toLocaleString()}</span></td>
</tr>
<tr>
  <!-- <td><span style="color:#bda62a;">Driller</span></td> -->
  <td style="height:50px;">${getPromoLevel(Driller.promotions, Driller.type)}</td>
  <td><span style="color:red;">${Driller.xp.toLocaleString()}</span></td>
</tr>
<tr>
 <!-- <td><span style="color:#83a637;">Gunner</span></td>  -->
  <td style="height:50px;">${getPromoLevel(Gunner.promotions, Gunner.type)}</td>
  <td><span style="color:red;">${Gunner.xp.toLocaleString()}</span></td>
</tr>
</table>
<br>
<h2 id="results" class="collapsed" style="font-size:40px;">
Total XP: <span style="color:red;">${total_xp.toLocaleString()}<br></span>
Total Promotions: ${total_promotions.toLocaleString()}<br>
<img src="/files/Player_rank_icon.png">${(Badges-0.333).toFixed(2)}<br>
XP Per Hour: ${(xp_per_hr).toLocaleString()}
</h2>
`;

output.innerHTML = tableContent;

function checkImagesLoaded() {
const images = document.getElementsByTagName('img');
for (let i = 0; i < images.length; i++) {
  if (!images[i].complete) {
    return false;
  }
}
return true;
}

function toggleTable() {
var table = document.getElementById("outputTable");
var results = document.getElementById("results");
table.classList.toggle("collapsed");
results.classList.toggle("collapsed");
}

var interval = setInterval(function() {
if (checkImagesLoaded()) {
  toggleTable();
  clearInterval(interval);
}
}, 100);
});
function startsubmit() {
var submitButton = document.getElementById("calcsubmit");
submitButton.click();
};
window.onload = function() {
startsubmit() };