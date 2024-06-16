import datetime
import subprocess
import time
import os
import json
import re
from time import sleep
from random import randint
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
    init_polling_server,
    shut_down_polling_server,
    is_port_in_use,
    delete_file,
    print,
    cfg
)

def main():
    maximize_window()
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
    
    
    while True:
        port = randint(12345, 65534)
        if not is_port_in_use(port, '127.0.0.1'):
            break
    
    with open('./mods/DailyDealsScraper/Scripts/main.lua', 'r') as f:
        main = f.readlines()
        f.close()
    main_lines = []
    for line in main:
        #In case different amount is defined in script
        if 'local total_days' in line:
            total_increments = int(line.split('=')[1].strip())
            total_increments_ = int(str(total_increments))
        if line.startswith('    local port'):
            line = f'    local port = {port}\n'
        main_lines.append(line)
    with open('./mods/DailyDealsScraper/Scripts/main.lua', 'w') as f:
        f.writelines(main_lines)
        f.close()
    
    #Disable automatic system time
    disable_system_time()
    sleep(2)
    
    # Set the clock to 00:00:00
    subprocess.run(['date', reverse_date_format(currytime[0]), '&', 'time', currytime[1]], shell=True)

    #Run Deep Rock Galactic headless
    subprocess.Popen(['start', 'steam://run/548430//'], shell=True)
    
    AllTheDeals = []
    polling_list = []
    server_socket, accept_thread = init_polling_server(port, AllTheDeals, polling_list)

    #Wait for JSON
    polls = 0
    polling = True
    avg_poll_time = 1
    start_time = None
    elapsed_time = 0
    while True:
        try:
            polling_list.pop(0)
            start_time = time.monotonic()
            break
        except:
            pass

    while True:
        timeout_seconds = (total_increments_ * avg_poll_time) + 300
        
        try:
            poll = polling_list.pop(0)
            elapsed_time = time.monotonic() - start_time
            polls += 1
            avg_poll_time = elapsed_time / polls
            estimated_time_completion =  total_increments * avg_poll_time
            total_increments -= 1
            percent = round((total_increments_ - total_increments) / total_increments_ * 100, 2)
            print(f"{percent:.2f}% Completed | Elapsed time: {format_seconds(elapsed_time)} | {format_seconds(timeout_seconds - elapsed_time)} until timeout | Estimated time until completion: {format_seconds(estimated_time_completion)}    ", end='\r')
            
            if poll == 'fin':
                AllTheDeals = json.loads(re.sub(r':\d{2}Z', ':00Z', ''.join(AllTheDeals)))
                print('Complete. Ending FSD & Unreal processes...')
                kill_process_by_name_starts_with('FSD')
                kill_process_by_name_starts_with('Unreal')
                break
        
        except:
            if elapsed_time > timeout_seconds:
                print('', include_timestamp=False)
                print('Timeout... process crashed or froze')
                kill_process_by_name_starts_with('FSD')
                kill_process_by_name_starts_with('Unreal')
                
                start_time = time.monotonic()
                total_increments = int(str(total_increments_))
                polls = 0
                
                enable_system_time()
                time.sleep(4)
                disable_system_time()
                subprocess.Popen(['start', 'steam://run/548430//'], shell=True)
                
    shut_down_polling_server(server_socket, accept_thread)

    #Reset mods.txt
    with open('./mods/mods.txt', 'w') as f:
        f.close()
        
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