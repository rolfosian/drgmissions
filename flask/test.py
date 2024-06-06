import threading
from functools import wraps
from flask import Flask
from signal import SIGINT, SIGTERM, SIG_DFL, getsignal, signal
from time import sleep

go_flag = threading.Event()
go_flag.set()

def dummy(go_flag):
    print('starting')
    while go_flag.is_set():
        sleep(0.2)
    print('closing')

threads = [threading.Thread(target=dummy, args=(go_flag,)) for _ in range(10)]

def start_threads():
    for thread in threads:
        thread.start()
        
def join_threads(go_flag):
    go_flag.clear()
    for thread in threads:
        thread.join()

def set_signal_handlers(SIGINT, SIGTERM, go_flag):
    def handler_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # print('Joining threads...')
            join_threads(go_flag)
            return func(*args, **kwargs)
        return wrapper

    sigint_handler = getsignal(SIGINT)
    sigterm_handler = getsignal(SIGTERM)
    
    wrapped_sigint_handler = handler_wrapper(sigint_handler)
    wrapped_sigterm_handler = handler_wrapper(sigterm_handler)
    
    signal(SIGINT, wrapped_sigint_handler)
    signal(SIGTERM, wrapped_sigterm_handler)

from werkzeug._reloader import StatReloaderLoop, reloader_loops
class DummyReloaderLoop(StatReloaderLoop):
    def trigger_reload(self, filename: str) -> None:
        join_threads(go_flag)
        return super().trigger_reload(filename)
    def restart_with_reloader(self) -> int:
        signal(SIGINT, SIG_DFL)
        signal(SIGTERM, SIG_DFL)
        return super().restart_with_reloader()
        
reloader_loops['auto'] = DummyReloaderLoop

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    start_threads()
    set_signal_handlers(SIGINT, SIGTERM, go_flag)
    app.run(threaded=True, host='127.0.0.1', debug=True, use_reloader=True, port=5000)