from certifi import where

def post_worker_init(worker):
    from main import start_threads, join_threads, go_flag, set_signal_handlers
    from signal import signal, SIGINT, SIGTERM, SIG_DFL
    from functools import wraps
    
    def custom_changed(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            join_threads(go_flag)
            signal(SIGINT, SIG_DFL)
            signal(SIGTERM, SIG_DFL)
            return func(*args, **kwargs)
        return wrapper
    worker.reloader._callback = custom_changed(worker.reloader._callback)
    
    start_threads()
    set_signal_handlers(SIGINT, SIGTERM, go_flag)

worker_class = 'gthread'
reload = True
reload_extra_files = ['drgmissionsgod.json', 'drgdailydeals.json']
threads = 8
bind = '127.0.0.1:5000'

ca_certs = where()
keyfile = None
certfile = None
cert_reqs = 0