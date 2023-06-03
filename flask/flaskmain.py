#PILLOW AND HTML RENDERING SCRIPT FOR USE IN CONJUNCTION WITH MISSION DATA FETCHED BY LUA SCRIPT, GENERATES MISSION ICONS OF CURRENT MISSIONS AND UPLOADS TO STATIC WEB HOST (in this case netlify)
from PIL import Image, ImageDraw, ImageFont
import re
import os
import json
import requests
import time 
import subprocess
from datetime import datetime, timezone, timedelta
import shutil
from dateutil import parser
from flask import Flask, render_template, render_template_string, request, send_from_directory, jsonify

def order_dictionary_by_date(dictionary):
    sorted_keys = sorted(dictionary.keys(), key=lambda x: parser.isoparse(x))
    ordered_dictionary = {}
    for key in sorted_keys:
        ordered_dictionary[key] = dictionary[key]
    return ordered_dictionary

def select_timestamp(DRG):
    current_time = datetime.utcnow()
    keys = list(DRG.keys())
    for i in range(len(keys) - 1):
        timestamp = datetime.fromisoformat(keys[i].replace('Z', ''))
        next_timestamp = datetime.fromisoformat(keys[i+1].replace('Z', ''))
        if current_time > timestamp and current_time < next_timestamp:
            print(keys[i])
            return keys[i]

def scale_image(image, i):
    new_width = int(image.width * i)
    new_height = int(image.height * i)
    resized_image = image.resize((new_width, new_height))
    return resized_image

def calc_center_y(image):
    height = image.height
    center_y = height // 2
    return center_y

def calc_center_x(image):
    width = image.width
    center_x = width // 2
    return center_x

def calc_center(image, background):
    return calc_center_x(background)-calc_center_x(image), calc_center_y(background)-calc_center_y(image)

def render_mission(m_d):
    primary_objs = {
        'Mining Expedition': './img/Mining_expedition_icon.png',
        'Egg Hunt': './img/Egg_collection_icon.png',
        'On-Site Refining': './img/Refining_icon.png',
        'Salvage Operation': './img/Salvage_icon.png',
        'Escort Duty': './img/Escort_icon.png',
        'Point Extraction': './img/Point_extraction_icon.png',
        'Elimination': './img/Elimination_icon.png',
        'Industrial Sabotage': './img/Sabotage_icon.png'
            }
    secondary_objs = {
        'ApocaBlooms': './img/Apoca_bloom_icon.png',
        'Fossils': './img/Fossil_icon.png',
        'Boolo Caps': './img/Boolo_cap_icon.png',
        'Dystrum': './img/Dystrum_icon.png',
        'Ebonuts': './img/Ebonut_icon.png',
        'Fester Fleas': './img/Fleas_icon.png',
        'Gunk Seeds': './img/Gunk_seed_icon.png',
        'Hollomite': './img/Hollomite_icon.png'
            }
    complexities = {
        '1': './img/Icons_complexity_1.png',
        '2': './img/Icons_complexity_2.png',
        '3': './img/Icons_complexity_3.png'
            }
    lengths = {
        '1': './img/Icons_length_1.png',
        '2': './img/Icons_length_2.png',
        '3': './img/Icons_length_3.png'
            }
    mutators = {
        'Critical Weakness': './img/Mutator_critical_weakness_icon.png',
        'Gold Rush': './img/Mutator_gold_rush_icon.png',
        'Double XP': './img/Mutator_triple_xp_icon.png',
        'Golden Bugs': './img/Mutator_golden_bugs_icon.png',
        'Low Gravity': './img/Mutator_no_fall_damage_icon.png',
        'Mineral Mania': './img/Mutator_mineral_mania_icon.png',
        'Rich Atmosphere': './img/Mutator_rich_atmosphere_icon.png',
        'Volatile Guts': './img/Mutator_volatile_guts_icon.png'
            }
    warnings = {
        'Cave Leech Cluster': './img/Warning_cave_leech_cluster_icon.png',
        'Exploder Infestation': './img/Warning_exploder_infestation_icon.png',
        'Haunted Cave': './img/Warning_haunted_cave_icon.png',
        'Lethal Enemies': './img/Warning_lethal_enemies_icon.png',
        'Low Oxygen': './img/Warning_low_oxygen_icon.png',
        'Mactera Plague': './img/Warning_mactera_plague_icon.png',
        'Parasites': './img/Warning_parasites_icon.png',
        'Regenerative Bugs': './img/Warning_regenerative_bugs_icon.png',
        'Shield Disruption': './img/Warning_shield_disruption_icon.png',
        'Elite Threat': './img/Warning_elite_threat_icon.png',
        'Swarmageddon': './img/Warning_swarmageddon_icon.png',
        'Lithophage Outbreak': './img/Warning_lithophage_outbreak_icon.png',
        'Rival Presence': './img/Warning_rival_presence_icon.png'
            }
    
    BACKGROUND = Image.new("RGBA", (350, 300), (0,0,0,0))
    
    PrimaryObj = m_d['PrimaryObjective']
    PRIMARY = primary_objs[PrimaryObj]
    PRIMARY = Image.open(PRIMARY)
    PRIMARY = scale_image(PRIMARY, 0.4)
    x, y = calc_center(PRIMARY, BACKGROUND)
    BACKGROUND.paste(PRIMARY, (x, y), mask=PRIMARY)
    
    SecondaryObj = m_d['SecondaryObjective']
    SECONDARY = secondary_objs[SecondaryObj]
    SECONDARY = Image.open(SECONDARY)
    SECONDARY = scale_image(SECONDARY, 0.2)
    x, y = calc_center(SECONDARY, BACKGROUND)
    BACKGROUND.paste(SECONDARY, (x-110, y+95), mask=SECONDARY)
    
    if 'MissionWarnings' in m_d:
        MISSIONWARNING1 = None
        MISSIONWARNING2 = None
        MissionWarnings = []
        for warning in m_d['MissionWarnings']:
            MissionWarnings.append(warning)
        MISSIONWARNING1 = warnings[MissionWarnings[0]]
        MISSIONWARNING1 = Image.open(MISSIONWARNING1)
        MISSIONWARNING1 = scale_image(MISSIONWARNING1, 0.38)
        x, y = calc_center(MISSIONWARNING1, BACKGROUND)
        if len(MissionWarnings) == 1:
            BACKGROUND.paste(MISSIONWARNING1, (x+100, y-15), mask=MISSIONWARNING1)
        elif len(MissionWarnings) == 2:
            BACKGROUND.paste(MISSIONWARNING1, (x+100, y-60), mask=MISSIONWARNING1)
            MISSIONWARNING2 = warnings[MissionWarnings[1]]
            MISSIONWARNING2 = Image.open(MISSIONWARNING2)
            MISSIONWARNING2 = scale_image(MISSIONWARNING2, 0.38)
            x, y = calc_center(MISSIONWARNING2, BACKGROUND)
            BACKGROUND.paste(MISSIONWARNING2, (x+100, y+40), mask=MISSIONWARNING2)

    if 'MissionMutator' in m_d:
        MissionMutator = m_d['MissionMutator']
        MISSIONMUTATOR = mutators[MissionMutator]
        MISSIONMUTATOR = Image.open(MISSIONMUTATOR)
        MISSIONMUTATOR = scale_image(MISSIONMUTATOR, 0.38)
        x, y = calc_center(MISSIONMUTATOR, BACKGROUND)
        BACKGROUND.paste(MISSIONMUTATOR, (x-100, y-10), mask=MISSIONMUTATOR)

    Complexity = m_d['Complexity']
    COMPLEXITY = complexities[Complexity]
    COMPLEXITY = Image.open(COMPLEXITY)
    COMPLEXITY = scale_image(COMPLEXITY, 0.45)
    x, y = calc_center(COMPLEXITY, BACKGROUND)
    BACKGROUND.paste(COMPLEXITY, (x, y-120), mask=COMPLEXITY)

    Length = m_d['Length']
    LENGTH = lengths[Length]
    LENGTH = Image.open(LENGTH)
    LENGTH = scale_image(LENGTH, 0.45)
    x, y = calc_center(LENGTH, BACKGROUND)
    BACKGROUND.paste(LENGTH, (x, y+120), mask=LENGTH)
    BACKGROUND = scale_image(BACKGROUND, 0.38)
    return BACKGROUND

def render_dd_stage(m_d):
    primary_objs = {
        'Mining Expedition': './img/Mining_expedition_icon.png',
        'Egg Hunt': './img/Egg_collection_icon.png',
        'On-Site Refining': './img/Refining_icon.png',
        'Salvage Operation': './img/Salvage_icon.png',
        'Escort Duty': './img/Escort_icon.png',
        'Point Extraction': './img/Point_extraction_icon.png',
        'Elimination': './img/Elimination_icon.png',
        'Industrial Sabotage': './img/Sabotage_icon.png'
            }
    secondary_objs = {
        'Repair Minimules': './img/Mini_mule_leg_icon.png',
        'Kill Dreadnought(s)': './img/Kill_Dreadnought_Objective_icon.png',
        'Mine Morkite': './img/Morkite_icon.png',
        'Get Alien Eggs': './img/Alien_egg_icon.png',
        'Black Box': './img/Blackbox_icon.png'
            }
    complexities = {
        '1': './img/Icons_complexity_1.png',
        '2': './img/Icons_complexity_2.png',
        '3': './img/Icons_complexity_3.png'
            }
    lengths = {
        '1': './img/Icons_length_1.png',
        '2': './img/Icons_length_2.png',
        '3': './img/Icons_length_3.png'
            }
    mutators = {
        'Critical Weakness': './img/Mutator_critical_weakness_icon.png',
        'Gold Rush': './img/Mutator_gold_rush_icon.png',
        'Double XP': './img/Mutator_triple_xp_icon.png',
        'Golden Bugs': './img/Mutator_golden_bugs_icon.png',
        'Low Gravity': './img/Mutator_no_fall_damage_icon.png',
        'Mineral Mania': './img/Mutator_mineral_mania_icon.png',
        'Rich Atmosphere': './img/Mutator_rich_atmosphere_icon.png',
        'Volatile Guts': './img/Mutator_volatile_guts_icon.png'
            }
    warnings = {
        'Cave Leech Cluster': './img/Warning_cave_leech_cluster_icon.png',
        'Exploder Infestation': './img/Warning_exploder_infestation_icon.png',
        'Haunted Cave': './img/Warning_haunted_cave_icon.png',
        'Lethal Enemies': './img/Warning_lethal_enemies_icon.png',
        'Low Oxygen': './img/Warning_low_oxygen_icon.png',
        'Mactera Plague': './img/Warning_mactera_plague_icon.png',
        'Parasites': './img/Warning_parasites_icon.png',
        'Regenerative Bugs': './img/Warning_regenerative_bugs_icon.png',
        'Shield Disruption': './img/Warning_shield_disruption_icon.png',
        'Elite Threat': './img/Warning_elite_threat_icon.png',
        'Swarmageddon': './img/Warning_swarmageddon_icon.png',
        'Lithophage Outbreak': './img/Warning_lithophage_outbreak_icon.png',
        'Rival Presence': './img/Warning_rival_presence_icon.png'
            }
    resources = {
        }
    
    BACKGROUND = Image.new("RGBA", (350, 300), (0,0,0,0))
    
    PrimaryObj = m_d['PrimaryObjective']
    PRIMARY = primary_objs[PrimaryObj]
    PRIMARY = Image.open(PRIMARY)
    PRIMARY = scale_image(PRIMARY, 0.4)
    x, y = calc_center(PRIMARY, BACKGROUND)
    BACKGROUND.paste(PRIMARY, (x, y), mask=PRIMARY)
    
    SecondaryObj = m_d['SecondaryObjective']
    SECONDARY = secondary_objs[SecondaryObj]
    SECONDARY = Image.open(SECONDARY)
    if SecondaryObj == 'Mine Morkite':
        SECONDARY = scale_image(SECONDARY, 0.2)
    elif SecondaryObj == 'Black Box':
        SECONDARY = scale_image(SECONDARY, 0.3)
    elif SecondaryObj == 'Get Alien Eggs':
        SECONDARY = scale_image(SECONDARY, 0.2)
    else:
        SECONDARY = scale_image(SECONDARY, 0.1)
    x, y = calc_center(SECONDARY, BACKGROUND)
    BACKGROUND.paste(SECONDARY, (x-110, y+95), mask=SECONDARY)
    
    if 'MissionWarnings' in m_d:
        MISSIONWARNING1 = None
        MISSIONWARNING2 = None
        MissionWarnings = []
        for warning in m_d['MissionWarnings']:
            MissionWarnings.append(warning)
        MISSIONWARNING1 = warnings[MissionWarnings[0]]
        MISSIONWARNING1 = Image.open(MISSIONWARNING1)
        MISSIONWARNING1 = scale_image(MISSIONWARNING1, 0.38)
        x, y = calc_center(MISSIONWARNING1, BACKGROUND)
        if len(MissionWarnings) == 1:
            BACKGROUND.paste(MISSIONWARNING1, (x+100, y-15), mask=MISSIONWARNING1)
        elif len(MissionWarnings) == 2:
            BACKGROUND.paste(MISSIONWARNING1, (x+100, y-60), mask=MISSIONWARNING1)
            MISSIONWARNING2 = warnings[MissionWarnings[1]]
            MISSIONWARNING2 = Image.open(MISSIONWARNING2)
            MISSIONWARNING2 = scale_image(MISSIONWARNING2, 0.38)
            x, y = calc_center(MISSIONWARNING2, BACKGROUND)
            BACKGROUND.paste(MISSIONWARNING2, (x+100, y+40), mask=MISSIONWARNING2)

    if 'MissionMutator' in m_d:
        MissionMutator = m_d['MissionMutator']
        MISSIONMUTATOR = mutators[MissionMutator]
        MISSIONMUTATOR = Image.open(MISSIONMUTATOR)
        MISSIONMUTATOR = scale_image(MISSIONMUTATOR, 0.38)
        x, y = calc_center(MISSIONMUTATOR, BACKGROUND)
        BACKGROUND.paste(MISSIONMUTATOR, (x-100, y-10), mask=MISSIONMUTATOR)

    #Complexity = m_d['Complexity']
    #COMPLEXITY = complexities[Complexity]
    #COMPLEXITY = Image.open(COMPLEXITY)
    #COMPLEXITY = scale_image(COMPLEXITY, 0.45)
    #x, y = calc_center(COMPLEXITY, BACKGROUND)
    #BACKGROUND.paste(COMPLEXITY, (x, y-120), mask=COMPLEXITY)

    #Length = m_d['Length']
    #LENGTH = lengths[Length]
    #LENGTH = Image.open(LENGTH)
    #LENGTH = scale_image(LENGTH, 0.45)
    #x, y = calc_center(LENGTH, BACKGROUND)
    #BACKGROUND.paste(LENGTH, (x, y+120), mask=LENGTH)
    BACKGROUND = scale_image(BACKGROUND, 0.38)
    return BACKGROUND

def render_biomes(Biomes):
    rendered_biomes = {}
    rendered_deep_dives = {}
    for biome, missions in Biomes.items():
        biome1 = []
        for mission in missions:
            mission1 = {}
            mission1['CodeName'] = mission['CodeName']
            mission_png = render_mission(mission)
            mission1['rendered_mission'] = mission_png
            biome1.append(mission1)
        rendered_biomes[biome] = biome1
    return rendered_biomes

def render_deepdives(DeepDives):
    rendered_deepdives = {}
    for t, deepdive in DeepDives.items():
        rendered_deepdives[t] = {}
        rendered_deepdives[t]['Biome'] = DeepDives[t]['Biome']
        rendered_deepdives[t]['Stages'] = []
        rendered_deepdives[t]['CodeName'] = DeepDives[t]['CodeName']
        sorted_stages = sorted(deepdive['Stages'], key=lambda x: x['id'], reverse=True)
        for stage in sorted_stages:
            stage_png = render_dd_stage(stage)
            rendered_deepdives[t]['Stages'].append(stage_png)
    return rendered_deepdives

def render_index(DRG):
    def scanners(html):
        html += '          <br><span class="scanners">// SCANNERS OUT OF RANGE \\\\</span>\n'
        return html
    def array_standard_missions(Biomes, biome_str, img_count, html):
        html += '         <br>\n'       
        folder_name = biome_str.replace(' ', '_')
        os.mkdir(f'./index/{folder_name}')
        for mission in Biomes[biome_str]:
            img_count += 1
            fname = str(img_count)
            mission['rendered_mission'].save(f'./index/{folder_name}/{fname}.png')
            html += f'         <img class="mission" src="/{folder_name}/{fname}.png"></img>\n'
        return html, img_count
    def array_dd_missions(dds, dd_str, img_count, html):
        if 'Crystalline Caverns' == dds[dd_str]['Biome']:
            html += '         <img class="image-container" src="https://cdn.discordapp.com/attachments/426026691077472269/1113074252762071081/DeepDive_MissionBar_CrystalCaves.png"></img>\n'
        elif 'Glacial Strata' == dds[dd_str]['Biome']:
            html += '         <img class="image-container" src="https://cdn.discordapp.com/attachments/426026691077472269/1113074253261189191/DeepDive_MissionBar_GlacialStrata.png"></img>\n'
        elif 'Radioactive Exclusion Zone' == dds[dd_str]['Biome']:
            html += '         <img class="image-container" src="https://cdn.discordapp.com/attachments/426026691077472269/1113074254418821242/DeepDive_MissionBar_Radioactive.png"></img>\n'
        elif 'Fungus Bogs' == dds[dd_str]['Biome']:
            html += '         <img class="image-container" src="https://cdn.discordapp.com/attachments/426026691077472269/1113074252996939917/DeepDive_MissionBar_FungusBogs.png"></img>\n'
        elif 'Dense Biozone' == dds[dd_str]['Biome']:
            html += '         <img class="image-container" src="https://cdn.discordapp.com/attachments/426026691077472269/1113074253789663242/DeepDive_MissionBar_LushDownpour.png"></img>\n'
        elif 'Salt Pits' == dds[dd_str]['Biome']:
            html += '         <img class="image-container" src="https://cdn.discordapp.com/attachments/426026691077472269/1113074254754353192/DeepDive_MissionBar_SaltPits.png"></img>\n'
        elif 'Sandblasted Corridors' == dds[dd_str]['Biome']:
            html += '         <img class="image-container" src="https://cdn.discordapp.com/attachments/426026691077472269/1113074252120330240/DeepDive_MissionBar_Sandblasted.png"></img>\n'
        elif 'Magma Core' == dds[dd_str]['Biome']:
            html += '         <img class="image-container" src="https://cdn.discordapp.com/attachments/426026691077472269/1113074254062301224/DeepDive_MissionBar_MagmaCore.png"></img>\n'
        elif 'Azure Weald' == dds[dd_str]['Biome']:
            html += '         <img class="image-container" src="https://cdn.discordapp.com/attachments/426026691077472269/1113074254754353192/DeepDive_MissionBar_SaltPits.png"></img>\n'
        elif 'Hollow Bough' == dds[dd_str]['Biome']:
            html += '         <img class="image-container" src="https://cdn.discordapp.com/attachments/426026691077472269/1113074252996939917/DeepDive_MissionBar_FungusBogs.png"></img>\n'
        html += '         <br>\n'
        folder_name = dd_str.replace(' ', '_')
        os.mkdir(f'./index/{folder_name}')
        for mission in dds[dd_str]['Stages']:
            img_count += 1
            fname = str(img_count)
            mission.save(f'./index/{folder_name}/{fname}.png')
            html += f'         <img class="missionr" src="/{folder_name}/{fname}.png"></img>\n'
        return html, img_count
    img_count = 0
    Biomes = DRG['Biomes']
    html = ''
    html += '''<!doctype html>
                <html>
                 <head>
                 <script>
                    document.addEventListener("DOMContentLoaded", function() {
                        const targetDay = 4; // Thursday (0 = Sunday, 1 = Monday, etc.)
                        const targetHour = 11; // 11am UTC
                        const targetTime = new Date();
                        targetTime.setUTCHours(targetHour, 0, 0, 0);
                        if (targetTime.getUTCDay() === targetDay && Date.now() > targetTime.getTime()) {
                            targetTime.setUTCDate(targetTime.getUTCDate() + 7); // Add 7 days to go to the next Thursday
                        }
                        while (targetTime.getUTCDay() !== targetDay) {
                            targetTime.setUTCDate(targetTime.getUTCDate() + 1);
                        }
                        const countdownTimer = setInterval(() => {
                            const now = Date.now();
                            const remainingTime = targetTime - now;
                            if (remainingTime < 0) {
                                clearInterval(countdownTimer);
                                document.getElementById("ddcountdown").innerHTML = "REFRESH THE PAGE FOR NEW DEEP DIVES";
                            } else {
                                const days = Math.floor(remainingTime / (1000 * 60 * 60 * 24));
                                const hours = Math.floor((remainingTime % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                                const minutes = Math.floor((remainingTime % (1000 * 60 * 60)) / (1000 * 60));
                                const seconds = Math.floor((remainingTime % (1000 * 60)) / 1000);
                                document.getElementById("ddcountdown").innerHTML = `${days}d ${hours}h ${minutes}m ${seconds}s`;
                            }
                        }, 1000);
                    });
                    </script>
                    <script>
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
                            const countdownElement1 = document.getElementById(\'countdown\');
                            const countdownTimer1 = setInterval(updateCountdown1, 1000);
                                function updateCountdown1() {
                                    const remainingTime1 = Math.floor(((targetTime1 - new Date() + 2 ) / 1000));
                                    if (remainingTime1 <= 0) {
                                        clearInterval(countdownTimer1);
                                        document.getElementById("countdown").innerHTML = "REFRESH THE PAGE FOR NEW MISSIONS";
                                    return;
                                }
                                const hours1 = Math.floor(remainingTime1 / 3600);
                                const minutes1 = Math.floor((remainingTime1 % 3600) / 60);
                                const seconds1 = remainingTime1 % 60;
                                const countdownString1 = `${hours1.toString().padStart(2, \'0\')} : ${minutes1.toString().padStart(2, \'0\')} : ${seconds1.toString().padStart(2, \'0\')}`;
                                countdownElement1.textContent = countdownString1;
                            }
                            });
                    </script>
                     <title>DRG MISSIONS</title>
                     <meta charset="UTF-8">
                     <meta name="viewport" content="width=device-width, initial-scale=1.0">
                     <meta property="og:title" content="DRG CURRENT MISSIONS">
                     <meta property="og:type" content="website">
                     <meta property="og:url" content="/drgmissions.json">
                     <meta property="og:description" content="Current Missions, generated by DRG from the current seed, and also the Current DDs.">
                     <style>
                         @font-face {
                             font-family: "BebasNeue";
                             src: url("/BebasNeue-Regular.woff2");
                         }
                         @font-face {
                             font-family: "HammerBro101MovieThin-Regular";
                             src: url("/HammerBro101MovieThin-Regular.woff");
                         }
                         .grid-container {
                            display: grid;
                            grid-template-columns: 1fr 1fr;
                            align-items: flex-start;
                            grid-column-gap: 0;
                         }
                         .mission {
                             display: inline-block;
                             margin-right: 5px;
                         }
                         .biome-container {
                             width: 100%;
                             height: auto;
                         }
                         .dd-container {
                             width: 50%;
                             height: 50%;
                         }
                         .image-container {
                             width: 80%;
                             height: auto;
                         }
                         .jsonlink {
                             color: #1E90FF;
                             font-size: 30px;
                             font-family: "BebasNeue", sans-serif;
                         }
                         .scanners {
                             color: red;
                             font-family: "HammerBro101MovieThin-Regular", sans-serif;
                             font-size: 15px;
                         }
                        .center-align {
                            display: flex;
                            align-items: flex-start;
                            justify-content: center;
                            text-align: center;
                        }
                        .left-align {
                            display: flex;
                            align-items: left;
                            justify-content: left;
                            text-align: left;
                        }
                        .right-align {
                            display: flex;
                            align-items: right;
                            justify-content: right;
                            text-align: right;
                        }
                        .missionscountdown {
                            text-align: center;
                            color: white;
                            font-size: 35px;
                            font-family: "BebasNeue", sans-serif;
                        }
                        span#countdown {
                            margin-bottom: 0;
                            display: flex;
                            align-items: center;
                            color: white;
                            font-size: 72px;
                            justify-content: center;
                            font-family: "BebasNeue", sans-serif;
                        }
                        span#ddcountdown {
                            margin-bottom: 0;
                            display: flex;
                            align-items: center;
                            color: white;
                            font-size: 72px;
                            justify-content: center;
                            font-family: "BebasNeue", sans-serif;
                        }
                        .gsgdisclaimer {
                            margin-bottom: 0;
                            color: white;
                            font-family: "BebasNeue", sans-serif;
                        }
                        }
                    </style>
                 </head>
                 <body bgcolor="#303030">
                  <div class="grid-container center-align">
                    <div>
                    <h2>'''
    html += '        <div class="biome-container">\n'
    html += '         <img class="image-container" src="https://cdn.discordapp.com/attachments/426026691077472269/1113074252762071081/DeepDive_MissionBar_CrystalCaves.png"></img>\n'
    if 'Crystalline Caverns' not in Biomes.keys():
        html = scanners(html)
    #else:
        #html, img_count = array_standard_missions(Biomes, 'Crystalline Caverns', img_count, html)
    html += '        </div>\n'
    html += '       </h2>\n'
    html += '       <h2>\n'
    html += '        <div class="biome-container">\n'
    html += '         <img class="image-container" src="https://cdn.discordapp.com/attachments/426026691077472269/1113074253261189191/DeepDive_MissionBar_GlacialStrata.png"></img>\n'
    if 'Glacial Strata' not in Biomes.keys():
        html = scanners(html)
    #else:
        #html, img_count = array_standard_missions(Biomes, 'Glacial Strata', img_count, html)
    html += '        </div>\n'
    html += '       </h2>\n'
    html += '       <h2>\n'
    html += '        <div class="biome-container">\n'
    html += '         <img class="image-container" src="https://cdn.discordapp.com/attachments/426026691077472269/1113074254062301224/DeepDive_MissionBar_MagmaCore.png"></img>\n'
    if 'Magma Core' not in Biomes.keys():
        html = scanners(html)
    #else:
        #html, img_count = array_standard_missions(Biomes, 'Magma Core', img_count, html)
    html += '        </div>\n'
    html += '       </h2>\n'
    html += '       <h2>\n'
    html += '        <div class="biome-container">\n'
    html += '         <img class="image-container" src="https://cdn.discordapp.com/attachments/426026691077472269/1113074254754353192/DeepDive_MissionBar_SaltPits.png"></img>\n'
    if 'Salt Pits' not in Biomes.keys():
        html = scanners(html)
    #else:
        #html, img_count = array_standard_missions(Biomes, 'Salt Pits', img_count, html)
    html += '        </div>\n'
    html += '       </h2>\n'
    html += '       <h2>\n'
    html += '        <div class ="biome-container">\n'
    html += '         <img class="image-container" src="https://cdn.discordapp.com/attachments/426026691077472269/1113074252460077056/DeepDive_MissionBar_AzureWeald.png"></img>\n'
    if 'Azure Weald' not in Biomes.keys():
        html = scanners(html)
    #else:
        #html, img_count = array_standard_missions(Biomes, 'Azure Weald', img_count, html)
    html += '        </div>\n'
    html += '       </h2>\n'
    html += '       <h2>\n'
    html += '        <div class ="biome-container">\n'
    html += '         <img class="image-container" src="https://cdn.discordapp.com/attachments/426026691077472269/1113074252120330240/DeepDive_MissionBar_Sandblasted.png"></img>\n'
    if 'Sandblasted Corridors' not in Biomes.keys():
        html = scanners(html)
    #else:
        #html, img_count = array_standard_missions(Biomes, 'Sandblasted Corridors', img_count, html)
    html += '        </div>\n'
    html += '       </h2>\n'
    html += '       <h2>\n'
    html += '        <div class ="biome-container">\n'
    html += '         <img class="image-container" src="https://cdn.discordapp.com/attachments/426026691077472269/1113074254418821242/DeepDive_MissionBar_Radioactive.png"></img>\n'
    if 'Radioactive Exclusion Zone' not in Biomes.keys():
        html = scanners(html)
    #else:
        #html, img_count = array_standard_missions(Biomes, 'Radioactive Exclusion Zone', img_count, html)
    html += '        </div>\n'
    html += '       </h2>\n'
    html += '       <h2>\n'
    html += '        <div class = "biome-container">\n'
    html += '         <img class="image-container" src="https://cdn.discordapp.com/attachments/426026691077472269/1113074252996939917/DeepDive_MissionBar_FungusBogs.png"></img>\n'
    if 'Fungus Bogs' not in Biomes.keys():
        html = scanners(html)
    #else:
        #html, img_count = array_standard_missions(Biomes, 'Fungus Bogs', img_count, html)
    html += '        </div>\n'
    html += '       </h2>\n'
    html += '       <h2>\n'
    html += '        <div class ="biome-container">\n'
    html += '         <img class="image-container" src="https://cdn.discordapp.com/attachments/426026691077472269/1113074253521240124/DeepDive_MissionBar_HollowBough.png"></img>\n'
    if 'Hollow Bough' not in Biomes.keys():
        html = scanners(html)
    #else:
        #html, img_count = array_standard_missions(Biomes, 'Hollow Bough', img_count, html)
    html += '        </div>\n'
    html += '       </h2>\n'
    html += '       <h2>\n'
    html += '        <div class ="biome-container">\n'
    html += '         <img class="image-container" src="https://cdn.discordapp.com/attachments/426026691077472269/1113074253789663242/DeepDive_MissionBar_LushDownpour.png"></img>\n'
    if 'Dense Biozone' not in Biomes.keys():
        html = scanners(html)
    #else:
        #html, img_count = array_standard_missions(Biomes, 'Dense Biozone', img_count, html)
    html += '        </div>\n'
    html += '        </div>\n'
    html += '        <div>\n'
    html += '        <div class="dd-container">\n'
    html += '           <div class="missionscountdown">NEW MISSIONS IN</div>\n'
    html += '          <span id="countdown"></span>\n'
    html += '           <div class="missionscountdown">NEW DEEP DIVES IN</div>\n'
    html += '          <span id="ddcountdown"></span>\n'
    html += '           <h2>\n'    
    html += '          <img class="image-container" src="https://cdn.discordapp.com/attachments/426026691077472269/1113470269940564048/dd.png"></img>\n'
    #html, img_count = array_dd_missions(DeepDives, 'Deep Dive Normal', img_count, html)
    html += '         </h2>\n'
    html += '        </div>\n'
    html += '        <div class="dd-container">\n'
    html += '           <h2>\n'
    html += '          <img class="image-container" src="https://cdn.discordapp.com/attachments/426026691077472269/1113165203077607494/edd.png"</img>\n'
    #html, img_count = array_dd_missions(DeepDives, 'Deep Dive Elite', img_count, html)
    html += '           </h2>\n'
    html += '           <hr>\n'
    html += '         <a class="jsonlink" href="/?json=bulkmissions"><strong>FULL MISSION DATA</strong></a> <a class="jsonlink" href="/?json=current"><strong>CURRENT DATA</strong></a> <a class="jsonlink" href="/?json=DD"><strong>CURRENT DD DATA</strong></a>\n'
    html += "          <p class='gsgdisclaimer'>This website is a third-party platform and is not affiliated, endorsed, or sponsored by Ghost Ship Games. The use of Deep Rock Galactic's in-game assets on this website is solely for illustrative purposes and does not imply any ownership or association with the game or its developers. All copyrights and trademarks belong to their respective owners. For official information about Deep Rock Galactic, please visit the official Ghost Ship Games website.</p>\n"
    html += '       </div>\n'
    html += '       </div>\n'
    html += '       </div>\n'
    html += '    </body>\n'
    html += '</html>\n'
    return html

with open('drgmissionsgod.json', 'r') as f:
    DRG = f.read()
    f.close()
    
DRG = json.loads(DRG)

DRG = order_dictionary_by_date(DRG)
    
app = Flask(__name__, template_folder='./templates', static_folder='')

@app.route('/')
def home():
    applicable_timestamp = select_timestamp(DRG)
    json_arg = request.args.get('json')
    img_arg = request.args.get('img')
    if img_arg:
        #Biomes = DRG[applicable_timestamp]['Biomes']
        #Biomes = render_biomes(Biomes)
        #DRG['Biomes'] = Biomes
        pass
    if json_arg:
        if json_arg == 'bulkmissions':
            return jsonify(DRG)
        elif json_arg == 'DD':
            return jsonify(DDs)
        elif json_arg == 'current':
            data = DRG[applicable_timestamp]
            return jsonify(data), 200, {'Title': applicable_timestamp}
        else:
            return "No applicable data", 404
    return render_template_string(render_index(DRG[applicable_timestamp]))

if __name__ == '__main__':
    app.run()

#DeepDives = DRG['Deep Dives']
#DeepDives = render_deepdives(DeepDives)
#DRG['Deep Dives'] = DeepDives

#Biomes = DRG['Biomes']
#Biomes = render_biomes(Biomes)
#DRG['Biomes'] = Biomes

#if os.path.exists('./index'):
    #shutil.rmtree('./index')
    #os.mkdir('index')
