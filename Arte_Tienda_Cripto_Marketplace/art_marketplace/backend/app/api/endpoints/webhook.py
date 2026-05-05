from fastapi import APIRouter, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.deps import get_db
from app.models.order import Order, OrderStatus

router = APIRouter()

@router.post("/webhook/btcpay")
async def btcpay_webhook(request: Request, db: AsyncSession = None):
    """
    Recibe notificaciones de BTCPay Server cuando un pago es confirmado.
    """
    db = await anext(get_db())
    try:
        data = await request.json()

        # BTCPay envía el orderId como metadata
        order_id_bytes32 = data.get("metadata", {}).get("orderId")
        if not order_id_bytes32:
            order_id_bytes32 = data.get("invoiceId")

        # Buscar la orden en la base de datos
        stmt = select(Order).where(Order.order_id_bytes32 == order_id_bytes32)
        result = await db.execute(stmt)
        order = result.scalar_one_or_none()

        if order and order.status == OrderStatus.PENDING:
            # Verificar si el pago fue confirmado
            status = data.get("status", "")
            if status in ["confirmed", "complete", "paid"]:
                order.status = OrderStatus.PAID
                order.tx_hash = data.get("txid", "")
                await db.commit()
                return {"status": "ok", "message": "Pago confirmado"}

        return {"status": "ignored", "message": "Orden no encontrada o ya procesada"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
