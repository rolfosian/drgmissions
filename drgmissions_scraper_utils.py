import datetime
import subprocess
import time
import psutil
import os
import requests
import winreg
import json
import re
from drgmissions_validator import (
    order_dictionary_by_date,
    reconstruct_dictionary,
    find_duplicates,
    find_missing_timestamps,
    check_missions_keys,
    check_missions_length_complexity,
    check_sum_of_missions
)

def upload_file(url, file_path, bearer_token):
    headers = {
        'Authorization': 'Bearer ' + bearer_token
    }

    with open(file_path, 'rb') as file:
        files = {'file': file}
        response = requests.post(url, headers=headers, files=files)
    return response

def wait_until_next_hour():
    now = datetime.datetime.now()
    if now.hour == 23:
        next_hour = now.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
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
    timedelta = datetime.timedelta(seconds=seconds)
    hours = int(timedelta.total_seconds() // 3600)
    minutes = int((timedelta.total_seconds() % 3600) // 60)
    remaining_seconds = timedelta.total_seconds() % 60
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
            user_date = datetime.datetime.strptime(user_input, "%Y-%m-%d")
            if user_date > current_time:
                break
            else:
                print("Please enter a date and time ahead of the current time.")
        except Exception:
            print("Invalid date format. Please enter the date in the format (YYYY-MM-DD).")
    return user_date

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
        print('Invalid timestamps:')
        for timestamp in invalid_keys:
            print(timestamp)
        patched = True
        
        toggle_system_time()
        print('\nPatching invalid timestamps...')
        
        with open('invalid_keys.txt', 'w') as f:
            filestr = ''
            for key in invalid_keys:
                filestr += f'{key}\n'
            f.write(filestr.strip())
            f.close()

        with open('./mods/mods.txt', 'w') as f:
            f.write('one_round_mission_data_collector : 1')
            f.close()
        
        subprocess.Popen(['start', 'steam://run/548430//-nullrhi'], shell=True)
        files = []
        timeout_seconds = (len(invalid_keys) * 1.6) + 120
        estimated_time_completion = (len(invalid_keys) *1.5) + 25
        start_time = time.monotonic()
        while True:
            elapsed_time = time.monotonic() - start_time
            print(f'{format_seconds(timeout_seconds-elapsed_time)} until timeout. Estimated time until completion: {format_seconds(estimated_time_completion-elapsed_time)}', end="\r")

            if time.monotonic() - start_time > timeout_seconds:
                print('TIMEOUT, GAME FROZE OR CRASHED. RESTARTING')
                kill_process_by_name_starts_with('FSD')
                kill_process_by_name_starts_with('Unreal')
                time.sleep(4)
                subprocess.Popen(['start', 'steam://run/548430//-nullrhi'], shell=True)
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
            DRG[timestamp]['timestamp'] = timestamp

        DRG = order_dictionary_by_date(DRG)
        DRG = reconstruct_dictionary(DRG)

        with open('./mods/mods.txt', 'w') as f:
            f.close()
        toggle_system_time()
        os.remove('invalid_keys.txt')
        os.remove('redonemissions.json')

        return validate_drgmissions(DRG, patched)
    
    print('No invalid timestamps found.')
    return DRG, patched