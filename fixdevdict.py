import json
import re
from drgmissions_scraper_utils import (
    order_dictionary_by_date_FIRST_KEY_ROUNDING,
    reconstruct_dictionary,
)

def compare_dicts(dict1, dict2, ignore_keys):
    dict1_filtered = {k: v for k, v in dict1.items() if k not in ignore_keys}
    dict2_filtered = {k: v for k, v in dict2.items() if k not in ignore_keys}
    return dict1_filtered == dict2_filtered

with open('drgmissionsdev.json', 'r') as f:
    DRG = order_dictionary_by_date_FIRST_KEY_ROUNDING(json.load(f))
    DRG = re.sub(r':\d{2}Z', ':00Z', json.dumps(DRG))
    DRG = json.loads(DRG)
    DRG = reconstruct_dictionary(DRG)

for timestamp, seasons_dict in list(DRG.items()):
    for season, d in list(seasons_dict.items()):
        if season == 's2' or season == 's4' or season == 's5':
            del DRG[timestamp][season]

# seen = {}
# seasons_to_check = ['s1', 's3']

# for j, timestamp in enumerate(DRG):
# if True:
#     timestamp = '2024-06-22T01:00:00Z'
#     for biome in DRG[timestamp]['s1']['Biomes']:
#         for i, mission in enumerate(DRG[timestamp]['s1']['Biomes'][biome]):
#             del DRG[timestamp]['s1']['Biomes'][biome][i]['id']
        
#     for biome in DRG[timestamp]['s3']['Biomes']:
#         for i, mission in enumerate(DRG[timestamp]['s3']['Biomes'][biome]):
#                 del DRG[timestamp]['s3']['Biomes'][biome][i]['id']
                
#     dups_with_diff_codenames = [f'{timestamp}']
#     for biome in DRG[timestamp]['s0']['Biomes']:
#         for i, mission in enumerate(DRG[timestamp]['s0']['Biomes'][biome]):
#                 del DRG[timestamp]['s0']['Biomes'][biome][i]['id']

#         for mission in DRG[timestamp]['s0']['Biomes'][biome]:
            
#             if mission not in DRG[timestamp]['s1']['Biomes'][biome]:
#                 for mission_ in DRG[timestamp]['s1']['Biomes'][biome]:
#                     if compare_dicts(mission, mission_, ignore_keys=['CodeName', 'season']):
#                         mission['season'] = 's0'
#                         mission_['season'] = 's1'
#                         dups_with_diff_codenames.append(' '.join(['-----------\n', str(mission_), '|', biome, '\n', str(mission), '|', biome]))
                        
#             if mission not in DRG[timestamp]['s3']['Biomes'][biome]:
#                 for mission_ in DRG[timestamp]['s3']['Biomes'][biome]:
#                     if compare_dicts(mission, mission_, ignore_keys=['CodeName', 'season']):
#                         mission['season'] = 's0'
#                         mission_['season'] = 's3'
#                         dups_with_diff_codenames.append(' '.join([str(mission_), '|', biome, '\n', str(mission), '|', biome]))
        
#     if len(dups_with_diff_codenames) > 1:
#         for dups in dups_with_diff_codenames:
#             print(dups)
    # if j == 20:
    #     break

 
with open('drgmissionsdev_fixed.json', 'w') as f:
    json.dump(DRG, f)