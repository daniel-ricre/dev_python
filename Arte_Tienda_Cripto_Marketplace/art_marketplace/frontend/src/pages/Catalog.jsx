import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';

export default function Catalog() {
  const [artworks, setArtworks] = useState([]);

  useEffect(() => {
    api.get('/artworks').then(res => setArtworks(res.data));
  }, []);

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 p-6">
      {artworks.map((art) => (
        <div key={art.id} className="border rounded-lg overflow-hidden shadow hover:shadow-lg">
          <img src={art.image_url} alt={art.title} className="w-full h-48 object-cover" />
          <div className="p-4">
            <h3 className="text-lg font-semibold">{art.title}</h3>
            <p className="text-gray-600">{art.artist?.name}</p>
            <p className="text-xl font-bold mt-2">${art.price_usd} USD</p>
            <Link to={`/checkout/${art.id}`} className="mt-3 inline-block bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
              Comprar
            </Link>
          </div>
        </div>
      ))}
    </div>
  );
}