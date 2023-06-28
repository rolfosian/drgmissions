#This script will throw exception if current hour is 11pm
#Automatically run with bat file on system wake from sleep via Task Scheduler on On event - Log: System, Source: Microsoft-Windows-Power-Troubleshooter, Event ID: 1
import datetime
import subprocess
import time
import psutil
import os
import requests

print(os.getcwd())

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
    next_hour = now.replace(hour=now.hour + 1, minute=0, second=0, microsecond=0)
    time_to_wait = (next_hour - now).total_seconds()
    time.sleep(time_to_wait)
        
def kill_process_by_name_starts_with(start_string):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'].startswith(start_string):
            print(f"Terminating process: {proc.info['name']} (PID: {proc.info['pid']})")
            proc.kill()

wait_until_next_hour()

with open('./mods/mods.txt', 'r') as f:
    mods = f.read()
    mods = mods.replace('dds_fetcher : 0', 'dds_fetcher : 1')
    f.close()
with open('./mods/mods.txt', 'w') as f:
    f.write(mods)
    f.close()
    
subprocess.Popen(['start', 'steam://run/548430//-nullrhi'], shell=True)

with open('token.txt') as f:
    token = f.read().strip()

url = 'https://doublexp.net/upload'
files = []
while True:
    for filename in os.listdir():
        if filename.endswith('.json'):
            time.sleep(2)
            files.append(filename)
            kill_process_by_name_starts_with('FSD')
            kill_process_by_name_starts_with('Unreal')
    if files:
        for file in files:
            upload_file(url, file, token)
            os.remove(file)
        break

with open('./mods/mods.txt', 'r') as f:
    mods = f.read()
    mods = mods.replace('dds_fetcher : 1', 'dds_fetcher : 0')
    f.close()
with open('./mods/mods.txt', 'w') as f:
    f.write(mods)
    f.close()

subprocess.Popen(["rundll32.exe", "powrprof.dll,SetSuspendState", "Sleep"], shell=True)
