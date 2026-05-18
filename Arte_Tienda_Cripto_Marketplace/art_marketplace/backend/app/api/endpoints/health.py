from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health():
    return {"status": "ok"}

@router.get("/")
async def root_health():
    """Health check en la raíz del backend."""
    return {"status": "ok", "service": "Pont Culturel API"}
