import React from 'react';
import { WalletAdapterNetwork } from '@solana/wallet-adapter-base';
import { ConnectionProvider, WalletProvider } from '@solana/wallet-adapter-react';
import { WalletModalProvider } from '@solana/wallet-adapter-react-ui';
import { PhantomWalletAdapter, SolflareWalletAdapter } from '@solana/wallet-adapter-wallets';
import { clusterApiUrl, Connection } from '@solana/web3.js';
import KingOfTheHill from './components/KingOfTheHill';
import '@solana/wallet-adapter-react-ui/styles.css';
import './App.css';

function App() {
  // Can be set to 'devnet', 'testnet', or 'mainnet-beta'
  const network = WalletAdapterNetwork.Devnet;
  const endpoint = clusterApiUrl(network);
  
  // Initialize connection
  const connection = new Connection(endpoint, 'confirmed');

  const wallets = [
    new PhantomWalletAdapter(),
    new SolflareWalletAdapter({ network }),
  ];

  return (
    <ConnectionProvider endpoint={endpoint}>
      <WalletProvider wallets={wallets} autoConnect>
        <WalletModalProvider>
          <div className="App">
            <header className="App-header">
              <div className="logo">👑 King of the Hill</div>
              <div className="network-badge">{network.toUpperCase()}</div>
            </header>
            <main>
              <KingOfTheHill />
            </main>
            <footer>
              <p>Built for Pump.fun | Dethrone the King. Claim the Treasury.</p>
            </footer>
          </div>
        </WalletModalProvider>
      </WalletProvider>
    </ConnectionProvider>
  );
}

export default App;
