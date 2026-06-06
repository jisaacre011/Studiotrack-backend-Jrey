# Esquemas Pydantic v2 para validacion de entrada/salida de la API.
from datetime import date, time, datetime
from decimal import Decimal

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class EquipoOut(BaseModel):
    id: int
    nombre: str
    descripcion: str | None
    cantidad: int
    model_config = ConfigDict(from_attributes=True)


class EstudioOut(BaseModel):
    id: int
    nombre: str
    descripcion: str | None
    tipo: str
    capacidad: int
    precio_hora: Decimal
    imagen_url: str | None
    activo: bool
    model_config = ConfigDict(from_attributes=True)


class EstudioDetalle(EstudioOut):
    equipos: list[EquipoOut] = []


class ReservaCreate(BaseModel):
    estudio_id: int
    cliente_nombre: str = Field(min_length=2, max_length=120)
    cliente_email: EmailStr
    cliente_telefono: str | None = Field(default=None, max_length=40)
    fecha: date
    hora_inicio: time
    duracion_horas: int = Field(gt=0, le=24)
    metodo_pago: str = Field(pattern="^(tarjeta|transferencia|efectivo)$")


class ReservaOut(BaseModel):
    id: int
    estudio_id: int
    cliente_nombre: str
    cliente_email: EmailStr
    cliente_telefono: str | None
    fecha: date
    hora_inicio: time
    duracion_horas: int
    metodo_pago: str
    total: Decimal
    estado: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class EstudioCreate(BaseModel):
    nombre: str = Field(min_length=2, max_length=120)
    descripcion: str | None = None
    tipo: str = Field(min_length=2, max_length=60)
    capacidad: int = Field(gt=0, le=100)
    precio_hora: Decimal = Field(gt=0)
    imagen_url: str | None = None
    activo: bool = True


class ProductoCreate(BaseModel):
    nombre: str = Field(min_length=2, max_length=120)
    descripcion: str | None = None
    tipo: str = Field(pattern="^(venta|alquiler|ambos)$")
    precio_venta: Decimal | None = Field(default=None, gt=0)
    precio_alquiler_dia: Decimal | None = Field(default=None, gt=0)
    stock: int = Field(ge=0)
    imagen_url: str | None = None
    activo: bool = True


class ProductoOut(BaseModel):
    id: int
    nombre: str
    descripcion: str | None
    tipo: str
    precio_venta: Decimal | None
    precio_alquiler_dia: Decimal | None
    stock: int
    imagen_url: str | None
    activo: bool
    model_config = ConfigDict(from_attributes=True)


class CarritoItem(BaseModel):
    producto_id: int
    modalidad: str = Field(pattern="^(compra|alquiler)$")
    cantidad: int = Field(gt=0)
    dias: int = Field(default=1, gt=0)


class TransaccionCreate(BaseModel):
    cliente_nombre: str = Field(min_length=2, max_length=120)
    cliente_email: EmailStr
    cliente_telefono: str | None = Field(default=None, max_length=40)
    items: list[CarritoItem] = Field(min_length=1)


class DetalleOut(BaseModel):
    producto_id: int
    modalidad: str
    cantidad: int
    dias: int
    precio_unitario: Decimal
    subtotal: Decimal
    model_config = ConfigDict(from_attributes=True)


class TransaccionOut(BaseModel):
    id: int
    cliente_nombre: str
    cliente_email: EmailStr
    cliente_telefono: str | None
    total: Decimal
    created_at: datetime
    detalles: list[DetalleOut] = []
    model_config = ConfigDict(from_attributes=True)


class PlanOut(BaseModel):
    id: int
    nombre: str
    descripcion: str | None
    precio: Decimal
    activo: bool
    model_config = ConfigDict(from_attributes=True)


class PlanPrecioUpdate(BaseModel):
    precio: Decimal = Field(gt=0)


class PlanCreate(BaseModel):
    nombre: str = Field(min_length=2, max_length=80)
    descripcion: str | None = None
    precio: Decimal = Field(gt=0)
    activo: bool = True
