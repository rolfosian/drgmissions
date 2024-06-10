from datetime import datetime, timedelta
from functools import wraps
from ctypes import WinDLL
from copy import deepcopy
import subprocess
import time
import psutil
import os
import requests
import winreg
import json
import re
import threading

def cfg_():
    with open(os.getcwd()+'/scraper_cfg.json', 'r') as f:
        cfg = json.load(f)
    return cfg
cfg = cfg_()

def wrap_with_color(string, color):
    return f"\033[0;{color}m{string}\033[0m"

def subprocess_wrapper(command, shell=False, print_=True):
    def wrapper():
        event = threading.Event()
        event.set()
        process = subprocess.Popen(command, shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        def read_stdout(event, process, print_):
            if not print_:
                return
            while event.is_set():
                for line in process.stdout:
                    if line.endswith('\n'):
                        line = line[:-1]
                    print(line)

        stdout_thread = threading.Thread(target=read_stdout, args=(event, process, print_))
        stdout_thread.start()

        process.wait()

        event.clear()
        stdout_thread.join()
        try:
            return process.communicate()[0]
        except:
            return process.communicate()[1]
        
    return wrapper

def delete_file(filename):
    while True:
        try:
            os.remove(filename)
            break
        except:
            continue

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

def format_seconds(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    remaining_seconds = int(round(seconds % 60))
    if remaining_seconds == 60:
        minutes += 1
        remaining_seconds = 0
    formatted_time = "{:02d}:{:02d}:{:02d}".format(hours, minutes, remaining_seconds)
    return formatted_time

def maximize_window():
    user32 = WinDLL('user32')
    SW_MAXIMIZE = 3
    hWnd = user32.GetForegroundWindow()
    user32.ShowWindow(hWnd, SW_MAXIMIZE)
    
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
    for season, value in dictionary[sorted_keys[0]].items():
        value['timestamp'] = sorted_keys[0]
    
    ordered_dictionary = {}
    for key in sorted_keys:
        ordered_dictionary[key] = dictionary[key]
    return ordered_dictionary

def reconstruct_dictionary(dictionary):
    god = {}
    mission_key_order = ['PrimaryObjective', 'SecondaryObjective', 'MissionWarnings', 'MissionMutator', 'Complexity', 'Length', 'CodeName', 'id']
    biome_order = ['Glacial Strata', 'Crystalline Caverns', 'Salt Pits', 'Magma Core', 'Azure Weald', 'Sandblasted Corridors', 'Fungus Bogs', 'Radioactive Exclusion Zone', 'Dense Biozone', 'Hollow Bough']
    for timestamp, seasons_dict in dictionary.items():
        seasons_dict = sort_dictionary(seasons_dict, ['s0', 's1', 's2', 's3', 's4', 's5'])
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

def find_duplicate_seasons(dictionary, invalid_keys):
    def find_duplicate_strings(dictionary):
        strings = []
        keys = []
        for key, value in dictionary.items():
            if value in strings:
                keys.append(key)
            else:
                strings.append(value)
                
        if keys:
            return True
        return False
    dictionary_ = deepcopy(dictionary)
    
    god = {}
    invalid_keys_ = []
    for timestamp, seasons_dict in dictionary_.items():
        god[timestamp] = {}
        for season, master in seasons_dict.items():
            god[timestamp][season] = {'Biomes' : {} }
            for k, v in master.items():
                if k == 'Biomes':
                    for biome, missions in v.items():
                        for mission in missions:
                            del mission['id']
                        god[timestamp][season][k][biome] = missions
                else:
                    god[timestamp][season][k] = v
                            
            god[timestamp][season] = json.dumps(master)
            
        if find_duplicate_strings(god[timestamp]):
            if timestamp not in invalid_keys_:
                invalid_keys_.append((timestamp, find_duplicate_seasons.__name__))

    if invalid_keys_:
        print("Duplicate season data found:")
        for timestamp, func_name in invalid_keys_:
            print("Timestamp:", timestamp)
            if timestamp not in invalid_keys:
                invalid_keys.append((timestamp, func_name))
    else:
        print("No duplicate season data found.")

def find_duplicates(dictionary, invalid_keys):
    def is_not_longer_than_1_hour(datetime1, datetime2):
        time_difference = abs(datetime2 - datetime1)
        one_hour = timedelta(hours=1)
        
        if time_difference > one_hour:
            return False
        else:
            return True
    
    god = {}
    dictionary_ = deepcopy(dictionary)

    for timestamp, seasons_dict in dictionary_.items():
        for season, master in seasons_dict.items():
            del master['timestamp']
            for k, v in master.items():
                if k == 'Biomes':
                    for biome, missions in v.items():
                        for mission in missions:
                            try:
                                del mission['id']
                            except:
                                pass

    for key, value in dictionary_.items():
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
        print("Duplicate timestamps found:")
        for value, keys in duplicate_strings.items():
            print("Keys:", keys)
            datetime1 = datetime.strptime(keys[0], "%Y-%m-%dT%H:%M:%SZ")
            datetime2 = datetime.strptime(keys[1], "%Y-%m-%dT%H:%M:%SZ")

            if is_not_longer_than_1_hour(datetime1, datetime2):
                print('Found invalid')
                if key not in invalid_keys:
                    invalid_keys.append((keys[0], find_duplicates.__name__))
                    invalid_keys.append((keys[1], find_duplicates.__name__))
            else:
                print('Likely not invalid')

    else:
        print("No duplicate timestamps found.")

def check_sum_of_missions(dictionary, invalid_keys):
    missions_keys = []
    for timestamp, seasons_dict in dictionary.items():
        for master in seasons_dict.values():
            mission_count = 0
            for biome in master['Biomes']:
                mission_count += len(master['Biomes'][biome])
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
        for master in seasons_dict.values():
            for biome in master['Biomes']:
                for mission in master['Biomes'][biome]:
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

def check_missions_length_complexity(dictionary):
    missions_keys = []
    for timestamp, seasons_dict in dictionary.items():
        for master in seasons_dict.values():
            for biome in master['Biomes']:
                for mission in master['Biomes'][biome]:
                    if mission['Complexity'] == 'Indefinite' or mission['Length'] == 'Indefinite':
                        missions_keys.append((f'{timestamp}: {mission["CodeName"]}', f'{timestamp}:\n   {json.dumps(mission, indent=2)}\n'))

    if missions_keys:
        log = open('indefinite_lengths_complexities_log.txt', 'w')
        log.write('Indefinite complexity or length for mission(s) in:\n\n')
        print('Indefinite complexity or length for mission(s) in:')
        for timestamp_codename, timestamp_mission_json in missions_keys:
            log.write(f'{timestamp_mission_json}\n')
            print(f'{timestamp_codename}')
        log.close()
    else:
        print('No indefinite complexities or lengths found.')

def round_time_down(datetime_string):
    datetime_minutes = int(datetime_string[14:16])
    if datetime_minutes >= 30:
        new_datetime = datetime_string[:14] + '30:00Z'
    else:
        new_datetime = datetime_string[:14] + '00:00Z'
    return new_datetime

#------------------------------------------------------------------------------------------------------

def split_file(file_path, max_size):
    file_parts = []
    part_number = 1
    total_size = os.path.getsize(file_path)
    read_so_far = 0
    
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(max_size)
            if not chunk:
                break
            
            read_so_far += len(chunk)
            if read_so_far >= total_size:
                part_filename = f"{file_path}_{part_number}_last_part"
            else:
                part_filename = f"{file_path}_{part_number}_part"
                
            with open(part_filename, 'wb') as chunk_file:
                chunk_file.write(chunk)
                
            file_parts.append(part_filename)
            part_number += 1
    
    return file_parts

def upload_file(cfg, file_path):
    domain_name = cfg['domain_name']
    bearer_token = cfg['auth_token']
    max_body_size = cfg['max_body_size']
    is_reverse_proxy = cfg['is_reverse_proxy']
    
    protocol = 'http'
    if cfg['use_https']:
        protocol = 'https'
    if is_reverse_proxy:
        url = f'{protocol}://{domain_name}/upload'
    else:
        f"{protocol}://{cfg['service_bind']}/upload"
    
    headers = {
        'Authorization': 'Bearer ' + bearer_token
    }

    file_size = os.path.getsize(file_path)
    if file_size > max_body_size:
        file_parts = split_file(file_path, max_body_size)
    else:
        file_parts = [file_path]

    for part in file_parts:
        with open(part, 'rb') as file:
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
    
    while time_to_wait > 0:
        time_to_wait = (next_hour - datetime.utcnow()).total_seconds()
        print(f"Time to wait: {format_seconds(time_to_wait)}", end="\r")
        time.sleep(0.2)
        
    print(f"Time to wait: {format_seconds(0)}")

def wait_until_next_thursday_11am_utc():
    now = datetime.utcnow()
    
    days_until_thursday = (3 - now.weekday()) % 7
    
    next_thursday = now + timedelta(days=days_until_thursday)
    next_thursday_11am_utc = datetime(next_thursday.year, next_thursday.month, next_thursday.day, 11, 0, 0)
    
    if days_until_thursday == 0 and now.hour >= 11:
        next_thursday_11am_utc += timedelta(days=7)
    
    time_to_wait = (next_thursday_11am_utc - now).total_seconds()
    
    while time_to_wait > 0:
        time_to_wait = (next_thursday_11am_utc - datetime.utcnow()).total_seconds()
        print(f"Time to wait: {format_seconds(round(time_to_wait))}", end="\r")
        time.sleep(0.5)
    
    print(f"Time to wait: {format_seconds(0)}")

def get_previous_thursday_date():
    today = datetime.today()

    if today.weekday() == 3:
        previous_thursday = today
    else:
        days_to_subtract = (today.weekday() - 3) % 7
        previous_thursday = today - timedelta(days=days_to_subtract)

    return previous_thursday.date().isoformat()

def kill_process_by_name_starts_with(start_string):
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'].startswith(start_string):
                print(f"Terminating process: {proc.info['name']} (PID: {proc.info['pid']})")
                proc.kill()
    except:
        return

def enable_system_time():
    try:
        print('-------------------------------------------------------------------------', include_timestamp=False)
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\\CurrentControlSet\\Services\\W32Time\\Parameters', 0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, 'Type', 0, winreg.REG_SZ, 'NTP')
        winreg.CloseKey(key)
        subprocess_wrapper(['sc', 'config', 'w32time', 'start=', 'auto'], shell=True)()
        subprocess_wrapper(['net', 'start', 'w32time'], shell=True)()
        time.sleep(2)
        subprocess_wrapper(['w32tm', '/resync'], shell=True)()
        print("Automatic system time enabled.")
        print("-------------------------------------------------------------------------", include_timestamp=False)
    except Exception as e:
        print(f"Error: {e}")
def disable_system_time():
    try:
        print('-------------------------------------------------------------------------', include_timestamp=False)
        output = subprocess.check_output('sc query w32time', stderr=subprocess.PIPE, shell=True).decode('utf-8')
        if 'RUNNING' in output:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\\CurrentControlSet\\Services\\W32Time\\Parameters', 0, winreg.KEY_WRITE)
            winreg.SetValueEx(key, 'Type', 0, winreg.REG_SZ, 'NoSync')
            winreg.CloseKey(key)
            subprocess_wrapper(['sc', 'config', 'w32time', 'start=', 'disabled'], shell=True)()
            subprocess_wrapper(['net', 'stop', 'w32time'], shell=True)()
            print("Automatic system time disabled.")
            print("-------------------------------------------------------------------------", include_timestamp=False)
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
    find_duplicate_seasons(DRG, invalid_keys)
    find_duplicates(DRG, invalid_keys)
    check_sum_of_missions(DRG, invalid_keys)   
    check_missions_length_complexity(DRG)
    
    if invalid_keys:
        if os.path.isfile('poll.txt'):
            delete_file('poll.txt')
        if os.path.isfile('firstpoll.txt'):
            delete_file('firstpoll.txt')
            
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
            f.write('InvalidTimestampsScraper : 1')
            f.close()
        
        subprocess.Popen(['start', 'steam://run/548430//'], shell=True)
        
        files = []
        total_increments = len(invalid_keys)
        total_increments_ = int(str(total_increments))
        timeout_seconds = (total_increments * 1) + 300
        estimated_time_completion = (total_increments * 0.8) + 30
        
        #Wait for JSON
        polls = 0
        poll_switch = False
        avg_poll_time = 1
        files = []
        start_time = None
        elapsed_time = 0
        while True:
            timeout_seconds = (total_increments_ * avg_poll_time) + 300
            if start_time:
                elapsed_time = time.monotonic() - start_time
            
            if poll_switch:
                polls += 1
                avg_poll_time = elapsed_time / polls
                estimated_time_completion =  total_increments * avg_poll_time
                
                total_increments -= 1
                percent = round((total_increments_ - total_increments) / total_increments_ * 100, 2)
                print(f"{percent}% Completed | Elapsed time: {format_seconds(elapsed_time)} | {format_seconds(timeout_seconds - elapsed_time)} until timeout | Estimated time until completion: {format_seconds(estimated_time_completion)}    ", end='\r')
                poll_switch = False

            for filename in os.listdir():
                if filename == 'firstpoll.txt':
                    start_time = time.monotonic()
                    delete_file('firstpoll.txt')

                if filename == 'poll.txt':
                    poll_switch = True
                    delete_file('poll.txt')

                        
                if filename == 'redonemissions.json':
                    files.append(filename)
                    print(f"100.00% Completed | Elapsed time: {format_seconds(elapsed_time)} | {format_seconds(timeout_seconds - elapsed_time)} until timeout | Estimated time until completion: {format_seconds(estimated_time_completion)}    ")
                    print('Complete. Ending FSD & Unreal processes...')
                    time.sleep(3)
                    kill_process_by_name_starts_with('FSD')
                    kill_process_by_name_starts_with('Unreal')
                    break
                    
            if files:
                break
            
            if elapsed_time > timeout_seconds:
                print('')
                print('Timeout... process crashed or froze')
                kill_process_by_name_starts_with('FSD')
                kill_process_by_name_starts_with('Unreal')
                
                start_time = None
                total_increments = int(str(total_increments_))
                polls = 0
                
                if os.path.isfile('poll.txt'):
                    delete_file('poll.txt')
                if os.path.isfile('firstpoll.txt'):
                    delete_file('firstpoll.txt')
                
                enable_system_time()
                time.sleep(4)
                disable_system_time()
                subprocess.Popen(['start', 'steam://run/548430//'], shell=True)
        
        if os.path.isfile('poll.txt'):
            delete_file('poll.txt')
        
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

def compare_dicts(dict1, dict2, ignore_keys):
    dict1_filtered = {k: v for k, v in dict1.items() if k not in ignore_keys}
    dict2_filtered = {k: v for k, v in dict2.items() if k not in ignore_keys}
    return dict1_filtered == dict2_filtered

def get_all_unique_code_names(dicts_list):
    filtered_list = [d for d in dicts_list if d["season"] != "s0"]
    
    codename_count = {}
    for d in filtered_list:
        codename = d["CodeName"]
        if codename:
            codename_count[codename] = codename_count.get(codename, 0) + 1
    
    unique_codenames = [codename for codename, count in codename_count.items() if count == 1]
    
    return unique_codenames

def flatten_seasons_v5(DRG):
    combined = {}
    timestamps = list(DRG.keys())
    seasons = ['s0', 's1', 's3']
    
    for timestamp in timestamps:
        del DRG[timestamp]['s2']
        del DRG[timestamp]['s4']
        del DRG[timestamp]['s5']
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