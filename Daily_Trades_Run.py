import datetime
import subprocess
import time
import psutil
import os
import json
from time import sleep
import winreg
import re

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

def kill_process_by_name_starts_with(start_string):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'].startswith(start_string):
            print(f"Terminating process: {proc.info['name']} (PID: {proc.info['pid']})")
            proc.kill()

def increment_datetime(datetime_str):
    year, month, day, hour, min, sec = map(int, datetime_str[:10].split("-") + datetime_str[11:19].split(":"))
    day += 1
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if month == 2 and year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        days_in_month[1] = 29
    if day > days_in_month[month - 1]:
        day = day - days_in_month[month - 1]
        month += 1
    if month > 12:
        month = month - 12
        year += 1
    updated_datetime = "{:02d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(day, month, year %100, hour, min, sec)
    return updated_datetime

def sanitize_datetime(datetime_str):
    year, month, day, hour, min, sec = map(int, datetime_str[:10].split("-") + datetime_str[11:19].split(":"))
    sanitized_datetime = "{:02d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(day, month, year %100, hour, min, sec)
    return sanitized_datetime

def reverse_date_format(input_date):
    year, month, day = input_date.split('-')
    input_date = f"{day}-{month}-{year[2:]}"
    return input_date

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
        subprocess.run(['w32tm', '/resync'], shell=True)
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
        output = subprocess.check_output('sc query w32time', shell=True).decode('utf-8')
        if 'RUNNING' in output:
            disable_system_time()
        else:
            enable_system_time()        
    except Exception as e:
        print(f"Error {e}")
        
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

def main_loop(total_increments, current_time, AllTheDeals):
    game_times = []
    for i in range(total_increments+1):
        sleep(2)
        #Start the game
        subprocess.Popen(['start', 'steam://run/548430//-nullrhi'], shell=True)
        game_start_time = time.monotonic()
        timestamp = current_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        timestamp = re.sub(r':\d{2}Z', ':00Z', timestamp)
        waiting_for_json = True
        timeout = False
        wait_start_time = time.monotonic()
        #Wait for JSON
        while waiting_for_json:
            if time.monotonic() - wait_start_time > 120:
                print('TIMEOUT.')
                timeout = True
                kill_process_by_name_starts_with('FSD')
                kill_process_by_name_starts_with('Unreal')
                sleep(3)
                print('RESTARTING')
                break
            for filename in os.listdir():
                if filename == 'drgdailydeal.json':
                    sleep(0.25)
                    with open(filename, 'r') as f:
                        deal = json.loads(f.read())
                    AllTheDeals[timestamp] = deal
                    os.remove(filename)
                    kill_process_by_name_starts_with('FSD')
                    kill_process_by_name_starts_with('Unreal')
                    sleep(3)
                    waiting_for_json = False
            sleep(0.5)
        if timeout:
            current_time = current_time.replace(hour=0, minute=0, second=1)
            currytime = current_time.strftime("%Y-%m-%dT%H:%M:%SZ")
            currytime = datetime.datetime.strptime(sanitize_datetime(currytime), "%d-%m-%yT%H:%M:%SZ")
            currytime = str(currytime).split(' ')
            subprocess.run(['date', reverse_date_format(currytime[0]), '&', 'time', currytime[1]], shell=True)
            return main_loop(total_increments, current_time, AllTheDeals)
        
        time_for_json = time.monotonic() - game_start_time
        game_times.append(time_for_json)
        print(f'Estimated time remaining: {format_seconds(calculate_average_float(game_times)*total_increments)}', end='\r')
        
        current_time = datetime.datetime.strptime(increment_datetime(timestamp), "%d-%m-%yT%H:%M:%SZ")
        current_time = current_time.replace(hour=0, minute=0, second=1)
        newtime = str(current_time).split(' ')
        #Set clock forward 1 day
        subprocess.run(['date', reverse_date_format(newtime[0]), '&', 'time', newtime[1]], shell=True)
        total_increments -= 1
    print(f'Estimated time remaining: {format_seconds(0)}')
    return AllTheDeals

def main():
    #Set mods.txt for GetDailyDeals
    with open('./mods/mods.txt', 'r') as f:
        mods = f.read()
        mods = mods.replace('dds_fetcher : 1', 'dds_fetcher : 0')
        mods = mods.replace('long_term_mission_data_collector : 1', 'long_term_mission_data_collector : 0')
        mods = mods.replace('GetDailyDeals : 0', 'GetDailyDeals : 1')
        f.close()
    with open('./mods/mods.txt', 'w') as f:
        f.write(mods)
        f.close()

    # Get the current UTC date
    current_time = datetime.datetime.utcnow()
    current_time = current_time.replace(hour=0, minute=0, second=0)
    currytime = current_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    currytime = datetime.datetime.strptime(sanitize_datetime(currytime), "%d-%m-%yT%H:%M:%SZ")
    currytime = str(currytime).split(' ')
    
    # Set the target date
    target_date = user_input_set_target_date(current_time)

    #Disable automatic system time
    toggle_system_time()
    sleep(2)
    
    # Set the clock to 00:00:00
    subprocess.run(['date', reverse_date_format(currytime[0]), '&', 'time', currytime[1]], shell=True)

    # Calculate the difference between the target date and the current time
    diff_seconds = (target_date - current_time).total_seconds()

    # Calculate the total number of 24-hour increments
    total_increments = int(diff_seconds // 86400)
    total_increments += 1
    print(f'Total daily deals to be fetched: {total_increments}')

    #Initialize master dictionary
    AllTheDeals = {}
    
    # Loop for the increments
    start_time = time.monotonic()
    AllTheDeals = main_loop(total_increments, current_time, AllTheDeals)
    print(f'Total time elapsed: {format_seconds(time.monotonic() - start_time)}')
    sleep(2)
    #Reset mods.txt
    with open('./mods/mods.txt', 'r') as f:
        mods = f.read()
        mods = mods.replace('GetDailyDeals : 1', 'GetDailyDeals : 0')
        f.close()
    with open('./mods/mods.txt', 'w') as f:
        f.write(mods)
        f.close()
    
    #Write AllTheDeals JSON
    with open('drgdailydeals.json', 'w') as f:
        f.write(json.dumps(AllTheDeals))
        f.close()
    
    #Enable Automatic system time
    toggle_system_time()
    sleep(4)
try:
    if os.path.isfile('drgdailydeal.json'):
        os.remove('drgdailydeal.json')
    print(os.getcwd(), '\n')
    main()
except Exception as e:
    print(f'ERROR: {e}')
    input('Press enter to exit...')