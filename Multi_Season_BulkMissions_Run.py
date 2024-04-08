from BulkMissions_Run import main as BulkMissions_Run
from drgmissions_scraper_utils import user_input_set_target_date, user_input_set_target_seasons
from datetime import datetime
import os
import json

#script is currently defunct, investigation of season toggles ingame required

def combine_gods(gods, seasons):
    god_head = {}
    for timestamp in gods[0][0].keys():
        god_head[timestamp] = {}
        for season in seasons:
            god_head[timestamp][season] = {}
    
    for god, season in gods:
        for timestamp, dictionary in god.items():
            god_head[timestamp][season] = dictionary
    
    return god_head

def main():
    seasons = user_input_set_target_seasons()
    gods = []
    
    #Get target date from user input
    current_time = datetime.now()
    user_date = user_input_set_target_date(current_time)
    
    for season in seasons:
        god_dict = BulkMissions_Run(season, user_date)
        god = (god_dict, season)
        
        gods.append(god)
    
    god_head = combine_gods(gods, seasons)
    with open('drgmissionsgodhead.json', 'w') as f:
        json.dump(god_head, f)
    
    # for timestamp, dictionary in god_head.items():
    #     fname = timestamp.replace(':','-')
    #     with open(f'./json/BulkMissions/{fname}.json', 'w') as f:
    #         json.dump(dictionary, f)
    
if __name__ == '__main__':
    try:
        main()
        input('Press enter to exit...')
    except Exception as e:
        print(f'ERROR: {e}')
        input('Press enter to exit...')