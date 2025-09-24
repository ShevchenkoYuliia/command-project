from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import router 
from app.database import create_db

app = FastAPI()

app.include_router(router)

app.mount("/static", StaticFiles(directory="static"), name="static")
@app.on_event("startup")
def on_startup():
    create_db()
