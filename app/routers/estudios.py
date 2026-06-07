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

# Cuenta cuantas reservas tiene un estudio. Util para vista administrativa.
@router.get("/{estudio_id}/reservas/count")
def contar_reservas(estudio_id: int, db: Session = Depends(get_db)):
    estudio = db.query(models.Estudio).filter(models.Estudio.id == estudio_id).first()
    if estudio is None:
        raise HTTPException(status_code=404, detail="Estudio no encontrado")
    total = db.query(models.Reserva).filter(models.Reserva.estudio_id == estudio_id).count()
    return {"estudio_id": estudio_id, "total_reservas": total}

# Al inicio del archivo, junto a los otros imports, agrega:
from app.auth import verificar_admin


# --- Operaciones de administrador (protegidas con clave) ---

@router.post("", response_model=schemas.EstudioOut, status_code=201)
def crear_estudio(
    payload: schemas.EstudioCreate,
    db: Session = Depends(get_db),
    _: bool = Depends(verificar_admin),
):
    # Crea una nueva sala. Requiere clave admin.
    estudio = models.Estudio(**payload.model_dump())
    db.add(estudio)
    db.commit()
    db.refresh(estudio)
    return estudio


@router.put("/{estudio_id}", response_model=schemas.EstudioOut)
def editar_estudio(
    estudio_id: int,
    payload: schemas.EstudioCreate,
    db: Session = Depends(get_db),
    _: bool = Depends(verificar_admin),
):
    # Edita una sala existente. Requiere clave admin.
    estudio = db.query(models.Estudio).filter(models.Estudio.id == estudio_id).first()
    if estudio is None:
        raise HTTPException(status_code=404, detail="Estudio no encontrado")
    # Actualiza cada campo con los valores recibidos.
    for campo, valor in payload.model_dump().items():
        setattr(estudio, campo, valor)
    db.commit()
    db.refresh(estudio)
    return estudio


@router.delete("/{estudio_id}", status_code=204)
def borrar_estudio(
    estudio_id: int,
    db: Session = Depends(get_db),
    _: bool = Depends(verificar_admin),
):
    # Borra una sala. Requiere clave admin.
    estudio = db.query(models.Estudio).filter(models.Estudio.id == estudio_id).first()
    if estudio is None:
        raise HTTPException(status_code=404, detail="Estudio no encontrado")
    db.delete(estudio)
    db.commit()
    return None