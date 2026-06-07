# Endpoints de transacciones (facturas). El carrito llega del frontend,
# el total se calcula en servidor. Listado protegido (lo ve el admin).
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.auth import verificar_admin

router = APIRouter(prefix="/transacciones", tags=["transacciones"])


@router.post("", response_model=schemas.TransaccionOut, status_code=201)
def crear_transaccion(payload: schemas.TransaccionCreate, db: Session = Depends(get_db)):
    transaccion = models.Transaccion(
        cliente_nombre=payload.cliente_nombre,
        cliente_email=payload.cliente_email,
        cliente_telefono=payload.cliente_telefono,
        total=0,
    )

    total = 0
    for item in payload.items:
        prod = db.query(models.Producto).filter(
            models.Producto.id == item.producto_id,
            models.Producto.activo == True,
        ).first()
        if prod is None:
            raise HTTPException(status_code=404,
                                detail=f"Producto {item.producto_id} no disponible")

        # Determinar precio segun modalidad. Validar que el producto la soporte.
        if item.modalidad == "compra":
            if prod.precio_venta is None:
                raise HTTPException(status_code=400,
                                    detail=f"{prod.nombre} no esta en venta")
            precio_unit = prod.precio_venta
            subtotal = precio_unit * item.cantidad
            dias = 1
        else:  # alquiler
            if prod.precio_alquiler_dia is None:
                raise HTTPException(status_code=400,
                                    detail=f"{prod.nombre} no esta en alquiler")
            precio_unit = prod.precio_alquiler_dia
            subtotal = precio_unit * item.cantidad * item.dias
            dias = item.dias

        total += subtotal
        transaccion.detalles.append(models.TransaccionDetalle(
            producto_id=prod.id,
            modalidad=item.modalidad,
            cantidad=item.cantidad,
            dias=dias,
            precio_unitario=precio_unit,
            subtotal=subtotal,
        ))

    transaccion.total = total
    db.add(transaccion)
    db.commit()
    db.refresh(transaccion)
    return transaccion


@router.get("", response_model=list[schemas.TransaccionOut])
def listar_transacciones(db: Session = Depends(get_db), _: bool = Depends(verificar_admin)):
    return db.query(models.Transaccion).order_by(
        models.Transaccion.created_at.desc()).all()
