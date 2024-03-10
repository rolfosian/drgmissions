#Automatically run with bat file on system wake from sleep via Task Scheduler on On event - Log: System, Source: Microsoft-Windows-Power-Troubleshooter, Event ID: 1
import subprocess
import time
import os
from drgmissions_scraper_utils import (
    upload_file,
    enable_system_time,
    wait_until_next_hour,
    kill_process_by_name_starts_with
)

def main():
    print(os.getcwd())
    time_service_query = subprocess.check_output('sc query w32time', stderr=subprocess.PIPE, shell=True).decode('utf-8')
    if 'RUNNING' not in time_service_query:
        enable_system_time()
        time.sleep(2)
    else:
        subprocess.run(['w32tm', '/resync'], stderr=subprocess.PIPE, shell=True)
    wait_until_next_hour()

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
                time.sleep(2)
                files.append(filename)
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

    subprocess.Popen(["rundll32.exe", "powrprof.dll,SetSuspendState", "Sleep"], shell=True)

try:
    main()
except Exception as e:
    print(e)
    input('Press enter to exit...')