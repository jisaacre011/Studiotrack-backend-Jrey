# Punto de entrada de la API StudioTrack.
# Monta CORS y conecta todos los routers por dominio.
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import estudios, reservas, health, admin, productos, transacciones, planes

app = FastAPI(title="StudioTrack API", version="1.0.0")

# CORS: permite que el frontend Reflex consuma la API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers por dominio.
app.include_router(health.router)
app.include_router(estudios.router)
app.include_router(reservas.router)
app.include_router(planes.router)  # <-- SOLO EDITÉ ESTO (añadí esta línea)


@app.get("/")
def root():
    return {"mensaje": "StudioTrack API operativa"}