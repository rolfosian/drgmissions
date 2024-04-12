import json
import shutil
import os
from datetime import datetime, timedelta
from hashlib import md5

def extract_days_from_json(data, num_days):
    timestamps = {datetime.fromisoformat(key.replace('Z', '')): value for key, value in data.items()}
    current_datetime = datetime.utcnow()

    days_from_now = current_datetime + timedelta(days=num_days)
    relevant_days = {f"{str(key).replace(' ', 'T')}Z": value for key, value in timestamps.items() if current_datetime <= key < days_from_now}
    return relevant_days

def split_json(num_days, bs):
    shutil.rmtree('./static/json/bulkmissions')
    os.mkdir('./static/json/bulkmissions')
    DRG = extract_days_from_json(bs, num_days)
    
    for timestamp, dictionary in (DRG.items()):
        fname = timestamp.replace(':','-')
        with open(f'./static/json/bulkmissions/{fname}.json', 'w') as f:
            f.write(json.dumps(dictionary))
            f.close()

def round_time_down(datetime_string):
    datetime_minutes = int(datetime_string[14:16])
    if datetime_minutes >= 30:
        new_datetime = datetime_string[:14] + '30:00Z'
    else:
        new_datetime = datetime_string[:14] + '00:00Z'
    return new_datetime

def flatten_seasons(DRG):
    combined_biomes = {}
    missions_count = 0
    missions_per_season = {}
    for season in list(DRG.items())[1][1].keys():
        missions_per_season[season] = 0
        
    for timestamp, seasons_dict in DRG.items():
        combined_biomes[timestamp] = {}
        combined_biomes[timestamp]['timestamp'] = timestamp
        combined_biomes[timestamp]['Biomes'] = {biome : [] for biome in seasons_dict['s0']['Biomes'].keys()}
        combined_missions = []
        for season, season_dict  in seasons_dict.items():
            for biome, missions in season_dict['Biomes'].items():
                
                for mission in missions:
                    id = mission['id']
                    del mission['id']
                    md5_ = md5(json.dumps(mission).encode()).hexdigest()
                    mission['id'] = id
                    mission['season'] = season
                    
                    combined_missions.append((timestamp, season, biome, mission, md5_))
                    missions_count += 1
                    missions_per_season[season] += 1
                        
        combined_biomes[timestamp]['Biomes'][biome] = sorted(combined_missions, key=lambda x: x[1])

    amount_of_timestamps = len(list(DRG.keys()))
    
    # print(missions_per_season['s0'])
    # missions_per_timestamp = missions_per_season['s0'] / amount_of_timestamps
    # print(missions_per_timestamp)
    
    # print(missions_per_season['s4'])
    # missions_per_timestamp = missions_per_season['s4'] / amount_of_timestamps
    # print(missions_per_timestamp)
    
    # print(missions_count)
    missions_count = 0

    god = {}
    for timestamp, biomes in combined_biomes.items():
        god[timestamp] = {}
        god[timestamp]['Biomes'] = {}
        god[timestamp]['timestamp'] = timestamp
        md5s = []
        
        for biome, missions in biomes['Biomes'].items():
            god[timestamp]['Biomes'][biome] = []
            
            for timestamp_, season, biome, mission, mission_md5 in missions:
                if season == 's0':
                    md5s.append(timestamp+mission_md5)
                    god[timestamp_]['Biomes'][biome].append(mission)
                    missions_count += 1
                elif timestamp+mission_md5 in md5s:
                    continue
                else:
                    god[timestamp_]['Biomes'][biome].append(mission)
                    missions_count += 1
    # print(missions_count)

    # missions_per_timestamp = missions_count / amount_of_timestamps
    # print(missions_per_timestamp)
    
    # for b, ms in bs.items():
    #     print(b)
    #     for m in ms:
    #         print(json.dumps(m, indent=4))
    

    return god

def find_duplicates(dict_list, ignore_keys):
    for i, dict1 in enumerate(dict_list):
        for dict2 in dict_list[i+1:]:
            if all(dict1.get(k) == dict2.get(k) for k in dict1 if k not in ignore_keys):
                return True
    return False


with open('drgmissionsgod.json', 'r') as f:
    DRG = json.load(f)

flat_or_not = input('Flat or not: ')
if flat_or_not.lower() == 'flat':
    DRG, bs = flatten_seasons(DRG)  

split_json(7, DRG)
bs = DRG[round_time_down(datetime.utcnow().isoformat())]
fname = round_time_down(datetime.utcnow().isoformat()).replace(':', '-')
with open (f'./static/json/bulkmissions/{fname}.json', 'w') as f:
    json.dump(bs, f)

# def poll_file_modification_rate(file_path, list_, total_increments):
#     last_modification_time = os.path.getmtime(file_path)
#     time_per_count_list = []
    
#     while True:
#         current_modification_time = os.path.getmtime(file_path)
#         list_.append(current_modification_time)
#         time_difference = current_modification_time - last_modification_time
#         time_per_count_list.append(time_difference)
        
#         if current_modification_time != last_modification_time:
#             with open(file_path, 'r') as f:
#                 remaining_count = total_increments - int(f.read().strip())
#                 average_time_per_count = sum(time_per_count_list) / len(time_per_count_list)
#                 estimated_time_remaining = average_time_per_count * remaining_count
#                 list_.pop(0)
#                 list_.append(estimated_time_remaining)
        
#         if time_difference > 10:
#             break

# import threading
# import time
# import random

# list_ = []
# file_path = 'C:\\example.json'
# total_increments = 3941
# thread = threading.Thread(target=poll_file_modification_rate, args=(file_path, list_))
# thread.start()

# count = 0
# while True:
#     estimated_time_remaining = list_[0]
#     print(estimated_time_remaining)
#     time.sleep(1)
#     count += random.randint(1, 4)
#     with open('C:\\example.json', 'w') as f:
#         f.write(count)