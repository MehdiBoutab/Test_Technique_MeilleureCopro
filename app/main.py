from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api import router as api_router

app = FastAPI(
    title="API MeilleureCopro",
    description="Statistiques et gestion d’annonces depuis Bienici.com",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(api_router)
