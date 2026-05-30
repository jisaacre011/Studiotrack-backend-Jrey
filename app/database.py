# Configuracion de la conexion a MySQL mediante SQLAlchemy.
# El engine se crea una sola vez y se reutiliza en toda la app.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import settings

# pool_pre_ping=True evita errores por conexiones muertas:
# Railway cierra conexiones inactivas y sin esto la primera query tras un rato falla.
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_recycle=280,  # recicla conexiones antes de que Railway las corte (~300s)
)

# Cada request abrira y cerrara su propia sesion.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base de la que heredan todos los modelos ORM.
Base = declarative_base()


def get_db():
    """Dependencia de FastAPI: entrega una sesion y garantiza su cierre."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()