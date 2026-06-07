# Modelos ORM que representan las tablas de la base de datos.
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
    tipo = Column(String(60), nullable=False)
    capacidad = Column(Integer, nullable=False)
    precio_hora = Column(DECIMAL(10, 2), nullable=False)
    imagen_url = Column(String(255), nullable=True)
    activo = Column(Boolean, default=True, nullable=False)

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
    metodo_pago = Column(String(40), nullable=False)
    total = Column(DECIMAL(10, 2), nullable=False)
    estado = Column(String(30), default="pendiente", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    estudio = relationship("Estudio", back_populates="reservas")


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(120), nullable=False)
    descripcion = Column(Text, nullable=True)
    tipo = Column(String(20), nullable=False)
    precio_venta = Column(DECIMAL(10, 2), nullable=True)
    precio_alquiler_dia = Column(DECIMAL(10, 2), nullable=True)
    stock = Column(Integer, default=0, nullable=False)
    imagen_url = Column(String(255), nullable=True)
    activo = Column(Boolean, default=True, nullable=False)


class Transaccion(Base):
    __tablename__ = "transacciones"

    id = Column(Integer, primary_key=True, index=True)
    cliente_nombre = Column(String(120), nullable=False)
    cliente_email = Column(String(120), nullable=False)
    cliente_telefono = Column(String(40), nullable=True)
    total = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    detalles = relationship("TransaccionDetalle", back_populates="transaccion",
                            cascade="all, delete-orphan")


class TransaccionDetalle(Base):
    __tablename__ = "transaccion_detalle"

    id = Column(Integer, primary_key=True, index=True)
    transaccion_id = Column(Integer, ForeignKey("transacciones.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    modalidad = Column(String(20), nullable=False)
    cantidad = Column(Integer, nullable=False)
    dias = Column(Integer, default=1, nullable=False)
    precio_unitario = Column(DECIMAL(10, 2), nullable=False)
    subtotal = Column(DECIMAL(10, 2), nullable=False)

    transaccion = relationship("Transaccion", back_populates="detalles")
    producto = relationship("Producto")


class Plan(Base):
    __tablename__ = "planes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(80), nullable=False)
    descripcion = Column(Text, nullable=True)
    precio = Column(DECIMAL(10, 2), nullable=False)
    activo = Column(Boolean, default=True, nullable=False)
