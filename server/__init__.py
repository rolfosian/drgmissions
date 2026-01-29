from time import time

from fastapi.params import File
start = time()

from fastapi import FastAPI, Request, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, PlainTextResponse, FileResponse, StreamingResponse

from io import BytesIO
from datetime import datetime, timezone
from shutil import copy as shutil_copy
from drgmissionslib import (
    print,
    open_with_timestamped_write,
    cfg,
    get_previous_thursday_date,
    order_dictionary_by_date,
    round_time,
    shutil,
    subprocess,
)
import os
import json
import threading
import traceback
cwd = os.getcwd()
name = os.name

def get_DD() -> str:
    with open(f"./static/json/DD_{get_previous_thursday_date()}T11-00-00Z.json", "r") as f:
        return json.load(f)
    
def get_current() -> str:
    with open(f"./static/json/bulkmissions_granules/{round_time(datetime.now(tz=timezone.utc), False)}.json".replace(":", "-"), "r") as f:
        return json.load(f)

def get_next() -> str:
    with open(f"./static/json/bulkmissions_granules/{round_time(datetime.now(tz=timezone.utc), True)}.json".replace(":", "-"), "r") as f:
        return json.load(f)

def get_daily_deal() -> str:
    with open("drgdailydeals.json", "r") as f:
        return json.load(f)[datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT00:00:00Z")]

def serialize_json() -> dict:
    # from subprocess import run
    # run(["7z", "x", "drgmissionsgod_serialized_json.7z", "-o./static/json"])

    with open('drgdailydeals.json', 'r') as f:
        AllTheDeals = f.read()
        f.close()
    AllTheDeals = AllTheDeals.replace(':01Z', ':00Z')
    AllTheDeals = json.loads(AllTheDeals)
    AllTheDeals = order_dictionary_by_date(AllTheDeals)

    return AllTheDeals

def create_app(AllTheDeals: dict) -> FastAPI:
    app = FastAPI()
    app.mount("/static", StaticFiles(directory="static"), name="static")

    four_0_four_response = PlainTextResponse(status_code=404, content='<!doctype html><html lang="en"><title>404 Not Found</title><h1>Not Found</h1><p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>')
    four_0_0_response = PlainTextResponse(status_code=400, content='<!doctype html><html lang="en"><title>400 Bad Request</title><h1>Bad Request</h1><p>The server could not understand your request. Please make sure you have entered the correct information and try again.</p>')
    
    home_response = FileResponse(path=f"{cwd}/index.html", media_type="text/html")
    @app.get('/')
    def home():
        return home_response

    #json endpoint
    #eg http://127.0.0.1:5000/json?data=current for current mission metadata
    json_args = {
        'DD': get_DD,
        'current': get_current,
        'next': get_next,
        'dailydeal': get_daily_deal
    }
    @app.get('/json')
    def serve_json(request: Request):
        try:
            return JSONResponse(content=json_args[request.query_params['data']]())
        except:
            return four_0_0_response

    AUTH_TOKEN = cfg['auth_token']


    class FileStorageWrapper:
        def __init__(self, upload_file: UploadFile):
            self.upload_file = upload_file
            self.filename = upload_file.filename

        def save(self, dst):
            with open(dst, "wb") as f:
                f.write(self.upload_file.file.read())

    #Route for deployment of weekly deep dive metadata
    file_parts = {}
    @app.post("/upload")
    async def upload(request: Request, file: UploadFile = File(...)):
        try:
            token = request.headers.get("Authorization")
            if not token or token != f"Bearer {AUTH_TOKEN}":
                return four_0_four_response

            file_ = FileStorageWrapper(file)
            filename = file_.filename

            if filename.endswith(".json") or filename.endswith(".py"):
                file_.save(f"{cwd}/{filename}")
                if filename.startswith("DD"):
                    for f_name in os.listdir(f"{cwd}/static/json"):
                        if f_name.startswith("DD"):
                            os.remove(f"{cwd}/static/json/{f_name}")
                    shutil.copy(f"{cwd}/{filename}", f"{cwd}/static/json/{filename}")
                    
                return JSONResponse(status_code=200, content={"message": "Success"})
            
            file_.save(f"{cwd}/{filename}")
            if filename.endswith('json.7z'):
                subprocess.run(["python3" if os.name == "posix" else "python", f"extract_json.py", filename])
                
            return JSONResponse(status_code=200, content={"message": "Success"})

        except Exception:
            with open_with_timestamped_write("error.log", "a") as f:
                f.write(f"{traceback.format_exc()}\n")
            return four_0_four_response

    @app.get('/test')
    def test():
        return FileResponse(path=f"{cwd}/static/test.html", media_type='text/html')

    return app
