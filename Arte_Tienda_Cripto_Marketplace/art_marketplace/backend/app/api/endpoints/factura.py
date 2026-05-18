from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.api.deps import get_db
from app.services.escrow import EscrowService
from app.core.config import settings

router = APIRouter()

class FacturaRequest(BaseModel):
    artwork_id: str
    artist_address: str
    buyer_address: str = "0x0000000000000000000000000000000000000000"
    amount: str
    currency: str = "USDC"

@router.post("/factura/crear")
async def crear_factura(data: FacturaRequest, db: AsyncSession = Depends(get_db)):
    """Crea una factura de pago con todos los datos necesarios para el comprador."""
    escrow_service = EscrowService(db)
    order = await escrow_service.create_order(data)
    
    # Construir URL de pago para wallets móviles (deep link)
    if data.currency == "USDC":
        payment_url = f"ethereum:{settings.ONG_PUBLIC_KEY}?value={order.amount}&token={settings.USDC_ADDRESS}"
    else:
        payment_url = f"ethereum:{settings.ONG_PUBLIC_KEY}?value={order.amount}"
    
    return {
        "order_id": str(order.id),
        "order_id_bytes32": order.order_id_bytes32,
        "payment_wallet": settings.ONG_PUBLIC_KEY,
        "amount_usdc": float(data.amount),
        "amount_raw": str(order.amount),
        "currency": data.currency,
        "payment_url": payment_url,
        "qr_data": payment_url,
        "status": "pending"
    }
