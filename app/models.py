# Modelos ORM que representan las tablas de la base de datos.
# SQLAlchemy genera el SQL CREATE TABLE a partir de estas clases.
from datetime import datetime

from sqlalchemy import (
    Column, Integer, String, Text, Boolean, DateTime,
    ForeignKey, DECIMAL, Date, Time,
)
from sqlalchemy.orm import relationship

from app.database import Base


class Estudio(Base):
    __tablename__ = "estudios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(120), nullable=False)
    descripcion = Column(Text, nullable=True)
    tipo = Column(String(60), nullable=False)          # ej: grabacion, ensayo
    capacidad = Column(Integer, nullable=False)
    precio_hora = Column(DECIMAL(10, 2), nullable=False)
    imagen_url = Column(String(255), nullable=True)
    activo = Column(Boolean, default=True, nullable=False)

    # Relaciones: un estudio tiene muchos equipos y muchas reservas.
    equipos = relationship("Equipo", back_populates="estudio", cascade="all, delete-orphan")
    reservas = relationship("Reserva", back_populates="estudio")


class Equipo(Base):
    __tablename__ = "equipos"

    id = Column(Integer, primary_key=True, index=True)
    estudio_id = Column(Integer, ForeignKey("estudios.id"), nullable=False)
    nombre = Column(String(120), nullable=False)
    descripcion = Column(Text, nullable=True)
    cantidad = Column(Integer, default=1, nullable=False)

    estudio = relationship("Estudio", back_populates="equipos")


class Reserva(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, index=True)
    estudio_id = Column(Integer, ForeignKey("estudios.id"), nullable=False)
    cliente_nombre = Column(String(120), nullable=False)
    cliente_email = Column(String(120), nullable=False)
    cliente_telefono = Column(String(40), nullable=True)
    fecha = Column(Date, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    duracion_horas = Column(Integer, nullable=False)
    metodo_pago = Column(String(40), nullable=False)   # tarjeta, transferencia, efectivo
    total = Column(DECIMAL(10, 2), nullable=False)
    estado = Column(String(30), default="pendiente", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    estudio = relationship("Estudio", back_populates="reservas")


class Plan(Base):
    __tablename__ = "planes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(80), nullable=False)
    descripcion = Column(Text, nullable=True)       # que incluye el plan
    precio = Column(DECIMAL(10, 2), nullable=False) # editable por admin
    activo = Column(Boolean, default=True, nullable=False)