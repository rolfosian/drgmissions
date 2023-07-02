import subprocess
import psutil
import time
from time import sleep
import os
import datetime
import json
from drgmissions_validator import order_dictionary_by_date, reconstruct_dictionary, find_duplicates, check_sum_of_missions, check_missions_keys
import winreg

def enable_system_time():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\\CurrentControlSet\\Services\\W32Time\\Parameters', 0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, 'Type', 0, winreg.REG_SZ, 'NTP')
        winreg.CloseKey(key)
        subprocess.run(['sc', 'config', 'w32time', 'start=', 'demand'], shell=True)
        subprocess.run(['sc', 'start', 'w32time'], shell=True)
        sleep(2)
        subprocess.run(['w32tm', '/resync'], shell=True)
        print("Automatic system time enabled.\n\n")
    except Exception as e:
        print(f"Error: {e}")
def disable_system_time():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\\CurrentControlSet\\Services\\W32Time\\Parameters', 0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, 'Type', 0, winreg.REG_SZ, 'NoSync')
        winreg.CloseKey(key)
        subprocess.run(['sc', 'config', 'w32time', 'start=', 'disabled'], shell=True)
        subprocess.run(['sc', 'stop', 'w32time'], shell=True)
        print("Automatic system time disabled.\n\n")
    except Exception as e:
        print(f"Error: {e}")
def toggle_system_time():
    try:
        output = subprocess.check_output('sc query w32time', shell=True).decode('utf-8')
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
            print("Invalid date format. Please enter the date in the format (YYY-MM-DD).")
    print('\n')
    return user_date

def main():
    #Set mods.txt for BulkMissions collector
    with open('./mods/mods.txt', 'r') as f:
        mods = f.read()
        mods = mods.replace('dds_fetcher : 1', 'dds_fetcher : 0')
        mods = mods.replace('GetDailyDeals : 1', 'GetDailyDeals: 0')
        mods = mods.replace('long_term_mission_data_collector : 0', 'long_term_mission_data_collector : 1')
        f.close()
    with open('./mods/mods.txt', 'w') as f:
        f.write(mods)
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
    
    #Disable automatic time sync
    toggle_system_time()
    
    #Run Deep Rock Galactic headless
    subprocess.Popen(['start', 'steam://run/548430//-nullrhi'], shell=True)

    #Wait for JSON
    files = []
    while True:
        for filename in os.listdir():
            if filename == 'drgmissionsgod.json':
                sleep(10)
                files.append(filename)
                kill_process_by_name_starts_with('FSD')
                kill_process_by_name_starts_with('Unreal')
        if files:
            break
        sleep(1.5)
    print('\n')

    #Reset mods.txt
    with open('./mods/mods.txt', 'r') as f:
        mods = f.read()
        mods = mods.replace('long_term_mission_data_collector : 1', 'long_term_mission_data_collector : 0')
        f.close()

    with open('./mods/mods.txt', 'w') as f:
        f.write(mods)
        f.close()
        
    #Enable automatic time sync
    toggle_system_time()
    
    #Validate JSON
    with open('drgmissionsgod.json', 'r') as f:
        DRG = f.read()
        DRG = DRG.replace(':02Z', ':00Z')
        DRG = json.loads(DRG)
        f.close()

    DRG = order_dictionary_by_date(DRG)
    with open('drgmissionsgod.json', 'w') as f:
        f.write(json.dumps(DRG))
        f.close()

    DRG = reconstruct_dictionary(DRG)

    find_duplicates(DRG)
    check_sum_of_missions(DRG)
    check_missions_keys(DRG)

    #Pause to allow user to check terminal for output
    input('Press enter to exit...')
try:
    print(os.getcwd())
    main()
except Exception as e:
    print(e)
    input('Press enter to exit...')