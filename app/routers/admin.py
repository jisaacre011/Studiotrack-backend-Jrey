# Endpoints relacionados con la administracion.
from fastapi import APIRouter, Depends

from app.auth import verificar_admin

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/login")
def login_admin(_: bool = Depends(verificar_admin)):
    """Valida la clave admin. Si la dependencia pasa, la clave es correcta."""
    return {"ok": True, "mensaje": "Acceso de administrador concedido"}