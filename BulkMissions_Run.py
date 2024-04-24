import subprocess
import time
from time import sleep
import os
from datetime import datetime
import json
import re
from drgmissions_scraper_utils import(
    order_dictionary_by_date_FIRST_KEY_ROUNDING,
    reconstruct_dictionary,
    toggle_system_time,
    enable_system_time,
    format_seconds,
    kill_process_by_name_starts_with,
    user_input_set_target_date,
    validate_drgmissions
)

def main():
    time_service_query = subprocess.check_output('sc query w32time', stderr=subprocess.PIPE, shell=True).decode('utf-8')
    if 'RUNNING' not in time_service_query:
        enable_system_time()
        sleep(2)
    if os.path.isfile('poll.txt'):
        os.remove('poll.txt')
    if os.path.isfile('firstpoll.txt'):
        os.remove('firstpoll.txt')

    #Set mods.txt for BulkMissions collector

    with open('./mods/mods.txt', 'w') as f:
        f.write('long_term_mission_data_collector : 1')
        f.close()

    #Get target date from user input
    current_time = datetime.now()
    user_date = user_input_set_target_date(current_time)
            
    target_date_format = user_date.strftime("    local target_date = os.time{year=%Y, month=%m, day=%d, hour=%H, min=%M, sec=%S}\n")
    #Set the target date in the lua script
    with open('./mods/long_term_mission_data_collector/Scripts/main.lua', 'r') as f:
        main = f.readlines()
        f.close()
    main_lines = []
    for line in main:
        if line.startswith('    local target_date'):
            line = line.replace(line, target_date_format)
            main_lines.append(line)
        else:
            main_lines.append(line)
            
    with open('./mods/long_term_mission_data_collector/Scripts/main.lua', 'w') as f:
        f.writelines(main_lines)
        f.close()
    
    # Calculate the difference in seconds between the current UTC time and the target date
    current_utc = datetime.utcnow()
    diff_seconds = (user_date - current_utc).total_seconds()
    # Calculate the total amount of 30-minute increments between the current time and the target date
    total_increments = int(diff_seconds // 1800) + 1
    total_increments_ = int(str(total_increments)) + 1
    print(f'Total 30 minute increments: {str(total_increments)}')
    estimated_time_completion = (total_increments*1.8)+25

    #Calculate timeout total seconds duration
    timeout_seconds = (total_increments * 1.9) + 300
    print(f'\n{format_seconds(timeout_seconds)} until timeout\n')

    print(f'Estimated time until completion: {format_seconds(estimated_time_completion)}', end='\r')
    
    #Disable automatic time sync
    toggle_system_time()
    sleep(1)
    #Run Deep Rock Galactic headless
    subprocess.Popen(['start', 'steam://run/548430//'], shell=True)

    #Wait for JSON
    polls = 0
    poll_switch = False
    poll_interval = None
    poll_time = None
    files = []
    start_time = None
    while True:
        if poll_switch:
            elapsed_time = time.monotonic() - start_time
            avg_poll_time = elapsed_time / polls
            timeout_seconds = (total_increments * poll_interval) + 300
            estimated_time_completion = total_increments * poll_interval
            total_increments -= 1
            print(f'{format_seconds(timeout_seconds)} until timeout. Estimated time until completion: {format_seconds(estimated_time_completion)}', end='\r')
            poll_switch = False
            
            if time.monotonic() - start_time > timeout_seconds:
                print('')
                print('Timeout... process crashed or froze')
                kill_process_by_name_starts_with('FSD')
                kill_process_by_name_starts_with('Unreal')
                
                start_time = None
                total_increments = int(str(total_increments_))
                polls = 0
                
                if os.path.isfile('poll.txt'):
                    os.remove('poll.txt')
                if os.path.isfile('firstpoll.txt'):
                    os.remove('firstpoll.txt')
                    
                sleep(4)
                subprocess.Popen(['start', 'steam://run/548430//'], shell=True)

        for filename in os.listdir():
            if filename == 'firstpoll.txt':
                start_time = time.monotonic()
                poll_time = time.monotonic()
                while True:
                    try:
                        os.remove('firstpoll.txt')
                        break
                    except:
                        continue
                break
            
            if filename == 'poll.txt':
                polls += 1
                poll_switch = True
                poll_interval = time.monotonic() - poll_time
                poll_time = time.monotonic()
                while True:
                    try:
                        os.remove('poll.txt')
                        break
                    except:
                        continue
                    
            if filename == 'drgmissionsgod.json':
                files.append(filename)
                sleep(5)
                kill_process_by_name_starts_with('FSD')
                kill_process_by_name_starts_with('Unreal')
                break
                
        if files:
            print('\n')
            print(f'Estimated time until completion: {format_seconds(0.00)}')
            print(f'\n---\nElapsed time: {format_seconds(elapsed_time)}               \n---')
            break


    if os.path.isfile('poll.txt'):
        os.remove('poll.txt')
        
    #Reset mods.txt
    with open('./mods/mods.txt', 'w') as f:
        f.close()
        
    #Enable automatic time sync
    toggle_system_time()

    with open('drgmissionsgod.json', 'r') as f:
        DRG = f.read()
        DRG = re.sub(r':\d{2}Z', ':00Z', DRG)
        DRG = json.loads(DRG)
        f.close()

    DRG = order_dictionary_by_date_FIRST_KEY_ROUNDING(DRG)
    DRG = reconstruct_dictionary(DRG)
    with open('drgmissionsgod.json', 'w') as f:
        json.dump(DRG, f)
    
    #Validate JSON
    patched = False
    DRG, patched = validate_drgmissions(DRG, patched)
    if patched:
        with open('drgmissionsgod.json', 'w') as f:
            json.dump(DRG, f)

    return DRG
            
if __name__ == '__main__':
    try:
        if os.path.isfile('drgmissionsgod.json'):
            os.remove('drgmissionsgod.json')
        print(os.getcwd(), '\n')
        main()
        input('Press enter to exit...')
    except Exception as e:
        print(f'ERROR: {e}')
        input('Press enter to exit...')