import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

export default function AdminLogin() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const formData = new URLSearchParams();
      formData.append('username', username);
      formData.append('password', password);
      const res = await api.post('/auth/login', formData);
      localStorage.setItem('token', res.data.access_token);
      navigate('/admin/panel');
    } catch (err) {
      alert('Credenciales inválidas');
    }
  };

  return (
    <div className="max-w-sm mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">Acceso Administración</h1>
      <form onSubmit={handleLogin} className="space-y-4">
        <input
          type="text" placeholder="Usuario" value={username}
          onChange={e => setUsername(e.target.value)} className="w-full border p-2 rounded"
        />
        <input
          type="password" placeholder="Contraseña" value={password}
          onChange={e => setPassword(e.target.value)} className="w-full border p-2 rounded"
        />
        <button type="submit" className="w-full bg-gray-800 text-white py-2 rounded">
          Ingresar
        </button>
      </form>
    </div>
  );
}