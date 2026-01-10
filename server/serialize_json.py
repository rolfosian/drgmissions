import os
import json
from datetime import datetime, timezone
import shutil
from subprocess import run

# Too little vps ram and i cant be bothered refactoring existing code for chunks
# INLINE TRASH

def select_timestamp_from_dict(dictionary, next_):
    current_time = datetime.now(timezone.utc)
    keys = list(dictionary.keys())
    for i in range(len(keys) - 1):
        timestamp = datetime.fromisoformat(keys[i][:-1]+"+00:00")
        next_timestamp = datetime.fromisoformat(keys[i+1][:-1]+"+00:00")
        if current_time > timestamp and current_time < next_timestamp:
            if next_:
                return keys[i+1]
            else:
                return keys[i]
        else:
            try:
                del dictionary[keys[i]]
            except KeyError:
                pass

def split_all_mission_timestamps(DRG):
    if os.path.isdir('/tmp/bulkmissions_granules'):
        while True:
            try:
                shutil.rmtree('/tmp/bulkmissions_granules')
                break
            except:
                pass
    os.mkdir('/tmp/bulkmissions_granules')
    
    for ts, v in DRG.items():
        with open(f'/tmp/bulkmissions_granules/{ts.replace(":", "-")}.json', 'w') as f:
            json.dump(v, f)

def group_by_day_and_split_all(DRG):
    def group_json_by_days(DRG):
        timestamps_dt = [datetime.fromisoformat(ts[:-1]) for ts in DRG.keys()]

        grouped_by_days = {}
        for timestamp in timestamps_dt:
            date = timestamp.date().strftime('%Y-%m-%d')
            if date not in grouped_by_days:
                grouped_by_days[date] = {}
            timestamp = timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
            grouped_by_days[date][timestamp] = DRG[timestamp]

        return grouped_by_days
    def add_daily_deals_to_grouped_json(DRG):
        with open('drgdailydeals.json', 'r') as f:
            AllTheDeals = json.load(f)

            for timestamp, deal in AllTheDeals.items():
                deal['timestamp'] = timestamp
                try:
                    DRG[timestamp.split('T')[0]]['dailyDeal'] = deal
                except:
                    continue
        return DRG
    def split_json_bulkmissions_raw(DRG):
        if os.path.isdir('/tmp/bulkmissions'):
            while True:
                try:
                    shutil.rmtree('/tmp/bulkmissions')
                    break
                except:
                    continue
        os.mkdir('/tmp/bulkmissions')

        for timestamp, dictionary in DRG.items():
            dictionary['ver'] = 5
            fname = timestamp.replace(':','-')
            with open(f'/tmp/bulkmissions/{fname}.json', 'w') as f:
                json.dump(dictionary, f)

    to_split = group_json_by_days(DRG)
    to_split = add_daily_deals_to_grouped_json(to_split)
    split_json_bulkmissions_raw(to_split)


def main():
    path_orig = os.getcwd()
    
    with open('drgmissionsgod.json', 'r') as f:
        print('Loading bulkmissions json...')
        DRG = json.load(f)
        f.close()

    # Remove past timestamps from memory
    t = select_timestamp_from_dict(DRG, False)
    del t

    # split into individual json
    print('Adding daily deals, grouping timestamps by day, and spltting json files for static site...')
    group_by_day_and_split_all(DRG)
    print('Splitting all timestamps...')
    split_all_mission_timestamps(DRG)
    del DRG
    
    os.chdir("/tmp")
    run(['7z', 'a', 'drgmissionsgod_serialized_json.7z', 'bulkmissions', 'bulkmissions_granules'])
    run(['mv', "drgmissionsgod_serialized_json.7z", f"{path_orig}"])
    shutil.rmtree("/tmp/bulkmissions")
    shutil.rmtree("/tmp/bulkmissions_granules")

if __name__ == "__main__":
    if os.name != 'posix':
        input("Unsupported OS. Press enter to exit...")
        quit()
        
    main()