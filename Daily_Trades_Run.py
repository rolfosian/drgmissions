import datetime
import subprocess
import time
import os
import json
import re
from time import sleep
from drgmissions_scraper_utils import (
    kill_process_by_name_starts_with,
    calculate_average_float,
    enable_system_time,
    toggle_system_time,
    user_input_set_target_date,
    format_seconds,
    sanitize_datetime,
    reverse_date_format,
    order_dictionary_by_date,
    print,
)

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

def main_loop(total_increments, current_time, AllTheDeals):
    game_times = []
    for i in range(total_increments+1):
        sleep(2)
        
        #Start the game
        subprocess.Popen(['start', 'steam://run/548430//'], shell=True)
        game_start_time = time.monotonic()
        timestamp = current_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        timestamp = re.sub(r':\d{2}Z', ':00Z', timestamp)
        waiting_for_json = True
        timeout = False
        wait_start_time = time.monotonic()
        
        #Wait for JSON
        while waiting_for_json:
            if time.monotonic() - wait_start_time > 120:
                print('Timeout... process froze or crashed')
                timeout = True
                kill_process_by_name_starts_with('FSD')
                kill_process_by_name_starts_with('Unreal')
                sleep(3)
                print('restarting...')
                break
            
            for filename in os.listdir():
                if filename == 'drgdailydeal.json':
                    while True:
                        try:
                            with open(filename, 'r') as f:
                                deal = json.loads(f.read())
                            os.remove(filename)
                            break
                        except:
                            continue
                    AllTheDeals[timestamp] = deal
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
    time_service_query = subprocess.check_output('sc query w32time', stderr=subprocess.PIPE, shell=True).decode('utf-8')
    if 'RUNNING' not in time_service_query:
        enable_system_time()
        sleep(2)
    
    #Set mods.txt for GetDailyDeals
    with open('./mods/mods.txt', 'w') as f:
        f.write('GetDailyDeals : 1')
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
    AllTheDeals = order_dictionary_by_date(AllTheDeals)
    AllTheDeals = re.sub(r':\d{2}Z', ':00Z', json.dumps(AllTheDeals))
    print(f'Total time elapsed: {format_seconds(time.monotonic() - start_time)}')
    sleep(2)
    #Reset mods.txt
    with open('./mods/mods.txt', 'w') as f:
        f.close()
    
    #Write AllTheDeals JSON
    with open('drgdailydeals.json', 'w') as f:
        f.write(AllTheDeals)
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