# Datos de prueba: inserta estudios y equipos para poder probar la API.
# Idempotente basico: no duplica si ya hay estudios.
from app.database import SessionLocal
from app import models

db = SessionLocal()

if db.query(models.Estudio).count() == 0:
    sala_a = models.Estudio(
        nombre="Sala Neptuno",
        descripcion="Estudio de grabacion con tratamiento acustico profesional.",
        tipo="grabacion",
        capacidad=6,
        precio_hora=45.00,
        imagen_url="https://placehold.co/600x400/1a1a24/7F77DD?text=Sala+Neptuno",
        activo=True,
    )
    sala_a.equipos = [
        models.Equipo(nombre="Consola SSL", descripcion="Mesa de mezcla analogica 24 canales", cantidad=1),
        models.Equipo(nombre="Microfono Neumann U87", descripcion="Microfono de condensador", cantidad=2),
    ]

    sala_b = models.Estudio(
        nombre="Sala Apolo",
        descripcion="Sala de ensayo amplia para bandas.",
        tipo="ensayo",
        capacidad=8,
        precio_hora=25.00,
        imagen_url="https://placehold.co/600x400/1a1a24/1D9E75?text=Sala+Apolo",
        activo=True,
    )
    sala_b.equipos = [
        models.Equipo(nombre="Bateria Pearl", descripcion="Bateria acustica completa", cantidad=1),
        models.Equipo(nombre="Amplificador Marshall", descripcion="Cabezal de guitarra 100W", cantidad=2),
    ]

    db.add_all([sala_a, sala_b])
    db.commit()
    print("Datos de prueba insertados.")
else:
    print("Ya existen estudios, no se inserto nada.")

db.close()