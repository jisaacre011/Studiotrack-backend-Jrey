# Endpoints de productos: lectura publica, escritura protegida por admin.
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.auth import verificar_admin

router = APIRouter(prefix="/productos", tags=["productos"])


@router.get("", response_model=list[schemas.ProductoOut])
def listar_productos(db: Session = Depends(get_db)):
    return db.query(models.Producto).filter(models.Producto.activo == True).all()


@router.get("/{producto_id}", response_model=schemas.ProductoOut)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    p = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if p is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return p


@router.post("", response_model=schemas.ProductoOut, status_code=201)
def crear_producto(payload: schemas.ProductoCreate, db: Session = Depends(get_db),
                   _: bool = Depends(verificar_admin)):
    p = models.Producto(**payload.model_dump())
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


@router.put("/{producto_id}", response_model=schemas.ProductoOut)
def editar_producto(producto_id: int, payload: schemas.ProductoCreate,
                    db: Session = Depends(get_db), _: bool = Depends(verificar_admin)):
    p = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if p is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    for campo, valor in payload.model_dump().items():
        setattr(p, campo, valor)
    db.commit()
    db.refresh(p)
    return p


@router.delete("/{producto_id}", status_code=204)
def borrar_producto(producto_id: int, db: Session = Depends(get_db),
                    _: bool = Depends(verificar_admin)):
    p = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if p is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(p)
    db.commit()
    return None