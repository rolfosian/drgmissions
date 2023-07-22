from drgmissionslib import render_xp_calc_index, order_dictionary_by_date, rotate_biomes, rotate_dailydeal, rotate_DDs, rotate_index, rotate_timestamp, rotate_timestamp_from_dict, wait_rotation, SERVER_READY, class_xp_levels, Dwarf
import os
import json
from flask import Flask, render_template_string, request, send_file, jsonify, make_response
import threading
from io import BytesIO
# import requests
# from time import sleep
# import time 
# import subprocess
# import shutil
# from dateutil import parser
# import queue
# import glob
# import hashlib
# import gc
# import re
# import sys
# from concurrent.futures import ThreadPoolExecutor, as_completed, wait

with open('drgmissionsgod.json', 'r') as f:
    DRG = json.load(f)
    f.close()

with open('drgdailydeals.json', 'r') as f:
    AllTheDeals = f.read()
    f.close()
AllTheDeals = AllTheDeals.replace(':01Z', ':00Z')
AllTheDeals = json.loads(AllTheDeals)
AllTheDeals = order_dictionary_by_date(AllTheDeals)

#tstamp = queue.Queue()
tstamp = []
tstampthread = threading.Thread(target=rotate_timestamp, args=(tstamp, False,))

#next_tstamp = queue.Queue()
next_tstamp = []
next_tstampthread = threading.Thread(target=rotate_timestamp, args=(next_tstamp, True,))

#dailydeal_tstamp = queue.Queue()
dailydeal_tstamp = []
dailydeal_tstampthread = threading.Thread(target=rotate_timestamp_from_dict, args=(AllTheDeals, dailydeal_tstamp, False))

#dailydeal = queue.Queue()
dailydeal = []
dailydealthread = threading.Thread(target=rotate_dailydeal, args=(AllTheDeals, dailydeal_tstamp, dailydeal))

rendering_event = threading.Event()
#currybiomes = queue.Queue()
currybiomes = []
biomesthread = threading.Thread(target=rotate_biomes, args=(DRG, tstamp, currybiomes, rendering_event))

rendering_event_next = threading.Event()
#nextbiomes = queue.Queue()
nextbiomes = []
nextbiomesthread = threading.Thread(target=rotate_biomes, args=(DRG, next_tstamp, nextbiomes, rendering_event_next))

#DDs = queue.Queue()
DDs = []
ddsthread = threading.Thread(target=rotate_DDs, args=(DDs,))

index_event = threading.Event()
#index_Queue = queue.Queue()
index_Queue = []
index_thread = threading.Thread(target=rotate_index, args=(DRG, rendering_event, rendering_event_next, tstamp, next_tstamp, DDs, index_event, index_Queue))

wait_rotationthread = threading.Thread(target=wait_rotation, args=(rendering_event, rendering_event_next, index_event))

SERVER_READY_thread = threading.Thread(target=SERVER_READY, args=(index_event,))

def start_threads():
    tstampthread.start()
    next_tstampthread.start()
    
    biomesthread.start()
    nextbiomesthread.start()
    
    ddsthread.start()
    
    wait_rotationthread.start()
    
    dailydeal_tstampthread.start()
    dailydealthread.start()
    
    index_thread.start()
    
    SERVER_READY_thread.start()
    #GARBAGE_thread.start()
    
#def join_threads():
    #tstampthread.join()
    #next_tstampthread.join()
    #biomesthread.join()
    #nextbiomesthread.join()
    #ddsthread.join()
    #wait_rotationthread.join()
    #dailydeal_tstampthread.join()
    #dailydealthread.join()
    #index_thread.join()
    #SERVER_READY_thread.join()
    #GARBAGE_thread.join()
    
app = Flask(__name__, static_folder=f'{os.getcwd()}/files')

@app.route('/')
def home():
    index_event.wait()
    if request.headers.get('If-None-Match') == index_Queue[0]['etag']:
        return '', 304
    response = make_response(render_template_string(index_Queue[0]['index']))
    response.headers['ETag'] = index_Queue[0]['etag']
    return response

@app.route('/png')
def serve_img():
    img_arg = request.args.get('img')
    try:
        img_arg = img_arg.split('_')
        biomestr = img_arg[0].replace('%20', ' ')
        mission = currybiomes[0][biomestr][img_arg[1]]
        if request.headers.get('If-None-Match') == mission['etag']:
            return '', 304
        return send_file(BytesIO(mission['rendered_mission'].getvalue()), mimetype='image/png', etag=mission['etag'])
    except Exception:
        return '<!doctype html><html lang=en><title>404 Not Found</title><h1>Not Found</h1><p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>', 404

@app.route('/upcoming_png')
def serve_next_img():
    img_arg = request.args.get('img')
    try:
        img_arg = img_arg.split('_')
        biomestr = img_arg[0].replace('%20', ' ')
        mission = nextbiomes[0][biomestr][img_arg[1]]
        if request.headers.get('If-None-Match') == mission['etag']:
            return '', 304
        return send_file(BytesIO(mission['rendered_mission'].getvalue()), mimetype='image/png', etag=mission['etag'])
    except Exception:
        return '<!doctype html><html lang=en><title>404 Not Found</title><h1>Not Found</h1><p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>', 404

@app.route('/dailydeal')
def serve_dailydeal_png():
    try:
        if request.headers.get('If-None-Match') == dailydeal[0]['etag']:
            return '', 304
        return send_file(BytesIO(dailydeal[0]['rendered_dailydeal'].getvalue()), mimetype='image/png', etag=dailydeal[0]['etag'])
    except Exception:
        return '<!doctype html><html lang=en><title>404 Not Found</title><h1>Not Found</h1><p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>', 404

@app.route('/json')
def serve_json():
    json_arg = request.args.get('data')
    try:
        json_args = {
            'DD': DDs[0],
            'current': DRG[tstamp[0]],
            'next': DRG[next_tstamp[0]],
            'dailydeal': AllTheDeals[dailydeal_tstamp[0]]
        }
        return jsonify(json_args[json_arg])
    except Exception:
        return '<!doctype html><html lang=en><title>404 Not Found</title><h1>Not Found</h1><p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>', 404   

xp_calculator_index = render_xp_calc_index()
@app.route('/xp_calculator')
def xp_calc_form():
    if request.headers.get('If-None-Match') == xp_calculator_index['etag']:
        return '', 304
    return send_file(BytesIO(xp_calculator_index['index']), mimetype='text/html', etag=xp_calculator_index['etag'])
    
@app.route('/xp_calc')
def xp_calc():
    try:
        class_levels = {
            'engineer' : int(request.args.get('engineer_level')),
            'scout' : int(request.args.get('scout_level')),
            'driller' : int(request.args.get('driller_level')),
            'gunner' : int(request.args.get('gunner_level')),
        }
        promos = {
            'engineer' : int(request.args.get('engineer_promos')),
            'scout' : int(request.args.get('scout_promos')),
            'driller' : int(request.args.get('driller_promos')),
            'gunner' : int(request.args.get('gunner_promos')),
        }
        hours_played = int(request.args.get('hrs'))
        
        
        Engineer = Dwarf()
        Engineer.level = class_levels['engineer']
        Engineer.promotions = promos['engineer']
        Engineer.calculate_class_xp(class_xp_levels)
        
        Scout = Dwarf()
        Scout.level = class_levels['scout']
        Scout.promotions = promos['scout']
        Scout.calculate_class_xp(class_xp_levels)
        
        Driller = Dwarf()
        Driller.level = class_levels['driller']
        Driller.promotions = promos['driller']
        Driller.calculate_class_xp(class_xp_levels)
        
        Gunner = Dwarf()
        Gunner.level = class_levels['gunner']
        Gunner.promotions = promos['gunner']
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
    app.run(threaded=True, host='127.0.0.1', port=5000)