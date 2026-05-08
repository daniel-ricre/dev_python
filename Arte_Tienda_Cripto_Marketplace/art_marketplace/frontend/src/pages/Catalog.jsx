import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';

export default function Catalog() {
  const [artworks, setArtworks] = useState([]);

  useEffect(() => {
    api.get('/artworks').then(res => setArtworks(res.data));
  }, []);

  return (
    <div className="min-h-screen">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-gray-800 mb-8">Galería de Arte</h1>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
          {artworks.map((art) => (
            <div key={art.id} className="bg-white rounded-xl shadow-md hover:shadow-xl transition-shadow duration-300 overflow-hidden">
              <img src={art.image_url} alt={art.title} className="w-full h-56 object-cover" />
              <div className="p-5">
                <h3 className="text-xl font-semibold text-gray-800 mb-1">{art.title}</h3>
                <p className="text-gray-500 text-sm mb-3">{art.artist?.name}</p>
                <div className="flex items-center justify-between mb-4">
                  <span className="bg-green-100 text-green-800 text-lg font-bold px-3 py-1 rounded-full">
                    ${art.price_usd} USD
                  </span>
                </div>
                <Link
                  to={`/checkout/${art.id}`}
                  className="block w-full text-center bg-gradient-to-r from-blue-600 to-blue-500 text-white font-medium py-2.5 rounded-lg hover:from-blue-700 hover:to-blue-600 transition duration-200"
                >
                  Comprar
                </Link>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
