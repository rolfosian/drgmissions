#Automatically run with bat file on system wake from sleep via Task Scheduler on On event - Log: System, Source: Microsoft-Windows-Power-Troubleshooter, Event ID: 1
import datetime
import subprocess
import time
import psutil
import os
import requests
import winreg

def upload_file(url, file_path, bearer_token):
    headers = {
        'Authorization': 'Bearer ' + bearer_token
    }

    with open(file_path, 'rb') as file:
        files = {'file': file}
        response = requests.post(url, headers=headers, files=files)
    return response

def enable_system_time():
    try:
        print('-------------------------------------------------------------------------')
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\\CurrentControlSet\\Services\\W32Time\\Parameters', 0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, 'Type', 0, winreg.REG_SZ, 'NTP')
        winreg.CloseKey(key)
        subprocess.run(['sc', 'config', 'w32time', 'start=', 'auto'], shell=True)
        subprocess.run(['net', 'start', 'w32time'], shell=True)
        time.sleep(2)
        subprocess.run(['w32tm', '/resync'], stderr=subprocess.PIPE, shell=True)
        print("Automatic system time enabled.\n-------------------------------------------------------------------------\n")
    except Exception as e:
        print(f"Error: {e}")

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