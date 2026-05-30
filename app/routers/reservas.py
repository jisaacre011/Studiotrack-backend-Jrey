# Endpoints de reservas: creacion (publico) y listado (administrativo).
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/reservas", tags=["reservas"])


@router.post("", response_model=schemas.ReservaOut, status_code=201)
def crear_reserva(payload: schemas.ReservaCreate, db: Session = Depends(get_db)):
    # 1. Verificar que el estudio exista y este activo.
    estudio = (
        db.query(models.Estudio)
        .filter(models.Estudio.id == payload.estudio_id, models.Estudio.activo == True)
        .first()
    )
    if estudio is None:
        raise HTTPException(status_code=404, detail="Estudio no disponible")

    # 2. Calcular el total en el servidor (nunca confiar en el cliente).
    total = estudio.precio_hora * payload.duracion_horas

    # 3. Crear la reserva.
    reserva = models.Reserva(
        estudio_id=payload.estudio_id,
        cliente_nombre=payload.cliente_nombre,
        cliente_email=payload.cliente_email,
        cliente_telefono=payload.cliente_telefono,
        fecha=payload.fecha,
        hora_inicio=payload.hora_inicio,
        duracion_horas=payload.duracion_horas,
        metodo_pago=payload.metodo_pago,
        total=total,
        estado="pendiente",
    )
    db.add(reserva)
    db.commit()
    db.refresh(reserva)
    return reserva


@router.get("", response_model=list[schemas.ReservaOut])
def listar_reservas(db: Session = Depends(get_db)):
    # Uso administrativo. Sin autenticacion por ahora (ver advertencia).
    return db.query(models.Reserva).order_by(models.Reserva.created_at.desc()).all()