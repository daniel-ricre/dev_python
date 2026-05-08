import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Catalog from './pages/Catalog';
import Checkout from './pages/Checkout';
import AdminLogin from './pages/AdminLogin';
import AdminPanel from './pages/AdminPanel';
import Navbar from './components/Navbar';
import TidioChat from './components/TidioChat';

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <TidioChat />
      <Routes>
        <Route path="/" element={<Catalog />} />
        <Route path="/checkout/:artworkId" element={<Checkout />} />
        <Route path="/admin" element={<AdminLogin />} />
        <Route path="/admin/panel" element={<AdminPanel />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
