import json
import shutil
import os
from datetime import datetime, timedelta

def split_json_raw(DRG):
    if os.path.isdir('./static/json/bulkmissions'):
        shutil.rmtree('./static/json/bulkmissions')
        os.mkdir('./static/json/bulkmissions')
    
    for timestamp, dictionary in DRG.items():
        fname = timestamp.replace(':','-')
        with open(f'./static/json/bulkmissions/{fname}.json', 'w') as f:
            json.dump(dictionary, f)

def split_json(num_days, DRG):
    def extract_days_from_json(data, num_days):
        timestamps = {datetime.fromisoformat(key.replace('Z', '')): value for key, value in data.items()}
        current_datetime = datetime.utcnow()

        days_from_now = current_datetime + timedelta(days=num_days)
        relevant_days = {f"{str(key).replace(' ', 'T')}Z": value for key, value in timestamps.items() if current_datetime <= key < days_from_now}
        return relevant_days
    shutil.rmtree('./static/json/bulkmissions')
    os.mkdir('./static/json/bulkmissions')
    
    bs = DRG[round_time_down(datetime.utcnow().isoformat())]
    DRG = extract_days_from_json(DRG, num_days)
    
    for timestamp, dictionary in (DRG.items()):
        fname = timestamp.replace(':','-')
        with open(f'./static/json/bulkmissions/{fname}.json', 'w') as f:
            json.dump(dictionary, f)

    fname = round_time_down(datetime.utcnow().isoformat()).replace(':', '-')
    with open (f'./static/json/bulkmissions/{fname}.json', 'w') as f:
        json.dump(bs, f)

def round_time_down(datetime_string):
    datetime_minutes = int(datetime_string[14:16])
    if datetime_minutes >= 30:
        new_datetime = datetime_string[:14] + '30:00Z'
    else:
        new_datetime = datetime_string[:14] + '00:00Z'
    return new_datetime

def flatten_seasons_new(DRG):
    def compare_dicts(dict1, dict2, ignore_keys):
        dict1_filtered = {k: v for k, v in dict1.items() if k not in ignore_keys}
        dict2_filtered = {k: v for k, v in dict2.items() if k not in ignore_keys}

        return dict1_filtered == dict2_filtered
    combined = {}
    missions_per_season = {}
    seasons = list(list(DRG.items())[1][1].keys())
    timestamps = list(DRG.keys())
    
    for season in seasons:
        missions_per_season[season] = 0
    missions_count = 0
    
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
                missions_per_season['s0'] += 1
                missions_count += 1
                
            combined[timestamp]['Biomes'][biome] = [mission for mission in missions]
        del DRG[timestamp]['s0']
    seasons.remove('s0')
    
    duplicates = []
    for timestamp in timestamps:
        for season in seasons:
            for biome, missions in DRG[timestamp][season]['Biomes'].items():
                for index, mission in enumerate(missions):
                    missions_per_season[season] += 1
                    missions_count += 1
                    mission['season'] = season
                    if mission['CodeName'] in combined[timestamp]['Biomes'][biome+'codenames']:
                        duplicates.append([timestamp, biome, mission])
                    else:
                        try:
                            combined[timestamp]['Biomes'][biome].insert(index, mission)
                        except:
                            combined[timestamp]['Biomes'][biome].append(mission)
    
    for timestamp, biome, dup_mission in duplicates:
        for season in seasons:
            for mission in combined[timestamp]['Biomes'][biome]:
                if dup_mission['CodeName'] != mission['CodeName']:
                    continue
                if compare_dicts(mission, dup_mission, ['season', 'id', 'season_modified']):
                    continue
                if 'season_modified' not in mission:
                    mission['season_modified'] = {}
                mission['season_modified'][season] = dup_mission
                missions_count -= 1
                
    # seasons.insert(0, 's0')
    # amount_of_timestamps = len(timestamps)
    # total_missions = 0
    # for season in seasons:
    #     print(f'\n{season}')
    #     print(missions_per_season[season])
    #     total_missions += missions_per_season[season]
    #     missions_per_timestamp = missions_per_season[season] / amount_of_timestamps
    #     print(missions_per_timestamp)
    #     print('---------')
    
    # print(missions_count)
    # print(total_missions)
    # missions_per_timestamp = missions_count / amount_of_timestamps
    # print(missions_per_timestamp)

    for timestamp in timestamps:
        for k in list(combined[timestamp]['Biomes'].keys()):
            if k.endswith('codenames'):
                del combined[timestamp]['Biomes'][k]

    return combined

#never used
def group_json_by_weeks(DRG):
    timestamps_dt = [datetime.fromisoformat(ts[:-1]) for ts in DRG.keys()]
    
    grouped_by_week = {}
    for timestamp in timestamps_dt:
        week_number = timestamp.isocalendar()[1]
        if week_number not in grouped_by_week:
            grouped_by_week[week_number] = {}
        timestamp = timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
        grouped_by_week[week_number][timestamp] = DRG[timestamp]
        
    return grouped_by_week

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

def split_daily_deals_json():
    with open('drgdailydeals.json', 'r') as f:
        AllTheDeals = json.load(f)
    
    dirpath = './static/json/dailydeals'
    if os.path.isdir(dirpath):
        shutil.rmtree(dirpath)
    os.mkdir(dirpath)

    for timestamp, deal in AllTheDeals.items():
        fname = timestamp.replace(':', '-')
        with open(f'./static/json/dailydeals/{fname}.json', 'w') as f:
            json.dump(deal, f)

def add_daily_deals_to_grouped_json(DRG):
    with open('drgdailydeals.json', 'r') as f:
        AllTheDeals = json.load(f)
    
        for timestamp, deal in AllTheDeals.items():
            deal[timestamp] = timestamp
            try:
                DRG[timestamp.split('T')[0]]['dailyDeal'] = deal
            except:
                continue
    return DRG

# def simpleHash(input):
#     hash = 0
#     for char in input:
#         charCode = ord(char)
#         hash = ((hash << 5) - hash) + charCode
#         hash &= 0xffffffff 
#     return hash if hash < 0x80000000 else hash - 0x100000000

# # hashes must be written before they are assigned to DRG dict
# def write_string_hashes(DRG):
#     hashes_dict = {}
#     for day, dictionary in DRG.items():
#         hash_ = simpleHash(json.dumps(dictionary))             
#         hashes_dict[day] = hash_
    
#     with open('drgmissionsdailyhashes.json', 'w') as f:
#         json.dump(hashes_dict, f)

# def add_string_hashes(DRG):
#     hashes_dict = {}
#     for day, dictionary in DRG.items():
#         hash_ = simpleHash(json.dumps(dictionary))             
#         DRG[day]['stringHash'] =  hash_
#         hashes_dict[day] = hash_
        
#     return DRG

def main():
    with open('drgmissionsgod.json', 'r') as f:
        DRG = json.load(f)
        
    flat_or_not = input('Flat or not: ')
    if flat_or_not.lower() == 'flat'  or flat_or_not.lower() == 'yes' or flat_or_not.lower() == 'y':
        DRG = flatten_seasons_new(DRG)

    days_or_not = input('Group by days or not: ')
    if days_or_not.lower() == 'days' or days_or_not.lower() == 'yes' or days_or_not.lower() == 'y':
        DRG = group_json_by_days(DRG)
        
        daily_deals_or_not = input('Daily deals or not: ')
        if daily_deals_or_not.lower() == 'yes' or daily_deals_or_not.lower() == 'y':
            DRG = add_daily_deals_to_grouped_json(DRG)
        
        num_days = int(input('Number of days: '))
        DRG = extract_days_from_json(DRG, num_days)

    else:
        days_or_not_ungrouped = input('Split by days (Ungrouped)?')
        if days_or_not_ungrouped.lower() == 'yes' or days_or_not_ungrouped.lower() == 'y':
            num_days = int(input('Amount of days to split (from the current date): '))
            split_json(num_days, DRG)
            return

    split_json_raw(DRG)

# main()

# with open('drgmissionsgod.json', 'r') as f:
#     DRG = json.load(f)

# DRG = flatten_seasons_new(DRG)
# DRG = group_json_by_days(DRG)
# DRG = add_daily_deals_to_grouped_json(DRG)
# DRG = extract_days_from_json(DRG, 300)
# print(len(list(DRG.keys())))