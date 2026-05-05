import { useParams } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { ethers } from 'ethers';
import api from '../services/api';

const CONTRACT_ADDRESS = import.meta.env.VITE_ESCROW_CONTRACT;
const USDC_ADDRESS = import.meta.env.VITE_USDC_ADDRESS;

export default function Checkout() {
  const { artworkId } = useParams();
  const [artwork, setArtwork] = useState(null);
  const [paymentMethod, setPaymentMethod] = useState('wallet');
  const [loading, setLoading] = useState(false);
  const [paymentData, setPaymentData] = useState(null);

  useEffect(() => {
    api.get(`/artworks/${artworkId}`).then(res => setArtwork(res.data));
  }, [artworkId]);

  const handleCreateOrder = async (currency) => {
    if (!artwork) return;
    try {
      const provider = new ethers.BrowserProvider(window.ethereum);
      const signer = await provider.getSigner();
      const buyerAddress = await signer.getAddress();

      const res = await api.post('/orders', {
        artwork_id: artwork.id,
        artist_address: artwork.artist.wallet_address,
        buyer_address: buyerAddress,
        amount: artwork.price_usd.toString(),
        currency: currency
      });
      setPaymentData(res.data);
    } catch (err) {
      alert('Error al crear la orden');
      console.error(err);
    }
  };

  const handleWalletPayment = async () => {
    if (!paymentData) return;
    setLoading(true);
    try {
      const provider = new ethers.BrowserProvider(window.ethereum);
      const signer = await provider.getSigner();

      if (paymentData.payment_currency === 'USDC') {
        const usdcContract = new ethers.Contract(
          USDC_ADDRESS,
          ['function transfer(address to, uint256 amount) public returns (bool)'],
          signer
        );
        const tx = await usdcContract.transfer(
          paymentData.payment_wallet,
          paymentData.payment_amount
        );
        await tx.wait();
      } else {
        const tx = await signer.sendTransaction({
          to: paymentData.payment_wallet,
          value: paymentData.payment_amount
        });
        await tx.wait();
      }
      alert('Pago enviado correctamente. La ONG verificara y liberara los fondos.');
    } catch (err) {
      alert('Error al enviar el pago');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (!artwork) return <div className="p-6">Cargando...</div>;

  return (
    <div className="max-w-md mx-auto p-6">
      <img src={artwork.image_url} alt={artwork.title} className="w-full rounded-lg mb-4" />
      <h1 className="text-2xl font-bold">{artwork.title}</h1>
      <p className="text-gray-700">{artwork.artist?.name}</p>
      <p className="text-3xl font-bold my-4">${artwork.price_usd} USD</p>

      <div className="mb-4">
        <label className="block text-sm font-medium mb-2">Metodo de pago</label>
        <select
          value={paymentMethod}
          onChange={(e) => setPaymentMethod(e.target.value)}
          className="w-full border p-2 rounded"
        >
          <option value="wallet">Pago directo (Wallet a Wallet)</option>
        </select>
      </div>

      {paymentMethod === 'wallet' && (
        <div className="space-y-3">
          <button
            onClick={() => handleCreateOrder('USDC')}
            disabled={loading}
            className="w-full bg-gray-600 text-white py-3 rounded hover:bg-gray-700 disabled:opacity-50"
          >
            {paymentData ? 'Orden creada' : '1. Crear orden de pago'}
          </button>
          {paymentData && (
            <div className="bg-gray-100 p-3 rounded text-sm">
              <p><strong>Enviar {paymentData.payment_amount / 1e6} USDC</strong></p>
              <p className="break-all text-xs mt-1">A: {paymentData.payment_wallet}</p>
            </div>
          )}
          <button
            onClick={handleWalletPayment}
            disabled={!paymentData || loading}
            className="w-full bg-green-600 text-white py-3 rounded hover:bg-green-700 disabled:opacity-50"
          >
            {loading ? 'Procesando...' : '2. Enviar pago'}
          </button>
        </div>
      )}
    </div>
  );
}
