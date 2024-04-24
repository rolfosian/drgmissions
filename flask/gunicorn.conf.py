def post_worker_init(worker):
    from main import start_threads, set_signal_handlers, go_flag
    from signal import SIGINT, SIGTERM
    start_threads()
    set_signal_handlers(SIGINT, SIGTERM, go_flag)

worker_class = 'gthread'
reload = False
threads = 8
bind = '127.0.0.1:5000'