import json

DRG = None

with open('drgmissionsgod.json', 'r') as f:
    DRG = json.load(f)
    f.close()

for i, (timestamp, dictionary) in enumerate(DRG.items()):
    fname = timestamp.replace(':','-')
    with open(f'./static/json/bulkmissions/{fname}.json', 'w') as f:
        f.write(json.dumps(dictionary))
        f.close()
    if i == 10:
        break