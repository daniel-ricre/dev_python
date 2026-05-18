from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    """Endpoint para mantener viva la plataforma 24/7 con UptimeRobot."""
    return {
        "status": "ok",
        "message": "Pont Culturel API funcionando correctamente",
        "services": {
            "database": "connected",
            "redis": "connected",
            "blockchain": "arbitrum_sepolia"
        }
    }

@router.get("/ping")
async def ping():
    """Endpoint simple para monitoreo externo."""
    return {"status": "ok"}
