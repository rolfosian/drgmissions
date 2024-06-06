from certifi import where

def when_ready(server):
    from main import join_threads, go_flag, set_signal_handlers, rendering_events, start_threads, M
    import atexit
    from functools import wraps
    from signal import SIGINT, SIGTERM
    from multiprocessing.util import _exit_function
    atexit.unregister(_exit_function)

    def custom_changed_(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for event in rendering_events:
                rendering_events[event].wait()
            join_threads(go_flag)
            M.shutdown()
            atexit.register(_exit_function)
            return func(*args, **kwargs)
        return wrapper

    start_threads()
    server.stop = custom_changed_(server.stop)
    set_signal_handlers(SIGINT, SIGTERM, go_flag)

def post_worker_init(worker):
    from main import go_flag, set_signal_handlers, rendering_events
    from functools import wraps
    from signal import SIGINT, SIGTERM
    # import os
    # from time import sleep

    # def custom_changed(func, self):
    #     @wraps(func)
    #     def wrapper(fname):
    #         for event in rendering_events:
    #             rendering_events[event].wait()
    #         self.log.info("Worker reloading: %s modified", fname)
    #         self.alive = False
    #         os.write(self.PIPE[1], b"1")
    #         self.cfg.worker_int(self)
    #         sleep(0.1)
    #         exit(0)
    #     return wrapper

    # worker.reloader._callback = custom_changed(worker.reloader._callback, worker)
    set_signal_handlers(SIGINT, SIGTERM, go_flag)

worker_class = 'gthread'
threads = 8
bind = '0.0.0.0:5000'

ca_certs = where()
keyfile = None
certfile = None
cert_reqs = 0