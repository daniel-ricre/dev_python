from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/health")
@router.head("/health")
async def health(request: Request):
    return {"status": "ok"}

@router.get("/")
@router.head("/")
async def root_health(request: Request):
    """Health check en la raíz del backend."""
    return {"status": "ok", "service": "Pont Culturel API"}
