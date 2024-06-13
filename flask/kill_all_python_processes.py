import psutil

#see line 36 in main.py for why this script exists. im not supporting wangblows, sorry not sorry
def kill_python_processes():
    procs = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'].lower() in ['python', 'python.exe', 'py', 'py.exe', 'python3', 'python3.exe', 'gunicorn']:
                procs.append(proc)
        except (psutil.AccessDenied, psutil.ZombieProcess):
            pass

    for proc in procs:
        print(proc.info)
        proc.kill()

if __name__ == "__main__":
    kill_python_processes()