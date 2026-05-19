from pydantic import BaseModel, Field, field_validator
from app.models.order import Currency

class OrderCreate(BaseModel):
    artwork_id: str = Field(..., description="UUID de la obra")
    artist_address: str = Field(..., description="Dirección del artista en Arbitrum")
    buyer_address: str = Field(..., description="Dirección del comprador en Arbitrum")
    buyer_email: str | None = Field(None, description="Email del comprador para notificaciones (opcional)")
    amount: str = Field(..., description="Monto en USD (ej: 350.00)")
    currency: Currency = Field(..., description="USDC o ETH")

    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v: str) -> str:
        try:
            value = float(v)
            if value <= 0:
                raise ValueError('El monto debe ser mayor a 0')
        except ValueError:
            raise ValueError(f'Monto inválido: "{v}". Debe ser un número positivo.')
        return v

    @field_validator('buyer_email')
    @classmethod
    def validate_email(cls, v: str | None) -> str | None:
        if v and '@' not in v:
            raise ValueError(f'Email inválido: "{v}"')
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
