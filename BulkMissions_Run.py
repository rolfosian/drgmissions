import subprocess
import psutil
import time
from time import sleep
import os
import datetime
import json
from drgmissions_validator import (
    order_dictionary_by_date,
    order_dictionary_by_date_FIRST,
    reconstruct_dictionary,
    find_duplicates,
    check_sum_of_missions,
    check_missions_keys,
    check_missions_length_complexity,
    find_missing_timestamps
    )
import winreg
import re

def format_seconds(seconds):
    timedelta = datetime.timedelta(seconds=seconds)
    hours = int(timedelta.total_seconds() // 3600)
    minutes = int((timedelta.total_seconds() % 3600) // 60)
    remaining_seconds = timedelta.total_seconds() % 60
    formatted_time = "{:02d}:{:02d}:{:05.2f}".format(hours, minutes, remaining_seconds)
    return formatted_time

def enable_system_time():
    try:
        print('-------------------------------------------------------------------------')
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\\CurrentControlSet\\Services\\W32Time\\Parameters', 0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, 'Type', 0, winreg.REG_SZ, 'NTP')
        winreg.CloseKey(key)
        subprocess.run(['sc', 'config', 'w32time', 'start=', 'auto'], shell=True)
        subprocess.run(['net', 'start', 'w32time'], shell=True)
        sleep(2)
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

def kill_process_by_name_starts_with(start_string):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'].startswith(start_string):
            print(f"Terminating process: {proc.info['name']} (PID: {proc.info['pid']})")
            proc.kill()

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
                sleep(4)
                subprocess.Popen(['start', 'steam://run/548430//-nullrhi'], shell=True)
                start_time = time.monotonic()
            for filename in os.listdir():
                if filename == 'redonemissions.json':
                    sleep(5)
                    files.append(filename)
                    kill_process_by_name_starts_with('FSD')
                    kill_process_by_name_starts_with('Unreal')
            if files:
                print(f'Estimated time until completion: {format_seconds(0.00)}')
                print(f'\n---\nElapsed time: {format_seconds(elapsed_time)}               \n---')
                break
            sleep(0.1)
            
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

def main():
    time_service_query = subprocess.check_output('sc query w32time', stderr=subprocess.PIPE, shell=True).decode('utf-8')
    if 'RUNNING' not in time_service_query:
        enable_system_time()
        sleep(2)
        
    #Set mods.txt for BulkMissions collector

    with open('./mods/mods.txt', 'w') as f:
        f.write('long_term_mission_data_collector : 1')
        f.close()
        
    #Get target date from user input
    current_time = datetime.datetime.now()
    user_date = user_input_set_target_date(current_time)
            
    target_date_format = user_date.strftime("    local target_date = os.time{year=%Y, month=%m, day=%d, hour=%H, min=%M, sec=%S}\n")
    #Set the target date in the lua script
    with open('./mods/long_term_mission_data_collector/Scripts/main.lua', 'r') as f:
        main = f.readlines()
        f.close()
    main_lines = []
    for line in main:
        if line.startswith('    local target_date'):
            line = line.replace(line, target_date_format)
            main_lines.append(line)
        else:
            main_lines.append(line)
    with open('./mods/long_term_mission_data_collector/Scripts/main.lua', 'w') as f:
        f.writelines(main_lines)
        f.close()
    
    # Calculate the difference in seconds between the current UTC time and the target date
    current_utc = datetime.datetime.utcnow()
    diff_seconds = (user_date - current_utc).total_seconds()
    # Calculate the total amount of 30-minute increments between the current time and the target date
    total_increments = int(diff_seconds // 1800)
    total_increments += 1
    print(f'Total 30 minute increments: {str(total_increments)}')
    estimated_time_completion = (total_increments*1.5)+25

    #Calculate timeout total seconds duration
    timeout_seconds = (total_increments * 1.6) + 120
    print(f'{format_seconds(timeout_seconds)} until timeout\n')

    print(f'Estimated time until completion: {format_seconds(estimated_time_completion)}', end='\r')
    
    #Disable automatic time sync
    toggle_system_time()
    sleep(1)
    #Run Deep Rock Galactic headless
    subprocess.Popen(['start', 'steam://run/548430//-nullrhi'], shell=True)

    #Wait for JSON
    files = []
    start_time = time.monotonic()
    while True:
        elapsed_time = time.monotonic() - start_time
        print(f'{format_seconds(timeout_seconds-elapsed_time)} until timeout. Estimated time until completion: {format_seconds(estimated_time_completion-elapsed_time)}', end="\r")

        if time.monotonic() - start_time > timeout_seconds:
            print('TIMEOUT, GAME FROZE OR CRASHED BEFORE TARGET DATE REACHED. RESTARTING')
            kill_process_by_name_starts_with('FSD')
            kill_process_by_name_starts_with('Unreal')
            sleep(4)
            subprocess.Popen(['start', 'steam://run/548430//-nullrhi'], shell=True)
            start_time = time.monotonic()
        for filename in os.listdir():
            if filename == 'drgmissionsgod.json':
                sleep(5)
                files.append(filename)
                kill_process_by_name_starts_with('FSD')
                kill_process_by_name_starts_with('Unreal')
        if files:
            print(f'Estimated time until completion: {format_seconds(0.00)}')
            print(f'\n---\nElapsed time: {format_seconds(elapsed_time)}               \n---')
            break
        sleep(0.1)
        
    #Reset mods.txt
    with open('./mods/mods.txt', 'w') as f:
        f.close()
        
    #Enable automatic time sync
    toggle_system_time()

    with open('drgmissionsgod.json', 'r') as f:
        DRG = f.read()
        DRG = re.sub(r':\d{2}Z', ':00Z', DRG)
        DRG = json.loads(DRG)
        f.close()
        
    for timestamp, dict in DRG.items():
        DRG[timestamp]['timestamp'] = timestamp

    DRG = order_dictionary_by_date_FIRST(DRG)
    DRG = reconstruct_dictionary(DRG)
    with open('drgmissionsgod.json', 'w') as f:
        f.write(json.dumps(DRG))
        f.close()
    
    #Validate JSON
    patched = False
    DRG, patched = validate_drgmissions(DRG, patched)
    if patched:
        with open('drgmissionsgod.json', 'w') as f:
            f.write(json.dumps(DRG))
            f.close()
    #Pause to allow user to check terminal for output
    input('Press enter to exit...')
    
try:
    if os.path.isfile('drgmissionsgod.json'):
        os.remove('drgmissionsgod.json')
    print(os.getcwd(), '\n')
    main()
except Exception as e:
    print(f'ERROR: {e}')
    input('Press enter to exit...')