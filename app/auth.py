# Autenticacion de administrador.
# Las operaciones de escritura (crear, editar, borrar) exigen la clave admin
# enviada en el header 'X-Admin-Key'. Si no coincide, se rechaza con 401.
from fastapi import Header, HTTPException

from app.config import settings


def verificar_admin(x_admin_key: str = Header(default="")):
    """Dependencia que protege endpoints. Compara la clave del header con la configurada."""
    if x_admin_key != settings.admin_key:
        raise HTTPException(status_code=401, detail="Clave de administrador invalida")
    return True