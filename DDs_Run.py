#Automatically run with bat file on system wake from sleep via Task Scheduler on On event - Log: System, Source: Microsoft-Windows-Power-Troubleshooter, Event ID: 1
import datetime
import subprocess
import time
import psutil
import os
import requests

def upload_file(url, file_path, bearer_token):
    headers = {
        'Authorization': 'Bearer ' + bearer_token
    }

    with open(file_path, 'rb') as file:
        files = {'file': file}
        response = requests.post(url, headers=headers, files=files)
    return response

def wait_until_next_hour():
    now = datetime.datetime.now()
    if now.hour == 23:
        next_hour = now.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
    else:
        next_hour = now.replace(hour=now.hour + 1, minute=0, second=0, microsecond=0)
    time_to_wait = (next_hour - now).total_seconds()
    time.sleep(time_to_wait + 1)
        
def kill_process_by_name_starts_with(start_string):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'].startswith(start_string):
            print(f"Terminating process: {proc.info['name']} (PID: {proc.info['pid']})")
            proc.kill()
def main():
    print(os.getcwd())
    wait_until_next_hour()

    with open('./mods/mods.txt', 'w') as f:
        f.write('dds_fetcher : 1')
        f.close()
        
    subprocess.Popen(['start', 'steam://run/548430//-nullrhi'], shell=True)

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