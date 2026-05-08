import { Link } from 'react-router-dom';

export default function Navbar() {
  return (
    <nav className="bg-gradient-to-r from-blue-700 to-blue-500 shadow-lg p-4 flex justify-between items-center">
      <Link to="/" className="text-2xl font-extrabold text-white tracking-wide">
        Pont Culturel
      </Link>
      <Link to="/admin" className="text-white bg-blue-900 bg-opacity-30 hover:bg-opacity-50 px-4 py-2 rounded-full transition duration-200">
        Admin
      </Link>
    </nav>
  );
}
