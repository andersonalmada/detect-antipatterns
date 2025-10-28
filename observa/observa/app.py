from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from observa.api.router import router as api_router
from observa.database.database import Base, engine
from observa.database.models import SourceModel, DetectorModel
from observa.framework.manager import global_manager as manager
from dotenv import load_dotenv
from observa.sources.json_source import JsonSource
import os

print("\n####### Observa Framework #######\n")
load_dotenv()
print("Loaded environment variables ...")

SOURCES_LOCAL_NAME = os.getenv("SOURCES_LOCAL_NAME", "")
SOURCES_LOCAL_PATH = os.getenv("SOURCES_LOCAL_PATH", "")
DETECTOR_LOCAL_NAME = os.getenv("DETECTOR_LOCAL_NAME", "")
DETECTOR_LOCAL_PATH = os.getenv("DETECTOR_LOCAL_PATH", "")

Base.metadata.create_all(bind=engine)
print("Database loaded ...")

_manager = manager

_names_source = [item.strip() for item in SOURCES_LOCAL_NAME.split(',')]
_paths_source = [item.strip() for item in SOURCES_LOCAL_PATH.split(',')]

print("\n####### Available sources #######\n")

for i, value in enumerate(_names_source):
    if not _manager.get_source(value):
        _json = JsonSource(_paths_source[i])        
        _manager.register_source(value,_json.load())
        print(value + " - New !!")
    else:
        print(value)
        
for item in set(_manager.list_sources()).symmetric_difference(_names_source):
    print(item)

_names_detectors = [item.strip() for item in DETECTOR_LOCAL_NAME.split(',')]
_path_detectors = [item.strip() for item in DETECTOR_LOCAL_PATH.split(',')]

print("\n####### Available detectors #######\n")

for i, value in enumerate(_names_detectors):
    if not _manager.get_detector(value):
        _manager.register_detector(value, _path_detectors[i])
        print(value + " - New !!")
    else: 
        print(value)

for item in set(_manager.list_detectors()).symmetric_difference(_names_detectors):
    print(item)

app = FastAPI(title="Observa API + Frontend")
app.include_router(api_router)
app.mount("/static", StaticFiles(directory="observa/static"), name="static")
templates = Jinja2Templates(directory="observa/templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

print("\nReady !!!\n")