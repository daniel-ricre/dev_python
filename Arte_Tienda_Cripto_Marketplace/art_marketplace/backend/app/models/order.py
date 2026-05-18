import uuid
import enum
from datetime import datetime
from sqlalchemy import Column, String, Numeric, Enum, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base

class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    RELEASED = "released"
    REFUNDED = "refunded"
    EXPIRED = "expired"

class Currency(str, enum.Enum):
    USDC = "USDC"
    ETH = "ETH"

class Order(Base):
    __tablename__ = "orders"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id_bytes32 = Column(String(66), unique=True, nullable=False, index=True)
    artwork_id = Column(UUID(as_uuid=True), ForeignKey("artworks.id"))
    buyer_address = Column(String(42), nullable=False)
    artist_address = Column(String(42), nullable=False)
    amount = Column(Numeric, nullable=False)  # Cambiado de BigInteger a Numeric para soportar ETH (18 decimales)
    currency = Column(Enum(Currency), nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    tx_hash = Column(String(66))
    created_at = Column(DateTime, default=datetime.utcnow)
    released_at = Column(DateTime, nullable=True)

    artwork = relationship("Artwork", back_populates="orders")
