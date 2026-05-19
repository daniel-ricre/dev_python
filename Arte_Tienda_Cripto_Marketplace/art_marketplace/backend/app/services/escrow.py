import uuid
from web3 import Web3
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.order import Order, OrderStatus
from app.services.price_service import PriceService

class EscrowService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_order(self, order_data):
        order_id_bytes32 = "0x" + Web3.keccak(text=str(uuid.uuid4())).hex()[:64]
        
        amount_float = float(order_data.amount)
        if amount_float <= 0:
            raise ValueError(f"Monto inválido: '{order_data.amount}'")
        
        if order_data.currency == "USDC":
            amount = int(amount_float * 10**6)
        elif order_data.currency == "ETH":
            amount = await PriceService.usd_to_eth(amount_float)
        else:
            raise ValueError(f"Moneda no soportada: {order_data.currency}")

        order = Order(
            order_id_bytes32=order_id_bytes32,
            artwork_id=order_data.artwork_id,
            artist_address=order_data.artist_address,
            buyer_address=order_data.buyer_address,
            buyer_email=getattr(order_data, 'buyer_email', None),
            amount=amount,
            currency=order_data.currency,
            status=OrderStatus.PENDING,
        )
        self.db.add(order)
        await self.db.commit()
        await self.db.refresh(order)
        return order
