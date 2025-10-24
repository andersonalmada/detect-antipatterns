from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from observa.api.router import router as api_router
from observa.database import Base, engine
from observa.models import Source, Detector

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Observa API + Frontend")
app.include_router(api_router)
app.mount("/static", StaticFiles(directory="observa/static"), name="static")
templates = Jinja2Templates(directory="observa/templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})