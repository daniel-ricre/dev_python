from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.api.deps import get_db
from app.models.order import Order, OrderStatus
import json

router = APIRouter()


@router.post("/webhook/btcpay")
async def btcpay_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    """
    Recibe notificaciones de BTCPay Server cuando un pago es confirmado.
    Soporta tanto BTCPay Server como OxaPay como Depay.
    """
    try:
        # Intentar leer el cuerpo como JSON
        try:
            data = await request.json()
        except Exception:
            # Si no es JSON, intentar como form data
            body = await request.body()
            if not body:
                return {"status": "ignored", "message": "Cuerpo vacío, ignorado"}
            raise HTTPException(status_code=400, detail="El cuerpo debe ser JSON válido")

        if not data:
            return {"status": "ignored", "message": "Sin datos, ignorado"}

        # Intentar obtener el orderId desde diferentes formatos
        order_id_bytes32 = (
            data.get("metadata", {}).get("orderId") or
            data.get("invoiceId") or
            data.get("order_id") or
            data.get("orderId")
        )

        if not order_id_bytes32:
            return {"status": "ignored", "message": "No se encontró orderId en los datos"}

        # Buscar la orden
        stmt = select(Order).where(Order.order_id_bytes32 == str(order_id_bytes32))
        result = await db.execute(stmt)
        order = result.scalar_one_or_none()

        if order and order.status == OrderStatus.PENDING:
            status = str(data.get("status", "")).lower()
            if status in ["confirmed", "complete", "paid", "succeed", "success"]:
                order.status = OrderStatus.PAID
                order.tx_hash = str(data.get("txid", data.get("tx_hash", "")))
                await db.commit()
                return {"status": "ok", "message": "Pago confirmado"}

        if not order:
            return {"status": "ignored", "message": f"Orden {order_id_bytes32} no encontrada"}
        
        return {"status": "ignored", "message": f"Orden en estado {order.status}, no procesada"}

    except HTTPException:
        raise
    except Exception as e:
        # Log del error pero no devolver 500
        print(f"Error en webhook: {str(e)}")
        return {"status": "error", "message": f"Error procesando webhook: {str(e)}"}
