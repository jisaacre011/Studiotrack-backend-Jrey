# Planes iniciales. El contenido es fijo; el precio luego lo edita el admin.
from app.database import SessionLocal
from app import models

db = SessionLocal()

if db.query(models.Plan).count() == 0:
    planes = [
        models.Plan(nombre="Plan Basico",
                    descripcion="2 horas de estudio + ingeniero de sonido + 1 mezcla final.",
                    precio=120.00),
        models.Plan(nombre="Plan Pro",
                    descripcion="5 horas de estudio + ingeniero + 3 mezclas + masterizacion.",
                    precio=350.00),
        models.Plan(nombre="Plan Premium",
                    descripcion="Dia completo + ingeniero + mezclas ilimitadas + masterizacion + fotos de sesion.",
                    precio=750.00),
    ]
    db.add_all(planes)
    db.commit()
    print("Planes insertados.")
else:
    print("Ya existen planes, no se inserto nada.")

db.close()