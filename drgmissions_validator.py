from drgmissions_scraper_utils import (
    order_dictionary_by_date_FIRST_KEY_ROUNDING,
    reconstruct_dictionary,
    find_duplicates,
    find_missing_timestamps,
    check_missions_keys,
    check_missions_length_complexity,
    check_sum_of_missions
)
import json

if __name__ == '__main__':
    with open('drgmissionsgod.json', 'r') as f:
        DRG = json.load(f)
        f.close()

    DRG = order_dictionary_by_date_FIRST_KEY_ROUNDING(DRG)
    DRG = reconstruct_dictionary(DRG)
    
    invalid_keys = []
    
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