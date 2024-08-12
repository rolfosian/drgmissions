from time import time
start = time()
from signal import getsignal, signal, SIGINT, SIGTERM, SIG_DFL
from functools import wraps
from flask import Flask, request, send_file, jsonify
from io import BytesIO
from shutil import copy as shutil_copy
from drgmissionslib import (
    print,
    open_with_timestamped_write,
    cfg,
    class_xp_levels,
    select_timestamp_from_dict,
    flatten_seasons_v5,
    split_all_mission_timestamps,
    load_individual_mission_timestamp,
    group_by_day_and_split_all,
    order_dictionary_by_date,
    render_xp_calc_index,
    rotate_timestamps,
    rotate_timestamp_from_dict,
    rotate_dailydeal,
    rotate_biomes,
    rotate_DDs,
    rotate_index,
    get_mission_icon_suffix_for_rpng_endpoint,
    wait_rotation,
    GARBAGE,
    SERVER_READY,
    merge_parts,
    get_process_name,
    Dwarf,
    )
import os
import json
import threading
cwd = os.getcwd()
name = os.name

def serialize_json():
    with open('drgmissionsgod.json', 'r') as f:
        print('Loading bulkmissions json...')
        DRG = json.load(f)
        f.close()

    for k in DRG:
        if 's0' in DRG[k].keys():
            # merge season branches to one
            print('Merging seasons...')
            DRG = flatten_seasons_v5(DRG)
        break
    # Remove past timestamps from memory
    t = select_timestamp_from_dict(DRG, False)
    del t

    # split into individual json
    print('Adding daily deals, grouping timestamps by day, and spltting json files for static site...')
    group_by_day_and_split_all(DRG)
    print('Splitting all timestamps...')
    split_all_mission_timestamps(DRG)
    del DRG

    with open('drgdailydeals.json', 'r') as f:
        AllTheDeals = f.read()
        f.close()
    AllTheDeals = AllTheDeals.replace(':01Z', ':00Z')
    AllTheDeals = json.loads(AllTheDeals)
    AllTheDeals = order_dictionary_by_date(AllTheDeals)

    return AllTheDeals

def create_app(AllTheDeals, start=start, debug=False):
    if os.cpu_count() >= 4:
        from multiprocessing import Manager, Event
    else:
        from threading import Event
        if get_process_name() == 'gunicorn':
            from multiprocessing import Manager
        else:
            class Manager:
                def list(self):
                    return []
                def shutdown(self):
                    return

    M = Manager()
    rendering_event = Event()

    threads = []
    go_flag = threading.Event()
    go_flag.set()

    # Current and upcoming timestamps rotator
    tstamp = M.list()
    next_tstamp = M.list()
    threads.append(threading.Thread(target=rotate_timestamps, args=(tstamp, next_tstamp, go_flag)))

    # Daily Deal timestamp rotator
    dailydeal_tstamp = M.list()
    threads.append(threading.Thread(target=rotate_timestamp_from_dict, args=(AllTheDeals, dailydeal_tstamp, False, go_flag)))

    # Daily Deal rotator
    dailydeal = M.list()
    threads.append(threading.Thread(target=rotate_dailydeal, args=(AllTheDeals, dailydeal_tstamp, dailydeal, go_flag)))

    currybiomes = M.list()
    nextbiomes = M.list()
    threads.append(threading.Thread(target=rotate_biomes, args=(tstamp, next_tstamp, nextbiomes, currybiomes, rendering_event, go_flag)))

    # Deep Dives rotator
    DDs = M.list()
    threads.append(threading.Thread(target=rotate_DDs, args=(DDs, go_flag)))

    # Homepage HTML rotator, md5 hashes once to enable 304 on every 30 minute rollover and the home route doesn't need to render it again for every request and can just send copies
    # Clears index event and waits for rendering_event to be set before proceeding and then sets index event to enable homepage requests once more
    # old index is obsolete but i keep the rotator running witb bare event logic just in case
    index_event = threading.Event()
    index_Queue = M.list()
    threads.append(threading.Thread(target=rotate_index, args=(rendering_event, tstamp, next_tstamp, index_event, index_Queue, go_flag)))

    # Obsolete but kept the index event and rotation stuff just cause im not going to fix what isnt broken and i cant be bothered rewriting more stuff
    # Listener that clears the rendering event 1.5 seconds before the 30 minute mission rollover interval so the homepage won't load for clients until the rotators are done rendering the mission icons
    threads.append(threading.Thread(target=wait_rotation, args=(rendering_event, index_event, go_flag)))

    # threads.append(threading.Thread(target=GARBAGE, args=(DRG, go_flag)))
    threads.append(threading.Thread(target=SERVER_READY, args=(index_event, start)))

    def start_threads():
        for thread in threads:
            thread.start()

    def join_threads(go_flag):
        go_flag.clear()
        for thread in threads:
            thread.join()

    def set_signal_handlers(SIGINT, SIGTERM, go_flag, print_=True):
        sigs = {
            2: "SIGINT",
            15: "SIGTERM"
        }
        def handler_wrapper(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if print_:
                    print(f'Received Signal {sigs[args[0]]}. Shutting down...')
                rendering_event.wait()
                index_event.wait()
                join_threads(go_flag)
                M.shutdown()
                return func(*args, **kwargs)
            return wrapper

        sigint_handler = getsignal(SIGINT)
        sigterm_handler = getsignal(SIGTERM)

        wrapped_sigint_handler = handler_wrapper(sigint_handler)
        wrapped_sigterm_handler = handler_wrapper(sigterm_handler)

        signal(SIGINT, wrapped_sigint_handler)
        signal(SIGTERM, wrapped_sigterm_handler)


    if debug:
        # reloader override for flask debug server so it doesnt lock up on reload
        from werkzeug._reloader import StatReloaderLoop, reloader_loops
        class ReloaderLoop_(StatReloaderLoop):
            def trigger_reload(self, filename: str) -> None:
                rendering_event.wait()
                index_event.wait()
                join_threads(go_flag)
                M.shutdown()
                return super().trigger_reload(filename)
            def restart_with_reloader(self) -> int:
                rendering_event.wait()
                index_event.wait()
                signal(SIGINT, SIG_DFL)
                signal(SIGTERM, SIG_DFL)
                join_threads(go_flag)
                M.shutdown()
                return super().restart_with_reloader()

        reloader_loops['auto'] = ReloaderLoop_

    app = Flask('drgmissions', static_folder='./static')

    #Homepage
    @app.route('/')
    def home():
        return send_file(f'{cwd}/index.html', mimetype='text/html')

    # Sends current mission icons, arg format f"?img={mission['CodeName'].replace(' ', '-')}{mission['id']}" - see rotate_biomes in drgmissionslib.py
    # eg http://127.0.0.1:5000/png?img=Spiked-Shelter42069 (mission['CodeName'] is 'Spiked Shelter' and mission['id'] is 42069)
    @app.route('/png')
    def serve_img():
        try:
            mission = currybiomes[0][request.args['img']]
            return send_file(BytesIO(mission['rendered_mission'].getvalue()), mimetype='image/png', etag=mission['etag'])
        except:
            return '<!doctype html><html lang=en><title>404 Not Found</title><h1>Not Found</h1><p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>', 404

    @app.route('/rpng')
    def serve_random_img():
        try:
            mission = currybiomes[0][get_mission_icon_suffix_for_rpng_endpoint(load_individual_mission_timestamp(tstamp[0]))]
            return send_file(BytesIO(mission['rendered_mission'].getvalue()), mimetype='image/png', etag=mission['etag'])
        except:
            return '<!doctype html><html lang=en><title>404 Not Found</title><h1>Not Found</h1><p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>', 404

    # Sends upcoming mission icons, arg format f"?img={Biome.replace(' ', '-')}{mission['CodeName'].replace(' ', '-')}{mission['id']}" - see rotate_biomes in drgmissionslib.py
    # eg http://127.0.0.1:5000/upcoming_png?img=Spiked-Shelter42069 (mission['CodeName'] is 'Spiked Shelter' and mission['id'] is 42069)
    @app.route('/upcoming_png')
    def serve_next_img():
        try:
            mission = nextbiomes[0][request.args['img']]
            return send_file(BytesIO(mission['rendered_mission'].getvalue()), mimetype='image/png', etag=mission['etag'])
        except:
            return '<!doctype html><html lang=en><title>404 Not Found</title><h1>Not Found</h1><p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>', 404

    #Sends current daily deal image
    @app.route('/dailydeal')
    def serve_dailydeal_png():
        try:
            return send_file(BytesIO(dailydeal[0]['rendered_dailydeal'].getvalue()), mimetype='image/png', etag=dailydeal[0]['etag'])
        except:
            return '<!doctype html><html lang=en><title>404 Not Found</title><h1>Not Found</h1><p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>', 404

    #json endpoint
    #eg http://127.0.0.1:5000/json?data=current for current mission metadata
    @app.route('/json')
    def serve_json():
        try:
            json_args = {
                'DD': DDs[0],
                'current': load_individual_mission_timestamp(tstamp[0]),
                'next': load_individual_mission_timestamp(next_tstamp[0]),
                'dailydeal': AllTheDeals[dailydeal_tstamp[0]]
            }
            return jsonify(json_args[request.args['data']])
        except:
            return '<!doctype html><html lang=en><title>404 Not Found</title><h1>Not Found</h1><p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>', 404

    #Class XP calculator HTML that has its own javascript. The JS doesn't use the below endpoint - it is client side, but there is a link to the endpoint on the page.
    xp_calculator_index = render_xp_calc_index()
    @app.route('/xp_calculator')
    def xp_calc_form():
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

    AUTH_TOKEN = cfg['auth_token']

    #Route for deployment of weekly deep dive metadata
    file_parts = {}
    @app.route('/upload', methods=['GET', 'POST'])
    def upload():
        try:
            token = request.headers.get('Authorization')
            if not token or token != f"Bearer {AUTH_TOKEN}":
                return '<!doctype html><html lang=en><title>404 Not Found</title><h1>Not Found</h1><p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>', 404
            if 'file' not in request.files:
                return "No file in the request", 400

            file_ = request.files['file']
            filename = file_.filename

            if filename.endswith('_part'):
                actual_filename = filename.split('.json')[0]+'.json'
                if actual_filename not in file_parts:
                    file_parts[actual_filename] = []

                if filename.endswith('last_part'):
                    file_.save(f'{cwd}/{filename}')
                    file_parts[actual_filename].append(filename)

                    merge_parts(file_parts[actual_filename], actual_filename)
                    del file_parts[actual_filename]

                    response_data = {'message': 'Success'}
                    return jsonify(response_data)

                else:
                    file_.save(f'{cwd}/{filename}')
                    file_parts[actual_filename].append(filename)

            elif filename.endswith('.json') or  filename.endswith('.py'):
                file_.save(f'{cwd}/{filename}')
                if filename.startswith('DD'):
                    for f in os.listdir(f"{cwd}/static/json"):
                        if f.startswith('DD'):
                            os.remove(f"{cwd}/static/json/{f}")
                    shutil_copy(f'{cwd}/{filename}', f'{cwd}/static/json/{filename}')

            elif filename.endswith('icon.png'):
                file_.save(f'{cwd}{filename}')

            else:
                file_.save(f'{cwd}/{filename}')

            response_data = {'message': 'Success'}
            return jsonify(response_data)
        except Exception as e:
            with open_with_timestamped_write('error.log', 'a') as f:
                f.write(f'{e}\n')
            return '<!doctype html><html lang=en><title>404 Not Found</title><h1>Not Found</h1><p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>', 404

    @app.route('/test')
    def test():
        return send_file(f"{cwd}/static/test.html", mimetype='text/html')

    return app, start_threads, join_threads, set_signal_handlers, go_flag, M, rendering_event
