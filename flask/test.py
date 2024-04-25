import threading
from flask import Flask
from signal import SIGINT, SIGTERM, signal
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

def signal_handler_exit(sig, frame, go_flag):
    print(f"Received signal {sig}. Exiting...")
    join_threads(go_flag)
    exit(0)
    
def set_signal_handlers(SIGINT, SIGTERM, go_flag):
    signal(SIGINT, lambda signum, frame: signal_handler_exit(signum, frame, go_flag))
    signal(SIGTERM, lambda signum, frame: signal_handler_exit(signum, frame, go_flag))

from werkzeug._reloader import StatReloaderLoop, reloader_loops
class DummyReloaderLoop(StatReloaderLoop):        
    def trigger_reload(self, filename: str) -> None:
        join_threads(go_flag)
        return super().trigger_reload(filename)
    
reloader_loops['auto'] = DummyReloaderLoop

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    start_threads()
    set_signal_handlers(SIGINT, SIGTERM, go_flag)
    app.run(threaded=True, host='127.0.0.1', debug=True, use_reloader=True, port=5000)