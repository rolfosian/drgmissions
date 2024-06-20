import datetime
import subprocess
import os
import json
from time import sleep
from random import randint
from drgmissions_scraper_utils import (
    IPCServer,
    wait_for_json,
    upload_file,
    yes_or_no,
    enable_system_time,
    disable_system_time,
    maximize_window,
    sanitize_datetime,
    reverse_date_format,
    order_dictionary_by_date,
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
    
    while True:
        port = randint(12345, 65534)
        if not is_port_in_use(port, '127.0.0.1'):
            break
    IPC = IPCServer(port)
    
    with open('./mods/DailyDealsScraper/Scripts/main.lua', 'r') as f:
        main = f.readlines()
        f.close()
    main_lines = []
    for line in main:
        #In case different amount is defined in script
        if 'local total_days' in line:
            total_increments = int(line.split('=')[1].strip())
        if line.startswith('    local port'):
            line = f'    local port = {port}\n'
        main_lines.append(line)
    with open('./mods/DailyDealsScraper/Scripts/main.lua', 'w') as f:
        f.writelines(main_lines)
        f.close()
    
    #Disable automatic system time
    print('Disabling automatic system time...')
    disable_system_time()
    sleep(2)
    
    # Set the clock to 00:00:00
    subprocess.run(['date', reverse_date_format(currytime[0]), '&', 'time', currytime[1]], shell=True)

    #Run Deep Rock Galactic headless
    subprocess.Popen(['start', 'steam://run/548430//'], shell=True)
    
    AllTheDeals = wait_for_json(IPC, total_increments)

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
    print('Enabling automatic system time...')
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