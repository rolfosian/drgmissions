import subprocess
import psutil
import time
from time import sleep
import os

def kill_process_by_name_starts_with(start_string):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'].startswith(start_string):
            print(f"Terminating process: {proc.info['name']} (PID: {proc.info['pid']})")
            proc.kill()

with open('./mods/mods.txt', 'r') as f:
    mods = f.read()
    mods = mods.replace('long_term_mission_data_collector : 0', 'long_term_mission_data_collector : 1')
    f.close()
with open('./mods/mods.txt', 'w') as f:
    f.write(mods)
    f.close()

subprocess.Popen(['start', 'steam://run/548430//-nullrhi'], shell=True)
files = []
while True:
    for filename in os.listdir():
        if filename == 'drgmissionsgod.json':
            time.sleep(10)
            files.append(filename)
            kill_process_by_name_starts_with('FSD')
            kill_process_by_name_starts_with('Unreal')
    if files:
        break
    sleep(1)

with open('./mods/mods.txt', 'r') as f:
    mods = f.read()
    mods = mods.replace('long_term_mission_data_collector : 1', 'long_term_mission_data_collector : 0')

with open('./mods/mods.txt', 'w') as f:
    f.write(mods)
    f.close()