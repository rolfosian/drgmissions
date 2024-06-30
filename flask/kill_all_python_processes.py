import psutil
import os

# for multiprocessing debugging
def kill_python_processes():
    procs = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'].lower() in ['python', 'python.exe', 'py', 'py.exe', 'python3', 'python3.exe', 'gunicorn']:
                if proc.info['pid'] != os.getpid():
                    procs.append(proc)
        except (psutil.AccessDenied, psutil.ZombieProcess):
            pass

    for proc in procs:
        print(proc.info)
        try:
            proc.kill()
        except:
            pass

if __name__ == "__main__":
    kill_python_processes()