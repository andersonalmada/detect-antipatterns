from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from observa.api.router import router as api_router

app = FastAPI(title="Observa API + Frontend")
app.include_router(api_router)
app.mount("/static", StaticFiles(directory="observa/static"), name="static")
templates = Jinja2Templates(directory="observa/templates")

# Endpoint "/" só precisa renderizar index.html
from fastapi import Request
from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
