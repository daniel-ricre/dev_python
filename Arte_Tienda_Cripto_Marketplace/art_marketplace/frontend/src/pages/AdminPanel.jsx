import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

export default function AdminPanel() {
  const [orders, setOrders] = useState([]);
  const token = localStorage.getItem('token');
  const navigate = useNavigate();

  useEffect(() => {
    if (!token) {
      navigate('/admin');
      return;
    }
    api.get('/admin/orders', { headers: { Authorization: `Bearer ${token}` } })
      .then(res => setOrders(res.data))
      .catch(() => navigate('/admin'));
  }, []);

  const release = async (orderId) => {
    try {
      await api.post(`/admin/orders/${orderId}/release`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setOrders(prev => prev.map(o => o.id === orderId ? { ...o, status: 'released' } : o));
    } catch (err) {
      alert('Error al liberar pago');
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Órdenes</h1>
      <div className="overflow-x-auto">
        <table className="min-w-full border">
          <thead>
            <tr className="bg-gray-100">
              <th className="p-2">Obra</th>
              <th className="p-2">Comprador</th>
              <th className="p-2">Monto</th>
              <th className="p-2">Estado</th>
              <th className="p-2">Acción</th>
            </tr>
          </thead>
          <tbody>
            {orders.map(order => (
              <tr key={order.id} className="border-t">
                <td className="p-2">{order.artwork?.title}</td>
                <td className="p-2 text-sm">{order.buyer_address}</td>
                <td className="p-2">{order.amount / (order.currency === 'USDC' ? 1e6 : 1e18)} {order.currency}</td>
                <td className="p-2">{order.status}</td>
                <td className="p-2">
                  {order.status === 'paid' && (
                    <button onClick={() => release(order.id)} className="bg-green-600 text-white px-3 py-1 rounded">
                      Liberar pago
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
