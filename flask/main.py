from drgmissionslib import (
    select_timestamp_from_dict,
    render_xp_calc_index, 
    order_dictionary_by_date,
    rotate_biomes,
    rotate_dailydeal,
    rotate_DDs,
    rotate_index,
    rotate_timestamps,
    rotate_timestamp_from_dict,
    wait_rotation,
    class_xp_levels,
    Dwarf
    )
import os
import json
from flask import Flask, request, send_file, jsonify
import threading
from io import BytesIO
# import queue


with open('drgmissionsgod.json', 'r') as f:
    DRG = json.load(f)
    f.close()
    #Remove past timestamps from memory
    select_timestamp_from_dict(DRG, False)

with open('drgdailydeals.json', 'r') as f:
    AllTheDeals = f.read()
    f.close()
AllTheDeals = AllTheDeals.replace(':01Z', ':00Z')
AllTheDeals = json.loads(AllTheDeals)
AllTheDeals = order_dictionary_by_date(AllTheDeals)

#Current and upcoming timestamps rotator
#tstamp = queue.Queue()
tstamp = []
#next_tstamp = queue.Queue()
next_tstamp = []
tstampthread = threading.Thread(target=rotate_timestamps, args=(tstamp, next_tstamp,))

#Daily Deal timestamp rotator
#dailydeal_tstamp = queue.Queue()
dailydeal_tstamp = []
dailydeal_tstampthread = threading.Thread(target=rotate_timestamp_from_dict, args=(AllTheDeals, dailydeal_tstamp, False))

#Daily Deal rotator
#dailydeal = queue.Queue()
dailydeal = []
dailydealthread = threading.Thread(target=rotate_dailydeal, args=(AllTheDeals, dailydeal_tstamp, dailydeal))

#Mission icons rotator
rendering_event = threading.Event()
#currybiomes = queue.Queue()
#nextbiomes = queue.Queue()
currybiomes = []
nextbiomes = []
biomesthread = threading.Thread(target=rotate_biomes, args=(DRG, tstamp, next_tstamp, nextbiomes, currybiomes, rendering_event))

#Deep Dives rotator
#DDs = queue.Queue()
DDs = []
ddsthread = threading.Thread(target=rotate_DDs, args=(DDs,))

#Homepage HTML rotator, md5 hashes once to enable 304 on every 30 minute rollover and the home route doesn't need to render it again for every request and can just send copies
#Clears index event and waits for rendering_event to be set before proceeding and then sets index event to enable homepage requests once more
index_event = threading.Event()
#index_Queue = queue.Queue()
index_Queue = []
index_thread = threading.Thread(target=rotate_index, args=(DRG, rendering_event, tstamp, next_tstamp, index_event, index_Queue))

#Listener that clears the rendering event 1.5 seconds before the 30 minute mission rollover interval so the homepage won't load for clients until the rotators are done rendering the mission icons
wait_rotationthread = threading.Thread(target=wait_rotation, args=(rendering_event, index_event))

def start_threads():
    tstampthread.start()
    
    biomesthread.start()
    
    ddsthread.start()
    
    wait_rotationthread.start()
    
    dailydeal_tstampthread.start()
    dailydealthread.start()
    
    index_thread.start()
    
#def join_threads():
    #tstampthread.join()
    #biomesthread.join()
    #ddsthread.join()
    #wait_rotationthread.join()
    #dailydeal_tstampthread.join()
    #dailydealthread.join()
    #index_thread.join()
    
app = Flask(__name__, static_folder=f'{os.getcwd()}/files')

#Homepage
@app.route('/')
def home():
    index_event.wait()
    if request.headers.get('If-None-Match') == index_Queue[0]['etag']:
        return '', 304
    return send_file(BytesIO(index_Queue[0]['index']), mimetype='text/html', etag=index_Queue[0]['etag'])

#Sends current mission icons, arg format f"?img={Biome.replace(' ', '-')}{mission['id']}" - see rotate_biomes in drgmissionslib.py
@app.route('/png')
def serve_img():
    try:
        mission = currybiomes[0][request.args['img']]
        if request.headers.get('If-None-Match') == mission['etag']:
            return '', 304
        return send_file(BytesIO(mission['rendered_mission'].getvalue()), mimetype='image/png', etag=mission['etag'])
    except:
        return '<!doctype html><html lang=en><title>404 Not Found</title><h1>Not Found</h1><p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>', 404

#Sends upcoming mission icons, arg format f"?img={Biome.replace(' ', '-')}{mission['id']}" - see rotate_biomes in drgmissionslib.py
@app.route('/upcoming_png')
def serve_next_img():
    try:
        mission = nextbiomes[0][request.args['img']]
        if request.headers.get('If-None-Match') == mission['etag']:
            return '', 304
        return send_file(BytesIO(mission['rendered_mission'].getvalue()), mimetype='image/png', etag=mission['etag'])
    except:
        return '<!doctype html><html lang=en><title>404 Not Found</title><h1>Not Found</h1><p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>', 404

#Sends current daily deal image
@app.route('/dailydeal')
def serve_dailydeal_png():
    try:
        if request.headers.get('If-None-Match') == dailydeal[0]['etag']:
            return '', 304
        return send_file(BytesIO(dailydeal[0]['rendered_dailydeal'].getvalue()), mimetype='image/png', etag=dailydeal[0]['etag'])
    except:
        return '<!doctype html><html lang=en><title>404 Not Found</title><h1>Not Found</h1><p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>', 404

#Dictionary endpoints
#jsonify isn't very merciful when it comes to ram use for repeated requests of large dictionaries. It liked to use 300MB+ RAM as it doesn't hash what it serves and likes to keep it in memory up until a point so I took the full mission JSON out
@app.route('/json')
def serve_json():
    try:
        json_args = {
            'DD': DDs[0],
            'current': DRG[tstamp[0]],
            'next': DRG[next_tstamp[0]],
            'dailydeal': AllTheDeals[dailydeal_tstamp[0]]
        }
        return jsonify(json_args[request.args['data']])
    except:
        return '<!doctype html><html lang=en><title>404 Not Found</title><h1>Not Found</h1><p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>', 404   

#Class XP calculator HTML that has its own javascript. The JS doesn't use the below endpoint - it is client side, but there is a link to the endpoint on the page.
xp_calculator_index = render_xp_calc_index()
@app.route('/xp_calculator')
def xp_calc_form():
    if request.headers.get('If-None-Match') == xp_calculator_index['etag']:
        return '', 304
    return send_file(BytesIO(xp_calculator_index['index']), mimetype='text/html', etag=xp_calculator_index['etag'])

#Class XP calculator endpoint
@app.route('/xp_calc')
def xp_calc():
    try:
        class_levels = {
            'engineer' : int(request.args['engineer_level']),
            'scout' : int(request.args['scout_level']),
            'driller' : int(request.args['driller_level']),
            'gunner' : int(request.args['gunner_level']),
        }
        promos = {
            'engineer' : int(request.args['engineer_promos']),
            'scout' : int(request.args['scout_promos']),
            'driller' : int(request.args['driller_promos']),
            'gunner' : int(request.args['gunner_promos']),
        }
        hours_played = int(request.args['hrs'])
        
        
        Engineer = Dwarf(class_levels['engineer'], promos['engineer'])
        Engineer.calculate_class_xp(class_xp_levels)
        
        Scout = Dwarf(class_levels['scout'], promos['scout'])
        Scout.calculate_class_xp(class_xp_levels)
        
        Driller = Dwarf(class_levels['driller'], promos['driller'])
        Driller.calculate_class_xp(class_xp_levels)
        
        Gunner = Dwarf(class_levels['gunner'], promos['gunner'])
        Gunner.calculate_class_xp(class_xp_levels)
        
        total_promotions = sum([Engineer.promotions, Scout.promotions, Driller.promotions, Gunner.promotions])
        player_rank = round((sum([Engineer.total_level/3, Scout.total_level/3, Driller.total_level/3, Gunner.total_level/3])-0.333), 2)
        total_xp = sum([Engineer.xp, Scout.xp, Driller.xp, Gunner.xp])
        if hours_played == 0:
            xp_per_hr = 0
        else:
            xp_per_hr = round(total_xp/hours_played, 2)
        
        values = {
            'engineer_xp' : "{:,}".format(Engineer.xp),
            'driller_xp' : "{:,}".format(Driller.xp),
            'scout_xp' : "{:,}".format(Scout.xp),
            'gunner_xp' : "{:,}".format(Gunner.xp),
            'total_xp' : "{:,}".format(total_xp),
            'total_promotions' : str(total_promotions),
            'player_rank' : str(player_rank),
            'xp_per_hr' : str(xp_per_hr),
            }
        return jsonify(values)
    except Exception as e:
        print(e)
        return '<!doctype html><html lang="en"><title>400 Bad Request</title><h1>Bad Request</h1><p>The server could not understand your request. Please make sure you have entered the correct information and try again.</p>', 400

with open('token.txt', 'r') as f:
    AUTH_TOKEN = f.read().strip()
    f.close()

#Route for deployment of weekly deep dive metadata
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    try:
        token = request.headers.get('Authorization')
        if not token or token != f"Bearer {AUTH_TOKEN}":
            return '<!doctype html><html lang=en><title>404 Not Found</title><h1>Not Found</h1><p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>', 404
        if 'file' not in request.files:
            return "No file in the request", 400
        file_ = request.files['file']
        cwd = os.getcwd()
        filename = file_.filename
        if filename.endswith('.json') or filename.endswith('.py'):
            file_.save(f'{cwd}/{filename}')
        elif filename.endswith('icon.png'):
            file_.save(f'{cwd}/img/{filename}')
        else:
            file_.save(f'{cwd}/files/{filename}')
        response_data = {'message': 'Success'}
        return jsonify(response_data)
    except Exception:
        return '<!doctype html><html lang=en><title>404 Not Found</title><h1>Not Found</h1><p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>', 404

if __name__ == '__main__':
    start_threads()
    app.run(threaded=True, host='127.0.0.1', debug=True, port=5000)
