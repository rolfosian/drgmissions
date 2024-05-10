#Automatically run with bat file on system wake from sleep via Task Scheduler on On event - Log: System, Source: Microsoft-Windows-Power-Troubleshooter, Event ID: 1
import subprocess
import time
import os
import re
from drgmissions_scraper_utils import (
    upload_file,
    enable_system_time,
    wait_until_next_thursday_11am_utc,
    kill_process_by_name_starts_with,
    maximize_window,
    subprocess_wrapper,
    print,
)

def main():
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
        f.write('dds_fetcher : 1')
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
                new_filename = re.sub(r'\d{2}-\d{2}-\d{2}Z', '11-00-00Z', filename)
                os.rename(filename, new_filename)
                time.sleep(2)
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

    # subprocess.Popen(["rundll32.exe", "powrprof.dll,SetSuspendState", "Sleep"], shell=True)
    subprocess.Popen(['shutdown', '/s', '/f', '/t', '0'])

try:
    main()
except Exception as e:
    print(e)
    input('Press enter to exit...')