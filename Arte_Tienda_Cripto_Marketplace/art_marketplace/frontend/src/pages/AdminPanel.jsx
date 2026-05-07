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
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Panel de Administración</h1>

      {/* Crear artista */}
      <div className="mb-8 p-4 border rounded">
        <h2 className="text-xl font-semibold mb-2">Registrar Artista</h2>
        <form onSubmit={handleCreateArtist} className="grid grid-cols-2 gap-3">
          <input type="text" placeholder="Nombre" value={artistForm.name}
            onChange={e => setArtistForm({...artistForm, name: e.target.value})}
            className="border p-2 rounded" required />
          <input type="text" placeholder="URL de imagen" value={artistForm.image_url}
            onChange={e => setArtistForm({...artistForm, image_url: e.target.value})}
            className="border p-2 rounded" />
          <textarea placeholder="Biografía" value={artistForm.bio}
            onChange={e => setArtistForm({...artistForm, bio: e.target.value})}
            className="border p-2 rounded" />
          <input type="text" placeholder="Dirección wallet (0x...)" value={artistForm.wallet_address}
            onChange={e => setArtistForm({...artistForm, wallet_address: e.target.value})}
            className="border p-2 rounded" required />
          <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">
            Registrar Artista
          </button>
        </form>
      </div>

      {/* Crear obra */}
      <div className="mb-8 p-4 border rounded">
        <h2 className="text-xl font-semibold mb-2">Publicar Obra</h2>
        <form onSubmit={handleCreateArtwork} className="grid grid-cols-2 gap-3">
          <input type="text" placeholder="Título" value={artworkForm.title}
            onChange={e => setArtworkForm({...artworkForm, title: e.target.value})}
            className="border p-2 rounded" required />
          <input type="text" placeholder="URL de imagen" value={artworkForm.image_url}
            onChange={e => setArtworkForm({...artworkForm, image_url: e.target.value})}
            className="border p-2 rounded" required />
          <textarea placeholder="Descripción" value={artworkForm.description}
            onChange={e => setArtworkForm({...artworkForm, description: e.target.value})}
            className="border p-2 rounded" />
          <input type="number" step="0.01" placeholder="Precio (USD)" value={artworkForm.price_usd}
            onChange={e => setArtworkForm({...artworkForm, price_usd: e.target.value})}
            className="border p-2 rounded" required />
          <select value={artworkForm.artist_id}
            onChange={e => setArtworkForm({...artworkForm, artist_id: e.target.value})}
            className="border p-2 rounded" required>
            <option value="">Seleccionar artista</option>
            {artists.map(artist => (
              <option key={artist.id} value={artist.id}>{artist.name}</option>
            ))}
          </select>
          <button type="submit" className="bg-green-600 text-white px-4 py-2 rounded">
            Publicar Obra
          </button>
        </form>
      </div>

      {/* Órdenes */}
      <h2 className="text-xl font-semibold mb-2">Órdenes</h2>
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
