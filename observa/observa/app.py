from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from observa.api.router import router as api_router
from observa.database.database import Base, engine
from observa.database.models import Source, Detector
from observa.framework.manager import global_manager as manager
from dotenv import load_dotenv
from observa.sources.json_source import JsonSource
import os
import importlib

load_dotenv()

SOURCES_LOCAL_NAME = os.getenv("SOURCES_LOCAL_NAME", "")
SOURCES_LOCAL_PATH = os.getenv("SOURCES_LOCAL_PATH", "")
DETECTOR_LOCAL_NAME = os.getenv("DETECTOR_LOCAL_NAME", "")
DETECTOR_LOCAL_PATH = os.getenv("DETECTOR_LOCAL_PATH", "")

Base.metadata.create_all(bind=engine)

_manager = manager

_names_source = [item.strip() for item in SOURCES_LOCAL_NAME.split(',')]
_paths_source = [item.strip() for item in SOURCES_LOCAL_PATH.split(',')]

for i, value in enumerate(_names_source):
    if not _manager.get_source(value):
        _json = JsonSource(_paths_source[i], None)        
        _manager.register_source(value,_json.load())

_names_detectors = [item.strip() for item in DETECTOR_LOCAL_NAME.split(',')]
_path_detectors = [item.strip() for item in DETECTOR_LOCAL_PATH.split(',')]

for i, value in enumerate(_names_detectors):
    if not _manager.get_detector(value):
        #module_name, class_name = _path_detectors[i].rsplit('.', 1)
        #module = importlib.import_module(module_name)
        #cls = getattr(module, class_name)
        #obj = cls()
        _manager.register_detector(value, _path_detectors[i])

app = FastAPI(title="Observa API + Frontend")
app.include_router(api_router)
app.mount("/static", StaticFiles(directory="observa/static"), name="static")
templates = Jinja2Templates(directory="observa/templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})