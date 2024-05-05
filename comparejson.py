import json
from drgmissions_scraper_utils import (
    reconstruct_dictionary,
    sort_dictionary,
    order_dictionary_by_date_FIRST_KEY_ROUNDING,
    find_duplicates
)
import re

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

    print(d1 == d2)
    
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
        # DRG_NEW = re.sub(r':\d{2}Z', ':00Z', f.read())
        # DRG_NEW = json.loads(DRG_NEW)
        # DRG_NEW = order_dictionary_by_date_FIRST_KEY_ROUNDING(DRG_NEW)

    DRG = reconstruct_dictionary(DRG)
    DRG_NEW = reconstruct_dictionary(DRG_NEW)
    # DRG_NEW = {k : v for k, v in DRG_NEW.items() if k not in invalid_timestamps}
    # DRG = {k : v for k, v in DRG.items() if k not in invalid_timestamps}
    
    for timestamp, seasons_dict in DRG.items():
        for season, master in seasons_dict.items():
            for biome, missions in master['Biomes'].items():
                for mission in missions:
                    del mission['id']

    for timestamp, seasons_dict in DRG_NEW.items():
        for season, master in seasons_dict.items():
            for biome, missions in master['Biomes'].items():
                for mission in missions:
                    del mission['id']

    god = {}
    for timestamp in list(DRG_NEW.keys()):
        # if timestamp not in invalid_timestamps:
        god[timestamp] = DRG[timestamp]
        
    # for timestamp in invalid_timestamps:
        # print(timestamp)
        # print(json.dumps(god[timestamp]['s4'], indent=4))
        # print(json.dumps(DRG_NEW[timestamp]['s4'], indent=4))
        # print (DRG_NEW[timestamp]['s0'] == DRG[timestamp]['s4'])
        # break
    
    print(god == DRG_NEW)
    
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

    
compare_gods()

# with open('drgmissionsgod.json', 'r') as f:
#     drg = json.load(f)

# timestamp = list(drg.keys())[-1]
# print(timestamp)