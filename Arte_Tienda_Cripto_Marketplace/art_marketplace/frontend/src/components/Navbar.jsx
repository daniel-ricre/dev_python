import { Link } from 'react-router-dom';

export default function Navbar() {
  return (
    <nav className="bg-white shadow p-4 flex justify-between">
      <Link to="/" className="text-xl font-bold">Pont Culturel</Link>
      <Link to="/admin" className="text-gray-600 hover:text-gray-800">Admin</Link>
    </nav>
  );
}
