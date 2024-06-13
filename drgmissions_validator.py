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
import sys
import json
from os import path, getcwd
cwd = getcwd()

try:
    if __name__ == '__main__':
        filename = 'drgmissionsgod.json'
        if path.isfile(cwd+'/drgmissionsdev.json'):
            if yes_or_no('Run on dev json? Y/N: '):
                filename = 'drgmissionsdev.json'
             
        if path.isfile(cwd+'/FSD-Win64-Shipping.exe'):
            if yes_or_no('Run JSON patcher? Y/N: '):
                with open(filename, 'r') as f:
                    DRG = json.load(f)
                    f.close()
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
        # find_duplicate_seasons(DRG, invalid_keys)
        find_missing_timestamps(DRG, invalid_keys)
        find_duplicates(DRG, invalid_keys)  
        check_sum_of_missions(DRG, invalid_keys)
        check_missions_keys(DRG, invalid_keys)
        check_missions_length_complexity(DRG)

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
except Exception as e:
    print(e)
    input('')