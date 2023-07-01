from drg_png_renderers import render_mission, render_dd_stage, render_dailydeal
#import re
import os
import json
#import requests
from time import sleep
import time 
#import subprocess
from datetime import datetime #, timezone, timedelta
import shutil
from dateutil import parser
from flask import Flask, render_template_string, request, send_file, jsonify, make_response
import queue
import threading
import glob
from io import BytesIO
import hashlib
#import sys
#from concurrent.futures import ThreadPoolExecutor, as_completed, wait

def sort_dictionary(dictionary, custom_order):
    sorted_dict = {}
    for key in custom_order:
        if key in dictionary:
            sorted_dict[key] = dictionary[key]
            del dictionary[key]
    sorted_dict.update(dictionary)
    return sorted_dict

def order_dictionary_by_date(dictionary):
    sorted_keys = sorted(dictionary.keys(), key=lambda x: parser.isoparse(x))
    ordered_dictionary = {}
    for key in sorted_keys:
        ordered_dictionary[key] = dictionary[key]
    return ordered_dictionary

def select_timestamp(DRG, next_):
    current_time = datetime.utcnow()
    keys = list(DRG.keys())
    for i in range(len(keys) - 1):
        timestamp = datetime.fromisoformat(keys[i].replace('Z', ''))
        next_timestamp = datetime.fromisoformat(keys[i+1].replace('Z', ''))
        if current_time > timestamp and current_time < next_timestamp:
            if next_:
                return keys[i+1]
            else:
                return keys[i]

def rotate_timestamp(DRG, tstamp_Queue, next_):
    applicable_timestamp = select_timestamp(DRG, next_=next_)
    tstamp_Queue.put(applicable_timestamp)
    timestamp = tstamp_Queue.queue[0]
    while True:
        applicable_timestamp = select_timestamp(DRG, next_=next_)
        if applicable_timestamp != timestamp:
            tstamp_Queue.put(applicable_timestamp)
            tstamp_Queue.get()
            timestamp = tstamp_Queue.queue[0]
        sleep(0.25)

def wait_rotation(rendering_event, rendering_event_next):
    target_minutes_59 = [29, 59]
    while True:
        current_time = datetime.now().time()
        current_minute = current_time.minute
        current_second = current_time.second + current_time.microsecond / 1e6
        if current_second > 59.20 and current_minute in target_minutes_59:
            rendering_event.clear()
            rendering_event_next.clear()
        sleep(0.25)

def rotate_dailydeal(AllTheDeals, tstamp_Queue, deal_Queue):
    while tstamp_Queue.qsize() == 0:
        continue
    deal_dict = AllTheDeals[tstamp_Queue.queue[0]]
    dailydeal = {}
    rendered_dailydeal = render_dailydeal(deal_dict)
    DailyDeal = BytesIO()
    rendered_dailydeal.save(DailyDeal, format='PNG')
    DailyDeal.seek(0)
    etag = hashlib.md5(DailyDeal.getvalue()).hexdigest()
    dailydeal['rendered_dailydeal'] = DailyDeal
    dailydeal['etag'] = etag
    deal_Queue.put(dailydeal)
    timestamp = tstamp_Queue.queue[0]
    while True:
        applicable_timestamp = tstamp_Queue.queue[0]
        if applicable_timestamp != timestamp:
            deal_dict = AllTheDeals[applicable_timestamp]
            dailydeal = {}
            rendered_dailydeal = render_dailydeal(deal_dict)
            DailyDeal = BytesIO()
            rendered_dailydeal.save(DailyDeal, format='PNG')
            DailyDeal.seek(0)
            etag = hashlib.md5(DailyDeal.getvalue()).hexdigest()
            dailydeal['rendered_dailydeal'] = DailyDeal
            dailydeal['etag'] = etag
            deal_Queue.put(dailydeal)
            deal_Queue.get()
            timestamp = applicable_timestamp
        sleep(0.75)
    
def rotate_biomes(DRG, tstamp_Queue, biomes_Queue, rendering_event):
    #order = ['Glacial Strata', 'Crystalline Caverns', 'Salt Pits', 'Magma Core', 'Azure Weald', 'Sandblasted Corridors', 'Fungus Bogs', 'Radioactive Exclusion Zone', 'Dense Biozone', 'Hollow Bough']
    #def process_mission(mission):
        #mission0 = {}
        #mission0['CodeName'] = mission['CodeName']
        #mission_icon = BytesIO()
        #mission['rendered_mission'].save(mission_icon, format='PNG')
        #mission_icon.seek(0)
        #etag = hashlib.md5(mission_icon.getvalue()).hexdigest()
        #mission0['etag'] = etag
        #mission0['rendered_mission'] = mission_icon
        #return mission0
    #def wrap_missions_executor(missions):
        #mission_futures = []
        #with ThreadPoolExecutor() as executor:
            #for mission in missions:
                #future = executor.submit(process_mission, mission)
                #mission_futures.append(future)
            #results = [future.result() for future in mission_futures]
            #return results
    #def wrap_biomes_executor(Biomes):
        #with ThreadPoolExecutor() as executor:
            #biome_futures = {}
            #for biome, missions in Biomes.items():
                #future = executor.submit(wrap_missions_executor, missions)
                #biome_futures[biome] = future
            #results = {biome: future.result() for biome, future in biome_futures.items()}
            #return results
    #def array_biomes(Biomes, timestamp):
        #Biomes1 = wrap_biomes_executor(Biomes)
        #return timestamp, Biomes1
    def array_biomes(Biomes, timestamp):
        Biomes1 = {}
        for biome in Biomes.keys():
            Biomes1[biome] = []
            for mission in Biomes[biome]:
                mission0 = {}
                mission0['CodeName'] = mission['CodeName']
                mission_icon = BytesIO()
                mission['rendered_mission'].save(mission_icon, format='PNG')
                mission_icon.seek(0)
                etag = hashlib.md5(mission_icon.getvalue()).hexdigest()
                mission0['etag'] = etag
                mission0['rendered_mission'] = mission_icon
                Biomes1[biome].append(mission0)
        return timestamp, Biomes1
    
    while tstamp_Queue.qsize() == 0:
        continue
    Biomes = DRG[tstamp_Queue.queue[0]]['Biomes']
    Biomes = render_biomes(Biomes)
    #Biomes = sort_dictionary(Biomes, order)
    timestamp, Biomes = array_biomes(Biomes, tstamp_Queue.queue[0])
    biomes_Queue.put(Biomes)
    rendering_event.set()
    while True:
        applicable_timestamp = tstamp_Queue.queue[0]
        if applicable_timestamp != timestamp:
                Biomes = DRG[applicable_timestamp]['Biomes']
                Biomes = render_biomes(Biomes)
                #Biomes = sort_dictionary(Biomes, order)
                timestamp, Biomes = array_biomes(Biomes, applicable_timestamp)
                biomes_Queue.put(Biomes)
                biomes_Queue.get()
                rendering_event.set()
        sleep(0.25)

def rotate_DDs(DDs):
    def sort_dd_json_list_by_timestamp(json_pattern):
        json_list = glob.glob(json_pattern)
        sorted_json_list = sorted(json_list, key=lambda x: datetime.strptime(x.split('_')[1].split('.')[0], "%Y-%m-%dT%H-%M-%SZ"), reverse=True)
        return sorted_json_list
    json_pattern = './DD_*.json'
    current_json = None
    while True:
        json_list = sort_dd_json_list_by_timestamp(json_pattern)
        if current_json != json_list[0]:
            current_json = json_list[0]
            with open(f'{json_list[0]}', 'r') as f:
                dds = json.load(f)
            if DDs.empty():
                DDs.put(dds)
            else:
                DDs.put(dds)
                DDs.get()
            dds = dds['Deep Dives']
            dds = render_deepdives(dds)
            dd_str = 'Deep Dive Normal'
            img_count = 0
            folder_name = dd_str.replace(' ', '_')
            if os.path.exists(f'./files/{folder_name}'):
                shutil.rmtree(f'./files/{folder_name}')
            os.mkdir(f'./files/{folder_name}')
            for mission in dds[dd_str]['Stages']:
                img_count += 1
                fname = str(img_count)
                mission.save(f'./files/{folder_name}/{fname}.png')
            dd_str = 'Deep Dive Elite'
            img_count = 0
            folder_name = dd_str.replace(' ', '_')
            if os.path.exists(f'./files/{folder_name}'):
                shutil.rmtree(f'./files/{folder_name}')
            os.mkdir(f'./files/{folder_name}')
            for mission in dds[dd_str]['Stages']:
                img_count += 1
                fname = str(img_count)
                mission.save(f'./files/{folder_name}/{fname}.png')
        sleep(0.25)

#def wrap_missions_executor(missions):
    #mission_futures = []
    #with ThreadPoolExecutor() as executor:
        #for mission in missions:
            #if len(mission) > 5:
                #six = True
            #else:
                #six = False
            #future = executor.submit(render_mission, mission, six)
            #mission_futures.append(future)
        #results = [future.result() for future in mission_futures]
        #return results
#def wrap_biomes_executor(Biomes):
    #with ThreadPoolExecutor() as executor:
        #biome_futures = {}
        #for biome, missions in Biomes.items():
            #future = executor.submit(wrap_missions_executor, missions)
            #biome_futures[biome] = future
        #results = {biome: future.result() for biome, future in biome_futures.items()}
        #return results
#def render_biomes(Biomes):
    #start_time = time.time()
    #rendered_biomes = wrap_biomes_executor(Biomes)
    #print(time.time() - start_time)
    #return rendered_biomes

def render_biomes(Biomes):
    rendered_biomes = {}
    for biome, missions in Biomes.items():
        biome1 = []
        if len(missions) > 5:
            six = True
        else:
            six = False
        for mission in missions:
            mission1 = {}
            mission1['CodeName'] = mission['CodeName']
            mission_png = render_mission(mission, six)
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
        has_id_999 = False
        has_id_0 = False
        for stage in deepdive['Stages']:
            if stage['id'] == 999:
                has_id_999 = True
            if stage['id'] == 0:
                has_id_0 = True
        for stage in deepdive['Stages']:
            if has_id_999 and has_id_0:
                if stage['id'] == 999:
                    stage['id'] = -1
        sorted_stages = sorted(deepdive['Stages'], key=lambda x: x['id'], reverse=True)
        for stage in sorted_stages:
            stage_png = render_dd_stage(stage)
            rendered_deepdives[t]['Stages'].append(stage_png)
    return rendered_deepdives


def scanners(html):
    html += '          <br><span class="scanners">// SCANNERS OUT OF RANGE \\\\</span>\n'
    return html
def array_standard_missions(Biomes, biome_str, html, nextindex):
    html += '         <br>\n'
    url_biome = biome_str.replace(' ', '%20')
    img_count = 0
    for mission in Biomes[biome_str]:
        img_count += 1
        if nextindex:
            fname = f'/upcoming_png?img={url_biome}_{str(img_count)}'
        else:
            fname = f'/png?img={url_biome}_{str(img_count)}'
        html += f'          <div class="mission-hover-zoom"><img class="mission" src="{fname}"></div>\n'
    return html
def array_dd_missions(dds, dd_str, stg_count, html):
    biomes = {
        'Crystalline Caverns': 'DeepDive_MissionBar_CrystalCaves.png',
        'Glacial Strata': 'DeepDive_MissionBar_GlacialStrata.png',
        'Radioactive Exclusion Zone': 'DeepDive_MissionBar_Radioactive.png',
        'Fungus Bogs': 'DeepDive_MissionBar_FungusBogs.png',
        'Dense Biozone': 'DeepDive_MissionBar_LushDownpour.png',
        'Salt Pits': 'DeepDive_MissionBar_SaltPits.png',
        'Sandblasted Corridors': 'DeepDive_MissionBar_Sandblasted.png',
        'Magma Core': 'DeepDive_MissionBar_MagmaCore.png',
        'Azure Weald': 'DeepDive_MissionBar_AzureWeald.png',
        'Hollow Bough': 'DeepDive_MissionBar_FungusBogs.png'
    }
    biome = dds[dd_str]['Biome']
    biome1 = biomes[biome]
    html += f'         <img title="{biome}" class="dd-biome" src="/files/{biome1}">\n'
    html += '         <br>\n'
    folder_name = dd_str.replace(' ', '_')
    for mission in dds[dd_str]['Stages']:
        stg_count += 1
        fname = str(stg_count)
        html += f'         <div class="mission-hover-zoom"><img class="mission" title="Stage {fname}" src="/files/{folder_name}/{fname}.png"></div>\n'
    return html
def render_index(timestamp, next_timestamp, DDs):
    img_count = 0
    Biomes = timestamp['Biomes']
    next_Biomes = next_timestamp['Biomes']
    DeepDives = DDs['Deep Dives']
    nextindex = False
    html = '''  <!DOCTYPE html>
    <html>
        <head>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.4/jquery.min.js"></script>
        <script>
        $(document).ready(function(){
            $(this).scrollTop(0);
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
            const countdownTimer1 = setInterval(updateCountdown1, 1000);

            function updateCountdown1() {
                const remainingTime1 = Math.floor(((targetTime1 - new Date() + 2) / 1000));
                if (remainingTime1 < 0 && !isReloading) {
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
                $("#DAILYDEAL").slideToggle(500, function() {
                if ($("#DAILYDEAL").is(":hidden")) {
                    $("#dailydealbutton").text("Show Daily Deal");
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
                slideButton.textContent = "Show countdown";
                currentButton.style.display = "inline-block";
                dailydealbutton.style.display = "inline-block";
                dailydealbutton.textContent = "Show Daily Deal";
                DAILYDEAL.style.display = "none";
                missionscountdown.style.display = "none";
                buttonsbutton.textContent = " x ";
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
        </script>
        <title>Current Missions from the Hoxxes IV Space Rig Mission Terminal</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta property="og:title" content="Current and Upcoming Missions from the Hoxxes IV Mission Terminal">
        <meta property="og:type" content="website">
        <meta property="og:image" content="/files/Mission_control_portrait.png">
        <meta property="og:description" content="Deep Rock Galactic Mission Tracker">
        <link rel ="icon" href="/files/favicon.ico" type="image/x-icon">
        <link rel ="stylesheet" href="/files/styles.css" type="text/css">
        </head>
        <body bgcolor="#303030">
        <video id="background-video" autoplay muted loop><source src="/files/space_rig.webm" type="video/webm"></video>
        <div class="overlay"></div>
        <p class="loading">Loading</p>
        <div id="countdowncontainer">
            <button id="backgroundButton">Hide background</button><button id="buttonsbutton">x</button><br>
            <div id=DAILYDEAL><img id="DailyDeal" class="daily_trade" src="/dailydeal"></div><button id="dailydealbutton">Show Daily Deal</button><br>
            <div id="missionscountdown">NEW MISSIONS IN<br>
            <span id="countdown"></span></div><button id="slideButton">Hide countdown</button><br>
            <button id="currentButton">Click here to see upcoming missions</button>
        </div>
        <div id="current">\n'''
    html += '''      <div class="grid-container">
            <h2>
            <div class="biome-container">
             <img title="Glacial Strata" class="image-container" src="/files/DeepDive_MissionBar_GlacialStrata.png">\n'''
    if 'Glacial Strata' not in Biomes.keys():
        html = scanners(html)
    else:
        html = array_standard_missions(Biomes, 'Glacial Strata', html, nextindex)
    html += '''        </div>
           </h2>
           <h2>
            <div class="biome-container">
             <img title="Crystalline Caverns" class="image-container" src="/files/DeepDive_MissionBar_CrystalCaves.png">\n'''
    if 'Crystalline Caverns' not in Biomes.keys():
        html = scanners(html)
    else:
        html = array_standard_missions(Biomes, 'Crystalline Caverns', html, nextindex)
    html += '''        </div>
       </h2>
       <h2>
        <div class="biome-container">
         <img title="Salt Pits" class="image-container" src="/files/DeepDive_MissionBar_SaltPits.png">\n'''
    if 'Salt Pits' not in Biomes.keys():
        html = scanners(html)
    else:
        html = array_standard_missions(Biomes, 'Salt Pits', html, nextindex)
    html += '''        </div>
       </h2>
       <h2>
        <div class="biome-container">
         <img title="Magma Core" class="image-container" src="/files/DeepDive_MissionBar_MagmaCore.png">\n'''
    if 'Magma Core' not in Biomes.keys():
        html = scanners(html)
    else:
        html = array_standard_missions(Biomes, 'Magma Core', html, nextindex)
    html += '''        </div>
           </h2>
           <h2>
            <div class ="biome-container">
             <img title="Azure Weald" class="image-container" src="/files/DeepDive_MissionBar_AzureWeald.png">\n'''
    if 'Azure Weald' not in Biomes.keys():
        html = scanners(html)
    else:
        html = array_standard_missions(Biomes, 'Azure Weald', html, nextindex)
    html += '''        </div>
           </h2>
           <h2>
            <div class ="biome-container">
             <img title="Sandblasted Corridors" class="image-container" src="/files/DeepDive_MissionBar_Sandblasted.png">\n'''
    if 'Sandblasted Corridors' not in Biomes.keys():
        html = scanners(html)
    else:
        html = array_standard_missions(Biomes, 'Sandblasted Corridors', html, nextindex)
    html += '''        </div>
           </h2>
           <h2>
            <div class = "biome-container">
             <img title="Fungus Bogs" class="image-container" src="/files/DeepDive_MissionBar_FungusBogs.png">\n'''
    if 'Fungus Bogs' not in Biomes.keys():
        html = scanners(html)
    else:
        html = array_standard_missions(Biomes, 'Fungus Bogs', html, nextindex)
    html += '''        </div>
           </h2>
           <h2>
            <div class ="biome-container">
             <img title="Radioactive Exclusion Zone" class="image-container" src="/files/DeepDive_MissionBar_Radioactive.png">\n'''
    if 'Radioactive Exclusion Zone' not in Biomes.keys():
        html = scanners(html)
    else:
        html = array_standard_missions(Biomes, 'Radioactive Exclusion Zone', html, nextindex)
    html += '''        </div>
           </h2>
           <h2>
            <div class ="biome-container">
             <img title="Dense Biozone" class="image-container" src="/files/DeepDive_MissionBar_LushDownpour.png">\n'''
    if 'Dense Biozone' not in Biomes.keys():
        html = scanners(html)
    else:
        html = array_standard_missions(Biomes, 'Dense Biozone', html, nextindex)
    html += '''        </div>
           </h2>
           <h2>
            <div class ="biome-container">
             <img title="Hollow Bough" class="image-container" src="/files/DeepDive_MissionBar_HollowBough.png">\n'''
    if 'Hollow Bough' not in Biomes.keys():
        html = scanners(html)
    else:
        html = array_standard_missions(Biomes, 'Hollow Bough', html, nextindex)
    html += '''       </h2>
    	    </div>
    	    </div>\n'''
    nextindex = True
    html += '''          <div id="upcoming" style="visibility: hidden;">
          <div class="grid-container">
                    <h2>
            <div class="biome-container">
             <img title="Glacial Strata" class="image-container" src="/files/DeepDive_MissionBar_GlacialStrata.png">\n'''
    if 'Glacial Strata' not in next_Biomes.keys():
        html = scanners(html)
    else:
        html = array_standard_missions(next_Biomes, 'Glacial Strata', html, nextindex)
    html += '''        </div>
           </h2>
           <h2>
            <div class="biome-container">
             <img title="Crystalline Caverns" class="image-container" src="/files/DeepDive_MissionBar_CrystalCaves.png">\n'''
    if 'Crystalline Caverns' not in next_Biomes.keys():
        html = scanners(html)
    else:
        html = array_standard_missions(next_Biomes, 'Crystalline Caverns', html, nextindex)
    html += '''        </div>
       </h2>
       <h2>
        <div class="biome-container">
         <img title="Salt Pits" class="image-container" src="/files/DeepDive_MissionBar_SaltPits.png">\n'''
    if 'Salt Pits' not in next_Biomes.keys():
        html = scanners(html)
    else:
        html = array_standard_missions(next_Biomes, 'Salt Pits', html, nextindex)
    html += '''        </div>
       </h2>
       <h2>
        <div class="biome-container">
         <img title="Magma Core" class="image-container" src="/files/DeepDive_MissionBar_MagmaCore.png">\n'''
    if 'Magma Core' not in next_Biomes.keys():
        html = scanners(html)
    else:
        html = array_standard_missions(next_Biomes, 'Magma Core', html, nextindex)
    html += '''        </div>
           </h2>
           <h2>
            <div class ="biome-container">
             <img title="Azure Weald" class="image-container" src="/files/DeepDive_MissionBar_AzureWeald.png">\n'''
    if 'Azure Weald' not in next_Biomes.keys():
        html = scanners(html)
    else:
        html = array_standard_missions(next_Biomes, 'Azure Weald', html, nextindex)
    html += '''        </div>
           </h2>
           <h2>
            <div class ="biome-container">
             <img title="Sandblasted Corridors" class="image-container" src="/files/DeepDive_MissionBar_Sandblasted.png">\n'''
    if 'Sandblasted Corridors' not in next_Biomes.keys():
        html = scanners(html)
    else:
        html = array_standard_missions(next_Biomes, 'Sandblasted Corridors', html, nextindex)
    html += '''        </div>
           </h2>
           <h2>
            <div class = "biome-container">
             <img title="Fungus Bogs" class="image-container" src="/files/DeepDive_MissionBar_FungusBogs.png">\n'''
    if 'Fungus Bogs' not in next_Biomes.keys():
        html = scanners(html)
    else:
        html = array_standard_missions(next_Biomes, 'Fungus Bogs', html, nextindex)
    html += '''        </div>
           </h2>
           <h2>
            <div class ="biome-container">
             <img title="Radioactive Exclusion Zone" class="image-container" src="/files/DeepDive_MissionBar_Radioactive.png">\n'''
    if 'Radioactive Exclusion Zone' not in next_Biomes.keys():
        html = scanners(html)
    else:
        html = array_standard_missions(next_Biomes, 'Radioactive Exclusion Zone', html, nextindex)
    html += '''        </div>
           </h2>
           <h2>
            <div class ="biome-container">
             <img title="Dense Biozone" class="image-container" src="/files/DeepDive_MissionBar_LushDownpour.png">\n'''
    if 'Dense Biozone' not in next_Biomes.keys():
        html = scanners(html)
    else:
        html = array_standard_missions(next_Biomes, 'Dense Biozone', html, nextindex)
    html += '''        </div>
           </h2>
           <h2>
            <div class ="biome-container">
             <img title="Hollow Bough" class="image-container" src="/files/DeepDive_MissionBar_HollowBough.png">\n'''
    if 'Hollow Bough' not in next_Biomes.keys():
        html = scanners(html)
    else:
        html = array_standard_missions(next_Biomes, 'Hollow Bough', html, nextindex)
    img_count = 0
    html += '''       </h2>
         </div>
         </div>
           <div class="grid-container">
            <div class="dd-container">
               <h2>
              <img class="image-container" src="/files/dd.png">\n'''
    html = array_dd_missions(DeepDives, 'Deep Dive Normal', img_count, html)
    html += '''         </h2>
            </div>
            <div class="dd-container">
               <h2>
              <img class="image-container" src="/files/edd.png">\n'''
    html = array_dd_missions(DeepDives, 'Deep Dive Elite', img_count, html)
    html += '''           </h2>
            </div>
    	    </div>
              <div>
               <div class="ddscountdown">NEW DEEP DIVES IN</div>
              <span id="ddcountdown"></span>
               <hr>
            </div>
              <div class="jsonc">
             <div class="jsonlinks"><span><a class="jsonlink" href="/json?data=bulkmissions">FULL MISSION DATA</a> <a class="jsonlink" href="/json?data=current">CURRENT MISSION DATA</a> <a class="jsonlink" href="/json?data=next">UPCOMING MISSION DATA</a> <a class="jsonlink" href="/json?data=DD">CURRENT DD DATA</a> <a class="jsonlink" href="/json?data=dailydeal">CURRENT DAILY DEAL DATA</a></span></div>
               <span class="credits">Send credits (eth): 0xb9c8591A80A3158f7cFFf96EC3c7eA9adB7818E7</span></div>
              <p class='gsgdisclaimer'><i>This website is a third-party platform and is not affiliated, endorsed, or sponsored by Ghost Ship Games. The use of Deep Rock Galactic's in-game assets on this website is solely for illustrative purposes and does not imply any ownership or association with the game or its developers. All copyrights and trademarks belong to their respective owners. For official information about Deep Rock Galactic, please visit the official Ghost Ship Games website.</i></p></div>
        </body>
    </html>'''
    return html

with open('drgmissionsgod.json', 'r') as f:
    DRG = f.read()
    f.close()
DRG = DRG.replace(':02Z', ':00Z')
DRG = json.loads(DRG)
DRG = order_dictionary_by_date(DRG)

with open('drgdailydeals.json', 'r') as f:
    AllTheDeals = f.read()
    f.close()
AllTheDeals = AllTheDeals.replace(':01Z', ':00Z')
AllTheDeals = json.loads(AllTheDeals)
AllTheDeals = order_dictionary_by_date(AllTheDeals)

tstamp = queue.Queue()
tstampthread = threading.Thread(target=rotate_timestamp, args=(DRG, tstamp, False,))

next_tstamp = queue.Queue()
next_tstampthread = threading.Thread(target=rotate_timestamp, args=(DRG, next_tstamp, True,))

dailydeal_tstamp = queue.Queue()
dailydeal_tstampthread = threading.Thread(target=rotate_timestamp, args=(AllTheDeals, dailydeal_tstamp, False))

dailydeal = queue.Queue()
dailydealthread = threading.Thread(target=rotate_dailydeal, args=(AllTheDeals, dailydeal_tstamp, dailydeal))

rendering_event = threading.Event()
currybiomes = queue.Queue()
biomesthread = threading.Thread(target=rotate_biomes, args=(DRG, tstamp, currybiomes, rendering_event))

rendering_event_next = threading.Event()
nextbiomes = queue.Queue()
nextbiomesthread = threading.Thread(target=rotate_biomes, args=(DRG, next_tstamp, nextbiomes, rendering_event_next))

wait_rotationthread = threading.Thread(target=wait_rotation, args=(rendering_event, rendering_event_next))

DDs = queue.Queue()
ddsthread = threading.Thread(target=rotate_DDs, args=(DDs,))

def start_threads():
    tstampthread.start()
    next_tstampthread.start()
    
    biomesthread.start()
    nextbiomesthread.start()
    
    ddsthread.start()
    
    wait_rotationthread.start()
    
    dailydeal_tstampthread.start()
    dailydealthread.start()
    
#def join_threads():
    #tstampthread.join()
    #next_tstampthread.join()
    #biomesthread.join()
    #nextbiomesthread.join()
    #ddsthread.join()
    #wait_rotationthread.join()
    #dailydeal_tstampthread.join()
    #dailydealthread.join()

app = Flask(__name__, static_folder=f'{os.getcwd()}/files')

@app.route('/')
def home():
    rendering_event.wait()
    rendering_event_next.wait()
    current_timestamp = tstamp.queue[0]
    next_timestamp = next_tstamp.queue[0]
    DDs_ = DDs.queue[0]
    return render_template_string(render_index(DRG[current_timestamp], DRG[next_timestamp],  DDs_,))

@app.route('/png')
def serve_img():
    img_arg = request.args.get('img')
    try:
        img_arg = img_arg.split('_')
        biomestr = img_arg[0].replace('%20', ' ')
        img_index_ = int(img_arg[1])
        start_time = time.time()
        while True:
            try:
                Biomes = currybiomes.queue[0]
                break
            except Exception:
                if time.time() - start_time > 4:
                    return 'Response Timeout', 408
                continue
        count = 0
        for mission in Biomes[biomestr]:
            count += 1
            if count == img_index_:
                if request.headers.get('If-None-Match') == mission['etag']:
                    return '', 304
                mission1 = BytesIO()
                mission1.write(mission['rendered_mission'].getvalue())
                mission1.seek(0)
                response = make_response(send_file(mission1, mimetype='image/png'))
                response.headers['ETag'] = mission['etag']
                return response
    except Exception:
        return '<!doctype html><html lang=en><title>404 Not Found</title><h1>Not Found</h1><p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>', 404

@app.route('/upcoming_png')
def serve_next_img():
    img_arg = request.args.get('img')
    try:
        img_arg = img_arg.split('_')
        biomestr = img_arg[0].replace('%20', ' ')
        img_index_ = int(img_arg[1])
        start_time = time.time()
        while True:
            try:
                Biomes = nextbiomes.queue[0]
                break
            except Exception:
                if time.time() - start_time > 4:
                    return 'Response Timeout', 408
                continue
        count = 0
        for mission in Biomes[biomestr]:
            count += 1
            if count == img_index_:
                if request.headers.get('If-None-Match') == mission['etag']:
                    return '', 304
                mission1 = BytesIO()
                mission1.write(mission['rendered_mission'].getvalue())
                mission1.seek(0)
                response = make_response(send_file(mission1, mimetype='image/png'))
                response.headers['ETag'] = mission['etag']
                return response
    except Exception:
        return '<!doctype html><html lang=en><title>404 Not Found</title><h1>Not Found</h1><p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>', 404

@app.route('/dailydeal')
def serve_dailydeal_png():
    try:
        start_time = time.time()
        while True:
            try:
                daily_deal = dailydeal.queue[0]
                break
            except Exception:
                if time.time() - start_time > 4:
                    return 'Response Timeout', 408
                continue
        if request.headers.get('If-None-Match') == daily_deal['etag']:
            return '', 304
        daily_deal1 = BytesIO()
        daily_deal1.write(daily_deal['rendered_dailydeal'].getvalue())
        daily_deal1.seek(0)
        response = make_response(send_file(daily_deal1, mimetype='image/png'))
        response.headers['ETag'] = daily_deal['etag']
        return response
    except Exception:
        return '<!doctype html><html lang=en><title>404 Not Found</title><h1>Not Found</h1><p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>', 404
    

@app.route('/json')
def serve_json():
    json_arg = request.args.get('data')
    if json_arg:
        if json_arg == 'bulkmissions':
            return jsonify(DRG)
        elif json_arg == 'DD':
            return jsonify(DDs.queue[0])
        elif json_arg == 'current':
            applicable_timestamp = tstamp.queue[0]
            return jsonify(DRG[applicable_timestamp])
        elif json_arg == 'next':
            applicable_timestamp = next_tstamp.queue[0]
            return jsonify(DRG[applicable_timestamp])
        elif json_arg == 'dailydeal':
            applicable_timestamp = dailydeal_tstamp.queue[0]
            return jsonify(AllTheDeals[applicable_timestamp])
        else:
            return '<!doctype html><html lang=en><title>404 Not Found</title><h1>Not Found</h1><p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>', 404
    else:
        return '<!doctype html><html lang=en><title>404 Not Found</title><h1>Not Found</h1><p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>', 404

with open('token.txt', 'r') as f:
    AUTH_TOKEN = f.read().strip()
    f.close()
    
with open('ip.txt', 'r') as f:
    ALLOWED_IP = f.read().strip()
    f.close()
    
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    try:
        token = request.headers.get('Authorization')
        if not token or token != f"Bearer {AUTH_TOKEN}":
            return '<!doctype html><html lang=en><title>404 Not Found</title><h1>Not Found</h1><p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>', 404
        request_ip = request.headers.get('X-Forwarded-For')
        if request_ip != ALLOWED_IP:
            return "Forbidden", 403
        if 'file' not in request.files:
            return "No file in the request", 400
        file_ = request.files['file']
        cwd = os.getcwd()
        filename = file_.filename
        if filename.endswith('.json') or filename.endswith('.py'):
            file_.save(f'{cwd}/{filename}')
        elif filename.endswith('icon.png'):
            file_.save(f'{cwd}/img/{filename}')
        else:
            file_.save(f'{cwd}/files/{filename}')
        response_data = {'message': 'Success'}
        return jsonify(response_data)
    except Exception:
        return '<!doctype html><html lang=en><title>404 Not Found</title><h1>Not Found</h1><p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>', 404

if __name__ == '__main__':
    start_threads()
    app.run(threaded=True, host='127.0.0.1', port=5000)