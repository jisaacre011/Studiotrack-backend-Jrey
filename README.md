# StudioTrack — Backend

API para la plataforma de reservas de estudios de grabación StudioTrack.
Hecha con FastAPI y MySQL, maneja el catálogo de salas y las reservas.

El proyecto tiene dos repos:
- Este repo — API con FastAPI
- [studiotrack-frontend](https://github.com/jisaacre011/Studiotrack-frontend-Jrey) — interfaz en Reflex

Demo: https://studiotrack-backend-jrey.onrender.com/docs

## Tecnologías

Python 3, FastAPI, SQLAlchemy, PyMySQL, Pydantic v2, MySQL (Railway), Render.

## Cómo correrlo local

1. Clonar el repo y entrar a la carpeta
2. Crear el entorno virtual: `python -m venv venv`
3. Activarlo: `.\venv\Scripts\activate`
4. Instalar dependencias: `python -m pip install -r requirements.txt`
5. Crear `.env` con tus credenciales (ver `.env.example`)
6. Crear tablas: `python init_db.py`
7. Cargar datos de prueba: `python seed.py`
8. Correr: `python -m uvicorn app.main:app --reload --port 8001`

API disponible en http://localhost:8001 — Swagger en http://localhost:8001/docs

## Estructura

app/
main.py        # entrada principal
config.py      # variables de entorno
database.py    # conexión a MySQL
models.py      # tablas: estudios, equipos, reservas
schemas.py     # validación Pydantic
routers/
estudios.py  # GET /estudios
reservas.py  # POST y GET /reservas
health.py    # GET /health
init_db.py       # crea las tablas (solo se usa una vez)
seed.py          # datos de prueba
Procfile         # arranque en Render


## Créditos

Desarrollado por Juan Isaac
