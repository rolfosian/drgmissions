from datetime import datetime, timedelta
from functools import wraps
from typing import Union, Callable
from ctypes import wintypes, byref, WinDLL, WINFUNCTYPE, sizeof, create_unicode_buffer
from copy import deepcopy
from random import randint
import socket
import subprocess
import time
import psutil
import os
import requests
import winreg
import json
import re
import threading

class IPCServer:
    def __init__(self, port:int):
        self.port = port
        self.polling_list = []
        self.result_list = []
        self.poll_event = threading.Event()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = ('localhost', port)
        self.server_socket.bind(self.server_address)
        self.server_socket.listen(5)
        
        self.handshake_funcs = {
            'polling' : self.handle_polling_client,
            'pollingq' : lambda x, y: self.handle_polling_client(x, y, quiet=True),
            'result' : self.handle_result_client,
            'resultq' : lambda x, y: self.handle_result_client(x, y, quiet=True)
        }
        self.accept_thread = threading.Thread(target=self.accept_connections)
        self.accept_thread.start()
        print(f"\nIPC server is listening on {self.server_address}")

    def handle_polling_client(self, client_socket:socket.socket, client_address:tuple, quiet=False):
        client_socket.sendall('ack\n'.encode())
        print(f"\nPolling connection established from {client_address}") if not quiet else None
        
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                result = data.decode('utf-8').strip()
                while self.poll_event.is_set():
                    continue
                self.polling_list.append(result)
                self.poll_event.set()
                client_socket.sendall('ack\n'.encode())

        except Exception as e:
            print(f"\nError handling polling connection from {client_address}: {e}") if not quiet else None

        finally:
            print('\nPolling connection closed.') if not quiet else None
            client_socket.close()

    def handle_result_client(self, client_socket:socket.socket, client_address:tuple, quiet=False):
        client_socket.sendall('ack\n'.encode())
        print(f"\nResult connection established from {client_address}") if not quiet else None
        client_buffer = bytearray()

        try:
            while True:
                data = client_socket.recv(1024*1024*10)
                client_buffer.extend(data)
                if client_buffer[4:].decode('utf-8').strip().endswith('END'):
                    break

            while self.poll_event.is_set():
                continue
            self.result_list.append(client_buffer[:-3].decode('utf-8'))
            client_socket.sendall('ack\n'.encode())
            self.polling_list.append('fin')
            self.poll_event.set()
            

        except Exception as e:
            print(f"\nError handling result connection from {client_address}: {e}") if not quiet else None

        finally:
            print('\nResult connection closed.') if not quiet else None
            client_socket.close()

    def handshake(self, client_socket:socket.socket, client_address:tuple):
        try:
            handshake_message = client_socket.recv(1024).decode('utf-8').strip()
            self.handshake_funcs[handshake_message](client_socket, client_address)
        except Exception as e:
            print(f"\nHandshake error with {client_address}: {e}")
            client_socket.close()

    def accept_connections(self):
        print("Waiting for a connection...")
        while True:
            try:
                client_socket, client_address = self.server_socket.accept()
                client_thread = threading.Thread(target=self.handshake, args=(client_socket, client_address))
                client_thread.start()
            except:
                break

    def shut_down(self):
        print("\nIPC is shutting down.")
        self.server_socket.close()
        self.accept_thread.join()

    def restart_server(self):
        print("\nRestarting IPC server...")
        self.shut_down()
        self.__init__(self.port)

def cfg_():
    with open(os.getcwd()+'/scraper_cfg.json', 'r') as f:
        cfg = json.load(f)
    return cfg
cfg = cfg_()

def wrap_with_color(string:str, color:str):
    return f"\033[0;{color}m{string}\033[0m"

def subprocess_wrapper(command:str, shell=False, print_=True):
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

def is_port_in_use(port:int, ip:str):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind((ip, int(port)))
        s.close()
        return False
    except socket.error:
        return True

def delete_file(filename:str):
    while True:
        try:
            os.remove(filename)
            break
        except:
            continue

def timestamped_print(func:Callable[..., None]):
    @wraps(func)
    def wrapper(*args, **kwargs):
        include_timestamp = kwargs.pop('include_timestamp', True)
        start = kwargs.pop('start', '')
        args = [str(arg) for arg in args]
        args[0] = start + args[0]
        
        if include_timestamp:
            concatenated_args = ''.join(args)
            if concatenated_args.strip() != '':
                timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                args = (f'{timestamp}', *args)
        return func(*args, **kwargs)
    return wrapper
print = timestamped_print(print)

def format_seconds(seconds:Union[int, float]):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    remaining_seconds = int(round(seconds % 60))
    if remaining_seconds == 60:
        minutes += 1
        remaining_seconds = 0
    formatted_time = "{:02d}:{:02d}:{:02d}".format(hours, minutes, remaining_seconds)
    return formatted_time

def maximize_window():
    def enum_windows_proc(hwnd, lparam, windows):
        window_tid = wintypes.DWORD()
        user32.GetWindowThreadProcessId(hwnd, byref(window_tid))
        
        process_name = create_unicode_buffer(512)
        h_process = kernel32.OpenProcess(0x0400 | 0x0010, False, window_tid.value)
        kernel32.QueryFullProcessImageNameW(h_process, 0, process_name, byref(wintypes.DWORD(sizeof(process_name) // 2)))
        process_name = process_name.value.split("\\")[-1]

        if process_name == 'py.exe' or process_name == 'python.exe' and pid == window_tid.value:
            windows.append(hwnd)
            return False
        
        return True
    
    kernel32 = WinDLL('kernel32')
    user32 = WinDLL('user32')

    EnumWindowsProc = WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    pid = kernel32.GetCurrentProcessId()

    windows = []
    SW_MAXIMIZE = 3
    user32.EnumWindows(EnumWindowsProc(lambda *args: enum_windows_proc(*args, windows)), 0)

    if windows:
        interpreter_hwnd = windows[0]
        user32.ShowWindow(interpreter_hwnd, SW_MAXIMIZE)

#Validation
#-----------------------
def sort_dictionary(dictionary:dict, custom_order:list):
    sorted_dict = {}
    for key in custom_order:
        if key in dictionary:
            sorted_dict[key] = dictionary[key]
            del dictionary[key]

    sorted_dict.update(dictionary)
    return sorted_dict

def order_dictionary_by_date(dictionary:dict):
    sorted_keys = sorted(dictionary.keys(), key=lambda x: datetime.fromisoformat(x.replace('Z', '')))
    ordered_dictionary = {}
    for key in sorted_keys:
        ordered_dictionary[key] = dictionary[key]
    return ordered_dictionary

def order_dictionary_by_date_FIRST_KEY_ROUNDING(dictionary:dict):    
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

def reconstruct_dictionary(dictionary:dict):
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
                                mission1['MissionWarnings'] = sorted(mission['MissionWarnings'])
                            mission1 = sort_dictionary(mission1, mission_key_order)
                            missions1.append(mission1)
                        value[biome] = missions1

                god[timestamp][season][key] = value
    return god

def find_missing_timestamps(dictionary:dict, invalid_keys:list):
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

def find_duplicate_seasons(dictionary:dict, invalid_keys:list):
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
        
        dupes = find_duplicate_strings(god[timestamp])
        if dupes:
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

def find_duplicates(dictionary:dict, invalid_keys:list):
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

    def find_duplicate_strings(dictionary:dict):
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

def check_sum_of_missions(dictionary:dict, invalid_keys:list):
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
        
def check_missions_keys(dictionary:dict, invalid_keys:list):
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

def check_missions_length_complexity(dictionary:dict):
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

def round_time_down(datetime_string:str):
    datetime_minutes = int(datetime_string[14:16])
    if datetime_minutes >= 30:
        new_datetime = datetime_string[:14] + '30:00Z'
    else:
        new_datetime = datetime_string[:14] + '00:00Z'
    return new_datetime

#------------------------------------------------------------------------------------------------------

def split_file(file_path:str, max_size:int):
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

def upload_file(cfg:dict, file_path:str):
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

def kill_process_by_name_starts_with(start_string:str):
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

def sanitize_datetime(datetime_str:str):
    year, month, day, hour, min, sec = map(int, datetime_str[:10].split("-") + datetime_str[11:19].split(":"))
    sanitized_datetime = "{:02d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(day, month, year %100, hour, min, sec)
    return sanitized_datetime

def reverse_date_format(input_date:str):
    year, month, day = input_date.split('-')
    input_date = f"{day}-{month}-{year[2:]}"
    return input_date

def user_input_set_target_date(current_time:datetime):
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

def yes_or_no(prompt:str):
    while True:
        response = input(prompt).strip().lower()
        if response == 'y':
            return True
        elif response == 'n':
            return False
        else:
            print("Please enter 'Y' or 'N'.")

def wait_for_json(IPC:IPCServer, total_increments:int):
    
    total_increments_ = int(str(total_increments))
    estimated_time_completion = (total_increments * 0.2) + 30
    timeout_seconds = estimated_time_completion + 300

    print('', include_timestamp=False)
    print(f'Total increments: {str(total_increments)}')
    print(f'{format_seconds(timeout_seconds)} until timeout')
    print(f'Estimated time until completion: {format_seconds(estimated_time_completion)}')
    print('', include_timestamp=False)

    #Wait for JSON
    polls = 0
    avg_poll_time = 0.2
    start_time = None
    elapsed_time = 0
    IPC.poll_event.wait()
    IPC.polling_list.pop(0)
    start_time = time.monotonic()
    IPC.poll_event.clear()

    while True:
        timeout_ = IPC.poll_event.wait(timeout=timeout_seconds)
        elapsed_time = time.monotonic() - start_time
        
        if not timeout_:
            print('', include_timestamp=False)
            print('Timeout... process crashed or froze')
            kill_process_by_name_starts_with('FSD')
            kill_process_by_name_starts_with('Unreal')
            
            IPC.shut_down()
            IPC = IPCServer(IPC.port)
            
            total_increments = int(str(total_increments_))
            polls = 0
            avg_poll_time = 0.2
            estimated_time_completion =  total_increments * avg_poll_time
            timeout_seconds = estimated_time_completion + 300
            
            enable_system_time()
            time.sleep(4)
            disable_system_time()
            subprocess.Popen(['start', 'steam://run/548430//'], shell=True)
            
            start_time = time.monotonic()
            timeout_ = IPC.poll_event.wait(timeout=timeout_seconds)
            if not timeout_:
                timeout_seconds = 0.1
                continue
        
        poll = IPC.polling_list.pop(0)
        IPC.poll_event.clear()
        polls += 1
        
        avg_poll_time = elapsed_time / polls
        estimated_time_completion =  total_increments * avg_poll_time
        timeout_seconds = estimated_time_completion + 300
        total_increments -= 1
        
        percent = round((total_increments_ - total_increments) / total_increments_ * 100, 2)
        percent = f"{percent:.2f}% Completed"
        if poll == 'enc':
            percent = 'Encoding JSON...'    
        print(f"{percent} | {format_seconds(timeout_seconds)} until timeout | Estimated time remaining: {format_seconds(estimated_time_completion)}    ", end='\r')
        
        if poll == 'fin':
            dictionary = json.loads(re.sub(r':\d{2}Z', ':00Z', IPC.result_list[0]))
            print('\nComplete. Ending FSD & Unreal processes...')
            kill_process_by_name_starts_with('FSD')
            kill_process_by_name_starts_with('Unreal')
            break
    IPC.shut_down()
    
    return dictionary

def validate_drgmissions(DRG:dict, patched:bool):
    DRG = order_dictionary_by_date(DRG)
    DRG = reconstruct_dictionary(DRG)
    
    invalid_keys = []
    find_missing_timestamps(DRG, invalid_keys)
    check_missions_keys(DRG, invalid_keys)
    # find_duplicate_seasons(DRG, invalid_keys)
    find_duplicates(DRG, invalid_keys)
    check_sum_of_missions(DRG, invalid_keys)   
    check_missions_length_complexity(DRG)
    
    if invalid_keys:
        print('Invalid timestamps found...')
        with open('invalid_timestamps_log.txt', 'w') as f:
            s = ''
            for key, func in invalid_keys:
                s += f'{key} found invalid using {func} function\n'
            f.write(s)
            f.close()

        patched = True
        
        while True:
            port = randint(12345, 65534)
            if not is_port_in_use(port, '127.0.0.1'):
                break
        
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

        with open('./mods/InvalidTimestampsScraper/Scripts/main.lua', 'r') as f:
            main = f.readlines()
            f.close()
        main_lines = []
        for line in main:
            if line.startswith('    local port'):
                line = f'    local port = {port}\n'
            main_lines.append(line)
        with open('./mods/InvalidTimestampsScraper/Scripts/main.lua', 'w') as f:
            f.writelines(main_lines)
            f.close()
        
        subprocess.Popen(['start', 'steam://run/548430//'], shell=True)
        
        total_increments = len(invalid_keys)
        redone_missions = wait_for_json(port, total_increments)
        
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

def compare_dicts(dict1:dict, dict2:dict, ignore_keys:list):
    dict1_filtered = {k: v for k, v in dict1.items() if k not in ignore_keys}
    dict2_filtered = {k: v for k, v in dict2.items() if k not in ignore_keys}
    return dict1_filtered == dict2_filtered

def flatten_seasons_v5(DRG:dict):
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