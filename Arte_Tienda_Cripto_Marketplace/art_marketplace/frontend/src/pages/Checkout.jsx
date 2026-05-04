import { useParams } from 'react-router-dom';
import { useState, useEffect } from 'react';
import api from '../services/api';
import { useEscrow } from '../hooks/useEscrow';

const CONTRACT_ADDRESS = import.meta.env.VITE_ESCROW_CONTRACT;
const USDC_ADDRESS = import.meta.env.VITE_USDC_ADDRESS;

export default function Checkout() {
  const { artworkId } = useParams();
  const [artwork, setArtwork] = useState(null);
  const { purchase, loading } = useEscrow(CONTRACT_ADDRESS, USDC_ADDRESS);

  useEffect(() => {
    api.get(`/artworks/${artworkId}`).then(res => setArtwork(res.data));
  }, [artworkId]);

  const handleBuy = async (currency) => {
    if (!artwork) return;
    try {
      const result = await purchase({
        artworkId: artwork.id,
        artistAddress: artwork.artist.wallet_address,
        amount: artwork.price_usd.toString(),
        currency
      });
      alert(`Compra exitosa! Orden: ${result.orderId}`);
    } catch (err) {
      alert('Error en la transacción');
      console.error(err);
    }
  };

  if (!artwork) return <div className="p-6">Cargando...</div>;

  return (
    <div className="max-w-md mx-auto p-6">
      <img src={artwork.image_url} alt={artwork.title} className="w-full rounded-lg mb-4" />
      <h1 className="text-2xl font-bold">{artwork.title}</h1>
      <p className="text-gray-700">{artwork.artist?.name}</p>
      <p className="text-3xl font-bold my-4">${artwork.price_usd} USD</p>
      <div className="space-y-3">
        <button
          onClick={() => handleBuy('USDC')}
          disabled={loading}
          className="w-full bg-green-600 text-white py-3 rounded hover:bg-green-700 disabled:opacity-50"
        >
          {loading ? 'Procesando...' : 'Pagar con USDC'}
        </button>
        <button
          onClick={() => handleBuy('ETH')}
          disabled={loading}
          className="w-full bg-blue-600 text-white py-3 rounded hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Procesando...' : 'Pagar con ETH'}
        </button>
      </div>
    </div>
  );
}
