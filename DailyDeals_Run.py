from drgmissions_scraper_utils import (
    os,
    json,
    sleep,
    randint,
    subprocess,
    datetime, 
    timezone,
    IPCServer,
    handle_exc,
    kill_process_by_name_starts_with,
    wait_for_json,
    upload_file,
    yes_or_no,
    enable_system_time,
    disable_system_time,
    set_system_time,
    maximize_window,
    launch_game,
    sanitize_datetime,
    order_dictionary_by_date,
    is_port_in_use,
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
    
    #Set mods.txt for GetDailyDeals
    with open('./mods/mods.txt', 'w') as f:
        f.write('DailyDealsScraper : 1')
        f.close()

    # Get the current UTC date
    current_time = datetime.now(timezone.utc)
    current_time = current_time.replace(hour=0, minute=0, second=0)
    currytime = current_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    currytime = datetime.strptime(sanitize_datetime(currytime), "%d-%m-%yT%H:%M:%SZ")
    currytime = currytime.replace(tzinfo=timezone.utc, hour=0, minute=0, second=0)
    
    total_increments = 365
    
    while True:
        port = randint(12345, 65534)
        if not is_port_in_use(port, '127.0.0.1'):
            break
    IPC = IPCServer(port)
    
    with open('./mods/DailyDealsScraper/Scripts/main.lua', 'r') as f:
        main = f.readlines()
        f.close()
    main_lines = []
    for line in main:
        #In case different amount is defined in script
        if 'local total_days' in line:
            total_increments = int(line.split('=')[1].strip())
            
        if line.startswith('    local port'):
            line = f'    local port = {port}\n'
        main_lines.append(line)
        
    with open('./mods/DailyDealsScraper/Scripts/main.lua', 'w') as f:
        f.writelines(main_lines)
        f.close()
    
    #Disable automatic system time
    print(wrap_with_color('Disabling automatic system time...', '0;33'))
    disable_system_time()
    
    # Set the clock to 00:00:00
    set_system_time(currytime)

    #launch game with 'start steam://run/548430//' shell command
    launch_game(IPC)

    AllTheDeals = wait_for_json(IPC, total_increments)

    #Reset mods.txt
    with open('./mods/mods.txt', 'w') as f:
        f.close()
        
    AllTheDeals = order_dictionary_by_date(AllTheDeals)

    #Write AllTheDeals JSON
    with open('drgdailydeals.json', 'w') as f:
        json.dump(AllTheDeals, f)
    
    #Enable Automatic system time
    print(wrap_with_color('Enabling automatic system time...', '0;33'))
    enable_system_time()
    
    if yes_or_no('Upload JSON? Y/N: '):
        upload_file(cfg, 'drgdailydeals.json')

try:
    if os.path.isfile('drgdailydeals.json'):
        delete_file('drgdailydeals.json')
    main()
except Exception as e:
    handle_exc(e)