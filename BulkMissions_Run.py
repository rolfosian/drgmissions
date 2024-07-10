import subprocess
import os
import json
from time import sleep
from datetime import datetime
from random import randint
from drgmissions_scraper_utils import (
    IPCServer,
    kill_process_by_name_starts_with,
    order_dictionary_by_date_FIRST_KEY_ROUNDING,
    upload_file,
    yes_or_no,
    reconstruct_dictionary,
    disable_system_time,
    enable_system_time,
    user_input_set_target_date,
    wait_for_json,
    validate_drgmissions,
    flatten_seasons_v5,
    is_port_in_use,
    launch_game,
    hide_window,
    maximize_window,
    delete_file,
    wrap_with_color,
    print,
    cfg
)

def main():
    kill_process_by_name_starts_with('FSD')
    kill_process_by_name_starts_with('Unreal')
    maximize_window()
    time_service_query = subprocess.check_output('sc query w32time', stderr=subprocess.PIPE, shell=True).decode('utf-8')
    if 'RUNNING' not in time_service_query:
        print(wrap_with_color('Enabling automatic system time...', '0;33'))
        enable_system_time()
        sleep(2)

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
    IPC = IPCServer(port)
        
    target_date_format = user_date.strftime("    local target_date = os.time{year=%Y, month=%m, day=%d, hour=%H, min=%M, sec=%S}\n")
    #Set the target date and ipc server port in the lua script
    with open('./mods/BulkMissionsScraper/Scripts/main.lua', 'r') as f:
        main = f.readlines()
        f.close()
    main_lines = []
    for line in main:
        if line.startswith('    local target_date'):
            line = line.replace(line, target_date_format)
        elif line.startswith('    local port'):
            line = f'    local port = {port}\n'
        main_lines.append(line)
            
    with open('./mods/BulkMissionsScraper/Scripts/main.lua', 'w') as f:
        f.writelines(main_lines)
        f.close()
    
    current_utc = datetime.utcnow()
    diff_seconds = (user_date - current_utc).total_seconds()
    total_increments = int(diff_seconds // 1800) + 1

    #Disable automatic time sync
    print(wrap_with_color('Disabling automatic system time...', '0;33'))
    disable_system_time()
    
    #launch game with 'start steam://run/548430//' shell command
    launch_game(IPC)
        
    DRG = wait_for_json(IPC, total_increments)
        
    #Reset mods.txt
    with open('./mods/mods.txt', 'w') as f:
        f.close()
        
    #Enable automatic time sync
    print(wrap_with_color('Enabling automatic system time...', '0;33'))
    enable_system_time()
    
    print(wrap_with_color('Reconstructing JSON...', '40;92'))
    DRG = order_dictionary_by_date_FIRST_KEY_ROUNDING(DRG)
    DRG = reconstruct_dictionary(DRG)
    with open('drgmissionsgod.json.bak', 'w') as f:
        json.dump(DRG, f)
    
    #Validate JSON
    print(wrap_with_color('Validating JSON...', '40;92'))
    DRG = validate_drgmissions(DRG)
    
    print(wrap_with_color('Flattening seasons...', '40;92'))
    DRG = flatten_seasons_v5(DRG)
    with open('drgmissionsgod.json', 'w') as f:
        json.dump(DRG, f)
    
    if yes_or_no('Upload JSON? Y/N: '):
        upload_file(cfg, 'drgmissionsgod.json')
            
if __name__ == '__main__':
    try:
        if os.path.isfile('drgmissionsgod.json'):
            delete_file('drgmissionsgod.json')
        main()
    except Exception as e:
        print(f'ERROR: {e}')