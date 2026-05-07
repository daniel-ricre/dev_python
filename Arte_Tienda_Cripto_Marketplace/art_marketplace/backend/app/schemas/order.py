from pydantic import BaseModel, Field, field_validator
from app.models.order import Currency

class OrderCreate(BaseModel):
    artwork_id: str = Field(..., description="UUID de la obra")
    artist_address: str = Field(..., description="Dirección del artista en Arbitrum")
    buyer_address: str = Field(..., description="Dirección del comprador en Arbitrum")
    amount: str = Field(..., description="Monto en USD (ej: 350.00)")
    currency: Currency = Field(..., description="USDC o ETH")

    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v: str) -> str:
        try:
            value = float(v)
            if value <= 0:
                raise ValueError('El monto debe ser mayor a 0')
        except ValueError as e:
            raise ValueError(f'Monto inválido: "{v}". Debe ser un número positivo, por ejemplo: "350.00"')
        return v

    @field_validator('artwork_id')
    @classmethod
    def validate_uuid(cls, v: str) -> str:
        import uuid
        try:
            uuid.UUID(v)
        except ValueError:
            raise ValueError(f'ID de obra inválido: "{v}". Debe ser un UUID válido.')
        return v

class OrderResponse(BaseModel):
    order_id: str
    order_id_bytes32: str
    contract_address: str
    method: str
    params: dict
    usdc_address: str | None = None
    payment_wallet: str | None = None
    payment_amount: str | None = None
    payment_currency: str | None = None
    btcpay_url: str | None = None
