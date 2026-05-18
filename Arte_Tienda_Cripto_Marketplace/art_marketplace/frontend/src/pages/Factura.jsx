import { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import api from '../services/api';

export default function Factura() {
  const [searchParams] = useSearchParams();
  const orderId = searchParams.get('order_id');
  const [factura, setFactura] = useState(null);
  const [copied, setCopied] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (orderId) {
      api.get(`/orders/${orderId}`)
        .then(res => setFactura(res.data))
        .catch(console.error)
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, [orderId]);

  const copiarDireccion = () => {
    if (factura?.payment_wallet) {
      navigator.clipboard.writeText(factura.payment_wallet);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  if (loading) return <div className="p-6 text-center text-gray-500">Cargando factura...</div>;
  if (!factura) return <div className="p-6 text-center text-gray-500">Factura no encontrada</div>;

  return (
    <div className="min-h-screen flex items-center justify-center px-4">
      <div className="bg-white rounded-xl shadow-lg p-8 max-w-md w-full text-center">
        <h1 className="text-2xl font-bold text-gray-800 mb-2">Factura de Pago</h1>
        <p className="text-gray-500 mb-6">Escanea el QR o copia la dirección para pagar</p>
        
        <div className="bg-gray-100 p-4 rounded-lg mb-6">
          <img
            src={`https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(factura.payment_wallet)}`}
            alt="QR de pago"
            className="mx-auto w-48 h-48"
          />
        </div>

        <div className="bg-blue-50 p-4 rounded-lg mb-4">
          <p className="text-2xl font-bold text-blue-700">{factura.amount_usdc} USDC</p>
          <p className="text-sm text-gray-600 mt-1">Red: Arbitrum</p>
        </div>

        <div className="bg-gray-50 p-3 rounded-lg mb-4 break-all text-sm text-gray-700">
          <strong>Dirección:</strong><br/>
          {factura.payment_wallet}
        </div>

        <button
          onClick={copiarDireccion}
          className="w-full bg-blue-600 text-white py-3 rounded-lg hover:bg-blue-700 transition mb-3"
        >
          {copied ? '¡Copiado!' : 'Copiar dirección'}
        </button>

        <p className="text-xs text-gray-400 mt-4">
          Una vez realizado el pago, la ONG verificará y liberará los fondos al artista.
        </p>
      </div>
    </div>
  );
}
