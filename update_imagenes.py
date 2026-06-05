# Actualiza las URLs de imagen de estudios existentes sin duplicar datos.
# Busca cada estudio por nombre y solo cambia su imagen_url.
from app.database import SessionLocal
from app import models

# Mapeo nombre -> nueva URL de imagen (CDN directo de Unsplash).
IMAGENES = {
    "Sala Neptuno": "https://images.unsplash.com/photo-1598488035139-bdbb2231ce04?w=800&q=80",
    "Sala Apolo": "https://images.unsplash.com/photo-1525201548942-d8732f6617a0?w=800&q=80",
}

db = SessionLocal()

actualizados = 0
for nombre, url in IMAGENES.items():
    estudio = db.query(models.Estudio).filter(models.Estudio.nombre == nombre).first()
    if estudio:
        estudio.imagen_url = url
        actualizados += 1
        print(f"Actualizada imagen de: {nombre}")
    else:
        print(f"No encontrado: {nombre}")

db.commit()
db.close()
print(f"Listo. {actualizados} estudio(s) actualizado(s).")