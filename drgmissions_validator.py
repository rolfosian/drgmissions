import json
from datetime import datetime, timedelta
import re

def sort_dictionary(dictionary, custom_order):
    sorted_dict = {}
    for key in custom_order:
        if key in dictionary:
            sorted_dict[key] = dictionary[key]
            del dictionary[key]

    sorted_dict.update(dictionary)
    return sorted_dict

def order_dictionary_by_date(dictionary):
    sorted_keys = sorted(dictionary.keys(), key=lambda x: datetime.fromisoformat(x.replace('Z', '')))
    ordered_dictionary = {}
    for key in sorted_keys:
        ordered_dictionary[key] = dictionary[key]
    return ordered_dictionary

def order_dictionary_by_date_FIRST(dictionary):
    def round_time_down(date_string):
        dt_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        rounded_time = dt_object - timedelta(minutes=dt_object.minute % 30)
        rounded_time = rounded_time.replace(second=0)
        rounded_time_str = rounded_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        return rounded_time_str
    
    sorted_keys = sorted(dictionary.keys(), key=lambda x: datetime.fromisoformat(x.replace('Z', '')))
    ordered_dictionary = {}
    for i, key in enumerate(sorted_keys):
        if i == 0:
            if not re.findall(key[14:16], r'00|30'):
                new_key = round_time_down(key)
                dictionary[new_key] = dictionary[key]
                del dictionary[key]
                key = new_key
        ordered_dictionary[key] = dictionary[key]
    return ordered_dictionary

def reconstruct_dictionary(dictionary):
    god = {}
    list_order = ['PrimaryObjective', 'SecondaryObjective', 'MissionWarnings', 'MissionMutator', 'Complexity', 'Length', 'CodeName', 'id']
    biome_order = ['Glacial Strata', 'Crystalline Caverns', 'Salt Pits', 'Magma Core', 'Azure Weald', 'Sandblasted Corridors', 'Fungus Bogs', 'Radioactive Exclusion Zone', 'Dense Biozone', 'Hollow Bough']
    for key, value in dictionary.items():
        god[key] = {}
        god[key]['timestamp'] = key
        value = sort_dictionary(value, ['Biomes', 'timestamp'])
        for nested_key, nested_value in value.items():
            if nested_key == 'Biomes':
                god[key][nested_key] = sort_dictionary(nested_value, biome_order)
            else:
                pass
    for key, value in god.items():
        for nested_key, nested_value in value.items():
            if nested_key == 'Biomes':
                for biome, missions in nested_value.items():
                    missions1 = []
                    for mission in missions:
                        mission1 = mission
                        if 'MissionWarnings' in mission.keys():
                            for missionkey, missionvalue in mission.items():
                                if isinstance(missionvalue, list):
                                    mission1[missionkey] = sorted(missionvalue)
                        mission1 = sort_dictionary(mission1, list_order)
                        missions1.append(mission1)
                    god[key][nested_key][biome] = missions1

    return god

def find_missing_timestamps(DRG, invalid_keys):
    timestamps = [datetime.fromisoformat(timestamp[:-1]) for timestamp in DRG.keys()]
    expected_diff = timedelta(minutes=30)
    missing_timestamps = []
    
    for i in range(len(timestamps) - 1):
        while timestamps[i + 1] - timestamps[i] > expected_diff:
            missing_timestamps.append(timestamps[i] + expected_diff)
            timestamps[i] += expected_diff
    if missing_timestamps:
        print('Missing timestamps found:')
        for timestamp in missing_timestamps:
            print(timestamp)
            invalid_keys.append(f'{timestamp.isoformat()}Z')
    else:
        print('No missing timestamps found.')

def find_duplicates(dictionary, invalid_keys):
    god = {}
    for key, value in dictionary.items():
        god[key] = json.dumps(value)
    def find_duplicate_strings(dictionary):
        string_count = {}
        for key, value in dictionary.items():
            if value in string_count:
                string_count[value].append(key)
            else:
                string_count[value] = [key]
        duplicate_strings = {value: keys for value, keys in string_count.items() if len(keys) > 1}
        return duplicate_strings
    
    duplicate_strings = find_duplicate_strings(god)
    if duplicate_strings:
        print("Duplicate strings found:")
        for value, keys in duplicate_strings.items():
            print("Keys:", keys)
            for key in keys:
                if key not in invalid_keys:
                    invalid_keys.append(key)
    else:
        print("No duplicate strings found.")

def check_sum_of_missions(dictionary, invalid_keys):
    missions_keys = []
    for key, value in dictionary.items():
        mission_count = 0
        biomes = []
        for biome, missions in value['Biomes'].items():
            biomes.append(biome)
        for biome in biomes:
            mission_count += len(value['Biomes'][biome])
        if mission_count != 19:
            missions_keys.append(key)
            if key not in invalid_keys:
                invalid_keys.append(key)
    if missions_keys:
        print('Invalid number of missions in:')
        for key in missions_keys:
            print(f'Key:{key}')
    else:
        print('No sum of missions outside range.')
        
def check_missions_keys(dictionary, invalid_keys):
    missions_keys = []
    for key, value in dictionary.items():
        biomes = []
        for biome, missions in value['Biomes'].items():
            biomes.append(biome)
        for biome in biomes:
            for mission in value['Biomes'][biome]:
                key_count = len(list(mission.keys()))
                if key_count not in [6, 7, 8]:
                    missions_keys.append(f'{key}: {biome}')
                    if key not in invalid_keys:
                        invalid_keys.append(key)
    if missions_keys:
        print('Invalid number of keys in:')
        for key in missions_keys:
            print(f'Key:{key}')
    else:
        print('No sum of missions keys outside range.')

def check_missions_length_complexity(dictionary, invalid_keys):
    missions_keys = []
    for key, value in dictionary.items():
        biomes = []
        for biome, missions in value['Biomes'].items():
            biomes.append(biome)
        for biome in biomes:
            for mission in value['Biomes'][biome]:
                if mission['Complexity'] == 'Indefinite' or mission['Length'] == 'Indefinite':
                    missions_keys.append(f'{key}: {biome}')
                    if key not in invalid_keys:
                        invalid_keys.append(key)
    if missions_keys:
        print('Indefinite complexity or length for mission(s) in:')
        for key_biome in missions_keys:
            print(f'Key and Biome: {key_biome}')
    else:
        print('No indefinite complexities or lengths found.')

if __name__ == '__main__':
    with open('drgmissionsgod.json', 'r') as f:
        DRG = json.load(f)
        f.close()

    DRG = order_dictionary_by_date_FIRST(DRG)
    DRG = reconstruct_dictionary(DRG)
    
    invalid_keys = []
    
    check_missions_length_complexity(DRG, invalid_keys)
    find_missing_timestamps(DRG, invalid_keys)
    find_duplicates(DRG, invalid_keys)  
    check_sum_of_missions(DRG, invalid_keys)
    check_missions_keys(DRG, invalid_keys)
    input('')