from PIL import Image, ImageDraw, ImageFont, ImageFilter
from hashlib import md5
from time import sleep
from io import BytesIO
import os
from datetime import datetime, timedelta
from dateutil import parser
import shutil
import glob
import json
import gc
# import subprocess
#from concurrent.futures import ThreadPoolExecutor
#from concurrent.futures import ProcessPoolExecutor
#from os import cpu_count

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
    
    BUBBLE = Image.open('./img/Icon_TradeTerminal_SaleBubble.png')
    BUBBLE = scale_image(BUBBLE, 0.8)
    
    font_path = './img/Bungee-Regular.ttf'
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
    font_path = './img/Bungee-Regular.ttf'
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
    CREDITS = Image.open('./img/Credit.png')
    CREDITS = scale_image(CREDITS, 0.4)
    text = str(credits)
    font_path = './img/Bungee-Regular.ttf'
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
    font_path = './img/HammerBro101MovieBold-Regular.ttf'
    font_size = 45
    font = ImageFont.truetype(font_path, font_size)
    resources = {
        'Bismor': './img/Bismor_icon.png',
        'Croppa': './img/Croppa_icon.png',
        'Enor Pearl': './img/Enor_pearl_icon.png',
        'Jadiz': './img/Jadiz_icon.png',
        'Magnite': './img/Magnite_icon.png',
        'Umanite': './img/Umanite_icon.png',
        
        'Credits': './img/Credit.png',
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

    font_path = './img/Bungee-Regular.ttf'
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

def render_mission_obj_resource(primary_obj, complexity, length):
    font_path = './img/HammerBro101MovieBold-Regular.ttf'
    font_size = 45
    font = ImageFont.truetype(font_path, font_size)
    text_color = (255, 255, 255)
    primary_objs = {
        'Mining Expedition': './img/Morkite_icon.png',
        'Egg Hunt': './img/Alien_egg_icon.png',
        'On-Site Refining': './img/Icon_PumpingJack_Core_Simplified_Workfile.png',
        'Salvage Operation': './img/Icon_Salvage_Mules_Objective.png',
        'Escort Duty': './img/Icon_FuelCannister_Simplified.png',
        'Point Extraction': './img/Icons_Resources_Outline_Aquarq.png',
        'Elimination': './img/Kill_Dreadnought_Objective_icon.png',
        'Industrial Sabotage': './img/Icon_Facility_DataRack.png'
            }
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
    }
    
    BACKGROUND = Image.new("RGBA", (256, 256), (0,0,0,0))
    HEXAGON = Image.open('./img/hexagon.png')
    HEXAGON = scale_image(HEXAGON, 0.4)
    #x, y = calc_center(HEXAGON, BACKGROUND)
    #print(f'HEXAGON X: {str(x)}')
    #print(f'HEXAGON Y: {str(y)}')
    BACKGROUND.paste(HEXAGON, (69, 59), mask=HEXAGON)
    HEXAGON.close()
    
    RESOURCE = Image.open(primary_objs[primary_obj])
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

def render_mission(m_d, six):
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
    
    PRIMARY = Image.open(primary_objs[m_d['PrimaryObjective']])
    PRIMARY = scale_image(PRIMARY, 0.4)
    #x, y = calc_center(PRIMARY, BACKGROUND)
    #print(f'PRIMARY X: {str(x)}')
    #print(f'PRIMARY Y: {str(y)}')
    BACKGROUND.paste(PRIMARY, (83, 58), mask=PRIMARY)
    PRIMARY.close()

    SECONDARY = Image.open(secondary_objs[m_d['SecondaryObjective']])
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
    PRIMARY_OBJ_RESOURCE.close()
    
    if six:
        BACKGROUND = scale_image(BACKGROUND, 0.40)
    else:
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
        'Crystalline Caverns': './img/DeepDive_MissionBar_CrystalCaves.png',
        'Glacial Strata': './img/DeepDive_MissionBar_GlacialStrata.png',
        'Radioactive Exclusion Zone': './img/DeepDive_MissionBar_Radioactive.png',
        'Fungus Bogs': './img/DeepDive_MissionBar_FungusBogs.png',
        'Dense Biozone': './img/DeepDive_MissionBar_LushDownpour.png',
        'Salt Pits': './img/DeepDive_MissionBar_SaltPits.png',
        'Sandblasted Corridors': './img/DeepDive_MissionBar_Sandblasted.png',
        'Magma Core': './img/DeepDive_MissionBar_MagmaCore.png',
        'Azure Weald': './img/DeepDive_MissionBar_AzureWeald.png',
        'Hollow Bough': './img/DeepDive_MissionBar_HollowBough.png'
    }
    
    BACKGROUND = Image.open(biomes[biome])
    # BACKGROUND = add_shadowed_text_to_image(BACKGROUND, codename, 'white', '#000000', font_path, font_size)
    text_and_fonts = [('CODENAME: ', "./img/RiftSoft-Regular.ttf"), (f'{codename}', './img/BebasNeue-Regular.ttf')]
    BACKGROUND = add_shadowed_text_to_image_SPLITFONTS(BACKGROUND, text_and_fonts, 'white', '#000000', font_size=45)
    #BACKGROUND.save('TEST.png', format='PNG')
    #subprocess.run(['gwenview', 'TEST.png'])
    return BACKGROUND

def render_dd_secondary_obj_resource(secondary_obj):
    font_path = './img/HammerBro101MovieBold-Regular.ttf'
    font_size = 45
    font = ImageFont.truetype(font_path, font_size)
    text_color = (255, 255, 255)
    secondary_objs = {
        'Repair Minimules': './img/Icon_Salvage_Mules_Objective.png',
        'Kill Dreadnought(s)': './img/Kill_Dreadnought_Objective_icon.png',
        'Mine Morkite': './img/Morkite_icon.png',
        'Get Alien Eggs': './img/Alien_egg_icon.png',
        'Black Box': './img/Blackbox_icon.png'
            }
    values = {
        'Repair Minimules': '2',
        'Kill Dreadnought(s)': '1',
        'Mine Morkite': '150',
        'Get Alien Eggs':'2',
        'Black Box':'1',
    }

    BACKGROUND = Image.new("RGBA", (256, 256), (0,0,0,0))
    HEXAGON = Image.open('./img/hexagon.png')
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
        'Mining Expedition': './img/Mining_expedition_icon.png',
        'Egg Hunt': './img/Egg_collection_icon.png',
        'On-Site Refining': './img/Refining_icon.png',
        'Salvage Operation': './img/Salvage_icon.png',
        'Escort Duty': './img/Escort_icon.png',
        'Point Extraction': './img/Point_extraction_icon.png',
        'Elimination': './img/Elimination_icon.png',
        'Industrial Sabotage': './img/Sabotage_icon.png'
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
    
    #BACKGROUND.save('TEST.png', format='PNG')
    #subprocess.run(['gwenview', 'TEST.png'])
    return BACKGROUND 

#dev
#deal_dict = {"ChangePercent": 225.62124633789, "DealType": "Sell", "Credits": 42069, "ResourceAmount": 78, "Resource": "Enor Pearl"}
#render_dailydeal(deal_dict)

#m_d = {"CodeName":" ","Complexity":"2","Length":"2","MissionWarnings":["Lithophage Outbreak","Lethal Enemies"],"MissionMutator":"Double XP","PrimaryObjective":"Salvage Operation","SecondaryObjective":"Mine Morkite","id":654}
#render_dd_stage(m_d)

#m_d = {"CodeName":" ","Complexity":"2","Length":"2","MissionWarnings":["Lithophage Outbreak","Lethal Enemies"],"MissionMutator":"Double XP","PrimaryObjective":"Salvage Operation","SecondaryObjective":"Hollomite","id":654}
#render_mission(m_d)
#-------------------------------------------------------------------------------------------------------------------------------

#PRE-HASH PIL OBJECT ARRAYING

#thread pools for standard missions - microscopic gains. #TODO debug multiprocessing pools, gunicorn circular import
#def wrap_missions_executor(missions):
    #mission_futures = []
    #with ThreadPoolExecutor() as executor:
        #for mission in missions:
            #if len(missions) > 5:
                #six = True
            #else:
                #six = False
            #future = executor.submit(render_mission, mission, six)
            #mission_futures.append(future)
        #results = [future.result() for future in mission_futures]
        #return results
#def wrap_biome_worker(args):
    #biome, missions = args
    #return biome, wrap_missions_executor(missions)
#def wrap_biomes_executor_ThreadPool(Biomes):
    #with ThreadPoolExecutor() as executor:
        #biome_futures = {}
        #for biome, missions in Biomes.items():
            #future = executor.submit(wrap_missions_executor, missions)
            #biome_futures[biome] = future
        #results = {biome: future.result() for biome, future in biome_futures.items()}
        #return results
#def wrap_biomes_executor_ProcessPool(Biomes):
    #with ProcessPoolExecutor() as executor:
        #biome_futures = {}
        #for biome, missions in Biomes.items():
            #future = executor.submit(wrap_missions_executor, missions)
            #biome_futures[biome] = future
    #results = {biome: future.result() for biome, future in biome_futures.items()}
    #return results
#def wrap_biomes_executor(Biomes):
    #if cpu_count() == 1:
        #rendered_biomes = wrap_biomes_executor_ThreadPool(Biomes)
        #return rendered_biomes
    #rendered_biomes = wrap_biomes_executor_ProcessPool(Biomes)
    #return rendered_biomes
        
#def render_biomes(Biomes):
    ## start_time = time.time()
    #rendered_biomes = wrap_biomes_executor(Biomes)
    ## print(time.time() - start_time)
    #return rendered_biomes

#single threaded
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
            mission1['id'] = mission['id']
            mission1['rendered_mission'] = render_mission(mission, six)
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

#----------------------------------------------------------------
#ICON SAVE, HASH, AND ARRAY ROTATORS
def rotate_dailydeal(AllTheDeals, tstamp_Queue, deal_Queue):
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
    while True:
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
    
def rotate_biomes(DRG, tstamp_Queue, biomes_Queue, rendering_event):
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
    def array_biomes(Biomes, timestamp):
        Biomes1 = {}
        for biome in Biomes.keys():
            biome1 = biome.replace(' ', '-')
            Biomes1[biome1] = {}
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
    while len(tstamp_Queue) == 0:
        continue
    Biomes = DRG[tstamp_Queue[0]]['Biomes']
    Biomes = render_biomes(Biomes)
    #Biomes = sort_dictionary(Biomes, order)
    timestamp, Biomes = array_biomes(Biomes, tstamp_Queue[0])
    biomes_Queue.append(Biomes)
    rendering_event.set()
    del Biomes
    while True:
        applicable_timestamp = tstamp_Queue[0]
        if applicable_timestamp != timestamp:
                Biomes = DRG[applicable_timestamp]['Biomes']
                Biomes = render_biomes(Biomes)
                #Biomes = sort_dictionary(Biomes, order)
                timestamp, Biomes = array_biomes(Biomes, applicable_timestamp)
                biomes_Queue.append(Biomes)
                biomes_Queue.pop(0)
                rendering_event.set()
                del Biomes
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
            if os.path.exists(f'./files/{folder_name}'):
                shutil.rmtree(f'./files/{folder_name}')
            os.mkdir(f'./files/{folder_name}')
            BIOME_NORMAL = render_dd_biome_codename(f"{dds[dd_str]['CodeName']}", dds[dd_str]['Biome'])
            BIOME_NORMAL.save(f'./files/{folder_name}/dd_biome.png', format='PNG')
            for mission in dds[dd_str]['Stages']:
                img_count += 1
                fname = str(img_count)
                mission.save(f'./files/{folder_name}/{fname}.png')
                mission.close()
                
            dd_str = 'Deep Dive Elite'
            img_count = 0
            folder_name = dd_str.replace(' ', '_')
            if os.path.exists(f'./files/{folder_name}'):
                shutil.rmtree(f'./files/{folder_name}')
            os.mkdir(f'./files/{folder_name}')
            BIOME_ELITE = render_dd_biome_codename(f"{dds[dd_str]['CodeName']}", dds[dd_str]['Biome'])
            BIOME_ELITE.save(f'./files/{folder_name}/dd_biome.png', format='PNG')
            for mission in dds[dd_str]['Stages']:
                img_count += 1
                fname = str(img_count)
                mission.save(f'./files/{folder_name}/{fname}.png')
                mission.close()
            del dds
        sleep(0.25)
#----------------------------------------------------------------
#UTILS

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

#grug timedelta
#def round_time(current_time, next_):
    #rounded_time = current_time.replace(second=0, microsecond=0)
    #current_year, current_month, current_day, current_hour, current_minute, current_second = current_time.year, current_time.month, current_time.day, current_time.hour, current_time.minute, current_time.second
    #days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    #if next_:
        #if rounded_time.minute < 30:
            #rounded_time = rounded_time.replace(minute=30)
        #else:
            #if rounded_time.hour == 23:
                #try:
                    #rounded_time = rounded_time.replace(minute=0, hour=(rounded_time.hour + 1) % 24, day=(rounded_time.day + 1))
                #except ValueError:
                    #rounded_time = rounded_time.replace(minute=0, hour=(rounded_time.hour + 1) % 24)
                    #current_day += 1
                    #current_month += 1
                    #if current_month > 12:
                        #rounded_time = rounded_time.replace(month=current_month-12, year=current_year+1, day=1)
                    #else:
                        #if rounded_time.month == 2 and current_year % 4 == 0 and (current_year % 100 != 0 or current_year % 400 == 0):
                            #days_in_month[1] = 29
                        #if current_day > days_in_month[rounded_time.month - 1]:
                            #current_day = rounded_time.day - days_in_month[rounded_time.month - 1]
                            #rounded_time = rounded_time.replace(day=1)
                            #rounded_time = rounded_time.replace(month=current_month)
                    
            #else:
                #rounded_time = rounded_time.replace(minute=0, hour=(rounded_time.hour + 1) % 24)
    #else:
        #if current_time.minute < 30:
            #rounded_time = rounded_time.replace(minute=0)
        #else:
            #rounded_time = rounded_time.replace(minute=30)
        
    #rounded_time_str = rounded_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    #return rounded_time_str
#def select_timestamp(next_):
    #current_time = datetime.utcnow()
    #rounded_time_str = round_time(current_time, next_)
    #return rounded_time_str

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

def rotate_timestamp(tstamp_Queue, next_):
    applicable_timestamp = select_timestamp(next_=next_)
    tstamp_Queue.append(applicable_timestamp)
    timestamp = tstamp_Queue[0]
    while True:
        applicable_timestamp = select_timestamp(next_=next_)
        if applicable_timestamp != timestamp:
            tstamp_Queue.append(applicable_timestamp)
            tstamp_Queue.pop(0)
            timestamp = tstamp_Queue[0]
        sleep(0.25)

def rotate_timestamps(tstamp_Queue, next_tstamp_Queue):
    applicable_timestamp = select_timestamp(next_=False)
    applicable_next_timestamp = select_timestamp(next_=True)
    next_tstamp_Queue.append(applicable_next_timestamp)
    tstamp_Queue.append(applicable_timestamp)
    timestamp = tstamp_Queue[0]
    while True:
        applicable_timestamp = select_timestamp(next_=False)
        if applicable_timestamp != timestamp:
            select_timestamp(next_=True)
            next_tstamp_Queue.append(select_timestamp(next_=True))
            next_tstamp_Queue.pop(0)
            tstamp_Queue.append(applicable_timestamp)
            tstamp_Queue.pop(0)
            timestamp = tstamp_Queue[0]
        sleep(0.25)
        
def rotate_timestamp_from_dict(dictionary, tstamp_Queue, next_):
    applicable_timestamp = select_timestamp_from_dict(dictionary, next_=next_)
    gc.collect()
    tstamp_Queue.append(applicable_timestamp)
    timestamp = tstamp_Queue[0]
    while True:
        applicable_timestamp = select_timestamp_from_dict(dictionary, next_=next_)
        if applicable_timestamp != timestamp:
            tstamp_Queue.append(applicable_timestamp)
            tstamp_Queue.pop(0)
            timestamp = tstamp_Queue[0]
        sleep(0.25)

def wait_rotation(rendering_event, rendering_event_next, index_event):
    target_minutes_59 = [29, 59]
    while True:
        current_time = datetime.now().time()
        current_minute = current_time.minute
        current_second = current_time.second + current_time.microsecond / 1e6
        if current_second > 58.50 and current_minute in target_minutes_59:
            rendering_event.clear()
            rendering_event_next.clear()
            index_event.clear()
        sleep(0.2)
        
#def GARBAGE():
    #while True:
        #sleep(43200)
        #gc.collect()
#GARBAGE_thread = threading.Thread(target=GARBAGE)

def SERVER_READY(index_event):
    index_event.wait()
    now = datetime.now()
    formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")
    print(f'{formatted_datetime} DRGMISSIONS SERVER IS READY FOR REQUESTS')
    return

#----------------------------------------------------------------
#HTML STRING RENDERERS

#HOMEPAGE
def rotate_index(DRG, rendering_event, rendering_event_next, current_timestamp_Queue, next_timestamp_Queue, DDs_Queue, index_event, index_Queue):
    rendering_event.wait()
    rendering_event_next.wait()
    current_timestamp = current_timestamp_Queue[0]
    index = {}
    index_ = render_index(DRG[current_timestamp], DRG[next_timestamp_Queue[0]]).encode()
    index['index'] = index_
    etag = md5(index_).hexdigest()
    index['etag'] = etag
    index_Queue.append(index)
    index_event.set()
    while True:
        applicable_timestamp = current_timestamp_Queue[0]
        if applicable_timestamp != current_timestamp:
            rendering_event.wait()
            rendering_event_next.wait()
            current_timestamp = current_timestamp_Queue[0]
            index = {}
            index_ = render_index(DRG[current_timestamp], DRG[next_timestamp_Queue[0]]).encode()
            index['index'] = index_
            etag = md5(index_).hexdigest()
            index['etag'] = etag
            index_Queue.append(index)
            index_Queue.pop(0)
            index_event.set()
        sleep(0.33)

def array_standard_missions(Biomes, biome_str, html):
    html += '<br>\n'
    url_biome = biome_str.replace(' ', '-')
    for mission in Biomes[biome_str]:
        fname = f'/png?img={url_biome}{str(mission["id"])}'
        html += f'<div class="mission-hover-zoom"><img title="{mission["CodeName"]}" class="mission" src="{fname}"></div>\n'
    return html
def array_standard_missions_next(Biomes, biome_str, html):
    html += '<br>\n'
    url_biome = biome_str.replace(' ', '-')
    for mission in Biomes[biome_str]:
        fname = f'/upcoming_png?img={url_biome}{str(mission["id"])}'
        html += f'<div class="mission-hover-zoom"><img title="{mission["CodeName"]}" class="mission" src="{fname}"></div>\n'
    return html
def array_dd_missions(dd_str, html):
    folder_name = dd_str.replace(' ', '_')
    html += f'<img class="dd-biome" src="/files/{folder_name}/dd_biome.png">\n<br>\n'
    stg_count = 0
    for i in range(3):
        stg_count += 1
        fname = str(stg_count)
        html += f'<div class="mission-hover-zoom"><img class="mission" title="Stage {fname}" src="/files/{folder_name}/{fname}.png"></div>\n'
    return html

def render_index(timestamp, next_timestamp):
    Biomes = timestamp['Biomes']
    next_Biomes = next_timestamp['Biomes']
    html = '''<!DOCTYPE html>
<html>
<head>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.4/jquery.min.js"></script>
<script src="/files/homepage.js"></script>
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
<div id=DAILYDEAL><div id="dailydealhead">NEW DAILY DEAL IN<br><span id="DailyDealcountdown"></span></div><img id="DailyDeal" class="daily_trade" src="/dailydeal"></div>
<button id="dailydealbutton">Click here to see Daily Deal</button><br>
<div id="missionscountdown">NEW MISSIONS IN<br>
<span id="countdown"></span></div><button id="slideButton">Hide countdown</button><br>
<button id="currentButton">Click here to see upcoming missions</button>
</div>


<div id="current">\n'''
    html += '''<div class="grid-container">
<h2>
<div class="biome-container">
<img title="Glacial Strata" class="image-container" src="/files/DeepDive_MissionBar_GlacialStrata.png">\n'''
    if 'Glacial Strata' not in Biomes.keys():
        html += '<br><span class="scanners">// SCANNERS OUT OF RANGE \\\\</span>\n'
    else:
        html = array_standard_missions(Biomes, 'Glacial Strata', html)
    html += '''</div>
</h2>

<h2>
<div class="biome-container">
<img title="Crystalline Caverns" class="image-container" src="/files/DeepDive_MissionBar_CrystalCaves.png">\n'''
    if 'Crystalline Caverns' not in Biomes.keys():
        html += '<br><span class="scanners">// SCANNERS OUT OF RANGE \\\\</span>\n'
    else:
        html = array_standard_missions(Biomes, 'Crystalline Caverns', html)
    html += '''</div>
</h2>

<h2>
<div class="biome-container">
<img title="Salt Pits" class="image-container" src="/files/DeepDive_MissionBar_SaltPits.png">\n'''
    if 'Salt Pits' not in Biomes.keys():
        html += '<br><span class="scanners">// SCANNERS OUT OF RANGE \\\\</span>\n'
    else:
        html = array_standard_missions(Biomes, 'Salt Pits', html)
    html += '''</div>
</h2>

<h2>
<div class="biome-container">
<img title="Magma Core" class="image-container" src="/files/DeepDive_MissionBar_MagmaCore.png">\n'''
    if 'Magma Core' not in Biomes.keys():
        html += '<br><span class="scanners">// SCANNERS OUT OF RANGE \\\\</span>\n'
    else:
        html = array_standard_missions(Biomes, 'Magma Core', html)
    html += '''</div>
</h2>

<h2>
<div class ="biome-container">
<img title="Azure Weald" class="image-container" src="/files/DeepDive_MissionBar_AzureWeald.png">\n'''
    if 'Azure Weald' not in Biomes.keys():
        html += '<br><span class="scanners">// SCANNERS OUT OF RANGE \\\\</span>\n'
    else:
        html = array_standard_missions(Biomes, 'Azure Weald', html)
    html += '''</div>
</h2>

<h2>
<div class="biome-container">
<img title="Sandblasted Corridors" class="image-container" src="/files/DeepDive_MissionBar_Sandblasted.png">\n'''
    if 'Sandblasted Corridors' not in Biomes.keys():
        html += '<br><span class="scanners">// SCANNERS OUT OF RANGE \\\\</span>\n'
    else:
        html = array_standard_missions(Biomes, 'Sandblasted Corridors', html)
    html += '''</div>
</h2>

<h2>
<div class="biome-container">
<img title="Fungus Bogs" class="image-container" src="/files/DeepDive_MissionBar_FungusBogs.png">\n'''
    if 'Fungus Bogs' not in Biomes.keys():
        html += '<br><span class="scanners">// SCANNERS OUT OF RANGE \\\\</span>\n'
    else:
        html = array_standard_missions(Biomes, 'Fungus Bogs', html)
    html += '''</div>
</h2>

<h2>
<div class="biome-container">
<img title="Radioactive Exclusion Zone" class="image-container" src="/files/DeepDive_MissionBar_Radioactive.png">\n'''
    if 'Radioactive Exclusion Zone' not in Biomes.keys():
        html += '<br><span class="scanners">// SCANNERS OUT OF RANGE \\\\</span>\n'
    else:
        html = array_standard_missions(Biomes, 'Radioactive Exclusion Zone', html)
    html += '''</div>
</h2>

<h2>
<div class="biome-container">
<img title="Dense Biozone" class="image-container" src="/files/DeepDive_MissionBar_LushDownpour.png">\n'''
    if 'Dense Biozone' not in Biomes.keys():
        html += '<br><span class="scanners">// SCANNERS OUT OF RANGE \\\\</span>\n'
    else:
        html = array_standard_missions(Biomes, 'Dense Biozone', html)
    html += '''</div>
</h2>

<h2>
<div class="biome-container">
<img title="Hollow Bough" class="image-container" src="/files/DeepDive_MissionBar_HollowBough.png">\n'''
    if 'Hollow Bough' not in Biomes.keys():
        html += '<br><span class="scanners">// SCANNERS OUT OF RANGE \\\\</span>\n'
    else:
        html = array_standard_missions(Biomes, 'Hollow Bough', html)
    html += '''</div>
</h2>
</div>
</div>



'''
    html += '''<div id="upcoming" style="visibility: hidden;">
<div class="grid-container">
<h2>
<div class="biome-container">
    <img title="Glacial Strata" class="image-container" src="/files/DeepDive_MissionBar_GlacialStrata.png">\n'''
    if 'Glacial Strata' not in next_Biomes.keys():
        html += '<br><span class="scanners">// SCANNERS OUT OF RANGE \\\\</span>\n'
    else:
        html = array_standard_missions_next(next_Biomes, 'Glacial Strata', html)
    html += '''</div>
</h2>

<h2>
<div class="biome-container">
<img title="Crystalline Caverns" class="image-container" src="/files/DeepDive_MissionBar_CrystalCaves.png">\n'''
    if 'Crystalline Caverns' not in next_Biomes.keys():
        html += '<br><span class="scanners">// SCANNERS OUT OF RANGE \\\\</span>\n'
    else:
        html = array_standard_missions_next(next_Biomes, 'Crystalline Caverns', html)
    html += '''</div>
</h2>

<h2>
<div class="biome-container">
<img title="Salt Pits" class="image-container" src="/files/DeepDive_MissionBar_SaltPits.png">\n'''
    if 'Salt Pits' not in next_Biomes.keys():
        html += '<br><span class="scanners">// SCANNERS OUT OF RANGE \\\\</span>\n'
    else:
        html = array_standard_missions_next(next_Biomes, 'Salt Pits', html)
    html += '''</div>
</h2>

<h2>
<div class="biome-container">
<img title="Magma Core" class="image-container" src="/files/DeepDive_MissionBar_MagmaCore.png">\n'''
    if 'Magma Core' not in next_Biomes.keys():
        html += '<br><span class="scanners">// SCANNERS OUT OF RANGE \\\\</span>\n'
    else:
        html = array_standard_missions_next(next_Biomes, 'Magma Core', html)
    html += '''</div>
</h2>
<h2>
<div class="biome-container">
<img title="Azure Weald" class="image-container" src="/files/DeepDive_MissionBar_AzureWeald.png">\n'''
    if 'Azure Weald' not in next_Biomes.keys():
        html += '<br><span class="scanners">// SCANNERS OUT OF RANGE \\\\</span>\n'
    else:
        html = array_standard_missions_next(next_Biomes, 'Azure Weald', html)
    html += '''</div>
</h2>

<h2>
<div class="biome-container">
<img title="Sandblasted Corridors" class="image-container" src="/files/DeepDive_MissionBar_Sandblasted.png">\n'''
    if 'Sandblasted Corridors' not in next_Biomes.keys():
        html += '<br><span class="scanners">// SCANNERS OUT OF RANGE \\\\</span>\n'
    else:
        html = array_standard_missions_next(next_Biomes, 'Sandblasted Corridors', html)
    html += '''</div>
</h2>

<h2>
<div class="biome-container">
<img title="Fungus Bogs" class="image-container" src="/files/DeepDive_MissionBar_FungusBogs.png">\n'''
    if 'Fungus Bogs' not in next_Biomes.keys():
        html += '<br><span class="scanners">// SCANNERS OUT OF RANGE \\\\</span>\n'
    else:
        html = array_standard_missions_next(next_Biomes, 'Fungus Bogs', html)
    html += '''</div>
</h2>

<h2>
<div class="biome-container">
<img title="Radioactive Exclusion Zone" class="image-container" src="/files/DeepDive_MissionBar_Radioactive.png">\n'''
    if 'Radioactive Exclusion Zone' not in next_Biomes.keys():
        html += '<br><span class="scanners">// SCANNERS OUT OF RANGE \\\\</span>\n'
    else:
        html = array_standard_missions_next(next_Biomes, 'Radioactive Exclusion Zone', html)
    html += '''</div>
</h2>

<h2>
<div class="biome-container">
<img title="Dense Biozone" class="image-container" src="/files/DeepDive_MissionBar_LushDownpour.png">\n'''
    if 'Dense Biozone' not in next_Biomes.keys():
        html += '<br><span class="scanners">// SCANNERS OUT OF RANGE \\\\</span>\n'
    else:
        html = array_standard_missions_next(next_Biomes, 'Dense Biozone', html)
    html += '''</div>
</h2>

<h2>
<div class="biome-container">
<img title="Hollow Bough" class="image-container" src="/files/DeepDive_MissionBar_HollowBough.png">\n'''
    if 'Hollow Bough' not in next_Biomes.keys():
        html += '<br><span class="scanners">// SCANNERS OUT OF RANGE \\\\</span>\n'
    else:
        html = array_standard_missions_next(next_Biomes, 'Hollow Bough', html)

    html += '''</div>
</h2>
</div>
</div>


<div class="grid-container">
<div class="dd-container">
<h2>
<img class="image-container" src="/files/dd.png">\n'''
    html = array_dd_missions('Deep Dive Normal', html)
    html += '''</h2>
</div>
<div class="dd-container">
<h2>
<img class="image-container" src="/files/edd.png">\n'''
    html = array_dd_missions('Deep Dive Elite', html)
    html += '''</h2>
</div>
</div>


<div>
<div class="ddscountdown">NEW DEEP DIVES IN</div>
<span id="ddcountdown"></span>
<hr>
</div>
<div class="jsonc">
<div class="jsonlinks"><span style="color: white;font-size: 30px;font-family: BebasNeue, sans-serif;"> <a class="jsonlink" href="/json?data=current">CURRENT MISSION DATA</a> | <a class="jsonlink" href="/json?data=next">UPCOMING MISSION DATA</a> | <a class="jsonlink" href="/json?data=DD">CURRENT DEEP DIVE DATA</a> | <a class="jsonlink" href="/json?data=dailydeal">CURRENT DAILY DEAL DATA</a> | <a class="jsonlink" href="/xp_calculator">CLASS XP CALCULATOR</a> | <a class="jsonlink" href="https://github.com/rolfosian/drgmissions/">GITHUB</a></span> </div>
<span class="credits">Send credits (eth): 0xb9c8591A80A3158f7cFFf96EC3c7eA9adB7818E7</span></div>
<p class='gsgdisclaimer'><i>This website is a third-party platform and is not affiliated, endorsed, or sponsored by Ghost Ship Games. The use of Deep Rock Galactic's in-game assets on this website is solely for illustrative purposes and does not imply any ownership or association with the game or its developers. All copyrights and trademarks belong to their respective owners. For official information about Deep Rock Galactic, please visit the official Ghost Ship Games website.</i></p></div>
</body>
</html>'''
    return html

#CLASS XP CALCULATOR
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
    def __init__(self):
        self.xp = 0
        self.level = 0
        self.promotions = 0
        self.total_level = 0   
    def calculate_class_xp(self, levels):
        self.xp = levels[self.level] + (self.promotions * 315000)
        self.total_level = self.level + (self.promotions * 25)

#-----------------------------------------------------------------------------
