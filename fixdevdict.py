import json
import re
from drgmissions_scraper_utils import (
    order_dictionary_by_date_FIRST_KEY_ROUNDING,
    reconstruct_dictionary,
)

with open('drgmissionsdev.json', 'r') as f:
    DRG = order_dictionary_by_date_FIRST_KEY_ROUNDING(json.load(f))
    DRG = re.sub(r':\d{2}Z', ':00Z', json.dumps(DRG))
    DRG = DRG.replace('Exterminate ', '')
    DRG = json.loads(DRG)
    DRG = reconstruct_dictionary(DRG)

for timestamp, seasons_dict in list(DRG.items()):
    for season, d in list(seasons_dict.items()):
        if season == 's2' or season == 's4' or season == 's5':
            del DRG[timestamp][season]

# with open('drgmissionsdev_fixed.json', 'w') as f:
#     json.dump(DRG, f)