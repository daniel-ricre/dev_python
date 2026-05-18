from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str = "redis://localhost:6379/0"
    ARBITRUM_RPC_URL: str
    ESCROW_CONTRACT_ADDRESS: str
    ONG_PUBLIC_KEY: str
    ONG_PRIVATE_KEY: str
    USDC_ADDRESS: str = "0xaf88d065e77c8cC2239327C5EDb3A432268e5831"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str
    FRONTEND_URL: str = "https://art-frontend-cs3w.onrender.com"

    model_config = {"env_file": ".env"}

settings = Settings()
