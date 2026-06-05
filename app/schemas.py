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


# ---------- PLANES ----------
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