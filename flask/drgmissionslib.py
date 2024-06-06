from hashlib import md5
from time import sleep, time
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from datetime import datetime, timedelta
from functools import wraps
from multiprocessing.pool import Pool
from multiprocessing import Event, Manager
from signal import getsignal, signal, SIGINT, SIGTERM, SIG_DFL
import psutil
import os
import shutil
import glob
import json
import threading

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

    BUBBLE = Image.open('./static/img/Icon_TradeTerminal_SaleBubble.png')
    BUBBLE = scale_image(BUBBLE, 0.8)

    font_path = './static/img/Bungee-Regular.ttf'
    font_size = 75
    font = ImageFont.truetype(font_path, font_size)
    text = str(round(changepercent))
    if len(text) == 2:
        digit1 = list(text)[0]
        digit2 = f'{list(text)[1]}%'
        DIGIT1 = ImageDraw.Draw(BUBBLE)
        digit1_x, digit1_y = calc_text_center(BUBBLE.width, BUBBLE.height, digit1, font, font_size)
        DIGIT1.text((digit1_x-60, digit1_y-15), digit1, font=font, fill=(0, 0, 0))
        DIGIT2 = ImageDraw.Draw(BUBBLE)
        DIGIT2.text((digit1_x-5, digit1_y-15), digit2, font=font, fill=(0, 0, 0))
        del DIGIT1
        del DIGIT2
        SAVINGS_PROFIT = ImageDraw.Draw(BUBBLE)
        font_size = 30
        font = ImageFont.truetype(font_path, font_size)
        savings_x, savings_y = calc_text_center(BUBBLE.width, BUBBLE.height, save_profit[dealtype], font, font_size)
        SAVINGS_PROFIT.text((savings_x, savings_y+38), save_profit[dealtype], font=font, fill=(0, 0, 0))
    else:
        text = f'{text}%'
        CHANGEPERCENT = ImageDraw.Draw(BUBBLE)
        text_x, text_y = calc_text_center(BUBBLE.width, BUBBLE.height, text, font, font_size)
        CHANGEPERCENT.text((text_x, text_y-15), text, font=font, fill=(0, 0, 0))
        del CHANGEPERCENT
        SAVINGS_PROFIT = ImageDraw.Draw(BUBBLE)
        font_size = 30
        font = ImageFont.truetype(font_path, font_size)
        savings_x, savings_y = calc_text_center(BUBBLE.width, BUBBLE.height, save_profit[dealtype], font, font_size)
        SAVINGS_PROFIT.text((savings_x, savings_y+38), save_profit[dealtype], font=font, fill=(0, 0, 0))
    del SAVINGS_PROFIT
    return BUBBLE

def render_daily_deal_resource_and_amount(resources, resource, resourceamount):
    RESOURCE = Image.open(resources[resource])
    RESOURCE = scale_image(RESOURCE, 0.3)
    text = str(resourceamount)
    font_path = './static/img/Bungee-Regular.ttf'
    font_size = 75
    font = ImageFont.truetype(font_path, font_size)
    text_width = len(text) * font_size
    text_height = len(text) * font_size
    image_width = text_width + (2 * RESOURCE.width)
    image_height = text_height
    BACKGROUND = Image.new("RGBA", (image_width, image_height), (0, 0, 0, 0))
    x, y = calc_center(RESOURCE, BACKGROUND)
    BACKGROUND.paste(RESOURCE, (25,y))
    BACKGROUND.paste(RESOURCE.transpose(Image.FLIP_LEFT_RIGHT), ((image_width - RESOURCE.width)-25, y))
    RESOURCE.close()
    DRAW = ImageDraw.Draw(BACKGROUND)
    text_x, text_y = calc_text_center(BACKGROUND.width, BACKGROUND.height, text, font, font_size)
    DRAW.text((text_x, text_y), text, font=font, fill=(255,255,255))
    del DRAW
    return BACKGROUND

def render_daily_deal_credits(credits):
    CREDITS = Image.open('./static/img/Credit.png')
    CREDITS = scale_image(CREDITS, 0.4)
    text = str(credits)
    font_path = './static/img/Bungee-Regular.ttf'
    font_size = 75
    font = ImageFont.truetype(font_path, font_size)
    text_width = len(text) * font_size
    text_height = len(text) * font_size
    image_width = text_width + (2 * CREDITS.width)
    image_height = text_height
    BACKGROUND = Image.new("RGBA", (image_width, image_height), (0, 0, 0, 0))
    x, y = calc_center(CREDITS, BACKGROUND)
    if len(text) < 5:
        BACKGROUND.paste(CREDITS, (35,y+10))
        BACKGROUND.paste(CREDITS, ((image_width - CREDITS.width)-35, y+10))
    else:
        BACKGROUND.paste(CREDITS, (55,y+10))
        BACKGROUND.paste(CREDITS, ((image_width - CREDITS.width)-55, y+10))
    CREDITS.close()
    DRAW = ImageDraw.Draw(BACKGROUND)
    text_x, text_y = calc_text_center(BACKGROUND.width, BACKGROUND.height, text, font, font_size)
    DRAW.text((text_x, text_y), text, font=font, fill=(255,255,255))
    del DRAW
    return BACKGROUND

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

    BACKGROUND = Image.new("RGBA", (400, 635), (0, 44, 81, 255))
    BACKGROUND_HEAD = Image.new("RGBA", (400, 120), (57, 148, 136, 255))
    x, y = calc_center(BACKGROUND_HEAD, BACKGROUND)
    BACKGROUND.paste(BACKGROUND_HEAD, (x, y-257), mask = BACKGROUND_HEAD)
    BACKGROUND_HEAD.close()

    text = "TODAY'S OFFER:"
    BACKGROUND_TITLE = ImageDraw.Draw(BACKGROUND)
    text_x, text_y = calc_text_center(BACKGROUND.width, BACKGROUND.height, text, font, font_size)
    BACKGROUND_TITLE.text((text_x, text_y-295), text, font=font, fill=(0, 0, 0))
    del BACKGROUND_TITLE

    font_path = './static/img/Bungee-Regular.ttf'
    font_size = 60
    font = ImageFont.truetype(font_path, font_size)

    text = deal_dict['Resource']
    RESOURCE_TEXT = ImageDraw.Draw(BACKGROUND)
    text_x, text_y = calc_text_center(BACKGROUND.width, BACKGROUND.height, text, font, font_size)
    RESOURCE_TEXT.text((text_x, text_y-250), text, font=font, fill=(0, 0, 0))
    del RESOURCE_TEXT

    RESOURCEAMOUNT_AND_RESOURCE = render_daily_deal_resource_and_amount(resources, deal_dict['Resource'], deal_dict['ResourceAmount'])
    x, y = calc_center(RESOURCEAMOUNT_AND_RESOURCE, BACKGROUND)
    BACKGROUND.paste(RESOURCEAMOUNT_AND_RESOURCE, (x, y-130), mask=RESOURCEAMOUNT_AND_RESOURCE)
    RESOURCEAMOUNT_AND_RESOURCE.close()

    font_size = 35
    font = ImageFont.truetype(font_path, font_size)
    text = deal_dict['DealType']
    DEALTYPE = ImageDraw.Draw(BACKGROUND)
    text_x, text_y = calc_text_center(BACKGROUND.width, BACKGROUND.height, text, font, font_size)
    DEALTYPE.text((text_x, text_y-170), text, font=font, fill=(255, 255, 255))

    text = buy_or_get[deal_dict['DealType']]
    DEALTYPE = ImageDraw.Draw(BACKGROUND)
    text_x, text_y = calc_text_center(BACKGROUND.width, BACKGROUND.height, text, font, font_size)
    DEALTYPE.text((text_x, text_y-33), text, font=font, fill=(255, 255, 255))
    del DEALTYPE

    credits = deal_dict['Credits']
    CREDITS = render_daily_deal_credits(credits)
    x, y = calc_center(CREDITS, BACKGROUND)
    BACKGROUND.paste(CREDITS, (x, y+10), mask=CREDITS)
    CREDITS.close()

    BUBBLE = render_daily_deal_bubble(deal_dict['ChangePercent'], deal_dict['DealType'])
    BUBBLE = BUBBLE.rotate(-20, expand=True)
    x, y = calc_center(BUBBLE, BACKGROUND)
    BACKGROUND.paste(BUBBLE, (x-60, y+200), mask=BUBBLE)
    BUBBLE.close()

    BACKGROUND = scale_image(BACKGROUND, 0.5)
    # BACKGROUND.save('TEST.png', format='PNG')
    # subprocess.run(['gwenview', 'TEST.png'])
    return BACKGROUND

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
        'Exterminate Bha Barnacles' : Image.open('./static/img/Exterminate_Bha_Barnacles_icon.png'),
        'Exterminate Glyphid Eggs' : Image.open('./static/img/Exterminate_Glyphid_Eggs_icon.png')
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
        'Ebonite Outbreak' : Image.open('./static/img/Warning_ebonite_outbreak_icon.png')
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

    BACKGROUND = Image.new("RGBA", (256, 256), (0,0,0,0))
    HEXAGON = standard_mission_primary_resources_images['Hexagon'].copy()
    HEXAGON = scale_image(HEXAGON, 0.4)
    #x, y = calc_center(HEXAGON, BACKGROUND)
    #print(f'HEXAGON X: {str(x)}')
    #print(f'HEXAGON Y: {str(y)}')
    BACKGROUND.paste(HEXAGON, (69, 59), mask=HEXAGON)
    HEXAGON.close()

    RESOURCE = standard_mission_primary_resources_images[primary_obj].copy()
    if primary_obj == 'Mining Expedition':
        RESOURCE = scale_image(RESOURCE, 0.2)
    elif primary_obj == 'Egg Hunt':
        RESOURCE = scale_image(RESOURCE, 0.25)
    else:
        RESOURCE = scale_image(RESOURCE, 0.14)
    x, y = calc_center(RESOURCE, BACKGROUND)
    if primary_obj == 'Mining Expedition':
        BACKGROUND.paste(RESOURCE, (x, y-20), mask=RESOURCE)
    else:
        BACKGROUND.paste(RESOURCE, (x, y-13), mask=RESOURCE)
    RESOURCE.close()

    text = values.get((primary_obj, complexity, length), values.get((primary_obj, length), values.get((primary_obj, 'default'), 'Unknown')))
    DRAW = ImageDraw.Draw(BACKGROUND)
    text_x, text_y = calc_text_center(BACKGROUND.width, BACKGROUND.height, text, font, font_size)
    if primary_obj == 'Mining Expedition':
        DRAW.text((text_x, text_y+15), text, font=font, fill=text_color)
    else:
        DRAW.text((text_x, text_y+25), text, font=font, fill=text_color)
    del DRAW
    return BACKGROUND

def render_mission(m_d):
    BACKGROUND = Image.new("RGBA", (350, 300), (0,0,0,0))

    PRIMARY = standard_mission_images['primary_objs'][m_d['PrimaryObjective']].copy()
    PRIMARY = scale_image(PRIMARY, 0.4)
    #x, y = calc_center(PRIMARY, BACKGROUND)
    #print(f'PRIMARY X: {str(x)}')
    #print(f'PRIMARY Y: {str(y)}')
    BACKGROUND.paste(PRIMARY, (83, 58), mask=PRIMARY)
    PRIMARY.close()

    SECONDARY = standard_mission_images['secondary_objs'][m_d['SecondaryObjective']].copy()
    SECONDARY = scale_image(SECONDARY, 0.6)
    #x, y = calc_center(SECONDARY, BACKGROUND)
    #print(f'SECONDARY X: {str(x-110)}')
    #print(f'SECONDARY Y: {str(y-95)}')
    BACKGROUND.paste(SECONDARY, (-11, -21), mask=SECONDARY)
    SECONDARY.close()

    if 'MissionWarnings' in m_d:
        MissionWarnings = []
        for warning in m_d['MissionWarnings']:
            MissionWarnings.append(warning)
        MISSIONWARNING1 = standard_mission_images['warnings'][MissionWarnings[0]].copy()
        MISSIONWARNING1 = scale_image(MISSIONWARNING1, 0.38)
        #x, y = calc_center(MISSIONWARNING1, BACKGROUND)
        #print(f'LONEWARNING X: {str(x+100)}')
        #print(f'LONEWARNING Y: {str(y-15)}')
        if len(MissionWarnings) == 1:
            BACKGROUND.paste(MISSIONWARNING1, (227, 87), mask=MISSIONWARNING1)
            MISSIONWARNING1.close()
        elif len(MissionWarnings) == 2:
            #print(f'WARNING 1 X: {str(x+100)}')
            #print(f'WARNING 1 Y: {str(y-60)}')
            BACKGROUND.paste(MISSIONWARNING1, (227, 42), mask=MISSIONWARNING1)
            MISSIONWARNING1.close()

            MISSIONWARNING2 = standard_mission_images['warnings'][MissionWarnings[1]].copy()
            MISSIONWARNING2 = scale_image(MISSIONWARNING2, 0.38)
            #x, y = calc_center(MISSIONWARNING2, BACKGROUND)
            #print(f'WARNING 2 X: {str(x+100)}')
            #print(f'WARNING 2 Y: {str(y+40)}')
            BACKGROUND.paste(MISSIONWARNING2, (227, 142), mask=MISSIONWARNING2)
            MISSIONWARNING2.close()

    if 'MissionMutator' in m_d:
        MISSIONMUTATOR = standard_mission_images['mutators'][m_d['MissionMutator']].copy()
        MISSIONMUTATOR = scale_image(MISSIONMUTATOR, 0.38)
        #x, y = calc_center(MISSIONMUTATOR, BACKGROUND)
        #print(f'MUTATOR X: {str(x-100)}')
        #print(f'MUTATOR Y: {str(y-10)}')
        BACKGROUND.paste(MISSIONMUTATOR, (27, 92), mask=MISSIONMUTATOR)
        MISSIONMUTATOR.close()

    COMPLEXITY = standard_mission_images['complexities'][m_d['Complexity']].copy()
    COMPLEXITY = scale_image(COMPLEXITY, 0.45)
    #x, y = calc_center(COMPLEXITY, BACKGROUND)
    #print(f'COMPLEXITY X: {str(x)}')
    #print(f'COMPLEXITY Y: {str(y-120)}')
    BACKGROUND.paste(COMPLEXITY, (107, 2), mask=COMPLEXITY)
    COMPLEXITY.close()

    LENGTH = standard_mission_images['lengths'][m_d['Length']].copy()
    LENGTH = scale_image(LENGTH, 0.45)
    #x, y = calc_center(LENGTH, BACKGROUND)
    #print(f'LENGTH X: {str(x)}')
    #print(f'LENGTH Y: {str(y+120)}')
    BACKGROUND.paste(LENGTH, (107, 242), mask=LENGTH)
    LENGTH.close()

    PRIMARY_OBJ_RESOURCE = render_mission_obj_resource(m_d['PrimaryObjective'], m_d['Complexity'], m_d['Length'])
    PRIMARY_OBJ_RESOURCE = scale_image(PRIMARY_OBJ_RESOURCE, 0.8)
    #x, y = calc_center(PRIMARY_OBJ_RESOURCE, BACKGROUND)
    #print(f'OBJ_RESOURCE X: {str(x-110)}')
    #print(f'OBJ_RESOURCE Y: {str(y+95)}')
    BACKGROUND.paste(PRIMARY_OBJ_RESOURCE, (-37, 143), mask=PRIMARY_OBJ_RESOURCE)
    PRIMARY_OBJ_RESOURCE.close()

    BACKGROUND = scale_image(BACKGROUND, 0.46)
    #BACKGROUND.save('TEST.png', format='PNG')
    #subprocess.run(['gwenview', 'TEST.png'])
    #mission = {'rendered_mission': BACKGROUND, 'CodeName': m_d['CodeName'], 'id': m_d['id']}
    return BACKGROUND

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

    BACKGROUND = Image.open(biomes[biome])
    # BACKGROUND = add_shadowed_text_to_image(BACKGROUND, codename, 'white', '#000000', font_path, font_size)
    text_and_fonts = [('CODENAME: ', "./static/img/RiftSoft-Regular.ttf"), (f'{codename}', './static/img/BebasNeue-Regular.ttf')]
    BACKGROUND = add_shadowed_text_to_image_SPLITFONTS(BACKGROUND, text_and_fonts, 'white', '#000000', font_size=45)
    #BACKGROUND.save('TEST.png', format='PNG')
    #subprocess.run(['gwenview', 'TEST.png'])
    return BACKGROUND

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
        'Black Box': './static/img/Blackbox_icon.png'
            }
    values = {
        'Repair Minimules': '2',
        'Eliminate Dreadnought': '1',
        'Mine Morkite': '150',
        'Get Alien Eggs':'2',
        'Black Box':'1',
    }

    BACKGROUND = Image.new("RGBA", (256, 256), (0,0,0,0))
    HEXAGON = Image.open('./static/img/hexagon.png')
    HEXAGON = scale_image(HEXAGON, 0.4)
    #x, y = calc_center(HEXAGON, BACKGROUND)
    #print(f'HEXAGON X: {str(x)}')
    #print(f'HEXAGON Y: {str(y)}')
    BACKGROUND.paste(HEXAGON, (69, 59), mask=HEXAGON)
    HEXAGON.close()

    RESOURCE = Image.open(secondary_objs[secondary_obj])
    if secondary_obj == 'Mine Morkite' or secondary_obj == 'Get Alien Eggs':
        RESOURCE = scale_image(RESOURCE, 0.2)
    elif secondary_obj == 'Black Box':
        RESOURCE = scale_image(RESOURCE, 0.3)
    else:
        RESOURCE = scale_image(RESOURCE, 0.14)
    x, y = calc_center(RESOURCE, BACKGROUND)
    if secondary_obj == 'Mine Morkite':
        BACKGROUND.paste(RESOURCE, (x, y-20), mask=RESOURCE)
    else:
        BACKGROUND.paste(RESOURCE, (x, y-13), mask=RESOURCE)
    RESOURCE.close()

    text = values.get(secondary_obj)
    DRAW = ImageDraw.Draw(BACKGROUND)
    text_x, text_y = calc_text_center(BACKGROUND.width, BACKGROUND.height, text, font, font_size)
    if secondary_obj == 'Mine Morkite':
        DRAW.text((text_x, text_y+15), text, font=font, fill=text_color)
    else:
        DRAW.text((text_x, text_y+25), text, font=font, fill=text_color)
    del DRAW
    return BACKGROUND

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
            }

    BACKGROUND = Image.new("RGBA", (350, 300), (0,0,0,0))

    PRIMARY = Image.open(primary_objs[m_d['PrimaryObjective']])
    PRIMARY = scale_image(PRIMARY, 0.4)
    #x, y = calc_center(PRIMARY, BACKGROUND)
    #print(f'PRIMARY X: {str(x)}')
    #print(f'PRIMARY Y: {str(y)}')
    BACKGROUND.paste(PRIMARY, (83, 58), mask=PRIMARY)
    PRIMARY.close()

    SECONDARY = render_dd_secondary_obj_resource(m_d['SecondaryObjective'])
    SECONDARY = scale_image(SECONDARY, 0.6)
    #x, y = calc_center(SECONDARY, BACKGROUND)
    #print(f'SECONDARY X: {str(x-110)}')
    #print(f'SECONDARY Y: {str(y-95)}')
    BACKGROUND.paste(SECONDARY, (-11, -21), mask=SECONDARY)
    SECONDARY.close()

    if 'MissionWarnings' in m_d:
        MissionWarnings = []
        for warning in m_d['MissionWarnings']:
            MissionWarnings.append(warning)
        MISSIONWARNING1 = Image.open(warnings[MissionWarnings[0]])
        MISSIONWARNING1 = scale_image(MISSIONWARNING1, 0.38)
        #x, y = calc_center(MISSIONWARNING1, BACKGROUND)
        #print(f'LONEWARNING X: {str(x+100)}')
        #print(f'LONEWARNING Y: {str(y-15)}')
        if len(MissionWarnings) == 1:
            BACKGROUND.paste(MISSIONWARNING1, (227, 87), mask=MISSIONWARNING1)
            MISSIONWARNING1.close()
        elif len(MissionWarnings) == 2:
            #print(f'WARNING 1 X: {str(x+100)}')
            #print(f'WARNING 1 Y: {str(y-60)}')
            BACKGROUND.paste(MISSIONWARNING1, (227, 42), mask=MISSIONWARNING1)
            MISSIONWARNING1.close()

            MISSIONWARNING2 = Image.open(warnings[MissionWarnings[1]])
            MISSIONWARNING2 = scale_image(MISSIONWARNING2, 0.38)
            #x, y = calc_center(MISSIONWARNING2, BACKGROUND)
            #print(f'WARNING 2 X: {str(x+100)}')
            #print(f'WARNING 2 Y: {str(y+40)}')
            BACKGROUND.paste(MISSIONWARNING2, (227, 142), mask=MISSIONWARNING2)
            MISSIONWARNING2.close()

    if 'MissionMutator' in m_d:
        MISSIONMUTATOR = Image.open(mutators[m_d['MissionMutator']])
        MISSIONMUTATOR = scale_image(MISSIONMUTATOR, 0.38)
        #x, y = calc_center(MISSIONMUTATOR, BACKGROUND)
        #print(f'MUTATOR X: {str(x-100)}')
        #print(f'MUTATOR Y: {str(y-10)}')
        BACKGROUND.paste(MISSIONMUTATOR, (27, 92), mask=MISSIONMUTATOR)
        MISSIONMUTATOR.close()

    COMPLEXITY = Image.open(complexities[m_d['Complexity']])
    COMPLEXITY = scale_image(COMPLEXITY, 0.45)
    #x, y = calc_center(COMPLEXITY, BACKGROUND)
    #print(f'COMPLEXITY X: {str(x)}')
    #print(f'COMPLEXITY Y: {str(y-120)}')
    BACKGROUND.paste(COMPLEXITY, (107, 2), mask=COMPLEXITY)
    COMPLEXITY.close()

    LENGTH = Image.open(lengths[m_d['Length']])
    LENGTH = scale_image(LENGTH, 0.45)
    #x, y = calc_center(LENGTH, BACKGROUND)
    #print(f'LENGTH X: {str(x)}')
    #print(f'LENGTH Y: {str(y+120)}')
    BACKGROUND.paste(LENGTH, (107, 242), mask=LENGTH)
    LENGTH.close()

    PRIMARY_OBJ_RESOURCE = render_mission_obj_resource(m_d['PrimaryObjective'], m_d['Complexity'], m_d['Length'])
    PRIMARY_OBJ_RESOURCE = scale_image(PRIMARY_OBJ_RESOURCE, 0.8)
    #x, y = calc_center(PRIMARY_OBJ_RESOURCE, BACKGROUND)
    #print(f'OBJ_RESOURCE X: {str(x-110)}')
    #print(f'OBJ_RESOURCE Y: {str(y+95)}')
    BACKGROUND.paste(PRIMARY_OBJ_RESOURCE, (-37, 143), mask=PRIMARY_OBJ_RESOURCE)
    BACKGROUND = scale_image(BACKGROUND, 0.46)
    PRIMARY_OBJ_RESOURCE.close()

    return BACKGROUND

#-------------------------------------------------------------------------------------------------------------------------------

#PRE-HASH PIL OBJECT ARRAYING

#single threaded
def render_biomes(Biomes):
    rendered_biomes = {}
    for biome, missions in Biomes.items():
        biome1 = []
        for mission in missions:
            mission1 = {}
            mission1['CodeName'] = mission['CodeName']
            mission1['id'] = mission['id']
            mission1['rendered_mission'] = render_mission(mission)
            biome1.append(mission1)
        rendered_biomes[biome] = biome1
    return rendered_biomes

def render_biomes_FLAT(Biomes):
    rendered_biomes = {}
    for biome, missions in Biomes.items():
        biome1 = []
        for mission in missions:
            mission1 = {}
            if 'season_modified' in mission:
                mission1['season_modified'] = {}

                for season in mission['season_modified']:
                    modified_mission = mission['season_modified'][season]
                    mission1['season_modified'][season] = {}
                    mission1['season_modified'][season]['CodeName'] = modified_mission['CodeName']
                    mission1['season_modified'][season]['id'] = modified_mission['id']
                    mission1['season_modified'][season]['season'] = modified_mission['season']
                    mission1['season_modified'][season]['rendered_mission'] = render_mission(modified_mission)

            mission1['CodeName'] = mission['CodeName']
            mission1['season'] = mission['season']
            mission1['id'] = mission['id']
            mission1['rendered_mission'] = render_mission(mission)
            biome1.append(mission1)
        rendered_biomes[biome] = biome1
    return rendered_biomes

# Multiprocessed
def process_mission(mission):
    mission1 = {}
    if 'season_modified' in mission:
        mission1['season_modified'] = {}
        for season in mission['season_modified']:
            modified_mission = mission['season_modified'][season]
            mission1['season_modified'][season] = {
                'CodeName': modified_mission['CodeName'],
                'id': modified_mission['id'],
                'season': modified_mission['season'],
                'rendered_mission': render_mission(modified_mission)
            }
    mission1['CodeName'] = mission['CodeName']
    mission1['season'] = mission['season']
    mission1['id'] = mission['id']
    mission1['rendered_mission'] = render_mission(mission)
    return mission['biome'], mission1

def render_biomes_FLAT(Biomes, render_pool):
    all_missions = []
    for biome, missions in Biomes.items():
        for mission in missions:
            mission['biome'] = biome
            all_missions.append(mission)

    processed_missions = render_pool.map(process_mission, all_missions)

    rendered_biomes = {biome : [] for biome in Biomes.keys()}
    for biome, mission in processed_missions:
        rendered_biomes[biome].append(mission)
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
        # if sum([stage['id'] for stage in deepdive['Stages']]) == 1002:
                if stage['id'] == 999:
                    stage['id'] = -1

        sorted_stages = sorted(deepdive['Stages'], key=lambda x: x['id'], reverse=True)
        for stage in sorted_stages:
            stage_png = render_dd_stage(stage)
            rendered_deepdives[t]['Stages'].append(stage_png)

    return rendered_deepdives

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

def rotate_biomes(DRG, season, tstamp_Queue, next_tstamp_Queue, biomes_lists, rendering_event, go_flag):
    #order = ['Glacial Strata', 'Crystalline Caverns', 'Salt Pits', 'Magma Core', 'Azure Weald', 'Sandblasted Corridors', 'Fungus Bogs', 'Radioactive Exclusion Zone', 'Dense Biozone', 'Hollow Bough']
    #thread pools for saving and hashing PIL objects - microscopic gains. #TODO multiprocessing pools
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
    def read_biomes(timestamp, season):
        return timestamp, DRG[timestamp][season]

    def array_biomes(Biomes, timestamp):
        Biomes1 = {}
        for biome in Biomes.keys():
            biome1 = biome.replace(' ', '-')
            for mission in Biomes[biome]:
                mission0 = {}
                mission0['CodeName'] = mission['CodeName']
                mission_icon = BytesIO()
                mission['rendered_mission'].save(mission_icon, format='PNG')
                mission['rendered_mission'].close()
                mission_icon.seek(0)
                etag = md5(mission_icon.getvalue()).hexdigest()
                mission0['etag'] = etag
                mission0['rendered_mission'] = mission_icon
                Biomes1[biome1+str(mission['id'])] = mission0
        return timestamp, Biomes1

    while len(tstamp_Queue) == 0 and len(next_tstamp_Queue) == 0:
        continue
    biomes_Queue = biomes_lists[season][0]
    nextbiomes_Queue = biomes_lists[season][1]

    _, Biomes = read_biomes(tstamp_Queue[0], season)
    Biomes = render_biomes(Biomes['Biomes'])
    _, Biomes = array_biomes(Biomes, _)
    biomes_Queue.append(Biomes)
    timestamp_next, NextBiomes = read_biomes(next_tstamp_Queue[0], season)
    NextBiomes = render_biomes(NextBiomes['Biomes'])
    timestamp_next, NextBiomes = array_biomes(NextBiomes, timestamp_next)
    nextbiomes_Queue.append(NextBiomes)
    rendering_event.set()
    del Biomes
    del NextBiomes
    del _
    while go_flag.is_set():
        applicable_timestamp = next_tstamp_Queue[0]
        if applicable_timestamp != timestamp_next:
            timestamp_next, NextBiomes = read_biomes(applicable_timestamp, season)
            NextBiomes = render_biomes(NextBiomes['Biomes'])
            timestamp_next, NextBiomes = array_biomes(NextBiomes, applicable_timestamp)
            biomes_Queue.append(nextbiomes_Queue[0])
            biomes_Queue.pop(0)
            nextbiomes_Queue.append(NextBiomes)
            nextbiomes_Queue.pop(0)
            rendering_event.set()
            del NextBiomes
        sleep(0.25)

def rotate_biomes_FLAT(DRG, tstamp_Queue, next_tstamp_Queue, nextbiomes_Queue, biomes_Queue, rendering_events, go_flag):
    def init_worker():
        signal(SIGINT, SIG_DFL)
        signal(SIGTERM, SIG_DFL)

    def array_biomes(Biomes, timestamp):
        Biomes1 = {}
        for biome in Biomes.keys():
            biome1 = biome.replace(' ', '-')
            Biomes1[biome1] = {}
            for mission in Biomes[biome]:
                if 'season_modified' in mission:
                    for season in mission['season_modified']:
                        modified_mission = mission['season_modified'][season]
                        mission1 = {}
                        mission1['CodeName'] = mission['CodeName']
                        modified_mission_icon = BytesIO()
                        modified_mission['rendered_mission'].save(modified_mission_icon, format='PNG')
                        modified_mission['rendered_mission'].close()
                        modified_mission_icon.seek(0)
                        etag = md5(modified_mission_icon.getvalue()).hexdigest()
                        mission1['etag'] = etag
                        mission1['rendered_mission'] = modified_mission_icon
                        Biomes1[modified_mission['CodeName'].replace(' ', '-')+season] = mission1

                    mission0 = {}
                    mission0['CodeName'] = mission['CodeName']
                    mission_icon = BytesIO()
                    mission['rendered_mission'].save(mission_icon, format='PNG')
                    mission['rendered_mission'].close()
                    mission_icon.seek(0)
                    etag = md5(mission_icon.getvalue()).hexdigest()
                    mission0['etag'] = etag
                    mission0['rendered_mission'] = mission_icon
                    Biomes1[mission['CodeName'].replace(' ', '-')+mission['season']] = mission0

                else:
                    mission0 = {}
                    mission0['CodeName'] = mission['CodeName']
                    mission_icon = BytesIO()
                    mission['rendered_mission'].save(mission_icon, format='PNG')
                    mission['rendered_mission'].close()
                    mission_icon.seek(0)
                    etag = md5(mission_icon.getvalue()).hexdigest()
                    mission0['etag'] = etag
                    mission0['rendered_mission'] = mission_icon
                    Biomes1[mission['CodeName'].replace(' ', '-')+mission['season']] = mission0

        return timestamp, Biomes1

    while len(tstamp_Queue) == 0 and len(next_tstamp_Queue) == 0:
        sleep(0.1)
        continue

    with Pool(processes=os.cpu_count(), initializer=init_worker) as render_pool:
        Biomes = render_biomes_FLAT(DRG[tstamp_Queue[0]]['Biomes'], render_pool)
        _, Biomes = array_biomes(Biomes, tstamp_Queue[0])
        biomes_Queue.append(Biomes)
        NextBiomes = render_biomes_FLAT(DRG[next_tstamp_Queue[0]]['Biomes'], render_pool)
        timestamp_next, NextBiomes = array_biomes(NextBiomes, next_tstamp_Queue[0])
        nextbiomes_Queue.append(NextBiomes)
        # render_pool.close()

    for event in rendering_events:
        rendering_events[event].set()
    del Biomes
    del NextBiomes
    del _

    while go_flag.is_set():
        applicable_timestamp = next_tstamp_Queue[0]
        if applicable_timestamp != timestamp_next:

            with Pool(processes=os.cpu_count(), initializer=init_worker) as render_pool:
                NextBiomes = render_biomes_FLAT(DRG[applicable_timestamp]['Biomes'], render_pool)
                timestamp_next, NextBiomes = array_biomes(NextBiomes, applicable_timestamp)
                biomes_Queue.append(nextbiomes_Queue[0])
                biomes_Queue.pop(0)
                nextbiomes_Queue.append(NextBiomes)
                nextbiomes_Queue.pop(0)
                # render_pool.close()

            for event in rendering_events:
                rendering_events[event].set()
            del NextBiomes

        sleep(0.25)

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
            except Exception:
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

# def extract_days_from_json(data, num_days):
#     timestamps = {datetime.fromisoformat(key.replace('Z', '')): value for key, value in data.items()}
#     current_datetime = datetime.utcnow()

#     days_from_now = current_datetime + timedelta(days=num_days)
#     relevant_days = {f"{str(key).replace(' ', 'T')}Z": value for key, value in timestamps.items() if current_datetime <= key < days_from_now}
#     return relevant_days

# def split_json(num_days, DRG):
#     shutil.rmtree('./static/json/bulkmissions')
#     os.mkdir('./static/json/bulkmissions')

#     bs = DRG[round_time_down(datetime.utcnow().isoformat())]
#     DRG = extract_days_from_json(DRG, num_days)

#     for timestamp, dictionary in (DRG.items()):
#         fname = timestamp.replace(':','-')
#         with open(f'./static/json/bulkmissions/{fname}.json', 'w') as f:
#             json.dump(dictionary, f)

#     fname = round_time_down(datetime.utcnow().isoformat()).replace(':', '-')
#     with open (f'./static/json/bulkmissions/{fname}.json', 'w') as f:
#         json.dump(bs, f)

# def rotate_split_jsons(num_days, DRG, index_event):
#     split_json(num_days, DRG)
#     index_event.set()
#     while True:
#         sleep(num_days*86400-3600)
#         index_event.clear()
#         split_json(num_days)
#         index_event.set()

def split_daily_deals_json():
    with open('drgdailydeals.json', 'r') as f:
        AllTheDeals = json.load(f)

    shutil.rmtree('./static/json/dailydeals')
    os.mkdir('./static/json/dailydeals')

    for timestamp, deal in AllTheDeals.items():
        fname = timestamp.replace(':', '-')
        with open(f'./static/json/dailydeals/{fname}.json', 'w') as f:
            json.dump(deal, f)

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
        if os.path.isdir('./static/json/bulkmissions'):
            shutil.rmtree('./static/json/bulkmissions')
        os.mkdir('./static/json/bulkmissions')

        for timestamp, dictionary in DRG.items():
            fname = timestamp.replace(':','-')
            with open(f'./static/json/bulkmissions/{fname}.json', 'w') as f:
                json.dump(dictionary, f)

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

        current_datetime = datetime.utcnow()
        days_from_now = current_datetime + timedelta(days=num_days)
        relevant_days = {key: value for key, value in complete_data.items() if current_datetime <= datetime.strptime(key, '%Y-%m-%d') < days_from_now}
        current_datetime = datetime.utcnow().strftime('%Y-%m-%d')
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
    sorted_keys = sorted(dictionary.keys(), key=lambda x: datetime.fromisoformat(x.replace('Z', '')))
    ordered_dictionary = {}
    for key in sorted_keys:
        ordered_dictionary[key] = dictionary[key]
    return ordered_dictionary

# grug timedelta
# def round_time(current_time, next_):
#     rounded_time = current_time.replace(second=0, microsecond=0)
#     current_year, current_month, current_day, current_hour, current_minute, current_second = current_time.year, current_time.month, current_time.day, current_time.hour, current_time.minute, current_time.second
#     days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
#     if next_:
#         if rounded_time.minute < 30:
#             rounded_time = rounded_time.replace(minute=30)
#         else:
#             if rounded_time.hour == 23:
#                 try:
#                     rounded_time = rounded_time.replace(minute=0, hour=(rounded_time.hour + 1) % 24, day=(rounded_time.day + 1))
#                 except ValueError:
#                     rounded_time = rounded_time.replace(minute=0, hour=(rounded_time.hour + 1) % 24)
#                     current_day += 1
#                     current_month += 1
#                     if current_month > 12:
#                         rounded_time = rounded_time.replace(month=current_month-12, year=current_year+1, day=1)
#                     else:
#                         if rounded_time.month == 2 and current_year % 4 == 0 and (current_year % 100 != 0 or current_year % 400 == 0):
#                             days_in_month[1] = 29
#                         if current_day > days_in_month[rounded_time.month - 1]:
#                             current_day = rounded_time.day - days_in_month[rounded_time.month - 1]
#                             rounded_time = rounded_time.replace(day=1)
#                             rounded_time = rounded_time.replace(month=current_month)

#             else:
#                 rounded_time = rounded_time.replace(minute=0, hour=(rounded_time.hour + 1) % 24)
#     else:
#         if current_time.minute < 30:
#             rounded_time = rounded_time.replace(minute=0)
#         else:
#             rounded_time = rounded_time.replace(minute=30)

#     rounded_time_str = rounded_time.strftime("%Y-%m-%dT%H:%M:%SZ")
#     return rounded_time_str
# def select_timestamp(next_):
#     current_time = datetime.utcnow()
#     rounded_time_str = round_time(current_time, next_)
#     return rounded_time_str

def round_time(current_time, next_):
    if next_:
        rounded_time = current_time + timedelta(minutes=30) - timedelta(minutes=current_time.minute % 30)
    else:
        rounded_time = current_time - timedelta(minutes=current_time.minute % 30)
    rounded_time = rounded_time.replace(second=0)
    rounded_time_str = rounded_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    return rounded_time_str
def select_timestamp(next_):
    current_time = datetime.utcnow()
    rounded_time_str = round_time(current_time, next_)
    return rounded_time_str

# obsolete for its original purpose but serves to clear memory now
def select_timestamp_from_dict(dictionary, next_):
    current_time = datetime.utcnow()
    keys = list(dictionary.keys())
    for i in range(len(keys) - 1):
        timestamp = datetime.fromisoformat(keys[i].replace('Z', ''))
        next_timestamp = datetime.fromisoformat(keys[i+1].replace('Z', ''))
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

# obsolete, consolidated into rotate_timestamps
def rotate_timestamp(tstamp_Queue, next_, go_flag):
    applicable_timestamp = select_timestamp(next_=next_)
    tstamp_Queue.append(applicable_timestamp)
    timestamp = tstamp_Queue[0]

    while go_flag.is_set():
        applicable_timestamp = select_timestamp(next_=next_)
        if applicable_timestamp != timestamp:
            tstamp_Queue.append(applicable_timestamp)
            tstamp_Queue.pop(0)
            timestamp = tstamp_Queue[0]
        sleep(0.25)

def rotate_timestamps(tstamp_Queue, next_tstamp_Queue, go_flag):
    applicable_timestamp = select_timestamp(next_=False)
    applicable_next_timestamp = select_timestamp(next_=True)
    next_tstamp_Queue.append(applicable_next_timestamp)
    tstamp_Queue.append(applicable_timestamp)
    timestamp = tstamp_Queue[0]

    while go_flag.is_set():
        applicable_timestamp = select_timestamp(next_=False)
        if applicable_timestamp != timestamp:
            select_timestamp(next_=True)
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

# combines seasons to one key while removing duplicates, see render_biomes_FLAT in this file and renderBiomesFlat/arrayBiomes in index.js for postprocessing
def flatten_seasons(DRG):
    def compare_dicts(dict1, dict2, ignore_keys):
        dict1_filtered = {k: v for k, v in dict1.items() if k not in ignore_keys}
        dict2_filtered = {k: v for k, v in dict2.items() if k not in ignore_keys}

        return dict1_filtered == dict2_filtered
    combined = {}
    seasons = list(list(DRG.items())[1][1].keys())
    timestamps = list(DRG.keys())

    for timestamp in timestamps:
        combined[timestamp] = {}
        combined[timestamp]['timestamp'] = timestamp
        combined[timestamp]['Biomes'] = {}
        for biome in DRG[timestamp]['s0']['Biomes'].keys():
            combined[timestamp]['Biomes'][biome+'codenames'] = []

        for biome, missions in DRG[timestamp]['s0']['Biomes'].items():
            for mission in missions:
                mission['season'] = 's0'
                combined[timestamp]['Biomes'][biome+'codenames'].append(mission['CodeName'])

            combined[timestamp]['Biomes'][biome] = [mission for mission in missions]
        del DRG[timestamp]['s0']
    seasons.remove('s0')

    duplicates = []
    for timestamp in timestamps:
        for season in seasons:
            for biome, missions in DRG[timestamp][season]['Biomes'].items():
                for index, mission in enumerate(missions):
                    mission['season'] = season
                    if mission['CodeName'] in combined[timestamp]['Biomes'][biome+'codenames']:
                        duplicates.append([timestamp, biome, mission])
                        continue
                    try:
                        combined[timestamp]['Biomes'][biome].insert(index, mission)
                        combined[timestamp]['Biomes'][biome+'codenames'].append(mission['CodeName'])
                    except:
                        combined[timestamp]['Biomes'][biome].append(mission)
                        combined[timestamp]['Biomes'][biome+'codenames'].append(mission['CodeName'])

    for timestamp, biome, dup_mission in duplicates:
        for mission in combined[timestamp]['Biomes'][biome]:

            if dup_mission['CodeName'] != mission['CodeName']:
                continue
            if compare_dicts(mission, dup_mission, ['season', 'id', 'season_modified']):
                continue
            if 'season_modified' not in mission:
                mission['season_modified'] = {}

            mission['season_modified'][dup_mission['season']] = dup_mission

    for timestamp in timestamps:
        for k in list(combined[timestamp]['Biomes'].keys()):
            if k.endswith('codenames'):
                del combined[timestamp]['Biomes'][k]

    return combined

def wait_rotation(rendering_events, index_event, go_flag):
    target_minutes_59 = [29, 59]
    while go_flag.is_set():
        current_time = datetime.now().time()
        current_minute = current_time.minute
        current_second = current_time.second + current_time.microsecond / 1e6

        if current_second > 58.50 and current_minute in target_minutes_59:
            for s in rendering_events:
                rendering_events[s].clear()
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


def SERVER_READY(index_event):
    start = time()
    index_event.wait()
    print('Startup time:', round(time() - start, 3), 'seconds.')
    from psutil import Process
    print('Server is ready for requests')
    print("Memory used by process:", round(Process().memory_info().rss / (1024 * 1024), 2), "MB")
    del Process
    return

def timestamped_print(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        include_timestamp = kwargs.pop('include_timestamp', True)
        args = [str(arg) for arg in args]

        if include_timestamp:
            concatenated_args = ''.join(args)
            if concatenated_args.strip() != '':
                timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                args = (f'{timestamp}', *args)
        return func(*args, **kwargs)
    return wrapper
print = timestamped_print(print)

def timestamped_write(func):
    @wraps(func)
    def wrapper(data):
        if type(data) == str:
            timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
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
#HTML STRING RENDERERS

#HOMEPAGE
def rotate_index(rendering_events, current_timestamp_Queue, next_timestamp_Queue, index_event, index_Queue, go_flag):
    for e in rendering_events:
        rendering_events[e].wait()
    current_timestamp = current_timestamp_Queue[0]
    # index = {}
    # index_ = render_index().encode()
    # index['index'] = index_
    # etag = md5(index_).hexdigest()
    # index['etag'] = etag
    # index_Queue.append(index)
    index_event.set()
    while go_flag.is_set():
        applicable_timestamp = current_timestamp_Queue[0]
        if applicable_timestamp != current_timestamp:
            for e in rendering_events:
                rendering_events[e].wait()
            # index = {}
            # index_ = render_index().encode()
            # index['index'] = index_
            # etag = md5(index_).hexdigest()
            # index['etag'] = etag
            # index_Queue.append(index)
            # index_Queue.pop(0)
            index_event.set()
        sleep(0.33)

# def array_standard_missions(Biomes, biome_str, html):
#     html += '<br>\n'
#     url_biome = biome_str.replace(' ', '-')
#     for mission in Biomes[biome_str]:
#         fname = f'/png?img={url_biome}{str(mission["id"])}'
#         html += f'<div class="mission-hover-zoom"><img title="{mission["CodeName"]}" class="mission" src="{fname}"></div>\n'
#     return html
# def array_standard_missions_next(Biomes, biome_str, html):
#     html += '<br>\n'
#     url_biome = biome_str.replace(' ', '-')
#     for mission in Biomes[biome_str]:
#         fname = f'/upcoming_png?img={url_biome}{str(mission["id"])}'
#         html += f'<div class="mission-hover-zoom"><img title="{mission["CodeName"]}" class="mission" src="{fname}"></div>\n'
#     return html
# def array_dd_missions(dd_str, html):
#     folder_name = dd_str.replace(' ', '_')
#     html += f'<img class="dd-biome" src="/files/{folder_name}/dd_biome.png">\n<br>\n'
#     stg_count = 0
#     for i in range(3):
#         stg_count += 1
#         fname = str(stg_count)
#         html += f'<div class="mission-hover-zoom"><img class="mission" title="Stage {fname}" src="/files/{folder_name}/{fname}.png"></div>\n'
#     return html

#obsolete, refer to index.html
def render_index():
    html = '''<!doctype html>
<html>
<head>
<title>Current Missions from the Hoxxes IV Space Rig Mission Terminal</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta property="og:title" content="Current and Upcoming Missions from the Hoxxes IV Mission Terminal">
<meta property="og:type" content="website">
<meta property="og:image" content="/static/Mission_control_portrait.png">
<meta property="og:description" content="Deep Rock Galactic Mission Tracker">
<link rel ="icon" href="/static/favicon.ico" type="image/x-icon">
<link rel ="stylesheet" href="/static/styles.css" type="text/css">
<script src="/static/index.js"></script>
</head>
<body bgcolor="#303030">
<video id="background-video" autoplay muted loop><source src="/static/space_rig.webm" type="video/webm"></video>
<div class="overlay"></div>
<p class="loading">Loading</p>
<div id="mainContent">
<div id="countdowncontainer">
<button id="backgroundButton">Hide background</button><button id="buttonsbutton">x</button><br>
<div id=DAILYDEAL><div id="dailydealhead">NEW DAILY DEAL IN<br><span id="DailyDealcountdown"></span></div><div id="DailyDeal" class="daily_deal_container"></div></div>
<button id="dailydealbutton">Click here to see Daily Deal</button><br>
<div id="missionscountdown">NEW MISSIONS IN<br>
<span id="countdown"></span></div><button id="slideButton">Hide countdown</button><br>
<button id="currentButton">Click here to see upcoming missions</button>
<br>
<select id="season" name="season" class="seasonBox">
</select>
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
<div class="jsonlinks"><span style="color: white;font-size: 30px;font-family: BebasNeue, sans-serif;"> <a class="jsonlink" href="/json?data=current">CURRENT MISSION DATA</a> | <a class="jsonlink" href="/json?data=next">UPCOMING MISSION DATA</a> | <a class="jsonlink" href="/json?data=DD">CURRENT DEEP DIVE DATA</a> | <a class="jsonlink" href="/json?data=dailydeal">CURRENT DAILY DEAL DATA</a> | <a class="jsonlink" href="/xp_calculator">CLASS XP CALCULATOR</a> | <a class="jsonlink" href="https://github.com/rolfosian/drgmissions/">GITHUB</a></span> </div>
<span class="credits">Send credits (eth): 0xb9c8591A80A3158f7cFFf96EC3c7eA9adB7818E7</span>
</div>
<p class='gsgdisclaimer'><i>This website is a third-party platform and is not affiliated, endorsed, or sponsored by Ghost Ship Games. The use of Deep Rock Galactic's in-game assets on this website is solely for illustrative purposes and does not imply any ownership or association with the game or its developers. All copyrights and trademarks belong to their respective owners. For official information about Deep Rock Galactic, please visit the official Ghost Ship Games website.</i></p></div>
</div>
</body></html>'''
    return html

#CLASS XP CALCULATOR
# obsolete, refer to xp_calculator.html
def render_xp_calc_index():
    index = {}
    index_ = '''<!DOCTYPE html>
<html>
<head>
<link rel ="icon" href="/files/favicon.ico" type="image/x-icon">
<link rel ="stylesheet" href="/files/styles.css" type="text/css">
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
<img id="background-video" src="/files/drop_pod.jpg" type="video/webm">
<div class="overlay"></div>
<p class="loading">Loading</p>
<div id="scal" class="collapsed">
<div class="calc-grid-container">
<form id="xpForm">

<h2><div class="mission-hover-zoom"><img class="class-iconx" src="/files/class_icons/Icon_Character_Engineer.png"></div></h2>
<label class="classcalcsub" for="engineerLevels">Level:&nbsp;</label>
<input placeholder="1" class="calcbox" type="number" min="1" max="25" id="engineerLevels" name="engineerLevels"><br><br>
<label class="classcalcsub" for="engineerPromotions">Promotions:&nbsp;</label>
<input placeholder="0" class="calcbox" type="number" min="0" id="engineerPromotions" name="engineerPromotions"><br><br>

<h2><div class="mission-hover-zoom"><img class="class-iconx" src="/files/class_icons/Icon_Character_Scout.png"></div></h2>
<label class="classcalcsub" for="scoutLevels">Level:&nbsp;</label>
<input placeholder="1" class="calcbox" type="number" min="1" max="25" id="scoutLevels" name="scoutLevels"><br><br>
<label class="classcalcsub" for="scoutPromotions">Promotions:&nbsp;</label>
<input placeholder="0" class="calcbox" type="number" min="0" id="scoutPromotions" name="scoutPromotions"><br><br>

<h2><div class="mission-hover-zoom"><img class="class-iconx" src="/files/class_icons/Icon_Character_Driller.png"></div></h2>
<label class="classcalcsub" for="drillerLevels">Level:&nbsp;</label>
<input placeholder="1" class="calcbox" type="number" min="1" max="25" id="drillerLevels" name="drillerLevels"><br><br>
<label class="classcalcsub" for="drillerPromotions">Promotions:&nbsp;</label>
<input placeholder="0" class="calcbox" type="number" min="0" id="drillerPromotions" name="drillerPromotions"><br><br>

<h2><div class="mission-hover-zoom"><img class="class-iconx" src="/files/class_icons/Icon_Character_Gunner.png"></div></h2>
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
  <th><img title="Effective Level" src="/files/icon_class_level.png"></th>
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
<script src="/files/xp_calculator.js"></script>
<div class="collapsed">
<img class="class-icon" src="/files/class_icons/Icon_Character_Engineer_Bronze_1.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Engineer_Bronze_2.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Engineer_Bronze_3.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Engineer_Silver_1.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Engineer_Silver_2.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Engineer_Silver_3.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Engineer_Gold_1.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Engineer_Gold_2.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Engineer_Gold_3.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Engineer_Platinum_1.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Engineer_Platinum_2.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Engineer_Platinum_3.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Engineer_Emerald_1.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Engineer_Emerald_2.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Engineer_Emerald_3.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Engineer_Legendary_1.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Engineer_Legendary_2.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Engineer_Legendary_3.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Scout_Bronze_1.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Scout_Bronze_2.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Scout_Bronze_3.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Scout_Silver_1.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Scout_Silver_2.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Scout_Silver_3.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Scout_Gold_1.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Scout_Gold_2.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Scout_Gold_3.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Scout_Platinum_1.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Scout_Platinum_2.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Scout_Platinum_3.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Scout_Emerald_1.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Scout_Emerald_2.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Scout_Emerald_3.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Scout_Legendary_1.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Scout_Legendary_2.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Scout_Legendary_3.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Driller_Bronze_1.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Driller_Bronze_2.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Driller_Bronze_3.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Driller_Silver_1.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Driller_Silver_2.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Driller_Silver_3.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Driller_Gold_1.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Driller_Gold_2.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Driller_Gold_3.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Driller_Platinum_1.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Driller_Platinum_2.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Driller_Platinum_3.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Driller_Emerald_1.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Driller_Emerald_2.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Driller_Emerald_3.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Driller_Legendary_1.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Driller_Legendary_2.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Driller_Legendary_3.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Gunner_Bronze_1.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Gunner_Bronze_2.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Gunner_Bronze_3.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Gunner_Silver_1.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Gunner_Silver_2.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Gunner_Silver_3.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Gunner_Gold_1.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Gunner_Gold_2.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Gunner_Gold_3.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Gunner_Platinum_1.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Gunner_Platinum_2.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Gunner_Platinum_3.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Gunner_Emerald_1.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Gunner_Emerald_2.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Gunner_Emerald_3.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Gunner_Legendary_1.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Gunner_Legendary_2.png">
<img class="class-icon" src="/files/class_icons/Icon_Character_Gunner_Legendary_3.png">
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