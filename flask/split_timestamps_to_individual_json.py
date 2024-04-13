import json
import shutil
import os
from datetime import datetime, timedelta
from hashlib import md5
from time import sleep



def split_json(num_days, bs):
    def extract_days_from_json(data, num_days):
        timestamps = {datetime.fromisoformat(key.replace('Z', '')): value for key, value in data.items()}
        current_datetime = datetime.utcnow()

        days_from_now = current_datetime + timedelta(days=num_days)
        relevant_days = {f"{str(key).replace(' ', 'T')}Z": value for key, value in timestamps.items() if current_datetime <= key < days_from_now}
        return relevant_days
    
    shutil.rmtree('./static/json/bulkmissions')
    os.mkdir('./static/json/bulkmissions')
    DRG = extract_days_from_json(bs, num_days)
    
    for timestamp, dictionary in (DRG.items()):
        fname = timestamp.replace(':','-')
        with open(f'./static/json/bulkmissions/{fname}.json', 'w') as f:
            f.write(json.dumps(dictionary))
            f.close()
            
def split_json_by_days(num_days, DRG):
    def extract_days_from_json(data, num_days):
        timestamps = {datetime.strptime(key): value for key, value in data.items()}
        current_datetime = datetime.utcnow()

        days_from_now = current_datetime + timedelta(days=num_days)
        relevant_days = {f"{key}": value for key, value in timestamps.items() if current_datetime <= key < days_from_now}
        return relevant_days
    shutil.rmtree('./static/json/bulkmissions')
    os.mkdir('./static/json/bulkmissions')
    DRG = group_json_by_days(DRG)
    DRG = extract_days_from_json(num_days, DRG)
    
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

# def extract_days_from_json(data, num_days):
#     timestamps = {datetime.strptime(key, '%Y-%m-%d'): value for key, value in data.items()}
#     current_datetime = datetime.utcnow()

#     days_from_now = current_datetime + timedelta(days=num_days)
#     relevant_days = {f"{key.strftime('%Y-%m-%d')}": value for key, value in timestamps.items() if current_datetime <= key < days_from_now}
#     return relevant_days

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

# with open('drgdailydeals.json', 'r') as f:
#     DRG = json.load(f)

# shutil.rmtree('./static/json/dailydeals')
# os.mkdir('./static/json/dailydeals')

# for timestamp, deal in DRG.items():
#     fname = timestamp.replace(':', '-')
#     with open(f'./static/json/dailydeals/{fname}.json', 'w') as f:
#         json.dump(deal, f)
        
# today = datetime.today()
# today_midnight = today.replace(hour=0, minute=0, second=0, microsecond=0)
# iso_timestamp = today_midnight.isoformat().replace(':', '-')+'Z'
# print(iso_timestamp)

with open('drgmissionsgod.json', 'r') as f:
    DRG = flatten_seasons(json.load(f))
    
days = group_json_by_days(DRG)
days = extract_days_from_json(days, 2)
if os.path.isdir('./static/json/bulkmissions'):
    shutil.rmtree('./static/json/bulkmissions')
os.mkdir('./static/json/bulkmissions')
for day, timestamp in days.items():
    path = f'./static/json/bulkmissions/{day}.json'
    with open(path, 'w') as f:
        json.dump(timestamp, f)

def rotate_jsons_days(DRG, num_days):
    days = group_json_by_days(DRG)
    days = extract_days_from_json(DRG, num_days)
    if os.path.isdir('./static/json/bulkmissions'):
        shutil.rmtree('./static/json/bulkmissions')
    os.mkdir('./static/json/bulkmissions')
    for day, timestamp in days.items():
        with open(f'./static/json/bulkmissions/{day}.json') as f:
            json.dump(timestamp, f)
            
    while True:
        sleep(num_days*86400-3600)
        days = group_json_by_days(DRG)
        days = extract_days_from_json(days, num_days)
        if os.path.isdir('./static/json/bulkmissions'):
            shutil.rmtree('./static/json/bulkmissions')
        os.mkdir('./static/json/bulkmissions')
        for day, timestamp in days.items():
            with open(f'./static/json/bulkmissions/{day}.json') as f:
                json.dump(timestamp, f)
        
    

# flat_or_not = input('Flat or not: ')
# if flat_or_not.lower() == 'flat':
#     DRG, bs = flatten_seasons(DRG)  

# split_json(7, DRG)
# bs = DRG[round_time_down(datetime.utcnow().isoformat())]
# fname = round_time_down(datetime.utcnow().isoformat()).replace(':', '-')
# with open (f'./static/json/bulkmissions/{fname}.json', 'w') as f:
#     json.dump(bs, f)

# for week, timestamp in weeks.items():
#     encoded_string = json.dumps(timestamp).encode("utf-8")

#     # Get the size of the encoded bytes
#     size_in_bytes = len(encoded_string)

#     # Convert bytes to kilobytes
#     size_in_kb = size_in_bytes / 1024

#     print("Size in bytes:", size_in_bytes)
#     print("Size in kilobytes:", size_in_kb)
#     break

# for day, timestamp in days.items():
#     encoded_string = json.dumps(timestamp).encode("utf-8")

#     # Get the size of the encoded bytes
#     size_in_bytes = len(encoded_string)

#     # Convert bytes to kilobytes
#     size_in_kb = size_in_bytes / 1024

#     # print("Size in bytes:", size_in_bytes)
#     print("Size in kilobytes:", size_in_kb)




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

