def post_worker_init(worker):
    from main import start_threads 
    start_threads()

worker_class = 'gthread'
reload_extra_files = ['drgmissionsgod.json']
reload = True
threads = 12
bind = '127.0.0.1:5000'
