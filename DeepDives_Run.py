#Automatically run with bat file on system startup
import subprocess
import time
import os
import sys
from drgmissions_scraper_utils import (
    yes_or_no,
    upload_file,
    enable_system_time,
    wait_until_next_thursday_11am_utc,
    get_previous_thursday_date,
    kill_process_by_name_starts_with,
    maximize_window,
    hide_window,
    subprocess_wrapper,
    wrap_with_color,
    print,
    cfg
)

def main():
    kill_process_by_name_starts_with('FSD')
    kill_process_by_name_starts_with('Unreal')
    auto = True
    if len(sys.argv) > 1:
        if sys.argv[1].strip() == 'manual':
            auto = False

    for f in os.listdir():
        if f.startswith('DD_') and f.endswith('.json'):
            os.remove(f)
            
    maximize_window()
    
    time_service_query = subprocess_wrapper(['sc', 'query', 'w32time'], print_=False)()
    if 'RUNNING' not in time_service_query:
        print(wrap_with_color('Enabling automatic system time...', '0;33'))
        enable_system_time()
        time.sleep(2)
    else:
        print(wrap_with_color('Resyncing system time in case of drift...','0;33'))
        subprocess_wrapper(['w32tm', '/resync'], print_=False, check_timeout=True)()
    
    if auto:
        wait_until_next_thursday_11am_utc()

    with open('./mods/mods.txt', 'w') as f:
        f.write('DeepDivesScraper : 1')
        f.close()
        
    subprocess.Popen(['start', 'steam://run/548430//'], shell=True)
    hide_window('FSD-Win64-Shipping.exe')

    files = []
    start_time = time.time()
    while True:
        if time.time() - start_time > 300: #Timeout if crash/freeze
            kill_process_by_name_starts_with('FSD')
            kill_process_by_name_starts_with('Unreal')
            time.sleep(3)
            subprocess.Popen(['start', 'steam://run/548430//'], shell=True)
            start_time = time.time()
            # hide_window('FSD-Win64-Shipping.exe')
            continue
        
        for filename in os.listdir():
            if filename.startswith('DD_') and filename.endswith('.json'):
                new_filename = 'DD_'+get_previous_thursday_date()+'T11-00-00Z.json'
                while True:
                    try:
                        os.rename(filename, new_filename)
                        break
                    except:
                        continue
                files.append(new_filename)
                kill_process_by_name_starts_with('FSD')
                kill_process_by_name_starts_with('Unreal')
                break
                
        if files:
            for file in files:
                if auto:
                    upload_file(cfg, file)
                    os.remove(file)
                elif yes_or_no('Upload JSON? Y/N: '):
                    upload_file(cfg, file)
            break
        
        time.sleep(0.5)

    with open('./mods/mods.txt', 'w') as f:
        f.close()
        
    if auto:
        subprocess.Popen(['shutdown', '/s', '/f', '/t', '0'])

try:
    main()
except Exception as e:
    print(e)