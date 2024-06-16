import subprocess
import time
import os
import json
import re
from shutil import copy as shutil_copy
from datetime import datetime
from random import randint
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
    flatten_seasons_v5,
    is_port_in_use,
    init_polling_server,
    shut_down_polling_server,
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

    #Set mods.txt for BulkMissions collector
    with open('./mods/mods.txt', 'w') as f:
        f.write('BulkMissionsScraper : 1')
        f.close()

    #Get target date from user input
    current_time = datetime.now()
    user_date = user_input_set_target_date(current_time)
            
    while True:
        port = randint(12345, 65534)
        if not is_port_in_use(port, '127.0.0.1'):
            break
        
    target_date_format = user_date.strftime("    local target_date = os.time{year=%Y, month=%m, day=%d, hour=%H, min=%M, sec=%S}\n")
    #Set the target date and polling server port in the lua script
    with open('./mods/BulkMissionsScraper/Scripts/main.lua', 'r') as f:
        main = f.readlines()
        f.close()
    main_lines = []
    for line in main:
        if line.startswith('    local target_date'):
            line = line.replace(line, target_date_format)
        elif line.startswith('    local PollingClient'):
            line = f'    local PollingClient = utils.ConnectPollClient({port})\n'
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
    
    DRG = []
    polling_list = []
    server_socket, accept_thread = init_polling_server(polling_list, DRG, port)

    #Wait for JSON
    polls = 0
    avg_poll_time = 1
    start_time = None
    elapsed_time = 0
    while True:
        try:
            polling_list.pop(0)
            start_time = time.monotonic()
            break
        except:
            pass

    while True:
        timeout_seconds = (total_increments_ * avg_poll_time) + 300
        
        try:
            poll = polling_list.pop(0)
            elapsed_time = time.monotonic() - start_time
            polls += 1
            avg_poll_time = elapsed_time / polls
            estimated_time_completion =  total_increments * avg_poll_time
            total_increments -= 1
            percent = round((total_increments_ - total_increments) / total_increments_ * 100, 2)
            print(f"{percent:.2f}% Completed | Elapsed time: {format_seconds(elapsed_time)} | {format_seconds(timeout_seconds - elapsed_time)} until timeout | Estimated time until completion: {format_seconds(estimated_time_completion)}    ", end='\r')
            if poll == 'fin':
                DRG = json.loads(re.sub(r':\d{2}Z', ':00Z', ''.join(DRG)))
                print('Complete. Ending FSD & Unreal processes...')
                kill_process_by_name_starts_with('FSD')
                kill_process_by_name_starts_with('Unreal')
                break
        
        except:
            if elapsed_time > timeout_seconds:
                print('', include_timestamp=False)
                print('Timeout... process crashed or froze')
                kill_process_by_name_starts_with('FSD')
                kill_process_by_name_starts_with('Unreal')
                
                shut_down_polling_server(server_socket, accept_thread)
                DRG = []
                polling_list = []
                server_socket, accept_thread = init_polling_server(polling_list, DRG, port)
                
                total_increments = int(str(total_increments_))
                polls = 0
                
                enable_system_time()
                time.sleep(4)
                disable_system_time()
                subprocess.Popen(['start', 'steam://run/548430//'], shell=True)
                while True:
                    try:
                        polling_list.pop(0)
                        start_time = time.monotonic()
                        break
                    except:
                        pass
    
    shut_down_polling_server(server_socket, accept_thread)
        
    #Reset mods.txt
    with open('./mods/mods.txt', 'w') as f:
        f.close()
        
    #Enable automatic time sync
    enable_system_time()

    DRG = order_dictionary_by_date_FIRST_KEY_ROUNDING(DRG)
    DRG = reconstruct_dictionary(DRG)
    with open('drgmissionsgod.json', 'w') as f:
        json.dump(DRG, f)
    shutil_copy('drgmissionsgod.json', 'drgmissionsgod.json.bak')
    
    
    #Validate JSON
    patched = False
    DRG, patched = validate_drgmissions(DRG, patched)
    
    DRG = flatten_seasons_v5(DRG)
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