from PIL import Image, ImageDraw, ImageFont
import hashlib

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
        digit2_x, digit2_y = calc_text_center(BUBBLE.width, BUBBLE.height, digit2, font, font_size)
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
    ##mission = {'rendered_mission': BACKGROUND, 'CodeName': m_d['CodeName'], 'id': m_d['id']}
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


#deal_dict = {"ChangePercent": 225.62124633789, "DealType": "Sell", "Credits": 42069, "ResourceAmount": 78, "Resource": "Enor Pearl"}
#render_dailydeal(deal_dict)

#m_d = {"CodeName":" ","Complexity":"2","Length":"2","MissionWarnings":["Lithophage Outbreak","Lethal Enemies"],"MissionMutator":"Double XP","PrimaryObjective":"Salvage Operation","SecondaryObjective":"Mine Morkite","id":654}
#render_dd_stage(m_d)

#m_d = {"CodeName":" ","Complexity":"2","Length":"2","MissionWarnings":["Lithophage Outbreak","Lethal Enemies"],"MissionMutator":"Double XP","PrimaryObjective":"Salvage Operation","SecondaryObjective":"Hollomite","id":654}
#render_mission(m_d)

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
    etag = hashlib.md5(index['index']).hexdigest()
    index['etag'] = etag
    return index