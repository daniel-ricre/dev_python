import httpx

class PriceService:
    """Obtiene el precio actual de ETH en USD desde CoinGecko."""
    
    COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"
    
    @staticmethod
    async def get_eth_price() -> float:
        """Devuelve el precio de 1 ETH en USD."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    PriceService.COINGECKO_URL,
                    params={"ids": "ethereum", "vs_currencies": "usd"}
                )
                if response.status_code == 200:
                    data = response.json()
                    return float(data["ethereum"]["usd"])
                else:
                    return 3000.00
        except Exception:
            return 3000.00
    
    @staticmethod
    async def usd_to_eth(usd_amount: float) -> int:
        """Convierte USD a wei de ETH (18 decimales)."""
        eth_price = await PriceService.get_eth_price()
        eth_amount = usd_amount / eth_price
        wei_amount = int(eth_amount * 10**18)
        return wei_amount
