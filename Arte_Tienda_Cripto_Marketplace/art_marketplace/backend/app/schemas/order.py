from pydantic import BaseModel
from app.models.order import Currency


class OrderCreate(BaseModel):
    artwork_id: str
    artist_address: str
    buyer_address: str
    amount: str
    currency: Currency


class OrderResponse(BaseModel):
    order_id: str
    order_id_bytes32: str
    contract_address: str
    method: str
    params: dict
    usdc_address: str | None = None
