# Punto de entrada de la API. Por ahora solo monta CORS y un endpoint raiz.
# Los routers se conectan en el Modulo 2.
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings

app = FastAPI(title="StudioTrack API", version="1.0.0")

# CORS: permite que el frontend Reflex consuma la API desde otro origen.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"mensaje": "StudioTrack API operativa"}