from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.api.deps import get_db, get_current_ong_admin
from app.models.order import Order, OrderStatus
from app.services.blockchain import BlockchainService
import uuid

router = APIRouter()


@router.get("/orders")
async def list_orders(
    status: OrderStatus = None,
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_ong_admin)
):
    stmt = select(Order).options(joinedload(Order.artwork))
    if status:
        stmt = stmt.where(Order.status == status)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.post("/orders/{order_id}/release")
async def release_payment(
    order_id: str = Path(..., description="UUID de la orden"),
    db: AsyncSession = Depends(get_db),
    current_admin=Depends(get_current_ong_admin)
):
    # Validar UUID
    try:
        uuid.UUID(order_id)
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail=f"ID inválido: '{order_id}' no es un UUID válido."
        )
    
    stmt = select(Order).where(Order.id == order_id)
    result = await db.execute(stmt)
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    if order.status != OrderStatus.PAID:
        raise HTTPException(
            status_code=400, detail="La orden no está pagada o ya fue liberada")

    blockchain = BlockchainService()
    tx_hash = blockchain.release_escrow(order.order_id_bytes32)

    order.status = OrderStatus.RELEASED
    order.released_at = datetime.now(timezone.utc)
    await db.commit()
    return {"status": "released", "tx_hash": tx_hash}
