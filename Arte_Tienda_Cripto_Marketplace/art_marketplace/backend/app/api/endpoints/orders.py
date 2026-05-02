from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.schemas.order import OrderCreate, OrderResponse
from app.services.escrow import EscrowService
from app.core.config import settings

router = APIRouter()


@router.post("/orders", response_model=OrderResponse)
async def create_order(order_data: OrderCreate, db: AsyncSession = Depends(get_db)):
    escrow_service = EscrowService(db)
    order = await escrow_service.create_order(order_data)
    return {
        "order_id": str(order.id),
        "order_id_bytes32": order.order_id_bytes32,
        "contract_address": settings.ESCROW_CONTRACT_ADDRESS,
        "method": "createUsdcEscrow" if order.currency == "USDC" else "createEthEscrow",
        "params": {
            "orderId": order.order_id_bytes32,
            "artist": order.artist_address,
            "amount": str(order.amount)
        },
        "usdc_address": settings.USDC_ADDRESS if order.currency == "USDC" else None
    }
