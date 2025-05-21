from hashlib import md5
from time import sleep, time
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from datetime import datetime, timedelta, timezone
from functools import wraps
from psutil import Process, process_iter
from signal import signal, SIGINT, SIGTERM
from random import choice
from copy import deepcopy
import subprocess
import os
import shutil
import glob
import json
cpu_count = os.cpu_count()
cpu_count = 1 # dont bother lol

def get_process_name():
    return Process(os.getpid()).name()

if cpu_count >= 4:
    from multiprocessing import Pool, Manager, Event
    if os.name == 'nt':
        print('Look at these processes importing everything again lmao. Spawn sucks, man. I\'m not going to bother atomizing this module for spawn at this stage.')
else:
    Event = None
    if get_process_name() == 'gunicorn':
        from multiprocessing import Manager
    else:
        class Manager:
            def list(self):
                return []
            def shutdown(self):
                return
            
#----------------------------------------------
# MISSION ICONS AND DAILY DEAL PIL FUNCTIONS
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

def calc_text_center(image_width, image_height, text, font, font_size):
    temp_image = Image.new("RGB", (image_width, image_height))
    temp_draw = ImageDraw.Draw(temp_image)

    text_bbox = temp_draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]

    text_x = (image_width - text_width) // 2
    text_y = (image_height - text_height) // 2
    temp_image.close()
    del temp_draw
    return text_x, text_y

def render_daily_deal_bubble(changepercent, dealtype):
    save_profit = {
        'Buy':'Savings!',
        'Sell':'Profit!',
        }

    bubble = Image.open('./static/img/Icon_TradeTerminal_SaleBubble.png')
    bubble = scale_image(bubble, 0.8)

    font_path = './static/img/Bungee-Regular.ttf'
    font_size = 75
    font = ImageFont.truetype(font_path, font_size)
    text = str(round(changepercent))
    if len(text) == 2:
        digit1_text = list(text)[0]
        digit2_text = f'{list(text)[1]}%'

        digit1 = ImageDraw.Draw(bubble)
        digit1_x, digit1_y = calc_text_center(bubble.width, bubble.height, digit1_text, font, font_size)
        digit1.text((digit1_x-60, digit1_y-15), digit1_text, font=font, fill=(0, 0, 0))

        digit2 = ImageDraw.Draw(bubble)
        digit2.text((digit1_x-5, digit1_y-15), digit2_text, font=font, fill=(0, 0, 0))

        del digit1
        del digit2

        savings_profit = ImageDraw.Draw(bubble)
        font_size = 30
        font = ImageFont.truetype(font_path, font_size)
        savings_x, savings_y = calc_text_center(bubble.width, bubble.height, save_profit[dealtype], font, font_size)
        savings_profit.text((savings_x, savings_y+38), save_profit[dealtype], font=font, fill=(0, 0, 0))

    else:
        text = f'{text}%'
        changepercent = ImageDraw.Draw(bubble)
        text_x, text_y = calc_text_center(bubble.width, bubble.height, text, font, font_size)
        changepercent.text((text_x, text_y-15), text, font=font, fill=(0, 0, 0))
        del changepercent

        savings_profit = ImageDraw.Draw(bubble)
        font_size = 30
        font = ImageFont.truetype(font_path, font_size)
        savings_x, savings_y = calc_text_center(bubble.width, bubble.height, save_profit[dealtype], font, font_size)
        savings_profit.text((savings_x, savings_y+38), save_profit[dealtype], font=font, fill=(0, 0, 0))

    del savings_profit

    return bubble

def render_daily_deal_resource_and_amount(resources, resource, resourceamount):

    resource = Image.open(resources[resource])
    resource = scale_image(resource, 0.3)

    text = str(resourceamount)
    font_path = './static/img/Bungee-Regular.ttf'
    font_size = 75
    font = ImageFont.truetype(font_path, font_size)
    text_width = len(text) * font_size
    text_height = len(text) * font_size

    image_width = text_width + (2 * resource.width)
    image_height = text_height

    background = Image.new("RGBA", (image_width, image_height), (0, 0, 0, 0))
    x, y = calc_center(resource, background)
    background.paste(resource, (25,y))
    background.paste(resource.transpose(Image.FLIP_LEFT_RIGHT), ((image_width - resource.width)-25, y))
    resource.close()

    draw = ImageDraw.Draw(background)
    text_x, text_y = calc_text_center(background.width, background.height, text, font, font_size)
    draw.text((text_x, text_y), text, font=font, fill=(255,255,255))
    del draw

    return background

def render_daily_deal_credits(credits):
    credits_ = Image.open('./static/img/Credit.png')
    credits_ = scale_image(credits_, 0.4)

    text = str(credits)
    font_path = './static/img/Bungee-Regular.ttf'
    font_size = 75
    font = ImageFont.truetype(font_path, font_size)
    text_width = len(text) * font_size
    text_height = len(text) * font_size
    image_width = text_width + (2 * credits_.width)
    image_height = text_height
    background = Image.new("RGBA", (image_width, image_height), (0, 0, 0, 0))
    x, y = calc_center(credits_, background)

    if len(text) < 5:
        background.paste(credits_, (35,y+10))
        background.paste(credits_, ((image_width - credits_.width)-35, y+10))
    else:
        background.paste(credits_, (55,y+10))
        background.paste(credits_, ((image_width - credits_.width)-55, y+10))
    credits_.close()

    draw = ImageDraw.Draw(background)
    text_x, text_y = calc_text_center(background.width, background.height, text, font, font_size)
    draw.text((text_x, text_y), text, font=font, fill=(255,255,255))
    del draw

    return background

def render_dailydeal(deal_dict):
    font_path = './static/img/CarbonBold-W00-Regular.ttf'
    font_size = 45
    font = ImageFont.truetype(font_path, font_size)
    resources = {
        'Bismor': './static/img/Bismor_icon.png',
        'Croppa': './static/img/Croppa_icon.png',
        'Enor Pearl': './static/img/Enor_pearl_icon.png',
        'Jadiz': './static/img/Jadiz_icon.png',
        'Magnite': './static/img/Magnite_icon.png',
        'Umanite': './static/img/Umanite_icon.png',

        'Credits': './static/img/Credit.png',
            }
    buy_or_get = {
        'Buy' : 'Pay',
        'Sell': 'Get',
        }

    background = Image.new("RGBA", (400, 635), (0, 44, 81, 255))
    background_head = Image.new("RGBA", (400, 120), (57, 148, 136, 255))
    x, y = calc_center(background_head, background)
    background.paste(background_head, (x, y-257), mask = background_head)
    background_head.close()

    text = "TODAY'S OFFER:"
    background_title = ImageDraw.Draw(background)
    text_x, text_y = calc_text_center(background.width, background.height, text, font, font_size)
    background_title.text((text_x, text_y-295), text, font=font, fill=(0, 0, 0))
    del background_title

    font_path = './static/img/Bungee-Regular.ttf'
    font_size = 60
    font = ImageFont.truetype(font_path, font_size)

    text = deal_dict['Resource']
    resource_TEXT = ImageDraw.Draw(background)
    text_x, text_y = calc_text_center(background.width, background.height, text, font, font_size)
    resource_TEXT.text((text_x, text_y-250), text, font=font, fill=(0, 0, 0))
    del resource_TEXT

    resourceamount_and_resource = render_daily_deal_resource_and_amount(resources, deal_dict['Resource'], deal_dict['ResourceAmount'])
    x, y = calc_center(resourceamount_and_resource, background)
    background.paste(resourceamount_and_resource, (x, y-130), mask=resourceamount_and_resource)
    resourceamount_and_resource.close()

    font_size = 35
    font = ImageFont.truetype(font_path, font_size)
    text = deal_dict['DealType']
    dealtype = ImageDraw.Draw(background)
    text_x, text_y = calc_text_center(background.width, background.height, text, font, font_size)
    dealtype.text((text_x, text_y-170), text, font=font, fill=(255, 255, 255))

    text = buy_or_get[deal_dict['DealType']]
    dealtype = ImageDraw.Draw(background)
    text_x, text_y = calc_text_center(background.width, background.height, text, font, font_size)
    dealtype.text((text_x, text_y-33), text, font=font, fill=(255, 255, 255))
    del dealtype

    credits = deal_dict['Credits']
    credits_ = render_daily_deal_credits(credits)
    x, y = calc_center(credits_, background)
    background.paste(credits_, (x, y+10), mask=credits_)
    credits_.close()

    bubble = render_daily_deal_bubble(deal_dict['ChangePercent'], deal_dict['DealType'])
    bubble = bubble.rotate(-20, expand=True)
    x, y = calc_center(bubble, background)
    background.paste(bubble, (x-60, y+200), mask=bubble)
    bubble.close()

    background = scale_image(background, 0.5)
    # background.save('TEST.png', format='PNG')
    # subprocess.run(['gwenview', 'TEST.png'])
    return background

standard_mission_primary_resources_images = {
    'Mining Expedition': Image.open('./static/img/Morkite_icon.png'),
    'Egg Hunt': Image.open('./static/img/Alien_egg_icon.png'),
    'On-Site Refining': Image.open('./static/img/Icon_PumpingJack_Core_Simplified_Workfile.png'),
    'Salvage Operation': Image.open('./static/img/Icon_Salvage_Mules_Objective.png'),
    'Escort Duty': Image.open('./static/img/Icon_FuelCannister_Simplified.png'),
    'Point Extraction': Image.open('./static/img/Icons_Resources_Outline_Aquarq.png'),
    'Elimination': Image.open('./static/img/Kill_Dreadnought_Objective_icon.png'),
    'Industrial Sabotage': Image.open('./static/img/Icon_Facility_DataRack.png'),
    'Deep Scan' : Image.open('./static/img/Icons_Resources_Detailed_Outline_ResonanceScannerPod.png'),
    'Hexagon' : Image.open('./static/img/hexagon.png')
    }
for k in standard_mission_primary_resources_images:
    copy_ = standard_mission_primary_resources_images[k].copy()
    standard_mission_primary_resources_images[k].close()
    standard_mission_primary_resources_images[k] = copy_

standard_mission_images = {
    'primary_objs' : {
        'Mining Expedition': Image.open('./static/img/Mining_expedition_icon.png'),
        'Egg Hunt': Image.open('./static/img/Egg_collection_icon.png'),
        'On-Site Refining': Image.open('./static/img/Refining_icon.png'),
        'Salvage Operation': Image.open('./static/img/Salvage_icon.png'),
        'Escort Duty': Image.open('./static/img/Escort_icon.png'),
        'Point Extraction': Image.open('./static/img/Point_extraction_icon.png'),
        'Elimination': Image.open('./static/img/Elimination_icon.png'),
        'Industrial Sabotage': Image.open('./static/img/Sabotage_icon.png'),
        'Deep Scan' : Image.open('./static/img/Deep_scan_icon.png')
            },
    'secondary_objs' : {
        'ApocaBlooms': Image.open('./static/img/ApocaBlooms_icon.png'),
        'Fossils': Image.open('./static/img/Fossils_icon.png'),
        'Boolo Caps': Image.open('./static/img/Boolo_Caps_icon.png'),
        'Dystrum': Image.open('./static/img/Dystrum_icon.png'),
        'Ebonuts': Image.open('./static/img/Ebonuts_icon.png'),
        'Fester Fleas': Image.open('./static/img/Fester_Fleas_icon.png'),
        'Gunk Seeds': Image.open('./static/img/Gunk_Seeds_icon.png'),
        'Hollomite': Image.open('./static/img/Hollomite_icon.png'),
        'Bha Barnacles' : Image.open('./static/img/Bha_Barnacles_icon.png'),
        'Glyphid Eggs' : Image.open('./static/img/Glyphid_Eggs_icon.png')
            },
    'complexities' : {
        '1': Image.open('./static/img/Icons_complexity_1.png'),
        '2': Image.open('./static/img/Icons_complexity_2.png'),
        '3': Image.open('./static/img/Icons_complexity_3.png')
            },
    'lengths' : {
        '1': Image.open('./static/img/Icons_length_1.png'),
        '2': Image.open('./static/img/Icons_length_2.png'),
        '3': Image.open('./static/img/Icons_length_3.png')
            },
    'mutators' : {
        'Critical Weakness': Image.open('./static/img/Mutator_critical_weakness_icon.png'),
        'Gold Rush': Image.open('./static/img/Mutator_gold_rush_icon.png'),
        'Double XP': Image.open('./static/img/Mutator_triple_xp_icon.png'),
        'Golden Bugs': Image.open('./static/img/Mutator_golden_bugs_icon.png'),
        'Low Gravity': Image.open('./static/img/Mutator_no_fall_damage_icon.png'),
        'Mineral Mania': Image.open('./static/img/Mutator_mineral_mania_icon.png'),
        'Rich Atmosphere': Image.open('./static/img/Mutator_rich_atmosphere_icon.png'),
        'Volatile Guts': Image.open('./static/img/Mutator_volatile_guts_icon.png'),
        'Blood Sugar' : Image.open('./static/img/Mutator_blood_sugar_icon.png'),
        'Secret Secondary' : Image.open('./static/img/Mutator_secret_secondary_icon.png')
            },
    'warnings' : {
        'Cave Leech Cluster': Image.open('./static/img/Warning_cave_leech_cluster_icon.png'),
        'Exploder Infestation': Image.open('./static/img/Warning_exploder_infestation_icon.png'),
        'Haunted Cave': Image.open('./static/img/Warning_haunted_cave_icon.png'),
        'Lethal Enemies': Image.open('./static/img/Warning_lethal_enemies_icon.png'),
        'Low Oxygen': Image.open('./static/img/Warning_low_oxygen_icon.png'),
        'Mactera Plague': Image.open('./static/img/Warning_mactera_plague_icon.png'),
        'Parasites': Image.open('./static/img/Warning_parasites_icon.png'),
        'Regenerative Bugs': Image.open('./static/img/Warning_regenerative_bugs_icon.png'),
        'Shield Disruption': Image.open('./static/img/Warning_shield_disruption_icon.png'),
        'Elite Threat': Image.open('./static/img/Warning_elite_threat_icon.png'),
        'Swarmageddon': Image.open('./static/img/Warning_swarmageddon_icon.png'),
        'Lithophage Outbreak': Image.open('./static/img/Warning_lithophage_outbreak_icon.png'),
        'Rival Presence': Image.open('./static/img/Warning_rival_presence_icon.png'),
        'Duck and Cover': Image.open('./static/img/Warning_duck_and_cover_icon.png'),
        'Ebonite Outbreak' : Image.open('./static/img/Warning_ebonite_outbreak_icon.png'),
        'Tougher Enemies' : Image.open('./static/img/Warning_tougher_enemies_icon.png'),
            }
    }
for k in standard_mission_images.keys():
    for k_ in standard_mission_images[k].keys():
        copy_ = standard_mission_images[k][k_].copy()
        standard_mission_images[k][k_].close()
        standard_mission_images[k][k_] = copy_

def render_mission_obj_resource(primary_obj, complexity, length):
    font_path = './static/img/CarbonBold-W00-Regular.ttf'
    font_size = 45
    font = ImageFont.truetype(font_path, font_size)
    text_color = (255, 255, 255)
    values = {
        ('Mining Expedition', '1', '1'): '200',
        ('Mining Expedition', '1', '2'): '225',
        ('Mining Expedition', '2', '2'): '250',
        ('Mining Expedition', '2', '3'): '325',
        ('Mining Expedition', '3', '3'): '400',
        ('Egg Hunt', '1'): '4',
        ('Egg Hunt', '2'): '6',
        ('Egg Hunt', 'default'): '8',
        ('Point Extraction', '2'): '7',
        ('Point Extraction', 'default'): '10',
        ('Industrial Sabotage', 'default'): '1',
        ('On-Site Refining', 'default'): '3',
        ('Escort Duty', '2'): '1',
        ('Escort Duty', 'default'): '2',
        ('Elimination', '2'): '2',
        ('Elimination', 'default'): '3',
        ('Salvage Operation', '2'): '2',
        ('Salvage Operation', 'default'): '3',
        ('Deep Scan', '3', '2') : '5',
        ('Deep Scan', '2', '1') : '3',
    }

    background = Image.new("RGBA", (256, 256), (0,0,0,0))
    hexagon = standard_mission_primary_resources_images['Hexagon'].copy()
    hexagon = scale_image(hexagon, 0.4)
    #x, y = calc_center(hexagon, background)
    #print(f'hexagon X: {str(x)}')
    #print(f'hexagon Y: {str(y)}')
    background.paste(hexagon, (69, 59), mask=hexagon)
    hexagon.close()

    resource = standard_mission_primary_resources_images[primary_obj].copy()
    if primary_obj == 'Mining Expedition':
        resource = scale_image(resource, 0.2)
    elif primary_obj == 'Egg Hunt':
        resource = scale_image(resource, 0.25)
    else:
        resource = scale_image(resource, 0.14)
    x, y = calc_center(resource, background)
    if primary_obj == 'Mining Expedition':
        background.paste(resource, (x, y-20), mask=resource)
    else:
        background.paste(resource, (x, y-13), mask=resource)
    resource.close()

    text = values.get((primary_obj, complexity, length), values.get((primary_obj, length), values.get((primary_obj, 'default'), 'Unknown')))
    draw = ImageDraw.Draw(background)
    text_x, text_y = calc_text_center(background.width, background.height, text, font, font_size)
    if primary_obj == 'Mining Expedition':
        draw.text((text_x, text_y+15), text, font=font, fill=text_color)
    else:
        draw.text((text_x, text_y+25), text, font=font, fill=text_color)
    del draw
    return background

def render_mission(m_d):
    background = Image.new("RGBA", (350, 300), (0,0,0,0))

    primary = standard_mission_images['primary_objs'][m_d['PrimaryObjective']].copy()
    primary = scale_image(primary, 0.4)
    #x, y = calc_center(primary, background)
    #print(f'primary X: {str(x)}')
    #print(f'primary Y: {str(y)}')
    background.paste(primary, (83, 58), mask=primary)
    primary.close()

    secondary = standard_mission_images['secondary_objs'][m_d['SecondaryObjective']].copy()
    secondary = scale_image(secondary, 0.6)
    #x, y = calc_center(secondary, background)
    #print(f'secondary X: {str(x-110)}')
    #print(f'secondary Y: {str(y-95)}')
    background.paste(secondary, (-11, -21), mask=secondary)
    secondary.close()

    if 'MissionWarnings' in m_d:
        MissionWarnings = []
        for warning in m_d['MissionWarnings']:
            MissionWarnings.append(warning)
        missionwarning1 = standard_mission_images['warnings'][MissionWarnings[0]].copy()
        missionwarning1 = scale_image(missionwarning1, 0.38)
        #x, y = calc_center(missionwarning1, background)
        #print(f'LONEWARNING X: {str(x+100)}')
        #print(f'LONEWARNING Y: {str(y-15)}')
        if len(MissionWarnings) == 1:
            background.paste(missionwarning1, (227, 87), mask=missionwarning1)
            missionwarning1.close()
        elif len(MissionWarnings) == 2:
            #print(f'WARNING 1 X: {str(x+100)}')
            #print(f'WARNING 1 Y: {str(y-60)}')
            background.paste(missionwarning1, (227, 42), mask=missionwarning1)
            missionwarning1.close()

            missionwarning2 = standard_mission_images['warnings'][MissionWarnings[1]].copy()
            missionwarning2 = scale_image(missionwarning2, 0.38)
            #x, y = calc_center(missionwarning2, background)
            #print(f'WARNING 2 X: {str(x+100)}')
            #print(f'WARNING 2 Y: {str(y+40)}')
            background.paste(missionwarning2, (227, 142), mask=missionwarning2)
            missionwarning2.close()

    if 'MissionMutator' in m_d:
        missionmutator = standard_mission_images['mutators'][m_d['MissionMutator']].copy()
        missionmutator = scale_image(missionmutator, 0.38)
        #x, y = calc_center(MISSIONMUTATOR, background)
        #print(f'MUTATOR X: {str(x-100)}')
        #print(f'MUTATOR Y: {str(y-10)}')
        background.paste(missionmutator, (27, 92), mask=missionmutator)
        missionmutator.close()

    complexity = standard_mission_images['complexities'][m_d['Complexity']].copy()
    complexity = scale_image(complexity, 0.45)
    #x, y = calc_center(complexity, background)
    #print(f'complexity X: {str(x)}')
    #print(f'complexity Y: {str(y-120)}')
    background.paste(complexity, (107, 2), mask=complexity)
    complexity.close()

    length = standard_mission_images['lengths'][m_d['Length']].copy()
    length = scale_image(length, 0.45)
    #x, y = calc_center(length, background)
    #print(f'length X: {str(x)}')
    #print(f'length Y: {str(y+120)}')
    background.paste(length, (107, 242), mask=length)
    length.close()

    primary_obj_resource = render_mission_obj_resource(m_d['PrimaryObjective'], m_d['Complexity'], m_d['Length'])
    primary_obj_resource = scale_image(primary_obj_resource, 0.8)
    #x, y = calc_center(primary_obj_resource, background)
    #print(f'obj_resource X: {str(x-110)}')
    #print(f'obj_resource Y: {str(y+95)}')
    background.paste(primary_obj_resource, (-37, 143), mask=primary_obj_resource)
    primary_obj_resource.close()

    background = scale_image(background, 0.46)
    #background.save('TEST.png', format='PNG')
    #subprocess.run(['gwenview', 'TEST.png'])
    #mission = {'rendered_mission': background, 'CodeName': m_d['CodeName'], 'id': m_d['id']}
    return background

def add_shadowed_text_to_image(bg, text, text_color, shadow_color, font_path, font_size):
    x = bg.width // 2
    y = bg.height // 2

    font = ImageFont.truetype(font_path, font_size)

    blurred = Image.new('RGBA', bg.size)
    draw = ImageDraw.Draw(blurred)
    draw.text(xy=(x, y), text=text, fill=shadow_color, font=font, anchor='mm')
    blurred = blurred.filter(ImageFilter.BoxBlur(7))

    blurred_data = blurred.getdata()
    blurred_data = [(r, g, b, int(a * 2)) for r, g, b, a in blurred_data]
    blurred.putdata(blurred_data)

    bg.paste(blurred, (0, 0), blurred)

    draw = ImageDraw.Draw(bg)
    draw.text(xy=(x, y), text=text, fill=text_color, font=font, anchor='mm')
    return bg

def add_shadowed_text_to_image_SPLITFONTS(bg, text_and_fonts, text_color, shadow_color, font_size):
    def get_text_width(font, text):
        return font.getsize(text)[0]

    x = bg.width // 2
    y = bg.height // 2

    descriptor_text = text_and_fonts[0][0]
    descriptor_font_path = text_and_fonts[0][1]
    main_text = text_and_fonts[1][0]
    main_font_path = text_and_fonts[1][1]

    descriptor_font = ImageFont.truetype(descriptor_font_path, font_size)
    descriptor_width = get_text_width(descriptor_font, descriptor_text)

    main_font = ImageFont.truetype(main_font_path, font_size)
    main_width = get_text_width(main_font, main_text)

    total_width = descriptor_width + main_width

    combined_x = x - (total_width // 2)

    blurred = Image.new('RGBA', bg.size)
    draw_blurred = ImageDraw.Draw(blurred)
    draw_blurred.text(xy=(combined_x, y-26), text=descriptor_text, fill=shadow_color, font=descriptor_font)

    main_x = combined_x + descriptor_width

    draw_blurred.text(xy=(main_x, y-22), text=main_text, fill=shadow_color, font=main_font)
    blurred = blurred.filter(ImageFilter.BoxBlur(7))

    blurred_data = blurred.getdata()
    blurred_data = [(r, g, b, int(a * 2)) for r, g, b, a in blurred_data]
    blurred.putdata(blurred_data)

    bg.paste(blurred, (0, 0), blurred)

    draw = ImageDraw.Draw(bg)
    draw.text(xy=(combined_x, y-26), text=descriptor_text, fill=text_color, font=descriptor_font)
    draw.text(xy=(main_x, y-22), text=main_text, fill=text_color, font=main_font)

    return bg

def render_dd_biome_codename(codename, biome):
    biomes = {
        'Crystalline Caverns': './static/img/DeepDive_MissionBar_CrystalCaves.png',
        'Glacial Strata': './static/img/DeepDive_MissionBar_GlacialStrata.png',
        'Radioactive Exclusion Zone': './static/img/DeepDive_MissionBar_Radioactive.png',
        'Fungus Bogs': './static/img/DeepDive_MissionBar_FungusBogs.png',
        'Dense Biozone': './static/img/DeepDive_MissionBar_LushDownpour.png',
        'Salt Pits': './static/img/DeepDive_MissionBar_SaltPits.png',
        'Sandblasted Corridors': './static/img/DeepDive_MissionBar_Sandblasted.png',
        'Magma Core': './static/img/DeepDive_MissionBar_MagmaCore.png',
        'Azure Weald': './static/img/DeepDive_MissionBar_AzureWeald.png',
        'Hollow Bough': './static/img/DeepDive_MissionBar_HollowBough.png'
    }

    background = Image.open(biomes[biome])
    # background = add_shadowed_text_to_image(background, codename, 'white', '#000000', font_path, font_size)
    text_and_fonts = [('CODENAME: ', "./static/img/RiftSoft-Regular.ttf"), (f'{codename}', './static/img/BebasNeue-Regular.ttf')]
    background = add_shadowed_text_to_image_SPLITFONTS(background, text_and_fonts, 'white', '#000000', font_size=45)
    #background.save('TEST.png', format='PNG')
    #subprocess.run(['gwenview', 'TEST.png'])
    return background

def render_dd_secondary_obj_resource(secondary_obj):
    font_path = './static/img/CarbonBold-W00-Regular.ttf'
    font_size = 45
    font = ImageFont.truetype(font_path, font_size)
    text_color = (255, 255, 255)
    secondary_objs = {
        'Repair Minimules': './static/img/Icon_Salvage_Mules_Objective.png',
        'Eliminate Dreadnought': './static/img/Kill_Dreadnought_Objective_icon.png',
        'Mine Morkite': './static/img/Morkite_icon.png',
        'Get Alien Eggs': './static/img/Alien_egg_icon.png',
        'Black Box': './static/img/Blackbox_icon.png',
        'Build Liquid Morkite Pipeline' : './static/img/Icons_Resources_Detailed_Outline_LiquidMorkiteTankerPod.png',
        'Perform Deep Scans' : './static/img/Icons_Resources_Detailed_Outline_ResonanceScannerPod.png'
            }
    values = {
        'Repair Minimules': '2',
        'Eliminate Dreadnought': '1',
        'Mine Morkite': '150',
        'Get Alien Eggs':'2',
        'Black Box':'1',
        'Build Liquid Morkite Pipeline' : '1',
        'Perform Deep Scans' : '2'
    }

    background = Image.new("RGBA", (256, 256), (0,0,0,0))
    hexagon = Image.open('./static/img/hexagon.png')
    hexagon = scale_image(hexagon, 0.4)
    #x, y = calc_center(hexagon, background)
    #print(f'hexagon X: {str(x)}')
    #print(f'hexagon Y: {str(y)}')
    background.paste(hexagon, (69, 59), mask=hexagon)
    hexagon.close()

    resource = Image.open(secondary_objs[secondary_obj])
    if secondary_obj == 'Mine Morkite':
        resource = scale_image(resource, 0.2)
    elif secondary_obj == 'Black Box':
        resource = scale_image(resource, 0.3)
    elif secondary_obj == 'Get Alien Eggs':
        resource = scale_image(resource, 0.24)
    else:
        resource = scale_image(resource, 0.14)
    x, y = calc_center(resource, background)
    if secondary_obj == 'Mine Morkite' or secondary_obj == 'Black Box' or secondary_obj == 'Perform Deep Scans':
        background.paste(resource, (x, y-20), mask=resource)
    else:
        background.paste(resource, (x, y-13), mask=resource)
    resource.close()

    text = values.get(secondary_obj)
    draw = ImageDraw.Draw(background)
    text_x, text_y = calc_text_center(background.width, background.height, text, font, font_size)
    if secondary_obj == 'Mine Morkite':
        draw.text((text_x, text_y+15), text, font=font, fill=text_color)
    else:
        draw.text((text_x, text_y+25), text, font=font, fill=text_color)
    del draw
    return background

def render_dd_stage(m_d):
    primary_objs = {
        'Mining Expedition': './static/img/Mining_expedition_icon.png',
        'Egg Hunt': './static/img/Egg_collection_icon.png',
        'On-Site Refining': './static/img/Refining_icon.png',
        'Salvage Operation': './static/img/Salvage_icon.png',
        'Escort Duty': './static/img/Escort_icon.png',
        'Point Extraction': './static/img/Point_extraction_icon.png',
        'Elimination': './static/img/Elimination_icon.png',
        'Industrial Sabotage': './static/img/Sabotage_icon.png',
        'Deep Scan' : './static/img/Deep_scan_icon.png'
            }
    complexities = {
        '1': './static/img/Icons_complexity_1.png',
        '2': './static/img/Icons_complexity_2.png',
        '3': './static/img/Icons_complexity_3.png'
            }
    lengths = {
        '1': './static/img/Icons_length_1.png',
        '2': './static/img/Icons_length_2.png',
        '3': './static/img/Icons_length_3.png'
            }
    mutators = {
        'Critical Weakness': './static/img/Mutator_critical_weakness_icon.png',
        'Gold Rush': './static/img/Mutator_gold_rush_icon.png',
        'Double XP': './static/img/Mutator_triple_xp_icon.png',
        'Golden Bugs': './static/img/Mutator_golden_bugs_icon.png',
        'Low Gravity': './static/img/Mutator_no_fall_damage_icon.png',
        'Mineral Mania': './static/img/Mutator_mineral_mania_icon.png',
        'Rich Atmosphere': './static/img/Mutator_rich_atmosphere_icon.png',
        'Volatile Guts': './static/img/Mutator_volatile_guts_icon.png',
        'Blood Sugar' : './static/img/Mutator_blood_sugar_icon.png',
        'Secret Secondary' : './static/img/Mutator_secret_secondary_icon.png'
            }
    warnings = {
        'Cave Leech Cluster': './static/img/Warning_cave_leech_cluster_icon.png',
        'Exploder Infestation': './static/img/Warning_exploder_infestation_icon.png',
        'Haunted Cave': './static/img/Warning_haunted_cave_icon.png',
        'Lethal Enemies': './static/img/Warning_lethal_enemies_icon.png',
        'Low Oxygen': './static/img/Warning_low_oxygen_icon.png',
        'Mactera Plague': './static/img/Warning_mactera_plague_icon.png',
        'Parasites': './static/img/Warning_parasites_icon.png',
        'Regenerative Bugs': './static/img/Warning_regenerative_bugs_icon.png',
        'Shield Disruption': './static/img/Warning_shield_disruption_icon.png',
        'Elite Threat': './static/img/Warning_elite_threat_icon.png',
        'Swarmageddon': './static/img/Warning_swarmageddon_icon.png',
        'Lithophage Outbreak': './static/img/Warning_lithophage_outbreak_icon.png',
        'Rival Presence': './static/img/Warning_rival_presence_icon.png',
        'Duck and Cover': './static/img/Warning_duck_and_cover_icon.png',
        'Ebonite Outbreak' : './static/img/Warning_ebonite_outbreak_icon.png',
        'Tougher Enemies' : './static/img/Warning_tougher_enemies_icon.png'
            }

    background = Image.new("RGBA", (350, 300), (0,0,0,0))

    primary = Image.open(primary_objs[m_d['PrimaryObjective']])
    primary = scale_image(primary, 0.4)
    #x, y = calc_center(primary, background)
    #print(f'primary X: {str(x)}')
    #print(f'primary Y: {str(y)}')
    background.paste(primary, (83, 58), mask=primary)
    primary.close()

    secondary = render_dd_secondary_obj_resource(m_d['SecondaryObjective'])
    secondary = scale_image(secondary, 0.6)
    #x, y = calc_center(secondary, background)
    #print(f'secondary X: {str(x-110)}')
    #print(f'secondary Y: {str(y-95)}')
    background.paste(secondary, (-11, -21), mask=secondary)
    secondary.close()

    if 'MissionWarnings' in m_d:
        MissionWarnings = []
        for warning in m_d['MissionWarnings']:
            MissionWarnings.append(warning)
        missionwarning1 = Image.open(warnings[MissionWarnings[0]])
        missionwarning1 = scale_image(missionwarning1, 0.38)
        #x, y = calc_center(missionwarning1, background)
        #print(f'LONEWARNING X: {str(x+100)}')
        #print(f'LONEWARNING Y: {str(y-15)}')
        if len(MissionWarnings) == 1:
            background.paste(missionwarning1, (227, 87), mask=missionwarning1)
            missionwarning1.close()
        elif len(MissionWarnings) == 2:
            #print(f'WARNING 1 X: {str(x+100)}')
            #print(f'WARNING 1 Y: {str(y-60)}')
            background.paste(missionwarning1, (227, 42), mask=missionwarning1)
            missionwarning1.close()

            missionwarning2 = Image.open(warnings[MissionWarnings[1]])
            missionwarning2 = scale_image(missionwarning2, 0.38)
            #x, y = calc_center(missionwarning2, background)
            #print(f'WARNING 2 X: {str(x+100)}')
            #print(f'WARNING 2 Y: {str(y+40)}')
            background.paste(missionwarning2, (227, 142), mask=missionwarning2)
            missionwarning2.close()

    if 'MissionMutator' in m_d:
        missionmutator = Image.open(mutators[m_d['MissionMutator']])
        missionmutator = scale_image(missionmutator, 0.38)
        #x, y = calc_center(MISSIONMUTATOR, background)
        #print(f'MUTATOR X: {str(x-100)}')
        #print(f'MUTATOR Y: {str(y-10)}')
        background.paste(missionmutator, (27, 92), mask=missionmutator)
        missionmutator.close()

    complexity = Image.open(complexities[m_d['Complexity']])
    complexity = scale_image(complexity, 0.45)
    #x, y = calc_center(complexity, background)
    #print(f'complexity X: {str(x)}')
    #print(f'complexity Y: {str(y-120)}')
    background.paste(complexity, (107, 2), mask=complexity)
    complexity.close()

    length = Image.open(lengths[m_d['Length']])
    length = scale_image(length, 0.45)
    #x, y = calc_center(length, background)
    #print(f'length X: {str(x)}')
    #print(f'length Y: {str(y+120)}')
    background.paste(length, (107, 242), mask=length)
    length.close()

    primary_obj_resource = render_mission_obj_resource(m_d['PrimaryObjective'], m_d['Complexity'], m_d['Length'])
    primary_obj_resource = scale_image(primary_obj_resource, 0.8)
    #x, y = calc_center(primary_obj_resource, background)
    #print(f'obj_resource X: {str(x-110)}')
    #print(f'obj_resource Y: {str(y+95)}')
    background.paste(primary_obj_resource, (-37, 143), mask=primary_obj_resource)
    background = scale_image(background, 0.46)
    primary_obj_resource.close()

    return background

#-------------------------------------------------------------------------------------------------------------------------------

#PRE-HASH PIL OBJECT ARRAYING

#single threaded

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
        # if sum([stage['id'] for stage in deepdive['Stages']]) == 1002:
                if stage['id'] == 999:
                    stage['id'] = -1

        sorted_stages = sorted(deepdive['Stages'], key=lambda x: x['id'], reverse=True)
        for stage in sorted_stages:
            stage_png = render_dd_stage(stage)
            rendered_deepdives[t]['Stages'].append(stage_png)

    return rendered_deepdives

def render_biomes(Biomes):
    rendered_biomes = {}
    for biome, missions in Biomes.items():
        biome1 = []
        for mission in missions:
            mission1 = deepcopy(mission)
            mission1['rendered_mission'] = render_mission(mission)
            
            biome1.append(mission1)

        rendered_biomes[biome] = biome1
    return rendered_biomes

# Multiprocessed
def process_mission(biome_mission):
    biome, mission = biome_mission
    
    mission1 = deepcopy(mission)
    mission1['rendered_mission'] = render_mission(mission)

    return biome, mission1

def render_biomes_parallel(Biomes, render_pool):
    all_missions = []
    for biome, missions in Biomes.items():
        for mission in missions:
            all_missions.append([biome, mission])

    processed_missions = render_pool.map(process_mission, all_missions)

    rendered_biomes = {biome : [] for biome in Biomes.keys()}
    for biome, mission in processed_missions:
        rendered_biomes[biome].append(mission)
    return rendered_biomes

render_biomes = render_biomes_parallel if cpu_count >= 4 else render_biomes

#----------------------------------------------------------------
#ICON SAVE, HASH, AND ARRAY ROTATORS
def rotate_dailydeal(AllTheDeals, tstamp_Queue, deal_Queue, go_flag):
    while len(tstamp_Queue) == 0:
        continue

    deal_dict = AllTheDeals[tstamp_Queue[0]]
    dailydeal = {}
    rendered_dailydeal = render_dailydeal(deal_dict)

    DailyDeal = BytesIO()
    rendered_dailydeal.save(DailyDeal, format='PNG')
    rendered_dailydeal.close()
    DailyDeal.seek(0)
    etag = md5(DailyDeal.getvalue()).hexdigest()

    dailydeal['rendered_dailydeal'] = DailyDeal
    dailydeal['etag'] = etag
    deal_Queue.append(dailydeal)
    del dailydeal
    timestamp = tstamp_Queue[0]

    while go_flag.is_set():
        #applicable_timestamp = tstamp_Queue.queue[0]
        applicable_timestamp = tstamp_Queue[0]
        if applicable_timestamp != timestamp:
            deal_dict = AllTheDeals[applicable_timestamp]
            dailydeal = {}
            rendered_dailydeal = render_dailydeal(deal_dict)

            DailyDeal = BytesIO()
            rendered_dailydeal.save(DailyDeal, format='PNG')
            rendered_dailydeal.close()
            DailyDeal.seek(0)
            etag = md5(DailyDeal.getvalue()).hexdigest()

            dailydeal['rendered_dailydeal'] = DailyDeal
            dailydeal['etag'] = etag
            deal_Queue.append(dailydeal)
            deal_Queue.pop(0)
            del dailydeal
            timestamp = applicable_timestamp

        sleep(0.75)

#array as a VERB
def array_biomes(Biomes, timestamp):
    Biomes1 = {}
    for biome in Biomes.keys():
        biome1 = biome.replace(' ', '-')
        Biomes1[biome1] = {}
        for mission in Biomes[biome]:
            mission_icon = BytesIO()
            mission['rendered_mission'].save(mission_icon, format='PNG')
            mission['rendered_mission'].close()
            mission_icon.seek(0)

            etag = md5(mission_icon.getvalue()).hexdigest()
            mission['etag'] = etag
            mission['rendered_mission'] = mission_icon
            mission['biome'] = biome
            mission['included_in'] = mission['included_in']

            Biomes1[mission['CodeName'].replace(' ', '-')+str(mission['id'])] = mission

    return timestamp, Biomes1

def rotate_biomes(tstamp_Queue, next_tstamp_Queue, nextbiomes_Queue, biomes_Queue, rendering_event, go_flag):
    while len(tstamp_Queue) == 0 and len(next_tstamp_Queue) == 0:
        sleep(0.1)
        continue

    Biomes = render_biomes(load_individual_mission_timestamp(tstamp_Queue[0])['Biomes'])
    _, Biomes = array_biomes(Biomes, tstamp_Queue[0])
    NextBiomes = render_biomes(load_individual_mission_timestamp(next_tstamp_Queue[0])['Biomes'])
    timestamp_next, NextBiomes = array_biomes(NextBiomes, next_tstamp_Queue[0])

    nextbiomes_Queue.append(NextBiomes)
    biomes_Queue.append(Biomes)

    rendering_event.set()
    del Biomes
    del NextBiomes
    del _

    while go_flag.is_set():
        applicable_timestamp = next_tstamp_Queue[0]
        if applicable_timestamp != timestamp_next:
            NextBiomes = render_biomes(load_individual_mission_timestamp(applicable_timestamp)['Biomes'])
            timestamp_next, NextBiomes = array_biomes(NextBiomes, applicable_timestamp)

            biomes_Queue.append(nextbiomes_Queue[0])
            biomes_Queue.pop(0)
            nextbiomes_Queue.append(NextBiomes)
            nextbiomes_Queue.pop(0)

            rendering_event.set()
            del NextBiomes

        sleep(0.25)

def init_worker():
    try:
        def shutdown(*args):
            exit(0)
            quit()
        signal(SIGINT, shutdown)
        signal(SIGTERM, shutdown)
    except:
        exit(0)
        quit()

def rotate_biomes_parallel(tstamp_Queue, next_tstamp_Queue, nextbiomes_Queue, biomes_Queue, rendering_event, go_flag):
    render_pool = Pool(processes=cpu_count, initializer=init_worker)
    while len(tstamp_Queue) == 0 and len(next_tstamp_Queue) == 0:
        sleep(0.1)
        continue

    # with Pool(processes=cpu_count, initializer=init_worker) as render_pool:
    Biomes = render_biomes(load_individual_mission_timestamp(tstamp_Queue[0])['Biomes'], render_pool)
    _, Biomes = array_biomes(Biomes, tstamp_Queue[0])
    NextBiomes = render_biomes(load_individual_mission_timestamp(next_tstamp_Queue[0])['Biomes'], render_pool)
    timestamp_next, NextBiomes = array_biomes(NextBiomes, next_tstamp_Queue[0])

    nextbiomes_Queue.append(NextBiomes)
    biomes_Queue.append(Biomes)

    rendering_event.set()
    del Biomes
    del NextBiomes
    del _

    while go_flag.is_set():
        applicable_timestamp = next_tstamp_Queue[0]
        if applicable_timestamp != timestamp_next:

            # with Pool(processes=cpu_count, initializer=init_worker) as render_pool:
            try:
                NextBiomes = render_biomes(load_individual_mission_timestamp(applicable_timestamp)['Biomes'], render_pool)
                timestamp_next, NextBiomes = array_biomes(NextBiomes, applicable_timestamp)

                biomes_Queue.append(nextbiomes_Queue[0])
                biomes_Queue.pop(0)
                nextbiomes_Queue.append(NextBiomes)
                nextbiomes_Queue.pop(0)

                rendering_event.set()
                del NextBiomes
            except:
                pass
            
        sleep(0.25)
    
    # spawn seems to throw a shitfit here and imports this whole fucking module again on every process in the pool for some reason on sigint but it appears to close correctly so i shrug
    # beats initializing a new pool every rotation in any case
    render_pool.terminate()
    render_pool.close()
    
rotate_biomes = rotate_biomes_parallel if cpu_count >= 2 else rotate_biomes

def rotate_DDs(DDs, go_flag):
    def sort_dd_json_list_by_timestamp(json_pattern):
        json_list = glob.glob(json_pattern)
        sorted_json_list = sorted(json_list, key=lambda x: datetime.strptime(x.split('_')[1].split('.')[0], "%Y-%m-%dT%H-%M-%SZ"), reverse=True)
        return sorted_json_list
    json_pattern = './DD_*.json'
    current_json = None
    while go_flag.is_set():
        json_list = sort_dd_json_list_by_timestamp(json_pattern)
        if current_json != json_list[0]:
            current_json = json_list[0]
            with open(f'./{json_list[0]}', 'r') as f:
                dds = json.load(f)
            if len(DDs) == 0:
                DDs.append(dds)
            else:
                DDs.append(dds)
                DDs.pop(0)
            dds = dds['Deep Dives']
            try:
                dds = render_deepdives(dds)
            except:
                current_json = None
                sleep(0.5)
                continue
            if len(json_list) > 1:
                os.remove(json_list[1])

            dd_str = 'Deep Dive Normal'
            img_count = 0
            folder_name = dd_str.replace(' ', '_')
            if os.path.exists(f'./static/{folder_name}'):
                shutil.rmtree(f'./static/{folder_name}')
            os.mkdir(f'./static/{folder_name}')
            BIOME_NORMAL = render_dd_biome_codename(f"{dds[dd_str]['CodeName']}", dds[dd_str]['Biome'])
            BIOME_NORMAL.save(f'./static/{folder_name}/dd_biome.png', format='PNG')
            for mission in dds[dd_str]['Stages']:
                img_count += 1
                fname = str(img_count)
                mission.save(f'./static/{folder_name}/{fname}.png')
                mission.close()

            dd_str = 'Deep Dive Elite'
            img_count = 0
            folder_name = dd_str.replace(' ', '_')
            if os.path.exists(f'./static/{folder_name}'):
                shutil.rmtree(f'./static/{folder_name}')
            os.mkdir(f'./static/{folder_name}')
            BIOME_ELITE = render_dd_biome_codename(f"{dds[dd_str]['CodeName']}", dds[dd_str]['Biome'])
            BIOME_ELITE.save(f'./static/{folder_name}/dd_biome.png', format='PNG')
            for mission in dds[dd_str]['Stages']:
                img_count += 1
                fname = str(img_count)
                mission.save(f'./static/{folder_name}/{fname}.png')
                mission.close()
            del dds
        sleep(0.25)
#----------------------------------------------------------------
#UTILS 

def rmtree_older_than(path, age_minutes=30):
    cutoff = time.time() - (age_minutes * 60)
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            filepath = os.path.join(root, name)
            if os.path.getmtime(filepath) < cutoff:
                os.remove(filepath)
        for name in dirs:
            dirpath = os.path.join(root, name)
            try:
                if not os.listdir(dirpath):
                    os.rmdir(dirpath)
            except OSError:
                pass

def load_individual_mission_timestamp(applicable_timestamp):
    with open(f'./static/json/bulkmissions_granules/{applicable_timestamp.replace(":", "-")}.json', 'r') as f:
        return json.load(f)

def split_all_mission_timestamps(DRG):
    os.makedirs('./static/json/bulkmissions_granules', exist_ok=True)
    
    for ts, v in DRG.items():
        with open(f'./static/json/bulkmissions_granules/{ts.replace(":", "-")}.json', 'w') as f:
            json.dump(v, f)
    rmtree_older_than("./static/json/bulkmissions_granules", age_minutes=30)
            
def group_by_day_and_split_all(DRG):
    def group_json_by_days(DRG):
        timestamps_dt = [datetime.fromisoformat(ts[:-1]) for ts in DRG.keys()]

        grouped_by_days = {}
        for timestamp in timestamps_dt:
            date = timestamp.date().strftime('%Y-%m-%d')
            if date not in grouped_by_days:
                grouped_by_days[date] = {}
            timestamp = timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
            grouped_by_days[date][timestamp] = DRG[timestamp]

        return grouped_by_days
    def add_daily_deals_to_grouped_json(DRG):
        with open('drgdailydeals.json', 'r') as f:
            AllTheDeals = json.load(f)

            for timestamp, deal in AllTheDeals.items():
                deal['timestamp'] = timestamp
                try:
                    DRG[timestamp.split('T')[0]]['dailyDeal'] = deal
                except:
                    continue
        return DRG
    def split_json_bulkmissions_raw(DRG):
        os.makedirs('./static/json/bulkmissions', exist_ok=True)

        for timestamp, dictionary in DRG.items():
            dictionary['ver'] = 5
            fname = timestamp.replace(':','-')
            with open(f'./static/json/bulkmissions/{fname}.json', 'w') as f:
                json.dump(dictionary, f)
        rmtree_older_than("./static/json/bulkmissions", age_minutes=30)

    to_split = group_json_by_days(DRG)
    to_split = add_daily_deals_to_grouped_json(to_split)
    split_json_bulkmissions_raw(to_split)


def rotate_jsons_days(DRG, num_days, go_flag):

    def extract_days_from_json(data, num_days):
        timestamps = {datetime.strptime(key, '%Y-%m-%d'): value for key, value in data.items()}
        sorted_timestamps = sorted(timestamps.items())

        start_date = sorted_timestamps[0][0]
        end_date = sorted_timestamps[-1][0]

        complete_dates = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
        complete_data = {date.strftime('%Y-%m-%d'): timestamps.get(date, 0) for date in complete_dates}

        current_datetime = datetime.now(timezone.utc)
        days_from_now = current_datetime + timedelta(days=num_days)
        relevant_days = {key: value for key, value in complete_data.items() if current_datetime <= datetime.strptime(key, '%Y-%m-%d') < days_from_now}
        current_datetime = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        relevant_days[current_datetime] = data[current_datetime]

        return relevant_days
    def group_json_by_days(DRG):
        timestamps_dt = [datetime.fromisoformat(ts[:-1]) for ts in DRG.keys()]

        grouped_by_days = {}
        for timestamp in timestamps_dt:
            date = timestamp.date().strftime('%Y-%m-%d')
            if date not in grouped_by_days:
                grouped_by_days[date] = {}
            timestamp = timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
            grouped_by_days[date][timestamp] = DRG[timestamp]

        return grouped_by_days

    completed = []
    days = group_json_by_days(DRG)
    days = extract_days_from_json(DRG, num_days)

    dirpath = './static/json/bulkmissions'
    if os.path.isdir(dirpath):
        shutil.rmtree(dirpath)
    os.mkdir(dirpath)

    for day, timestamp in days.items():
        with open(f'{dirpath}/{day}.json') as f:
            json.dump(timestamp, f)

    while go_flag.is_set():
        sleep(num_days*86400-3600)
        days = group_json_by_days(DRG)
        days = extract_days_from_json(days, num_days)

        for path in completed:
            os.remove(path)
            completed.remove(path)

        for day, timestamp in days.items():
            path = f'./static/json/bulkmissions/{day}.json'
            completed.append(path)
            with open(path, 'w') as f:
                json.dump(timestamp, f)

def sort_dictionary(dictionary, custom_order):
    sorted_dict = {}
    for key in custom_order:
        if key in dictionary:
            sorted_dict[key] = dictionary[key]
            del dictionary[key]
    sorted_dict.update(dictionary)
    return sorted_dict

def order_dictionary_by_date(dictionary):
    sorted_keys = sorted(dictionary.keys(), key=lambda x: datetime.fromisoformat(x[:-1]))
    ordered_dictionary = {}
    for key in sorted_keys:
        ordered_dictionary[key] = dictionary[key]
    return ordered_dictionary

def round_time(current_time, next_):
    if next_:
        rounded_time = current_time + timedelta(minutes=30) - timedelta(minutes=current_time.minute % 30)
    else:
        rounded_time = current_time - timedelta(minutes=current_time.minute % 30)
    rounded_time = rounded_time.replace(second=0)
    rounded_time_str = rounded_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    return rounded_time_str
def select_timestamp(next_):
    current_time = datetime.now(timezone.utc)
    rounded_time_str = round_time(current_time, next_)
    return rounded_time_str

# obsolete for its original purpose but serves to clear memory now
def select_timestamp_from_dict(dictionary, next_):
    current_time = datetime.now(timezone.utc)
    keys = list(dictionary.keys())
    for i in range(len(keys) - 1):
        timestamp = datetime.fromisoformat(keys[i][:-1]+'+00:00')
        next_timestamp = datetime.fromisoformat(keys[i+1][:-1]+'+00:00')
        if current_time > timestamp and current_time < next_timestamp:
            if next_:
                return keys[i+1]
            else:
                return keys[i]
        else:
            try:
                del dictionary[keys[i]]
            except KeyError:
                pass

def rotate_timestamps(tstamp_Queue, next_tstamp_Queue, go_flag):
    applicable_timestamp = select_timestamp(next_=False)
    applicable_next_timestamp = select_timestamp(next_=True)
    next_tstamp_Queue.append(applicable_next_timestamp)
    tstamp_Queue.append(applicable_timestamp)
    timestamp = tstamp_Queue[0]

    while go_flag.is_set():
        applicable_timestamp = select_timestamp(next_=False)
        if applicable_timestamp != timestamp:
            next_tstamp_Queue.append(select_timestamp(next_=True))
            next_tstamp_Queue.pop(0)
            tstamp_Queue.append(applicable_timestamp)
            tstamp_Queue.pop(0)
            timestamp = tstamp_Queue[0]
        sleep(0.25)

# this runs like shit for drgmissionsgod.json but i still use it for drgdailydeals.json because there arent that many keys in it
def rotate_timestamp_from_dict(dictionary, tstamp_Queue, next_, go_flag):
    applicable_timestamp = select_timestamp_from_dict(dictionary, next_=next_)
    tstamp_Queue.append(applicable_timestamp)
    timestamp = tstamp_Queue[0]

    while go_flag.is_set():
        applicable_timestamp = select_timestamp_from_dict(dictionary, next_=next_)
        if applicable_timestamp != timestamp:
            tstamp_Queue.append(applicable_timestamp)
            tstamp_Queue.pop(0)
            timestamp = tstamp_Queue[0]

        sleep(0.25)

def round_time_down(datetime_string):
    datetime_minutes = int(datetime_string[14:16])
    if datetime_minutes >= 30:
        new_datetime = datetime_string[:14] + '30:00Z'
    else:
        new_datetime = datetime_string[:14] + '00:00Z'
    return new_datetime

def get_mission_icon_suffix_for_rpng_endpoint(dictionary):
    mission = choice(dictionary['Biomes'][choice(list(dictionary['Biomes'].keys()))])
    mission_icon_suffix = mission['CodeName'].replace(' ', '-') + str(mission['id'])
    return mission_icon_suffix

# combines seasons to one key while removing duplicates, see render_biomes_FLAT in this file and renderBiomesFlat/arrayBiomes in index.js for postprocessing
def compare_dicts(dict1, dict2, ignore_keys):
    dict1_filtered = {k: v for k, v in dict1.items() if k not in ignore_keys}
    dict2_filtered = {k: v for k, v in dict2.items() if k not in ignore_keys}
    return dict1_filtered == dict2_filtered

def flatten_seasons_v5(DRG):
    combined = {}
    timestamps = list(DRG.keys())
    seasons = ['s0', 's1', 's3']

    for timestamp in timestamps:
        # del DRG[timestamp]['s2']
        # del DRG[timestamp]['s4']
        # del DRG[timestamp]['s5']
        for season in seasons:
            for biome, missions in DRG[timestamp][season]['Biomes'].items():
                for mission in missions:
                    del mission['id']


    for timestamp in timestamps:
        combined[timestamp] = {}
        combined[timestamp]['timestamp'] = timestamp
        combined[timestamp]['Biomes'] = {}
        for i, season in enumerate(seasons):
            for biome, missions in DRG[timestamp][season]['Biomes'].items():
                if i == 0:
                    combined[timestamp]['Biomes'][biome] = []
                    combined[timestamp]['RandomSeed'] = DRG[timestamp][season]['RandomSeed']

                for j, mission in enumerate(missions):
                    mission['index'] = j
                    mission['season'] = season

                    seen = False
                    for season_ in seasons:
                        if season != season_:
                            for m in DRG[timestamp][season_]['Biomes'][biome]:
                                if compare_dicts(mission, m, ignore_keys=['index', 'season', 'included_in']):
                                    seen = True
                                    if 'included_in' not in mission:
                                        mission['included_in'] = []
                                    mission['included_in'].append(season_)
                                    mission['included_in'].append(season)

                    if not seen:
                        mission['included_in'] = [season]

                    mission['included_in'] = sorted(list(set(mission['included_in'])), key=lambda x: (str.isdigit(x), x.lower()))

                combined[timestamp]['Biomes'][biome] += [mission for mission in missions]

    id = 0
    for timestamp in timestamps:
        for biome, missions in combined[timestamp]['Biomes'].items():

            filtered_missions = []
            for i, mission in enumerate(missions):
                keep = True

                for j, m in enumerate(missions):
                    if i < j+1:
                        continue
                    if compare_dicts(m, mission, ignore_keys=['id', 'season', 'index']):
                        keep = False
                        break
                if keep:
                    filtered_missions.append(mission)

            combined[timestamp]['Biomes'][biome] = sorted(filtered_missions, key=lambda x: x['index'])

            for mission in combined[timestamp]['Biomes'][biome]:
                del mission['index']
                del mission['season']
                id += 1
                mission['id'] = id

    return combined

def wait_rotation(rendering_event, index_event, go_flag):
    target_minutes_59 = [29, 59]
    while go_flag.is_set():
        current_time = datetime.now().time()
        current_minute = current_time.minute
        current_second = current_time.second + current_time.microsecond / 1e6

        if current_second > 58.50 and current_minute in target_minutes_59:
            rendering_event.wait()
            index_event.clear()
        sleep(0.2)

def GARBAGE(dictionary, go_flag):
    total_sleep_time = 43200
    while go_flag.is_set():
        elapsed_time = 0
        while elapsed_time < total_sleep_time:
            if not go_flag.is_set():
                return
            sleep(0.2)
            elapsed_time += 0.2
        select_timestamp_from_dict(dictionary, False)

def get_available_memory():
    return int(subprocess.check_output(["free", "-b"]).splitlines()[1].split()[6])

def get_process_pss_mb(pid):
    try:
        with open(f'/proc/{pid}/smaps_rollup', 'r') as f:
            lines = f.readlines()
        for line in lines:
            if line.startswith('Pss:'):
                return round(int(line.split()[-2]) / 1024, 2)
    except Exception as e:
        print(f'Error accessing pid to get memory info: {e}')
        
def get_memory_info_iter(pid):
    for proc in process_iter(['pid', 'memory_info']):
        if pid == proc.info['pid']:
            return proc.info['memory_info']

def SERVER_READY(index_event, start):
    index_event.wait()
    print('Startup time:', round(time() - start, 3), 'seconds.')
    if os.name == 'nt':
        current_process = Process(os.getpid())
        mem_info = get_memory_info_iter(current_process.pid)
        main_process_memory = round(mem_info.private / (1024 * 1024), 2)
        print(f"Approx. memory used by main process {current_process.pid}: {main_process_memory} MB")

        total_child_processes_memory = 0
        
        children = list(current_process.children(recursive=True))
        for child in children:
            mem_info = get_memory_info_iter(child.pid)
            child_process_memory = round(mem_info.private / (1024 * 1024), 2)
            print(f"Approx. memory used by child process {child.pid}: {child_process_memory} MB")
            total_child_processes_memory += child_process_memory

        total_memory_used = round(main_process_memory + total_child_processes_memory, 2)
        print(f"Approx. total memory used by server and its child Processes: {total_memory_used} MB")
        
    else:
        total_memory_used = 0
        current_process = Process(os.getpid())
        total_memory_used += get_process_pss_mb(current_process.pid)

        print(f"Memory used by main process {current_process.pid} : {total_memory_used} MB")
        pids = []
        for child in current_process.children(recursive=True):
            pids.append(child.pid)

        for pid in pids:
            total_memory_used += get_process_pss_mb(pid)
            
        total_memory_used = round(total_memory_used, 2)
        print(f"Total memory used by server and its child processes: {total_memory_used} MB")


def timestamped_print(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        include_timestamp = kwargs.pop('include_timestamp', True)
        args = [str(arg) for arg in args]

        if include_timestamp:
            concatenated_args = ''.join(args)
            if concatenated_args.strip() != '':
                timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
                args = (f'{timestamp}', *args)
        return func(*args, **kwargs)
    return wrapper
print = timestamped_print(print)

def timestamped_write(func):
    @wraps(func)
    def wrapper(data):
        if type(data) == str:
            timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            data = f'{timestamp}: {data}'
        return func(data)
    return wrapper
def timestamped_open_wrapper(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        f = func(*args, **kwargs)
        f.write = timestamped_write(f.write)
        return f
    return wrapper
open_with_timestamped_write = timestamped_open_wrapper(open)

def cfg_():
    with open('cfg.json', 'r') as f:
        cfg = json.load(f)
        f.close()
    return cfg
cfg = cfg_()

def merge_parts(part_files, output_file):
    sorted_part_files = sorted(part_files)
    with open(output_file, 'wb') as merged_file:
        for part_file in sorted_part_files:
            with open(part_file, 'rb') as part:
                merged_file.write(part.read())

#----------------------------------------------------------------

def render_ogembed_html(mission, identifier, route, timestamp):
    s = {
        's0' : [0, 5],
        's1' : [1, 2],
        's3' : [3, 4],
    }
    mutator = mission['MissionMutator'] if 'MissionMutator' in mission else 'None'
    warnings = 'None'
    
    seasons = []
    for s_ in s:
        for s__ in s[s_]:
            seasons.append(s__)
    seasons.sort()
    seasons = ', '.join([str(x) for x in seasons])
    
    if 'MissionWarnings'in mission:
        warnings = mission['MissionWarnings']
        warnings = ', '.join(warnings) if len(warnings) == 2 else ''.join(warnings)
            
    return f'''<!DOCTYPE html>
<head>
<meta property="og:title" content="{mission['CodeName']}"/>
<meta property="og:type" content="website"/>
<meta property="og:image" content="/{route}?img={identifier}"/>
<meta property="og:image:width" content="350"/>
<meta property="og:image:height" content="300"/>
<meta property="og:description" content="Timestamp: {timestamp} (UTC)\nBiome: {mission['biome'].upper()}\nPrimary: {mission['PrimaryObjective'].upper()} | Secondary: {mission['SecondaryObjective'].upper()}\nIn Season(s): {seasons}\nComplexity: {mission['Complexity']}\nLength: {mission['Length']}\nMutator: {mutator.upper()}\nWarning(s): {warnings.upper()}\n"/>
<meta http-equiv="refresh" content="0;url=/">
</head>
</html>'''

def render_dd_ogembed_html(stage, dd, identifier):
    mutator = stage['MissionMutator'] if 'MissionMutator' in stage else 'None'
    warnings = 'None'
    
    if 'MissionWarnings'in stage:
        warnings = stage['MissionWarnings']
        warnings = ', '.join(warnings) if len(warnings) == 2 else ''.join(warnings)

    return f'''<!DOCTYPE html>
<head>
<meta property="og:title" content="{identifier[0]} Stage {identifier[1]}"/>
<meta property="og:type" content="website"/>
<meta property="og:image" content="/dd_png?img={'-'.join(identifier)}"/>
<meta property="og:image:width" content="350"/>
<meta property="og:image:height" content="300"/>
<meta property="og:description" content="Biome: {dd['Biome'].upper()}\nComplexity: {stage['Complexity']}\nLength: {stage['Length']}\nMutator: {mutator.upper()}\nWarning(s): {warnings.upper()}\n"/>
<meta http-equiv="refresh" content="0;url=/">
</head>
</html>'''

# this is useless and obsolete and i took all the string/etag hashing logic out of it but i keep it running because theres some reference to it somewhere that i cant be bothered checking to see if it will break something or not
def rotate_index(rendering_event, current_timestamp_Queue, next_timestamp_Queue, index_event, index_Queue, go_flag):
    rendering_event.wait()
    current_timestamp = current_timestamp_Queue[0]
    index_event.set()
    while go_flag.is_set():
        applicable_timestamp = current_timestamp_Queue[0]
        if applicable_timestamp != current_timestamp:
            rendering_event.wait()
            index_event.set()
        sleep(0.33)


#obsolete, refer to index.html
def render_index():
    return '''<!doctype html>
</html>'''

#CLASS XP CALCULATOR
# obsolete, refer to xp_calculator.html
def render_xp_calc_index():
    index = {}
    index_ = '''<!DOCTYPE html>
<html>
<head>
<link rel ="icon" href="/static/favicon.ico" type="image/x-icon">
<link rel ="stylesheet" href="/static/styles.css" type="text/css">
<title>DRG XP Calculator</title>
</head>
<style>
table {
  border-collapse: collapse;
  width: auto;
}
th, td {
  padding: 8px;
  text-align: center;
  border-bottom: 1px solid #ddd;
  min-width: 180px;
}
tr {
  height: 75px;
}
</style>
<body bgcolor="#303030">
<img id="background-video" src="/static/drop_pod.jpg" type="video/webm">
<div class="overlay"></div>
<p class="loading">Loading</p>
<div id="scal" class="collapsed">
<div class="calc-grid-container">
<form id="xpForm">

<h2><div class="mission-hover-zoom"><img class="class-iconx" src="/static/class_icons/Icon_Character_Engineer.png"></div></h2>
<label class="classcalcsub" for="engineerLevels">Level:&nbsp;</label>
<input placeholder="1" class="calcbox" type="number" min="1" max="25" id="engineerLevels" name="engineerLevels"><br><br>
<label class="classcalcsub" for="engineerPromotions">Promotions:&nbsp;</label>
<input placeholder="0" class="calcbox" type="number" min="0" id="engineerPromotions" name="engineerPromotions"><br><br>

<h2><div class="mission-hover-zoom"><img class="class-iconx" src="/static/class_icons/Icon_Character_Scout.png"></div></h2>
<label class="classcalcsub" for="scoutLevels">Level:&nbsp;</label>
<input placeholder="1" class="calcbox" type="number" min="1" max="25" id="scoutLevels" name="scoutLevels"><br><br>
<label class="classcalcsub" for="scoutPromotions">Promotions:&nbsp;</label>
<input placeholder="0" class="calcbox" type="number" min="0" id="scoutPromotions" name="scoutPromotions"><br><br>

<h2><div class="mission-hover-zoom"><img class="class-iconx" src="/static/class_icons/Icon_Character_Driller.png"></div></h2>
<label class="classcalcsub" for="drillerLevels">Level:&nbsp;</label>
<input placeholder="1" class="calcbox" type="number" min="1" max="25" id="drillerLevels" name="drillerLevels"><br><br>
<label class="classcalcsub" for="drillerPromotions">Promotions:&nbsp;</label>
<input placeholder="0" class="calcbox" type="number" min="0" id="drillerPromotions" name="drillerPromotions"><br><br>

<h2><div class="mission-hover-zoom"><img class="class-iconx" src="/static/class_icons/Icon_Character_Gunner.png"></div></h2>
<label class="classcalcsub" for="gunnerLevels">Level:&nbsp;</label>
<input placeholder="1" class="calcbox" type="number" min="1" max="25" id="gunnerLevels" name="gunnerLevels"><br><br>
<label class="classcalcsub" for="gunnerPromotions">Promotions:&nbsp;</label>
<input placeholder="0" class="calcbox" type="number" min="0" id="gunnerPromotions" name="gunnerPromotions"><br><br><br>


<label class="classcalcsub" for="hours">Hours played:&nbsp;</label>
<input placeholder="0" class="calcbox" type="number" min="0" id="hours" name="hours"><br><br>
<input id="calcsubmit" style="color:#303030;" class="classcalcsub" type="submit" value="Calculate XP">
<input id="reset" style="color:#303030;" class="classcalcsub" type="reset" value="Reset">
</form>
<div class="calcoutput" id="output">
<table id="outputTable">
<tr>
  <!-- <th>Class</th> -->
  <th>Rank</th>
  <th><img title="Effective Level" src="/static/icon_class_level.png"></th>
  <th>XP</th>

</tr>
<tr>
  <!-- <td><span style="color:#9f2c14;">Engineer</span></td> -->
  <td id="tableEngineerClassRank" style="height:50px;"></td>
  <td id="tableEngineerClassLevel"></td>
  <td id="tableEngineerClassXP"></td>
</tr>
<tr>
  <!-- <td><span style="color:#3062b1;">Scout</span></td> -->
  <td id="tableScoutClassRank" style="height:50px;"></td>
  <td id="tableScoutClassLevel"></td>
  <td id="tableScoutClassXP"></td>
</tr>
<tr>
  <!-- <td><span style="color:#bda62a;">Driller</span></td> -->
  <td id="tableDrillerClassRank" style="height:50px;"></td>
  <td id="tableDrillerClassLevel"></td>
  <td id="tableDrillerClassXP"></td>
</tr>
<tr>
 <!-- <td><span style="color:#83a637;">Gunner</span></td>  -->
  <td id="tableGunnerClassRank" style="height:50px;"></td>
  <td id="tableGunnerClassLevel"></td>
  <td id="tableGunnerClassXP"></td>
</tr>
</table>
<br>
<h2 id="results" style="font-size:40px;">
</h2>
</div>
</div>
<hr>
<span class="calctitle"><i>Note: To find your Classes' number of promotions, go to Options>Save Menu ingame.</i> | <a class="jsonlink" href="/">HOME</a> | <a class="jsonlink" href="/xp_calc?engineer_level=1&engineer_promos=0&scout_level=1&scout_promos=0&driller_level=1&driller_promos=0&gunner_level=1&gunner_promos=0&hrs=0">XP Calculator Endpoint</a></span><br>
<p class='gsgdisclaimer'><i>This website is a third-party platform and is not affiliated, endorsed, or sponsored by Ghost Ship Games. The use of Deep Rock Galactic's in-game assets on this website is solely for illustrative purposes and does not imply any ownership or association with the game or its developers. All copyrights and trademarks belong to their respective owners. For official information about Deep Rock Galactic, please visit the official Ghost Ship Games website.</i></p>
</div>
<script src="/static/xp_calculator.js"></script>
<div class="collapsed">
<img class="class-icon" src="/static/class_icons/Icon_Character_Engineer_Bronze_1.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Engineer_Bronze_2.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Engineer_Bronze_3.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Engineer_Silver_1.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Engineer_Silver_2.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Engineer_Silver_3.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Engineer_Gold_1.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Engineer_Gold_2.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Engineer_Gold_3.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Engineer_Platinum_1.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Engineer_Platinum_2.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Engineer_Platinum_3.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Engineer_Emerald_1.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Engineer_Emerald_2.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Engineer_Emerald_3.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Engineer_Legendary_1.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Engineer_Legendary_2.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Engineer_Legendary_3.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Scout_Bronze_1.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Scout_Bronze_2.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Scout_Bronze_3.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Scout_Silver_1.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Scout_Silver_2.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Scout_Silver_3.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Scout_Gold_1.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Scout_Gold_2.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Scout_Gold_3.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Scout_Platinum_1.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Scout_Platinum_2.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Scout_Platinum_3.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Scout_Emerald_1.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Scout_Emerald_2.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Scout_Emerald_3.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Scout_Legendary_1.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Scout_Legendary_2.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Scout_Legendary_3.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Driller_Bronze_1.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Driller_Bronze_2.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Driller_Bronze_3.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Driller_Silver_1.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Driller_Silver_2.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Driller_Silver_3.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Driller_Gold_1.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Driller_Gold_2.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Driller_Gold_3.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Driller_Platinum_1.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Driller_Platinum_2.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Driller_Platinum_3.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Driller_Emerald_1.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Driller_Emerald_2.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Driller_Emerald_3.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Driller_Legendary_1.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Driller_Legendary_2.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Driller_Legendary_3.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Gunner_Bronze_1.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Gunner_Bronze_2.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Gunner_Bronze_3.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Gunner_Silver_1.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Gunner_Silver_2.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Gunner_Silver_3.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Gunner_Gold_1.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Gunner_Gold_2.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Gunner_Gold_3.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Gunner_Platinum_1.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Gunner_Platinum_2.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Gunner_Platinum_3.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Gunner_Emerald_1.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Gunner_Emerald_2.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Gunner_Emerald_3.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Gunner_Legendary_1.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Gunner_Legendary_2.png">
<img class="class-icon" src="/static/class_icons/Icon_Character_Gunner_Legendary_3.png">
</div>
</body>
</html>'''
    index['index'] = index_.encode()
    etag = md5(index['index']).hexdigest()
    index['etag'] = etag
    return index

#xp calculator endpoint class
class_xp_levels = {
    1 : 0,
    2 : 3000,
    3 : 7000,
    4 : 12000,
    5 : 18000,
    6 : 25000,
    7 : 33000,
    8 : 42000,
    9 : 52000,
    10 : 63000,
    11 : 75000,
    12 : 88000,
    13 : 102000,
    14 : 117000,
    15 : 132500,
    16 : 148500,
    17 : 165000,
    18 : 182000,
    19 : 199500,
    20 : 217500,
    21 : 236000,
    22 : 255000,
    23 : 274500,
    24 : 294500,
    25 : 315000
}
class Dwarf():
    def __init__(self, levels, promotions):
        self.xp = 0
        self.level = levels
        self.promotions = promotions
        self.total_level = 0
    def calculate_class_xp(self, levels):
        self.xp = levels[self.level] + (self.promotions * 315000)
        self.total_level = self.level + (self.promotions * 25)

#-----------------------------------------------------------------------------
