import datetime
import subprocess
import time
import psutil
import os
import json
from time import sleep

def kill_process_by_name_starts_with(start_string):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'].startswith(start_string):
            print(f"Terminating process: {proc.info['name']} (PID: {proc.info['pid']})")
            proc.kill()

def increment_datetime(datetime_str):
    year, month, day, hour, min, sec = map(int, datetime_str[:10].split("-") + datetime_str[11:19].split(":"))
    day += 1
    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if month == 2 and year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
        days_in_month[1] = 29
    if day > days_in_month[month - 1]:
        day = day - days_in_month[month - 1]
        month += 1
    if month > 12:
        month = month - 12
        year += 1
    updated_datetime = "{:02d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}Z".format(day, month, year %100, hour, min, sec)
    return updated_datetime

def reverse_date_format(input_date):
    year, month, day = input_date.split('-')
    input_date = f"{day}-{month}-{year}"
    return input_date

print(os.getcwd())

with open('./mods/mods.txt', 'r') as f:
    mods = f.read()
    mods = mods.replace('GetDailyDeal : 0', 'GetDailyDeal : 1')
    f.close()
with open('./mods/mods.txt', 'w') as f:
    f.write(mods)
    f.close()

# Get the current UTC time
current_time = datetime.datetime.utcnow()
current_time = current_time.replace(hour=0, minute=0, second=0, microsecond=0)

# Set the target date
target_date = datetime.datetime(2023, 7, 18, 0, 0, 0)

# Calculate the difference between the target date and the current time
diff_seconds = (target_date - current_time).total_seconds()

# Calculate the total number of 24-hour increments
total_increments = int(diff_seconds // 86400)
# print(total_increments)

# Initialize the count variable
count = 0

AllTheDeals = {}
# Loop for the increments
for i in range(total_increments):
    subprocess.Popen(['start', 'steam://run/548430//-nullrhi'], shell=True)
    timestamp = current_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    waiting_for_json = True
    while waiting_for_json:
        for filename in os.listdir():
            if filename.endsiwth('.json'):
                sleep(0.25)
                with open(filename, 'r') as f:
                    deal = json.loads(f.read())
                AllTheDeals[timestamp] = deal
                os.remove(filename)
                kill_process_by_name_starts_with('FSD')
                kill_process_by_name_starts_with('Unreal')
                waiting_for_json = False
        sleep(0.5)
    current_time = datetime.datetime.strptime(increment_datetime(timestamp), "%d-%m-%yT%H:%M:%SZ")
    current_time = current_time.replace(hour=0, minute=0, second=1)
    newtime = str(current_time).split(' ')
    print(current_time)
    subprocess.run(['date', reverse_date_format(newtime[0]), '& time', newtime[1]])

with open('./mods/mods.txt', 'r') as f:
    mods = f.read()
    mods = mods.replace('GetDailyDeal : 1', 'GetDailyDeal : 0')
    f.close()
with open('./mods/mods.txt', 'w') as f:
    f.write(mods)
    f.close()
    
with open(AllTheDeals) as f:
    f.write(json.dumps(AllTheDeals))
    f.close()