from drgmissions_scraper_utils import (
    order_dictionary_by_date_FIRST_KEY_ROUNDING,
    reconstruct_dictionary,
    find_duplicate_seasons,
    find_duplicates,
    find_missing_timestamps,
    check_missions_keys,
    check_missions_length_complexity,
    check_sum_of_missions,
    validate_drgmissions,
    yes_or_no,
    print
)
import json
from os import path, getcwd
cwd = getcwd()

if __name__ == '__main__':
    if path.isfile(cwd+'/drgmissionsgod.json.bak'):
        if yes_or_no('Run on .bak file? Y/N: '):
            filename = 'drgmissionsgod.json.bak'
    else:
        filename = 'drgmissionsgod.json'
        
        with open(filename, 'r') as f:
            DRG = json.load(f)
            f.close()
            
        if path.isfile(cwd+'/FSD-Win64-Shipping.exe'):
            if yes_or_no('Run JSON patcher? Y/N: '):
                patched = False
                DRG, patched = validate_drgmissions(DRG, patched)
                if patched:
                    with open(filename, 'w') as f:
                        json.dump(DRG, f)
                input('Press enter to exit...')
                quit()
        
    with open(filename, 'r') as f:
        DRG = json.load(f)
        f.close()

    DRG = order_dictionary_by_date_FIRST_KEY_ROUNDING(DRG)
    DRG = reconstruct_dictionary(DRG)
    
    invalid_keys = []
    find_duplicate_seasons(DRG, invalid_keys)
    check_missions_length_complexity(DRG, invalid_keys)
    find_missing_timestamps(DRG, invalid_keys)
    find_duplicates(DRG, invalid_keys)  
    check_sum_of_missions(DRG, invalid_keys)
    check_missions_keys(DRG, invalid_keys)
    
    if invalid_keys:
        print('Invalid kv pairs found, writing to log...')
        with open('invalid_timestamps_log.txt', 'w') as f:
            s = ''
            for key, func in invalid_keys:
                s += f'{key} found invalid using {func} function\n'
            f.write(s)
            f.close()
        input('Press enter to exit...')
    else:
        input('No invalid kv pairs found. Press enter to exit...')