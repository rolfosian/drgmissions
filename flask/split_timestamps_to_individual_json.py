import json
import shutil
import os
from datetime import datetime, timedelta
from time import sleep


def extract_days_from_json(json_file_path, num_days):
    with open(json_file_path, 'r') as f:
        data = json.load(f)
    timestamps = {datetime.fromisoformat(key.replace('Z', '')): value for key, value in data.items()}
    current_datetime = datetime.now()

    days_from_now = current_datetime + timedelta(days=num_days)
    relevant_days = {key+'Z': value for key, value in timestamps.items() if current_datetime <= key < days_from_now}
    return relevant_days

def split_json(num_days):
    shutil.rmtree('./static/json/bulkmissions')
    os.mkdir('./static/json/bulkmissions')
    DRG = extract_days_from_json('drgmissionsgod.json', num_days)
    
    for timestamp, dictionary in (DRG.items()):
        fname = timestamp.replace(':','-')
        with open(f'./static/json/bulkmissions/{fname}.json', 'w') as f:
            f.write(json.dumps(dictionary))
            f.close()

def rotate_split_jsons(num_days):
    split_json(num_days)
    while True:
        sleep(num_days*23)
        split_json(num_days)

split_json(3)