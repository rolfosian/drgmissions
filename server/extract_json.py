import os
import shutil
import subprocess
import sys
import traceback

def main():
    filename: str = sys.argv[1]
    
    if os.path.exists("./tmp"):
        shutil.rmtree("./tmp")
        
    os.mkdir("./tmp")
    subprocess.run(["7z", "x", filename, "-o./tmp", "-y"])
    shutil.copytree("./tmp/bulkmissions", "./static/json/bulkmissions")
    shutil.copytree("./tmp/bulkmissions_granules", "./static/json/bulkmissions_granules")
    shutil.rmtree("./tmp")
    os.remove(filename)

main()
