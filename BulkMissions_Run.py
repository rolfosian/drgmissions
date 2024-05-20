import subprocess
import time
import os
from datetime import datetime
from shutil import copy as shutil_copy
import json
import re
from drgmissions_scraper_utils import(
    order_dictionary_by_date_FIRST_KEY_ROUNDING,
    upload_file,
    yes_or_no,
    reconstruct_dictionary,
    disable_system_time,
    enable_system_time,
    format_seconds,
    kill_process_by_name_starts_with,
    user_input_set_target_date,
    validate_drgmissions,
    maximize_window,
    delete_file,
    print,
    cfg
)

def main():
    maximize_window()
    time_service_query = subprocess.check_output('sc query w32time', stderr=subprocess.PIPE, shell=True).decode('utf-8')
    if 'RUNNING' not in time_service_query:
        enable_system_time()
        print('')
        time.sleep(2)
        
    if os.path.isfile('poll.txt'):
        delete_file('poll.txt')
    if os.path.isfile('firstpoll.txt'):
        delete_file('firstpoll.txt')

    #Set mods.txt for BulkMissions collector

    with open('./mods/mods.txt', 'w') as f:
        f.write('BulkMissionsScraper : 1')
        f.close()

    #Get target date from user input
    current_time = datetime.now()
    user_date = user_input_set_target_date(current_time)
            
    target_date_format = user_date.strftime("    local target_date = os.time{year=%Y, month=%m, day=%d, hour=%H, min=%M, sec=%S}\n")
    #Set the target date in the lua script
    with open('./mods/BulkMissionsScraper/Scripts/main.lua', 'r') as f:
        main = f.readlines()
        f.close()
    main_lines = []
    for line in main:
        if line.startswith('    local target_date'):
            line = line.replace(line, target_date_format)
            main_lines.append(line)
        else:
            main_lines.append(line)
            
    with open('./mods/BulkMissionsScraper/Scripts/main.lua', 'w') as f:
        f.writelines(main_lines)
        f.close()
    
    current_utc = datetime.utcnow()
    diff_seconds = (user_date - current_utc).total_seconds()
    total_increments = int(diff_seconds // 1800) + 1
    total_increments_ = int(str(total_increments)) + 1
    estimated_time_completion = (total_increments * 0.5) + 25

    timeout_seconds = (total_increments * 0.7) + 300
    
    #Disable automatic time sync
    disable_system_time()
    print('', include_timestamp=False)
    print(f'Total 30 minute increments: {str(total_increments)}')
    print(f'{format_seconds(timeout_seconds)} until timeout')
    print(f'Estimated time until completion: {format_seconds(estimated_time_completion)}')
    print('', include_timestamp=False)
    time.sleep(1)
    #Run Deep Rock Galactic headless
    subprocess.Popen(['start', 'steam://run/548430//'], shell=True)

    #Wait for JSON
    polls = 0
    poll_switch = False
    avg_poll_time = 1
    files = False
    start_time = None
    elapsed_time = 0
    while True:
        timeout_seconds = (total_increments_ * avg_poll_time) + 300
        if start_time:
            elapsed_time = time.monotonic() - start_time
        
        if poll_switch:
            polls += 1
            avg_poll_time = elapsed_time / polls
            estimated_time_completion =  total_increments * avg_poll_time
            
            total_increments -= 1
            percent = round((total_increments_ - total_increments) / total_increments_ * 100, 2)
            print(f"{percent}% Completed | Elapsed time: {format_seconds(elapsed_time)} | {format_seconds(timeout_seconds - elapsed_time)} until timeout | Estimated time until completion: {format_seconds(estimated_time_completion)}    ", end='\r')
            poll_switch = False

        for filename in os.listdir():
            if filename == 'firstpoll.txt':
                start_time = time.monotonic()
                delete_file('firstpoll.txt')
                break
            
            if filename == 'poll.txt':
                poll_switch = True
                delete_file('poll.txt')
                    
            if filename == 'drgmissionsgod.json':
                files = True
                print(f"{percent}% Completed | Elapsed time: {format_seconds(elapsed_time)} | {format_seconds(timeout_seconds - elapsed_time)} until timeout | Estimated time until completion: {format_seconds(estimated_time_completion)}    ")
                print('Complete. Ending FSD & Unreal processes...')
                time.sleep(3)
                kill_process_by_name_starts_with('FSD')
                kill_process_by_name_starts_with('Unreal')
                break
                
        if files:
            break

        if elapsed_time > timeout_seconds:
            print('')
            print('Timeout... process crashed or froze')
            kill_process_by_name_starts_with('FSD')
            kill_process_by_name_starts_with('Unreal')
            
            start_time = None
            total_increments = int(str(total_increments_))
            polls = 0
            
            if os.path.isfile('poll.txt'):
                delete_file('poll.txt')
            if os.path.isfile('firstpoll.txt'):
                delete_file('firstpoll.txt')
            
            enable_system_time()
            time.sleep(4)
            disable_system_time()
            subprocess.Popen(['start', 'steam://run/548430//'], shell=True)

    if os.path.isfile('poll.txt'):
        delete_file('poll.txt')
        
    #Reset mods.txt
    with open('./mods/mods.txt', 'w') as f:
        f.close()
        
    #Enable automatic time sync
    enable_system_time()

    with open('drgmissionsgod.json', 'r') as f:
        DRG = f.read()
        DRG = re.sub(r':\d{2}Z', ':00Z', DRG)
        DRG = json.loads(DRG)
        f.close()

    DRG = order_dictionary_by_date_FIRST_KEY_ROUNDING(DRG)
    DRG = reconstruct_dictionary(DRG)
    with open('drgmissionsgod.json', 'w') as f:
        json.dump(DRG, f)
    shutil_copy('drgmissionsgod.json', 'drgmissionsgod.json.bak')
    
    
    #Validate JSON
    patched = False
    DRG, patched = validate_drgmissions(DRG, patched)
    if patched:
        with open('drgmissionsgod.json', 'w') as f:
            json.dump(DRG, f)
    
    if yes_or_no('Upload JSON? Y/N: '):
        upload_file(cfg, 'drgmissionsgod.json')
            
if __name__ == '__main__':
    try:
        if os.path.isfile('drgmissionsgod.json'):
            delete_file('drgmissionsgod.json')
        print(os.getcwd(), '\n')
        main()
        input('Press enter to exit...')
    except Exception as e:
        print(f'ERROR: {e}')
        input('Press enter to exit...')