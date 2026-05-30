# Health check: Render lo consulta para saber si el servicio esta vivo.
from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check():
    return {"status": "ok"}