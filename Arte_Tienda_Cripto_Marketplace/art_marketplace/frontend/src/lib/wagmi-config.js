import { http, createConfig, injected } from 'wagmi'
import { walletConnect } from '@wagmi/connectors'
import { arbitrumSepolia, arbitrum } from 'wagmi/chains'

const projectId = 'b02910bd7a66d789cf2c18c1e9720e29'

export const config = createConfig({
  chains: [arbitrumSepolia, arbitrum],
  connectors: [
    injected(),
    walletConnect({ projectId }),
  ],
  transports: {
    [arbitrumSepolia.id]: http('https://sepolia-rollup.arbitrum.io/rpc'),
    [arbitrum.id]: http('https://arb1.arbitrum.io/rpc'),
  },
})
