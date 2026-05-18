import { BrowserRouter, Routes, Route } from 'react-router-dom'
import '@rainbow-me/rainbowkit/styles.css'
import Providers from './providers'
import Catalog from './pages/Catalog'
import Checkout from './pages/Checkout'
import AdminLogin from './pages/AdminLogin'
import AdminPanel from './pages/AdminPanel'
import Navbar from './components/Navbar'
import TidioChat from './components/TidioChat'

function App() {
  return (
    <Providers>
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
    </Providers>
  )
}

export default App
