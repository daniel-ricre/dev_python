from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.api.deps import get_db
from app.models.order import Order, OrderStatus
from app.services.email_service import EmailService
from app.schemas.webhook import WebhookData

router = APIRouter()


@router.post("/webhook/btcpay")
async def btcpay_webhook(
    data: WebhookData,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    order_id_bytes32 = (
        (data.metadata or {}).get("orderId") if data.metadata else None
    ) or data.orderId or data.order_id or data.invoiceId

    if not order_id_bytes32:
        return {"status": "ignored", "message": "No se encontró orderId en los datos"}

    stmt = select(Order).options(joinedload(Order.artwork)).where(Order.order_id_bytes32 == str(order_id_bytes32))
    result = await db.execute(stmt)
    order = result.scalar_one_or_none()

    if order and order.status == OrderStatus.PENDING:
        status = str(data.status or "").lower()
        if status in ["confirmed", "complete", "paid", "succeed", "success"]:
            order.status = OrderStatus.PAID
            order.tx_hash = str(data.txid or data.tx_hash or "")
            await db.commit()

            # Enviar correo de confirmación al comprador (si tiene email)
            if order.buyer_email and order.artwork:
                amount_display = f"{float(order.amount) / 1e6:.2f}" if order.currency == "USDC" else f"{float(order.amount) / 1e18:.6f}"
                await EmailService.send_payment_confirmation(
                    to_email=order.buyer_email,
                    order_id=str(order.id),
                    artwork_title=order.artwork.title,
                    amount=amount_display,
                    currency=order.currency
                )

            return {"status": "ok", "message": "Pago confirmado"}

    if not order:
        return {"status": "ignored", "message": f"Orden {order_id_bytes32} no encontrada"}
    
    return {"status": "ignored", "message": f"Orden en estado {order.status}, no procesada"}
