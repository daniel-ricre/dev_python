import { useState } from 'react';
import { ethers } from 'ethers';
import api from '../services/api';

const ESCROW_ABI = [
  "function createUsdcEscrow(bytes32 orderId, address payable artist, uint256 amount) external",
  "function createEthEscrow(bytes32 orderId, address payable artist) external payable"
];

const USDC_ABI = [
  "function approve(address spender, uint256 amount) public returns (bool)"
];

export function useEscrow(contractAddress, usdcAddress) {
  const [loading, setLoading] = useState(false);

  const purchase = async ({ artworkId, artistAddress, amount, currency }) => {
    setLoading(true);
    try {
      const provider = new ethers.BrowserProvider(window.ethereum);
      const signer = await provider.getSigner();
      const buyerAddress = await signer.getAddress();
      
      const res = await api.post('/orders', {
        artwork_id: artworkId,
        artist_address: artistAddress,
        buyer_address: buyerAddress,
        amount: amount,
        currency: currency
      });
      const orderData = res.data;

      const escrow = new ethers.Contract(contractAddress, ESCROW_ABI, signer);

      let tx;
      if (currency === 'USDC') {
        const usdc = new ethers.Contract(usdcAddress, USDC_ABI, signer);
        const amountWei = ethers.parseUnits(amount, 6);
        const approveTx = await usdc.approve(contractAddress, amountWei);
        await approveTx.wait();
        tx = await escrow.createUsdcEscrow(orderData.order_id_bytes32, artistAddress, amountWei);
      } else {
        const amountWei = ethers.parseEther(amount);
        tx = await escrow.createEthEscrow(orderData.order_id_bytes32, artistAddress, { value: amountWei });
      }
      await tx.wait();

      return { success: true, orderId: orderData.order_id, txHash: tx.hash };
    } catch (error) {
      console.error(error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  return { purchase, loading };
}
