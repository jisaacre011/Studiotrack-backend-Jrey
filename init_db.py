# Script de inicializacion: crea todas las tablas en la base de datos.
# Se ejecuta UNA vez (o tras cambiar modelos). Importa los modelos para
# que SQLAlchemy los registre antes de crear las tablas.
from app.database import Base, engine
from app import models  # noqa: F401  (necesario para registrar los modelos)

print("Creando tablas en la base de datos...")
Base.metadata.create_all(bind=engine)
print("Tablas creadas correctamente.")