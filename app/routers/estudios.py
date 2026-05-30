# Endpoints de consulta del catalogo de estudios.
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/estudios", tags=["estudios"])


@router.get("", response_model=list[schemas.EstudioOut])
def listar_estudios(db: Session = Depends(get_db)):
    # Solo devuelve estudios activos para el catalogo publico.
    return db.query(models.Estudio).filter(models.Estudio.activo == True).all()


@router.get("/{estudio_id}", response_model=schemas.EstudioDetalle)
def obtener_estudio(estudio_id: int, db: Session = Depends(get_db)):
    estudio = db.query(models.Estudio).filter(models.Estudio.id == estudio_id).first()
    if estudio is None:
        raise HTTPException(status_code=404, detail="Estudio no encontrado")
    return estudio