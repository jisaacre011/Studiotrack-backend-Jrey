# Endpoints de planes. Lectura publica; edicion de precio protegida por admin.
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.auth import verificar_admin

router = APIRouter(prefix="/planes", tags=["planes"])


@router.get("", response_model=list[schemas.PlanOut])
def listar_planes(db: Session = Depends(get_db)):
    return db.query(models.Plan).filter(models.Plan.activo == True).all()


@router.put("/{plan_id}/precio", response_model=schemas.PlanOut)
def actualizar_precio(plan_id: int, payload: schemas.PlanPrecioUpdate,
                      db: Session = Depends(get_db), _: bool = Depends(verificar_admin)):
    plan = db.query(models.Plan).filter(models.Plan.id == plan_id).first()
    if plan is None:
        raise HTTPException(status_code=404, detail="Plan no encontrado")
    plan.precio = payload.precio
    db.commit()
    db.refresh(plan)
    return plans