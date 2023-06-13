from glob import glob
def post_worker_init(worker):
    from main import start_threads 
    start_threads()

reload_extra_files = glob('*.json')
reload = True
threads = 12
bind = '127.0.0.1:5000'
