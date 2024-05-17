#Automatically run with bat file on system startup
import subprocess
import time
import os
from drgmissions_scraper_utils import (
    upload_file,
    enable_system_time,
    wait_until_next_thursday_11am_utc,
    get_previous_thursday_date,
    kill_process_by_name_starts_with,
    maximize_window,
    subprocess_wrapper,
    print,
)

def main():
    for f in os.listdir():
        if f.startswith('DD_') and f.endswith('.json'):
            os.remove(f)
            
    maximize_window()
    print(os.getcwd())
    
    time_service_query = subprocess_wrapper(['sc', 'query', 'w32time'], print_=False)()
    if 'RUNNING' not in time_service_query:
        enable_system_time()
        time.sleep(2)
    else:
        subprocess_wrapper(['w32tm', '/resync'])()
        
    wait_until_next_thursday_11am_utc()

    with open('./mods/mods.txt', 'w') as f:
        f.write('DeepDivesScraper : 1')
        f.close()
        
    subprocess.Popen(['start', 'steam://run/548430//'], shell=True)

    with open('token.txt') as f:
        token = f.read().strip()

    url = 'https://doublexp.net/upload'
    files = []
    start_time = time.time()
    while True:
        if time.time() - start_time > 300: #Timeout if crash/freeze
            kill_process_by_name_starts_with('FSD')
            kill_process_by_name_starts_with('Unreal')
            time.sleep(3)
            subprocess.Popen(['start', 'steam://run/548430//-nullrhi'], shell=True)
            start_time = time.time()
            continue
        
        for filename in os.listdir():
            if filename.startswith('DD_') and filename.endswith('.json'):
                new_filename = get_previous_thursday_date()+'T11-00-00Z.json'
                while True:
                    try:
                        os.rename(filename, new_filename)
                        break
                    except:
                        continue
                files.append(new_filename)
                kill_process_by_name_starts_with('FSD')
                kill_process_by_name_starts_with('Unreal')
                
        if files:
            for file in files:
                upload_file(url, file, token)
                os.remove(file)
            break
        
        time.sleep(0.5)

    with open('./mods/mods.txt', 'w') as f:
        f.close()

    subprocess.Popen(['shutdown', '/s', '/f', '/t', '0'])

try:
    main()
except Exception as e:
    print(e)
    input('Press enter to exit...')