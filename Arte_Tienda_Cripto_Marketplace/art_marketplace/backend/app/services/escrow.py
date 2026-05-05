import uuid
import random
from web3 import Web3
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.order import Order, OrderStatus

class EscrowService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_order(self, order_data):
        order_id_bytes32 = "0x" + Web3.keccak(text=str(uuid.uuid4())).hex()[:64]
        if order_data.currency == "USDC":
            amount = int(float(order_data.amount) * 10**6)
        else:
            amount = int(float(order_data.amount) * 10**18)

        # Generar wallet de depósito única para el comprador (wallet a wallet)
        deposit_wallet = "0x" + Web3.keccak(text=str(uuid.uuid4())).hex()[:40]

        order = Order(
            order_id_bytes32=order_id_bytes32,
            artwork_id=order_data.artwork_id,
            artist_address=order_data.artist_address,
            buyer_address=order_data.buyer_address,
            amount=amount,
            currency=order_data.currency,
            status=OrderStatus.PENDING,
        )
        self.db.add(order)
        await self.db.commit()
        await self.db.refresh(order)
        return order
