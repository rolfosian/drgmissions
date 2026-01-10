from drgmissions_scraper_utils import (
    os,
    json,
    sleep,
    randint,
    subprocess,
    datetime, 
    timezone,
    handle_exc,
    deepcopy,
    IPCServer,
    kill_process_by_name_starts_with,
    order_dictionary_by_date_FIRST_KEY_ROUNDING,
    upload_file,
    yes_or_no,
    reconstruct_dictionary,
    set_system_time,
    disable_system_time,
    enable_system_time,
    user_input_year_range,
    user_input_set_target_date,
    wait_for_json,
    validate_drgmissions,
    flatten_seasons_v6,
    is_port_in_use,
    launch_game,
    delete_file,
    wrap_with_color,
    print,
    cfg
)

def main():
    kill_process_by_name_starts_with('FSD')
    kill_process_by_name_starts_with('Unreal')
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
    year_range = yes_or_no("Do you want a specific year range for the dataset? Y/N: ")
    if year_range:
        yearly_results = []
        wanted_years = user_input_year_range()
        user_dates = [datetime(year=y, month=1, day=1, tzinfo=timezone.utc) for y in wanted_years]
        
        
        print(wrap_with_color('Disabling automatic system time...', '0;33'))
        disable_system_time()
        
        #Set system clock to start of target start year
        set_system_time(user_dates[0])
        
    else:
        current_time = datetime.now(timezone.utc)
        user_dates = [user_input_set_target_date(current_time)]
        
        print(wrap_with_color('Disabling automatic system time...', '0;33'))
        disable_system_time()
    
    for i in range(len(user_dates)):
        if i == 0 and year_range:
            continue

        while True:
            port = randint(12345, 65534)
            if not is_port_in_use(port, '127.0.0.1'):
                break
        IPC = IPCServer(port)

        target_date_format = user_dates[i].strftime("    local target_date = os.time{year=%Y, month=%m, day=%d, hour=%H, min=%M, sec=%S}\n")
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
        
        current_utc = datetime.now(timezone.utc)
        diff_seconds = (user_dates[i] - current_utc).total_seconds()
        total_increments = int(diff_seconds // 1800) + 1
        
        #launch game with 'start steam://run/548430//' shell command
        launch_game(IPC)
            
        DRG = wait_for_json(IPC, total_increments)
        
        print(wrap_with_color('Reconstructing JSON...', '40;92'))
        DRG = order_dictionary_by_date_FIRST_KEY_ROUNDING(DRG)
        DRG = reconstruct_dictionary(DRG)

        if not year_range:
            #Skipping python Validation for big datasets, I haven't seen any invalid data since before season 5 refactor anyhow. This takes forever because it's full of duplicating and I can't be fucked with optimizing it especially as it's not needed anymore
            print(wrap_with_color('Validating JSON...', '40;92'))
            DRG = validate_drgmissions(DRG)
        
        print(wrap_with_color('Flattening seasons...', '40;92'))
        DRG = flatten_seasons_v6(DRG)
        
        if not year_range:
            print(wrap_with_color("Writing to disk...", "40;92"))
            
            with open('drgmissionsgod.json', 'w') as f:
                json.dump(DRG, f)
            if yes_or_no('Upload JSON? Y/N: '):
                upload_file(cfg, 'drgmissionsgod.json')
                
            print(wrap_with_color('Enabling automatic system time...', '0;33'))
            enable_system_time()
            
            #Reset mods.txt
            with open('./mods/mods.txt', 'w') as f:
                f.close()
            return
                
        else:
            yearly_results.append(deepcopy(DRG))
            del DRG
            print(wrap_with_color(f"{user_dates[i].year-1} Completed...", "40;92"))
            
    print(wrap_with_color("Concatenating years...", "40;92"))
    DRG = {}
    while yearly_results:
        DRG.update(yearly_results.pop(0))
    
    print(wrap_with_color("Writing to disk...", "40;92"))
    with open('drgmissionsgod.json', 'w') as f:
        json.dump(DRG, f)

    print(wrap_with_color('Enabling automatic system time...', '0;33'))
    enable_system_time()
    
    #Reset mods.txt
    with open('./mods/mods.txt', 'w') as f:
        f.close()

if __name__ == '__main__':
    try:
        if os.path.isfile('drgmissionsgod.json'):
            delete_file('drgmissionsgod.json')
        main()
    except Exception as e:
        handle_exc(e)