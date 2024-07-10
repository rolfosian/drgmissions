import json
from drgmissions_scraper_utils import (
    reconstruct_dictionary,
    sort_dictionary,
    order_dictionary_by_date_FIRST_KEY_ROUNDING,
    # flatten_seasons_v4,
    compare_dicts,
    # round_time_down,
)
from datetime import datetime
import re

def find_duplicates(dictionary):
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
        print("Duplicate timestamps found:")
        for value, keys in duplicate_strings.items():
            print("Keys:", keys)

    else:
        print("No duplicate timestamps found.")

def reconstruct_deep_dive_dictionary(dictionary, num):
    dictionary_ = {}
    for k, v in dictionary.items():
        dictionary_[k] = sort_dictionary(v, ['Deep Dive Normal', 'Deep Dive Elite'])
        for k_, v_ in dictionary_[k].items():
            dictionary_[k][k_] = sort_dictionary(v_, ['Biome', 'CodeName', 'Stages'])
            for k__, v__ in dictionary_[k][k_].items():
                if k__ == 'Stages':
                    stages1 = []
                    for stage in v__:
                        del stage['id']
                        stage1 = sort_dictionary(stage, ['PrimaryObjective', 'SecondaryObjective', 'MissionWarnings', 'MissionMutator', 'Complexity', 'Length', 'CodeName'])
                        stages1.append(stage1)
                    stages1 = sorted(stages1, key=lambda x: x['PrimaryObjective'])
                    dictionary_[k][k_][k__] = stages1
                else:
                    dictionary_[k][k_][k__] = v__
            print(num)
            print('-------------------------')
            print(json.dumps(dictionary_[k][k_], indent=4))
    
    return dictionary_

def compare_dd_dicts(filename1, filename2):
    d1 = None
    d2 = None
    with open(filename1, 'r') as f:
        d1 = json.load(f)
        f.close()

    with open(filename2, 'r') as j:
        d2 = json.load(j)
        j.close()
    d1 = reconstruct_deep_dive_dictionary(d1, 1)
    d2 = reconstruct_deep_dive_dictionary(d2, 2)

    print(compare_dd_dicts.__name__, d1 == d2)
    
# compare_dd_dicts('DD_2024-04-28T10-08-22Z.json', 'DD_2024-04-25T11-00-00Z.json')

def compare_gods():
    # invalid_timestamps = [
    #     '2024-04-13T13:00:00Z',
    #     '2024-04-27T13:30:00Z',
    #     '2024-05-03T05:00:00Z',
    #     '2024-06-18T07:30:00Z',
    #     '2024-06-28T03:30:00Z'
    # ]
    with open('drgmissionsgod.json', 'r') as f:
        DRG = json.load(f)
    with open('drgmissionsdev.json', 'r') as f:
        DRG_NEW = json.load(f)
    
    print(list(DRG.keys())[-1])
    print(list(DRG_NEW.keys())[-1])
        # DRG_NEW = re.sub(r':\d{2}Z', ':00Z', f.read())
        # DRG_NEW = json.loads(DRG_NEW)
        # DRG_NEW = order_dictionary_by_date_FIRST_KEY_ROUNDING(DRG_NEW)

    # DRG = reconstruct_dictionary(DRG)
    # DRG_NEW = reconstruct_dictionary(DRG_NEW)
    # DRG_NEW = {k : v for k, v in DRG_NEW.items() if k not in invalid_timestamps}
    # DRG = {k : v for k, v in DRG.items() if k not in invalid_timestamps}
    
    # for timestamp, seasons_dict in DRG.items():
    #     for season, master in seasons_dict.items():
    #         for biome, missions in master['Biomes'].items():
    #             for mission in missions:
    #                 del mission['id']

    # for timestamp, seasons_dict in DRG_NEW.items():
    #     for season, master in seasons_dict.items():
    #         for biome, missions in master['Biomes'].items():
    #             for mission in missions:
    #                 del mission['id']
    
    for timestamp, master in DRG.items():
        for biome, missions in master['Biomes'].items():
            for mission in missions:
                del mission['id']

    for timestamp, master in DRG_NEW.items():
        del master['RandomSeed']
        for biome, missions in master['Biomes'].items():
            for mission in missions:
                del mission['id']
                del mission['Seed']

    god = {}
    for timestamp in list(DRG_NEW.keys()):
        # if timestamp not in invalid_timestamps:
        if timestamp in DRG:
            god[timestamp] = DRG[timestamp]
        else:
            del DRG_NEW[timestamp]
        
    # for timestamp in invalid_timestamps:
        # print(timestamp)
        # print(json.dumps(god[timestamp]['s4'], indent=4))
        # print(json.dumps(DRG_NEW[timestamp]['s4'], indent=4))
        # print (DRG_NEW[timestamp]['s0'] == DRG[timestamp]['s4'])
        # break
    
    print(compare_gods.__name__, god == DRG_NEW)
    
    # for timestamp, dict_ in god.items():
    #     print(json.dumps(dict_['s0'], indent=2))
        
    # for timestamp, dict_ in DRG_NEW.items():
    #     print(json.dumps(dict_['s0'], indent=2))
    # for timestamp in god:
    #     print(timestamp)
    #     print(json.dumps(DRG_NEW[timestamp], indent=4))
    #     break
    # for timestamp in god:
    #     print(timestamp)
    #     print(json.dumps(god[timestamp], indent=4))
    #     break

# compare_gods()

def comparedeals():
    with open('drgdailydeals.json', 'r') as f:
        dailydealsold = json.load(f)
    with open('drgdailydealsdev.json', 'r') as f:
        dailydealsnew_ = json.load(f)
    dailydealsold = {k: sort_dictionary(v, ['Resource', 'DealType', 'ResourceAmount', 'ChangePercent', 'Credits']) for k, v in dailydealsold.items()}
    dailydealsnew_ = {k: sort_dictionary(v, ['Resource', 'DealType', 'ResourceAmount', 'ChangePercent', 'Credits']) for k, v in dailydealsnew_.items()}
    
    dailydealsnew = {}
    for timestamp in list(dailydealsold.keys()):
        if timestamp in dailydealsnew_:
            dailydealsnew[timestamp] = dailydealsnew_[timestamp]
        else:
            del dailydealsold[timestamp]

    print(comparedeals.__name__, dailydealsnew == dailydealsold)

# comparedeals()

def check_duplicate_seasons():
    with open('drgmissionsdev.json', 'r') as f:
        DRG = order_dictionary_by_date_FIRST_KEY_ROUNDING(json.load(f))
        DRG = re.sub(r':\d{2}Z', ':00Z', json.dumps(DRG))
        DRG = json.loads(DRG)
        DRG = reconstruct_dictionary(DRG)
        
    seen = {}
    for k, v in DRG.items():
        seen[k] = {}
        for season, d in v.items():
            del d['timestamp']
            for biome in d['Biomes'].keys():
                for i, m in enumerate(d['Biomes'][biome]):
                    del d['Biomes'][biome][i]['id']
            seen[k][season] = json.dumps(d, indent=1)

    
    for i, (k, v) in enumerate(seen.items()):
        print(k)
        seent = []
        for season, d in v.items():
            for season_, d_ in v.items():
                if season_ == season:
                    continue
                if d == d_:
                    if [season, season_] in seent or [season_, season] in seent:
                        continue
                    seent.append([season, season_])
                    print( season, '==', season_)
        if i == 10:
            break

# check_duplicate_seasons()

def check_duplicate_missions():
    with open('drgmissionsdev.json', 'r') as f:
        DRG = order_dictionary_by_date_FIRST_KEY_ROUNDING(json.load(f))
        DRG = re.sub(r':\d{2}Z', ':00Z', json.dumps(DRG))
        DRG = json.loads(DRG)
        DRG = reconstruct_dictionary(DRG)
    
    seasons = ['s0', 's1', 's3']
    
    for timestamp in DRG.keys():
        for season in seasons:
            for biome, missions in DRG[timestamp][season]['Biomes'].items():
                seen = []
                for mission in missions:
                    seen.append(mission)
                for mission_ in seen:
                    if compare_dicts(mission_, mission, ignore_keys=['CodeName', 'id']):
                        if mission['CodeName'] == mission_['CodeName']:
                            continue
                        print(mission, '|', biome, '|', 'Season:', season)
                        print(mission_, '|', biome, '|', 'Season:', season)
                        print('--------')

def check_biome_obj_configs():
    with open('drgmissionsdev.json', 'r') as f:
        DRG = order_dictionary_by_date_FIRST_KEY_ROUNDING(json.load(f))
        DRG = re.sub(r':\d{2}Z', ':00Z', json.dumps(DRG))
        DRG = json.loads(DRG)
        DRG = reconstruct_dictionary(DRG)
        
        for timestamp in list(DRG.keys()):
            for season in list(DRG[timestamp].keys()):
                if season == 's2' or season == 's4' or season == 's5':
                    del DRG[timestamp][season]
                    
        seasons = list(list(DRG.items())[1][1].keys())
        timestamps = list(DRG.keys())
        
        for timestamp in timestamps:
            for season in seasons:
                for biome, missions in DRG[timestamp][season]['Biomes'].items():
                    seen = []
                    for mission in missions:
                        try:
                            del mission['id']
                        except:
                            pass
                        for m in missions:
                            try:
                                del m['id']
                            except:
                                pass
                            if compare_dicts(mission, m, ignore_keys=['id']):
                                continue
                            if m['PrimaryObjective'] == mission['PrimaryObjective']:
                                if m['Complexity'] == mission['Complexity'] and m['Length'] == mission['Length']:
                                    if mission in seen or m in seen:
                                        continue
                                    seen.append(m)
                                    seen.append(mission)
                                    
                                    print(timestamp, season, biome)
                                    print(mission, f'\n{str(m)}')
                                    print('---')

# check_biome_obj_configs()