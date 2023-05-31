from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from src.model.models import Base
from src.config.db import engine

from src.routes.users import router as router_users
from src.routes.products import router as router_products
from src.routes.login import router as router_login

app = FastAPI(debug=True)

app.mount("/static", StaticFiles(directory="src/static"), name="static")

templates = Jinja2Templates(directory="src/templates")
Base.metadata.create_all(bind=engine)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/login", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

app.include_router(router_users, prefix="/users", tags=["users"])
app.include_router(router_products, prefix="/products", tags=["products"])
app.include_router(router_login, prefix="", tags=["login"])
