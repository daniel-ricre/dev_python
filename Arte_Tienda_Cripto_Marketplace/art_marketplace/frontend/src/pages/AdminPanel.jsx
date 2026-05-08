import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

export default function AdminPanel() {
  const [orders, setOrders] = useState([]);
  const [artists, setArtists] = useState([]);
  const [artworkForm, setArtworkForm] = useState({
    title: '',
    description: '',
    price_usd: '',
    image_url: '',
    artist_id: '',
    available: true
  });
  const [artistForm, setArtistForm] = useState({
    name: '',
    bio: '',
    wallet_address: '',
    image_url: ''
  });
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
    api.get('/artists')
      .then(res => setArtists(res.data))
      .catch(console.error);
  }, []);

  const handleCreateArtist = async (e) => {
    e.preventDefault();
    try {
      await api.post('/admin/artists', artistForm, {
        headers: { Authorization: `Bearer ${token}` }
      });
      alert('Artista creado exitosamente');
      setArtistForm({ name: '', bio: '', wallet_address: '', image_url: '' });
      // Refresh artist list
      api.get('/artists').then(res => setArtists(res.data));
    } catch (err) {
      alert('Error al crear artista');
    }
  };

  const handleCreateArtwork = async (e) => {
    e.preventDefault();
    try {
      await api.post('/admin/artworks', artworkForm, {
        headers: { Authorization: `Bearer ${token}` }
      });
      alert('Obra creada exitosamente');
      setArtworkForm({ title: '', description: '', price_usd: '', image_url: '', artist_id: '', available: true });
    } catch (err) {
      alert('Error al crear obra');
    }
  };

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
    <div className="bg-gray-50 min-h-screen p-6">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-800 mb-8">Panel de Administración</h1>

        {/* Registrar Artista */}
        <div className="bg-white rounded-xl shadow-md p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4 text-gray-700">Registrar Artista</h2>
          <form onSubmit={handleCreateArtist} className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <input type="text" placeholder="Nombre" value={artistForm.name}
              onChange={e => setArtistForm({...artistForm, name: e.target.value})}
              className="border border-gray-300 p-2 rounded-lg focus:ring-2 focus:ring-blue-500" required />
            <input type="text" placeholder="URL de imagen" value={artistForm.image_url}
              onChange={e => setArtistForm({...artistForm, image_url: e.target.value})}
              className="border border-gray-300 p-2 rounded-lg focus:ring-2 focus:ring-blue-500" />
            <textarea placeholder="Biografía" value={artistForm.bio}
              onChange={e => setArtistForm({...artistForm, bio: e.target.value})}
              className="border border-gray-300 p-2 rounded-lg focus:ring-2 focus:ring-blue-500 col-span-1 sm:col-span-2" />
            <input type="text" placeholder="Dirección wallet (0x...)" value={artistForm.wallet_address}
              onChange={e => setArtistForm({...artistForm, wallet_address: e.target.value})}
              className="border border-gray-300 p-2 rounded-lg focus:ring-2 focus:ring-blue-500" required />
            <button type="submit" className="sm:col-span-2 bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition font-medium">
              Registrar Artista
            </button>
          </form>
        </div>

        {/* Publicar Obra */}
        <div className="bg-white rounded-xl shadow-md p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4 text-gray-700">Publicar Obra</h2>
          <form onSubmit={handleCreateArtwork} className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <input type="text" placeholder="Título" value={artworkForm.title}
              onChange={e => setArtworkForm({...artworkForm, title: e.target.value})}
              className="border border-gray-300 p-2 rounded-lg focus:ring-2 focus:ring-blue-500" required />
            <input type="text" placeholder="URL de imagen" value={artworkForm.image_url}
              onChange={e => setArtworkForm({...artworkForm, image_url: e.target.value})}
              className="border border-gray-300 p-2 rounded-lg focus:ring-2 focus:ring-blue-500" required />
            <textarea placeholder="Descripción" value={artworkForm.description}
              onChange={e => setArtworkForm({...artworkForm, description: e.target.value})}
              className="border border-gray-300 p-2 rounded-lg focus:ring-2 focus:ring-blue-500 col-span-1 sm:col-span-2" />
            <input type="number" step="0.01" placeholder="Precio (USD)" value={artworkForm.price_usd}
              onChange={e => setArtworkForm({...artworkForm, price_usd: e.target.value})}
              className="border border-gray-300 p-2 rounded-lg focus:ring-2 focus:ring-blue-500" required />
            <select value={artworkForm.artist_id}
              onChange={e => setArtworkForm({...artworkForm, artist_id: e.target.value})}
              className="border border-gray-300 p-2 rounded-lg focus:ring-2 focus:ring-blue-500" required>
              <option value="">Seleccionar artista</option>
              {artists.map(artist => (
                <option key={artist.id} value={artist.id}>{artist.name}</option>
              ))}
            </select>
            <button type="submit" className="sm:col-span-2 bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 transition font-medium">
              Publicar Obra
            </button>
          </form>
        </div>

        {/* Órdenes */}
        <div className="bg-white rounded-xl shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4 text-gray-700">Órdenes</h2>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-100">
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Obra</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Comprador</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Monto</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Acción</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {orders.map(order => (
                  <tr key={order.id} className="hover:bg-gray-50 transition-colors">
                    <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-900">{order.artwork?.title}</td>
                    <td className="px-4 py-3 whitespace-nowrap text-sm text-gray-500">{order.buyer_address}</td>
                    <td className="px-4 py-3 whitespace-nowrap text-sm font-medium text-gray-900">
                      {order.amount / (order.currency === 'USDC' ? 1e6 : 1e18)} {order.currency}
                    </td>
                    <td className="px-4 py-3 whitespace-nowrap">
                      <span className={`px-2 py-1 text-xs rounded-full font-semibold ${
                        order.status === 'paid' ? 'bg-yellow-100 text-yellow-800' :
                        order.status === 'released' ? 'bg-green-100 text-green-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {order.status}
                      </span>
                    </td>
                    <td className="px-4 py-3 whitespace-nowrap text-sm">
                      {order.status === 'paid' && (
                        <button onClick={() => release(order.id)} className="bg-green-600 text-white px-3 py-1 rounded-lg hover:bg-green-700 transition">
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
      </div>
    </div>
  );
}
