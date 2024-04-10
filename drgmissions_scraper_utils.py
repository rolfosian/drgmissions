from datetime import datetime, timedelta
import subprocess
import time
import psutil
import os
import requests
import winreg
import json
import re
import threading
import random
#Validation
#-----------------------
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

def order_dictionary_by_date_FIRST_KEY_ROUNDING(dictionary):    
    sorted_keys = sorted(dictionary.keys(), key=lambda x: datetime.fromisoformat(x.replace('Z', '')))
    
    first_key = sorted_keys[0]
    first_key_minutes = int(first_key[14:16])
    if first_key_minutes >= 30:
        new_key = first_key[:14] + '30' + first_key[16:]
        dictionary[new_key] = dictionary[first_key]
        sorted_keys[0] = new_key
    else:
        new_key = first_key[:14] + '00' + first_key[16:]
        dictionary[new_key] = dictionary[first_key]
        sorted_keys[0] = new_key
    
    ordered_dictionary = {}
    for key in sorted_keys:
        ordered_dictionary[key] = dictionary[key]
    return ordered_dictionary

def reconstruct_dictionary(dictionary):
    god = {}
    mission_key_order = ['PrimaryObjective', 'SecondaryObjective', 'MissionWarnings', 'MissionMutator', 'Complexity', 'Length', 'CodeName', 'id']
    biome_order = ['Glacial Strata', 'Crystalline Caverns', 'Salt Pits', 'Magma Core', 'Azure Weald', 'Sandblasted Corridors', 'Fungus Bogs', 'Radioactive Exclusion Zone', 'Dense Biozone', 'Hollow Bough']
    for timestamp, seasons_dict in dictionary.items():
        god[timestamp] = {}
        for season, master in seasons_dict.items():
            god[timestamp][season] = {}
            master = sort_dictionary(master, ['Biomes', 'timestamp'])
            for key, value in master.items():
                if key == 'Biomes':
                    value = sort_dictionary(value, biome_order)
                    for biome, missions in value.items():
                        missions1 = []
                        for mission in missions:
                            mission1 = mission
                            if 'MissionWarnings' in mission.keys():
                                for missionkey, missionvalue in mission.items():
                                    if isinstance(missionvalue, list):
                                        mission1[missionkey] = sorted(missionvalue)
                            mission1 = sort_dictionary(mission1, mission_key_order)
                            missions1.append(mission1)
                        value[biome] = missions1

                god[timestamp][season][key] = value
    return god

def find_missing_timestamps(dictionary, invalid_keys):
    timestamps = [datetime.fromisoformat(timestamp[:-1]) for timestamp in dictionary.keys()]
    expected_diff = timedelta(minutes=30)
    missing_timestamps = []
    
    for i in range(len(timestamps) - 1):
        while timestamps[i + 1] - timestamps[i] > expected_diff:
            missing_timestamps.append(timestamps[i] + expected_diff)
            timestamps[i] += expected_diff
    if missing_timestamps:
        print('Missing timestamps found:')
        for timestamp in missing_timestamps:
            print(timestamp)
            invalid_keys.append((f'{timestamp.isoformat()}Z', find_missing_timestamps.__name__))
    else:
        print('No missing timestamps found.')

def find_duplicates(dictionary, invalid_keys):
    god = {}
    for key, value in dictionary.items():
        god[key] = json.dumps(value)
    def find_duplicate_strings(dictionary):
        string_count = {}
        for key, value in dictionary.items():
            if value in string_count:
                string_count[value].append(key)
            else:
                string_count[value] = [key]
        duplicate_strings = {value: keys for value, keys in string_count.items() if len(keys) > 1}
        return duplicate_strings
    
    duplicate_strings = find_duplicate_strings(god)
    if duplicate_strings:
        print("Duplicate strings found:")
        for value, keys in duplicate_strings.items():
            print("Keys:", keys)
            for key in keys:
                if key not in invalid_keys:
                    invalid_keys.append((key, find_duplicates.__name__))
    else:
        print("No duplicate strings found.")

def check_sum_of_missions(dictionary, invalid_keys):
    missions_keys = []
    for timestamp, seasons_dict in dictionary.items():
        for season, master in seasons_dict.items():
            mission_count = 0
            biomes = []
            for biome, missions in master['Biomes'].items():
                mission_count += len(missions)
            if mission_count not in [19, 20, 21, 22, 23, 24]:
                missions_keys.append(timestamp)
                if timestamp not in invalid_keys:
                    invalid_keys.append((timestamp, check_sum_of_missions.__name__))
    if missions_keys:
        print('Invalid number of missions in:')
        for key in missions_keys:
            print(f'Key:{key}')
    else:
        print('No sum of missions outside range.')
        
def check_missions_keys(dictionary, invalid_keys):
    missions_keys = []
    for timestamp, seasons_dict in dictionary.items():
        for season, master in seasons_dict.items():
            biomes = []
            for biome, missions in master['Biomes'].items():
                for mission in missions:
                    key_count = len(list(mission.keys()))
                    if key_count not in [6, 7, 8]:
                        missions_keys.append(f'{key}: {biome}')
                        if timestamp not in invalid_keys:
                            invalid_keys.append((timestamp, check_missions_keys.__name__))
    if missions_keys:
        print('Invalid number of keys in:')
        for key in missions_keys:
            print(f'Key:{key}')
    else:
        print('No sum of missions keys outside range.')

def check_missions_length_complexity(dictionary, invalid_keys):
    missions_keys = []
    for timestamp, seasons_dict in dictionary.items():
        for season, master in seasons_dict.items():
            biomes = []
            for biome, missions in master['Biomes'].items():
                biomes.append(biome)
            for biome in biomes:
                for mission in master['Biomes'][biome]:
                    if mission['Complexity'] == 'Indefinite' or mission['Length'] == 'Indefinite':
                        missions_keys.append(f'{timestamp}: {biome}')
                        if timestamp not in invalid_keys:
                            invalid_keys.append((timestamp, check_missions_length_complexity.__name__))
    if missions_keys:
        print('Indefinite complexity or length for mission(s) in:')
        for key_biome in missions_keys:
            print(f'Key and Biome: {key_biome}')
    else:
        print('No indefinite complexities or lengths found.')
#------------------------------------------------------------------------------------------------------

def upload_file(url, file_path, bearer_token):
    headers = {
        'Authorization': 'Bearer ' + bearer_token
    }

    with open(file_path, 'rb') as file:
        files = {'file': file}
        response = requests.post(url, headers=headers, files=files)
    return response

def wait_until_next_hour():
    now = datetime.now()
    if now.hour == 23:
        next_hour = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    else:
        next_hour = now.replace(hour=now.hour + 1, minute=0, second=0, microsecond=0)
    time_to_wait = (next_hour - now).total_seconds()
    time.sleep(time_to_wait + 1)
        
def kill_process_by_name_starts_with(start_string):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'].startswith(start_string):
            print(f"Terminating process: {proc.info['name']} (PID: {proc.info['pid']})")
            proc.kill()
            
def enable_system_time():
    try:
        print('-------------------------------------------------------------------------')
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\\CurrentControlSet\\Services\\W32Time\\Parameters', 0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, 'Type', 0, winreg.REG_SZ, 'NTP')
        winreg.CloseKey(key)
        subprocess.run(['sc', 'config', 'w32time', 'start=', 'auto'], shell=True)
        subprocess.run(['net', 'start', 'w32time'], shell=True)
        time.sleep(2)
        subprocess.run(['w32tm', '/resync'], stderr=subprocess.PIPE, shell=True)
        print("Automatic system time enabled.\n-------------------------------------------------------------------------\n")
    except Exception as e:
        print(f"Error: {e}")
def disable_system_time():
    try:
        print('-------------------------------------------------------------------------')
        output = subprocess.check_output('sc query w32time', stderr=subprocess.PIPE, shell=True).decode('utf-8')
        if 'RUNNING' in output:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\\CurrentControlSet\\Services\\W32Time\\Parameters', 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, 'Type', 0, winreg.REG_SZ, 'NoSync')
            winreg.CloseKey(key)
            subprocess.run(['sc', 'config', 'w32time', 'start=', 'disabled'], shell=True)
            subprocess.run(['net', 'stop', 'w32time'], shell=True)
            print("Automatic system time disabled.\n-------------------------------------------------------------------------\n")
    except Exception as e:
        print(f"Error: {e}")
def toggle_system_time():
    try:
        output = subprocess.check_output('sc query w32time', stderr=subprocess.PIPE, shell=True).decode('utf-8')
        if 'RUNNING' in output:
            disable_system_time()
        else:
            enable_system_time()        
    except Exception as e:
        print(f"Error {e}")
        
def format_seconds(seconds):
    timedelta_ = timedelta(seconds=seconds)
    hours = int(timedelta_.total_seconds() // 3600)
    minutes = int((timedelta_.total_seconds() % 3600) // 60)
    remaining_seconds = timedelta_.total_seconds() % 60
    formatted_time = "{:02d}:{:02d}:{:05.2f}".format(hours, minutes, remaining_seconds)
    return formatted_time

def calculate_average_float(float_list):
    total = 0.0
    count = 0
    for num in float_list:
        total += num
        count += 1
    if count == 0:
        return 0.0
    average = total / count
    return round(average, 2)

def sanitize_datetime(datetime_str):
    year, month, day, hour, min, sec = map(int, datetime_str[:10].split("-") + datetime_str[11:19].split(":"))
    sanitized_datetime = "{:02d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(day, month, year %100, hour, min, sec)
    return sanitized_datetime

def reverse_date_format(input_date):
    year, month, day = input_date.split('-')
    input_date = f"{day}-{month}-{year[2:]}"
    return input_date

def user_input_set_target_date(current_time):
    while True:
        user_input = input("Enter the target date (YYYY-MM-DD): ")
        try:
            user_date = datetime.strptime(user_input, "%Y-%m-%d")
            if user_date > current_time:
                break
            else:
                print("Please enter a date and time ahead of the current time.")
        except Exception:
            print("Invalid date format. Please enter the date in the format (YYYY-MM-DD).")
    return user_date

def yes_or_no(prompt):
    while True:
        response = input(prompt).strip().lower()
        if response == 'y':
            return True
        elif response == 'n':
            return False
        else:
            print("Please enter 'Y' or 'N'.")

def validate_drgmissions(DRG, patched):
    DRG = order_dictionary_by_date(DRG)
    DRG = reconstruct_dictionary(DRG)
    
    invalid_keys = []
    find_missing_timestamps(DRG, invalid_keys)
    check_missions_keys(DRG, invalid_keys)
    find_duplicates(DRG, invalid_keys)
    check_sum_of_missions(DRG, invalid_keys)   
    check_missions_length_complexity(DRG, invalid_keys)
    
    if invalid_keys:
        print('Invalid timestamps found...')
        with open('invalid_timestamps_log.txt', 'w') as f:
            s = ''
            for key, func in invalid_keys:
                s += f'{key} found invalid using {func} function\n'
            f.write(s)
            f.close()
            
        patched = True
        
        disable_system_time()
        print('\nPatching invalid timestamps...')

        with open('invalid_keys.txt', 'w') as f:
            filestr = ''
            for key, func_name in invalid_keys:
                filestr += f'{key}\n'
            f.write(filestr.strip())
            f.close()

        with open('./mods/mods.txt', 'w') as f:
            f.write('invalid_timestamps_redoer : 1')
            f.close()
        
        subprocess.Popen(['start', 'steam://run/548430//'], shell=True)
        files = []
        timeout_seconds = (len(invalid_keys) * 1.9) + 120
        estimated_time_completion = (len(invalid_keys) *1.7) + 30
        start_time = time.monotonic()
        while True:
            elapsed_time = time.monotonic() - start_time
            print(f'{format_seconds(timeout_seconds-elapsed_time)} until timeout. Estimated time until completion: {format_seconds(estimated_time_completion-elapsed_time)}', end="\r")

            if time.monotonic() - start_time > timeout_seconds:
                print('TIMEOUT, GAME FROZE OR CRASHED. RESTARTING')
                kill_process_by_name_starts_with('FSD')
                kill_process_by_name_starts_with('Unreal')
                time.sleep(4)
                subprocess.Popen(['start', 'steam://run/548430//'], shell=True)
                start_time = time.monotonic()
            for filename in os.listdir():
                if filename == 'redonemissions.json':
                    time.sleep(5)
                    files.append(filename)
                    kill_process_by_name_starts_with('FSD')
                    kill_process_by_name_starts_with('Unreal')
            if files:
                print(f'Estimated time until completion: {format_seconds(0.00)}')
                print(f'\n---\nElapsed time: {format_seconds(elapsed_time)}               \n---')
                break
            time.sleep(0.1)
            
        with open('redonemissions.json', 'r') as f:
            redone_missions = f.read()
            redone_missions = re.sub(r':\d{2}Z', ':00Z', redone_missions)
            redone_missions = json.loads(redone_missions)
            f.close()
        
        for timestamp, dict in redone_missions.items():
            DRG[timestamp] = dict

        DRG = order_dictionary_by_date(DRG)
        DRG = reconstruct_dictionary(DRG)

        with open('./mods/mods.txt', 'w') as f:
            f.close()
        enable_system_time()
        os.remove('invalid_keys.txt')
        os.remove('redonemissions.json')

        return validate_drgmissions(DRG, patched)
    
    print('No invalid timestamps found.')
    return DRG, patched

# def poll_file_modification_rate(file_path, list_, total_increments):
#     last_modification_time = os.path.getmtime(file_path)
#     count = None
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

# list_ = []
# file_path = 'C:\\example.json'
# total_increments = 3941
# thread = threading.Thread(target=poll_file_modification_rate, args=(file_path, list_))
# thread.start()

# while not list_:
#     continue
# count = 0
# while True:
#     estimated_time_remaining = list_[0]
#     print(estimated_time_remaining)
#     time.sleep(1)
#     count += random.randint(1, 4)
#     with open('C:\\example.json', 'w') as f:
#         f.write(count)