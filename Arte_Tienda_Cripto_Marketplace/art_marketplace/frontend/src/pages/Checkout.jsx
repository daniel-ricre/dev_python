import { useParams } from 'react-router-dom'
import { useState, useEffect } from 'react'
import { useAccount, useSwitchChain, useWriteContract, useSendTransaction } from 'wagmi'
import { arbitrumSepolia } from 'wagmi/chains'
import api from '../services/api'
import { ConnectButton } from '@rainbow-me/rainbowkit'

const USDC_ADDRESS = import.meta.env.VITE_USDC_ADDRESS
const USDC_ABI = [
  {
    type: 'function',
    name: 'transfer',
    inputs: [
      { name: 'to', type: 'address' },
      { name: 'amount', type: 'uint256' }
    ],
    outputs: [{ name: '', type: 'bool' }]
  }
]

export default function Checkout() {
  const { artworkId } = useParams()
  const [artwork, setArtwork] = useState(null)
  const [loading, setLoading] = useState(false)
  const [paymentData, setPaymentData] = useState(null)
  const [selectedCurrency, setSelectedCurrency] = useState('USDC')
  const [paymentIntent, setPaymentIntent] = useState(false)
  const [errorMsg, setErrorMsg] = useState('')

  const { address, isConnected, chainId } = useAccount()
  const { switchChain, isPending: isSwitchingChain } = useSwitchChain()
  const { writeContract, isPending: isWritePending, isSuccess: isWriteSuccess, isError: isWriteError } = useWriteContract()
  const { sendTransaction, isPending: isSendPending, isSuccess: isSendSuccess, isError: isSendError } = useSendTransaction()

  const walletReady = isConnected && chainId === arbitrumSepolia.id

  useEffect(() => {
    api.get(`/artworks/${artworkId}`).then(res => setArtwork(res.data))
  }, [artworkId])

  useEffect(() => {
    if (isConnected && chainId !== arbitrumSepolia.id && !isSwitchingChain) {
      switchChain({ chainId: arbitrumSepolia.id })
    }
  }, [isConnected, chainId, isSwitchingChain, switchChain])

  const formatAmount = (amount, currency) => {
    if (!amount) return '0'
    const num = Number(amount)
    if (currency === 'USDC') return (num / 1e6).toFixed(2)
    return (num / 1e18).toFixed(6)
  }

  const handleCreateOrder = async (currency) => {
    if (!artwork) return
    setSelectedCurrency(currency)
    setLoading(true)
    setErrorMsg('')
    try {
      const buyerAddress = address || '0x0000000000000000000000000000000000000000'
      const res = await api.post('/orders', {
        artwork_id: artwork.id,
        artist_address: artwork.artist.wallet_address,
        buyer_address: buyerAddress,
        amount: artwork.price_usd.toString(),
        currency: currency
      })
      setPaymentData(res.data)
    } catch (err) {
      console.error('Error al crear orden:', err)
      setErrorMsg('Error al crear la orden. Verifica tu conexión e intenta de nuevo.')
    } finally {
      setLoading(false)
    }
  }

  const handleWalletPayment = () => {
    if (!paymentData || !walletReady) return
    setPaymentIntent(true)
    setLoading(true)
    if (paymentData.payment_currency === 'USDC') {
      writeContract({
        address: USDC_ADDRESS,
        abi: USDC_ABI,
        functionName: 'transfer',
        args: [paymentData.payment_wallet, BigInt(paymentData.payment_amount)],
      })
    } else {
      sendTransaction({
        to: paymentData.payment_wallet,
        value: BigInt(paymentData.payment_amount),
      })
    }
  }

  useEffect(() => {
    if (!paymentIntent) return
    if (isWriteSuccess || isSendSuccess) {
      setLoading(false)
      setPaymentData(null)
      setPaymentIntent(false)
      setErrorMsg('')
      alert('Pago enviado correctamente. La ONG verificará y liberará los fondos.')
    } else if (isWriteError || isSendError) {
      setLoading(false)
      setPaymentIntent(false)
      setErrorMsg('Error al enviar el pago. Verifica que tengas fondos suficientes y la red correcta.')
    }
  }, [isWriteSuccess, isWriteError, isSendSuccess, isSendError, paymentIntent])

  if (!artwork) return <div className="p-6 text-center text-gray-500">Cargando obra...</div>

  return (
    <div className="min-h-screen">
      <div className="max-w-lg mx-auto px-4 py-8">
        <div className="bg-white rounded-xl shadow-md overflow-hidden">
          <img src={artwork.image_url} alt={artwork.title} className="w-full h-64 object-cover" />
          <div className="p-6">
            <h1 className="text-2xl font-bold text-gray-800">{artwork.title}</h1>
            <p className="text-gray-500">{artwork.artist?.name}</p>
            <p className="text-3xl font-bold text-blue-700 my-4">${artwork.price_usd} USD</p>
            <hr className="mb-4" />

            {!walletReady && (
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-4 text-center">
                <p className="text-yellow-800 mb-2">{isSwitchingChain ? 'Cambiando...' : 'Para continuar, conecta tu wallet'}</p>
                <ConnectButton label="Conectar Wallet" />
              </div>
            )}

            {errorMsg && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-3 mb-4 text-sm text-red-800">{errorMsg}</div>
            )}

            {walletReady && (
              <>
                <div className="mb-4 flex items-center gap-2 text-sm text-green-700 bg-green-50 p-2 rounded-lg">
                  <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                  Wallet conectada: {address?.slice(0, 6)}...{address?.slice(-4)}
                </div>
                <p className="text-gray-600 mb-2">Método de pago: <strong>Wallet a Wallet</strong></p>
                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-700 mb-1">Moneda</label>
                  <div className="flex space-x-2">
                    <button onClick={() => setSelectedCurrency('USDC')} className={`px-4 py-2 rounded-lg font-medium transition ${selectedCurrency === 'USDC' ? 'bg-blue-600 text-white shadow' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'}`}>USDC</button>
                    <button onClick={() => setSelectedCurrency('ETH')} className={`px-4 py-2 rounded-lg font-medium transition ${selectedCurrency === 'ETH' ? 'bg-purple-600 text-white shadow' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'}`}>ETH</button>
                  </div>
                </div>
                <div className="space-y-3">
                  <button onClick={() => handleCreateOrder(selectedCurrency)} disabled={loading} className="w-full bg-gray-700 text-white py-3 rounded-lg hover:bg-gray-800 disabled:opacity-50 transition">
                    {loading && !paymentData ? 'Creando orden...' : paymentData ? 'Orden creada' : `1. Crear orden de pago (${selectedCurrency})`}
                  </button>
                  {paymentData && (
                    <div className="bg-gray-100 p-3 rounded-lg text-sm">
                      <p><strong>Enviar {formatAmount(paymentData.payment_amount, paymentData.payment_currency)} {paymentData.payment_currency}</strong></p>
                      <p className="break-all text-xs mt-1 text-gray-600">A: {paymentData.payment_wallet}</p>
                    </div>
                  )}
                  <button onClick={handleWalletPayment} disabled={!paymentData || loading} className="w-full bg-gradient-to-r from-green-600 to-green-500 text-white py-3 rounded-lg hover:from-green-700 hover:to-green-600 disabled:opacity-50 transition">
                    {loading && paymentData ? 'Procesando...' : '2. Enviar pago'}
                  </button>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
