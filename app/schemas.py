# Esquemas Pydantic v2 para validacion de entrada/salida de la API.
# Separar entrada y salida evita exponer campos internos y permite
# validar lo que llega del cliente de forma estricta.
from datetime import date, time, datetime
from decimal import Decimal

from pydantic import BaseModel, EmailStr, Field, ConfigDict


# ---------- EQUIPOS ----------
class EquipoOut(BaseModel):
    id: int
    nombre: str
    descripcion: str | None
    cantidad: int

    model_config = ConfigDict(from_attributes=True)


# ---------- ESTUDIOS ----------
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
    # Detalle incluye la lista de equipos asociados.
    equipos: list[EquipoOut] = []


# ---------- RESERVAS ----------
class ReservaCreate(BaseModel):
    # Lo que el frontend envia al crear una reserva.
    estudio_id: int
    cliente_nombre: str = Field(min_length=2, max_length=120)
    cliente_email: EmailStr
    cliente_telefono: str | None = Field(default=None, max_length=40)
    fecha: date
    hora_inicio: time
    duracion_horas: int = Field(gt=0, le=24)   # entre 1 y 24 horas
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

# ---------- ESTUDIOS: entrada para crear/editar (panel admin) ----------
class EstudioCreate(BaseModel):
    nombre: str = Field(min_length=2, max_length=120)
    descripcion: str | None = None
    tipo: str = Field(min_length=2, max_length=60)
    capacidad: int = Field(gt=0, le=100)
    precio_hora: Decimal = Field(gt=0)
    imagen_url: str | None = None
    activo: bool = True

# ---------- PRODUCTOS ----------
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


# ---------- CARRITO / TRANSACCIONES ----------
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