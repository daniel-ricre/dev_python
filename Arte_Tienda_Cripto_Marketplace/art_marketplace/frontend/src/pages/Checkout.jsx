import { useParams } from 'react-router-dom';
import { useState, useEffect } from 'react';
import { ethers } from 'ethers';
import api from '../services/api';

const USDC_ADDRESS = import.meta.env.VITE_USDC_ADDRESS;

export default function Checkout() {
  const { artworkId } = useParams();
  const [artwork, setArtwork] = useState(null);
  const [loading, setLoading] = useState(false);
  const [paymentData, setPaymentData] = useState(null);
  const [selectedCurrency, setSelectedCurrency] = useState('USDC');

  useEffect(() => {
    api.get(`/artworks/${artworkId}`).then(res => setArtwork(res.data));
  }, [artworkId]);

  const handleCreateOrder = async (currency) => {
    if (!artwork) return;
    setSelectedCurrency(currency);
    setLoading(true);
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
      alert('Error al crear la orden. Asegúrate de tener MetaMask instalada y conectada.');
      console.error(err);
    } finally {
      setLoading(false);
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
      alert('Pago enviado correctamente. La ONG verificará y liberará los fondos.');
    } catch (err) {
      alert('Error al enviar el pago. Verifica que tengas fondos suficientes.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (!artwork) return <div className="p-6 text-center text-gray-500">Cargando obra...</div>;

  return (
    <div className="min-h-screen">
      <div className="max-w-lg mx-auto px-4 py-8">
        <div className="bg-white rounded-xl shadow-md overflow-hidden">
          <img src={artwork.image_url} alt={artwork.title} className="w-full h-64 object-cover" />
          <div className="p-6">
            <h1 className="text-2xl font-bold text-gray-800">{artwork.title}</h1>
            <p className="text-gray-500">{artwork.artist?.name}</p>
            <p className="text-3xl font-bold text-blue-700 my-4">${artwork.price_usd} USD</p>
            <hr className="mb-4" />
            <p className="text-gray-600 mb-2">Método de pago: <strong>Wallet a Wallet</strong></p>

            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">Moneda</label>
              <div className="flex space-x-2">
                <button
                  onClick={() => setSelectedCurrency('USDC')}
                  className={`px-4 py-2 rounded-lg font-medium transition ${selectedCurrency === 'USDC' ? 'bg-blue-600 text-white shadow' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'}`}
                >
                  🇺🇸 USDC
                </button>
                <button
                  onClick={() => setSelectedCurrency('ETH')}
                  className={`px-4 py-2 rounded-lg font-medium transition ${selectedCurrency === 'ETH' ? 'bg-purple-600 text-white shadow' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'}`}
                >
                  💎 ETH
                </button>
              </div>
            </div>

            <div className="space-y-3">
              <button
                onClick={() => handleCreateOrder(selectedCurrency)}
                disabled={loading}
                className="w-full bg-gray-700 text-white py-3 rounded-lg hover:bg-gray-800 disabled:opacity-50 transition"
              >
                {loading ? 'Creando orden...' : paymentData ? 'Orden creada' : `1. Crear orden de pago (${selectedCurrency})`}
              </button>
              {paymentData && (
                <div className="bg-gray-100 p-3 rounded-lg text-sm">
                  <p><strong>Enviar {paymentData.payment_currency === 'USDC' ? (paymentData.payment_amount / 1e6).toFixed(2) : (Number(paymentData.payment_amount) / 1e18).toFixed(6)} {paymentData.payment_currency}</strong></p>
                  <p className="break-all text-xs mt-1 text-gray-600">A: {paymentData.payment_wallet}</p>
                </div>
              )}
              <button
                onClick={handleWalletPayment}
                disabled={!paymentData || loading}
                className="w-full bg-gradient-to-r from-green-600 to-green-500 text-white py-3 rounded-lg hover:from-green-700 hover:to-green-600 disabled:opacity-50 transition"
              >
                {loading ? 'Procesando...' : '2. Enviar pago'}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
