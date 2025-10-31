from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from observa.api.router import router as api_router
from observa.framework.orchestrator import global_orchestrator as orchestrator

orchestrator.load()

app = FastAPI(title="Observa API + Frontend")
app.include_router(api_router)
app.mount("/static", StaticFiles(directory="observa/static"), name="static")
templates = Jinja2Templates(directory="observa/templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})