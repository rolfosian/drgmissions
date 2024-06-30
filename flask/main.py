from __init__ import SIGINT, SIGTERM, name, create_app, serialize_json

if name == 'nt':
    if __name__ == '__main__':
        app, start_threads, join_threads, set_signal_handlers, go_flag, M, rendering_event = create_app(*serialize_json(), debug=True)
else:
    if __name__ == '__main__':
        debug=True
    else:
        debug=False
        
    app, start_threads, join_threads, set_signal_handlers, go_flag, M, rendering_event = create_app(*serialize_json(), debug=debug)

if __name__ == '__main__':
    print('Starting threads...')
    start_threads()

    print('Setting signal handlers...')
    set_signal_handlers(SIGINT, SIGTERM, go_flag)

    print('Starting server...')
    app.run(threaded=True, host='0.0.0.0', debug=True, port=5000, use_reloader=False)
