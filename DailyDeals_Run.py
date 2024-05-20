import datetime
import subprocess
import time
import os
import json
import re
from time import sleep
from drgmissions_scraper_utils import (
    kill_process_by_name_starts_with,
    upload_file,
    yes_or_no,
    enable_system_time,
    disable_system_time,
    maximize_window,
    format_seconds,
    sanitize_datetime,
    reverse_date_format,
    order_dictionary_by_date,
    delete_file,
    print,
    cfg
)

def main():
    maximize_window()
    if os.path.isfile('poll.txt'):
        os.remove('poll.txt')
    if os.path.isfile('firstpoll.txt'):
        os.remove('firstpoll.txt')
    time_service_query = subprocess.check_output('sc query w32time', stderr=subprocess.PIPE, shell=True).decode('utf-8')
    if 'RUNNING' not in time_service_query:
        enable_system_time()
        sleep(2)
    
    #Set mods.txt for GetDailyDeals
    with open('./mods/mods.txt', 'w') as f:
        f.write('DailyDealsScraper : 1')
        f.close()

    # Get the current UTC date
    current_time = datetime.datetime.utcnow()
    current_time = current_time.replace(hour=0, minute=0, second=0)
    currytime = current_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    currytime = datetime.datetime.strptime(sanitize_datetime(currytime), "%d-%m-%yT%H:%M:%SZ")
    currytime = str(currytime).split(' ')
    
    total_increments = 365
    total_increments_ = 365
    #In case different amount is defined in script
    with open('./mods/DailyDealsScraper/Scripts/main.lua', 'r') as f:
        script = f.readlines()
        for line in script:
            if 'local total_days' in line:
                total_increments = int(line.split('=')[1].strip())
                total_increments_ = int(str(total_increments))
                break
        f.close()
                
    #Disable automatic system time
    disable_system_time()
    sleep(2)
    
    # Set the clock to 00:00:00
    subprocess.run(['date', reverse_date_format(currytime[0]), '&', 'time', currytime[1]], shell=True)

    #Run Deep Rock Galactic headless
    subprocess.Popen(['start', 'steam://run/548430//'], shell=True)

    #Wait for JSON
    AllTheDeals = None
    polls = 0
    poll_switch = False
    avg_poll_time = 1
    files = False
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
                    
            if filename == 'drgdailydeals.json':
                files = True
                print(f"{percent}% Completed | Elapsed time: {format_seconds(elapsed_time)} | {format_seconds(timeout_seconds - elapsed_time)} until timeout | Estimated time until completion: {format_seconds(estimated_time_completion)}    ")
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
        
    #Reset mods.txt
    with open('./mods/mods.txt', 'w') as f:
        f.close()
    
    with open('drgdailydeals.json', 'r') as f:
        AllTheDeals = f.read()
        AllTheDeals = re.sub(r':\d{2}Z', ':00Z', AllTheDeals)
        AllTheDeals = json.loads(AllTheDeals)
        
    AllTheDeals = order_dictionary_by_date(AllTheDeals)

    #Reset mods.txt
    with open('./mods/mods.txt', 'w') as f:
        f.close()
    
    #Write AllTheDeals JSON
    with open('drgdailydeals.json', 'w') as f:
        json.dump(AllTheDeals, f)
    
    #Enable Automatic system time
    enable_system_time()
    
    if yes_or_no('Upload JSON? Y/N: '):
        upload_file(cfg, 'drgdailydeals.json')
    
    input('Press enter to exit...')
    
try:
    if os.path.isfile('drgdailydeals.json'):
        delete_file('drgdailydeals.json')
    print(os.getcwd(), '\n')
    main()
except Exception as e:
    print(f'ERROR: {e}')
    input('Press enter to exit...')