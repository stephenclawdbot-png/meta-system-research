import React, { useState, useEffect } from 'react';
import { useConnection, useWallet } from '@solana/wallet-adapter-react';
import { WalletMultiButton } from '@solana/wallet-adapter-react-ui';
import { PublicKey } from '@solana/web3.js';
import './KingOfTheHill.css';

const TOKEN_MINT = new PublicKey("Your_Token_Mint_Here");
const PROGRAM_ID = new PublicKey("Your_Program_ID_Here");

const KingOfTheHill = () => {
  const { connection } = useConnection();
  const wallet = useWallet();
  
  const [gameState, setGameState] = useState(null);
  const [playerStats, setPlayerStats] = useState(null);
  const [timeRemaining, setTimeRemaining] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [leaderboard, setLeaderboard] = useState([]);

  // Fetch game state
  const fetchGameState = async () => {
    try {
      // Get game PDA
      const [gamePDA] = await PublicKey.findProgramAddressSync(
        [Buffer.from("king_of_the_hill"), TOKEN_MINT.toBuffer()],
        PROGRAM_ID
      );
      
      // For now, mock the game state
      // In production, this would call the program
      const mockState = {
        currentKing: "7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU",
        thronePrice: 10000000, // 10 tokens
        totalPot: 500000000,    // 500 tokens
        lastClaimTime: Date.now() / 1000 - 3600, // 1 hour ago
        gameEnded: false,
      };
      
      setGameState(mockState);
      
      // Calculate time remaining (24h from last claim)
      const endTime = mockState.lastClaimTime + 86400;
      const now = Date.now() / 1000;
      setTimeRemaining(Math.max(0, endTime - now));
    } catch (err) {
      console.error("Error fetching game state:", err);
      setError("Failed to load game state");
    }
  };

  // Update timer every second
  useEffect(() => {
    fetchGameState();
    const interval = setInterval(() => {
      setTimeRemaining(prev => Math.max(0, prev - 1));
      if (timeRemaining <= 0) {
        fetchGameState();
      }
    }, 1000);
    
    return () => clearInterval(interval);
  }, []);

  // Format time remaining
  const formatTime = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);
    return `${hours}h ${mins}m ${secs}s`;
  };

  // Format token amount
  const formatTokens = (amount) => {
    return (amount / 1000000).toFixed(2);
  };

  // Claim throne
  const handleClaimThrone = async () => {
    if (!wallet.connected) {
      setError("Please connect wallet first");
      return;
    }
    
    setLoading(true);
    setError(null);
    setSuccess(null);
    
    try {
      // In production, call the program
      // const tx = await program.methods.claimThrone().accounts({...}).rpc();
      
      // Mock success
      await new Promise(r => setTimeout(r, 2000));
      setSuccess("Throne claimed successfully! You are now the King!");
      fetchGameState();
    } catch (err) {
      console.error("Error claiming throne:", err);
      setError(err.message || "Failed to claim throne");
    } finally {
      setLoading(false);
    }
  };

  // Claim victory
  const handleClaimVictory = async () => {
    if (!wallet.connected) {
      setError("Please connect wallet first");
      return;
    }
    
    setLoading(true);
    setError(null);
    setSuccess(null);
    
    try {
      // In production, call the program
      await new Promise(r => setTimeout(r, 2000));
      setSuccess(`Victory claimed! You won ${formatTokens(gameState?.totalPot || 0)} tokens!`);
      fetchGameState();
    } catch (err) {
      console.error("Error claiming victory:", err);
      setError(err.message || "Failed to claim victory");
    } finally {
      setLoading(false);
    }
  };

  // Shorten wallet address
  const shortenAddress = (address) => {
    if (!address) return "";
    return `${address.slice(0, 4)}...${address.slice(-4)}`;
  };

  // Check if current user is king
  const isKing = () => {
    if (!wallet.publicKey || !gameState) return false;
    return wallet.publicKey.toBase58() === gameState.currentKing;
  };

  // Check if game ended
  const canClaimVictory = () => {
    return timeRemaining === 0 && gameState && !gameState.gameEnded;
  };

  return (
    <div className="game-container">
      <div className="game-panel">
        <div className="panel-header">
          <h2>👑 Current King</h2>
        </div>
        
        <div className="king-display">
          <div className="king-avatar">👑</div>
          <div className="king-info">
            <p className="king-address">
              {gameState ? shortenAddress(gameState.currentKing) : "Loading..."}
            </p>
            <p className="king-badge">{isKing() ? "(It's You!)" : ""}</p>
          </div>
        </div>
        
        <div className="stats-grid">
          <div className="stat-card">
            <span className="stat-label">Throne Price</span>
            <span className="stat-value">{gameState ? formatTokens(gameState.thronePrice) : "--"} $KING</span>
          </div>
          
          <div className="stat-card highlight">
            <span className="stat-label">Treasury Pot</span>
            <span className="stat-value">{gameState ? formatTokens(gameState.totalPot) : "--"} $KING</span>
          </div>
          
          <div className="stat-card">
            <span className="stat-label">Time Remaining</span>
            <span className="stat-value timer">{formatTime(timeRemaining)}</span>
          </div>
        </div>
        
        {wallet.connected ? (
          <div className="action-section">
            {!isKing() && timeRemaining > 0 && (
              <button 
                className="btn btn-primary"
                onClick={handleClaimThrone}
                disabled={loading}
              >
                {loading ? "Claiming..." : "Claim Throne"}
              </button>
            )}
            
            {canClaimVictory() && (
              <button 
                className="btn btn-victory"
                onClick={handleClaimVictory}
                disabled={loading}
              >
                {loading ? "Claiming..." : "Claim Victory!"}
              </button>
            )}
            
            {isKing() && timeRemaining > 0 && (
              <div className="status-message">
                You are the King! Defend your throne!
              </div>
            )}
          </div>
        ) : (
          <div className="connect-section">
            <p>Connect wallet to play</p>
            <WalletMultiButton />
          </div>
        )}
        
        {error && <div className="error-message">{error}</div>}
        {success && <div className="success-message">{success}</div>}
        
        <div className="info-section">
          <h3>How It Works</h3>
          <ul>
            <li>👑 Pay the throne price to dethrone the current King</li>
            <li>💰 80% goes to previous King, 15% to pot, 5% burned</li>
            <li>⏰ If no one claims for 24 hours, the King wins the pot</li>
            <li>🔥 Price increases 10% with every claim</li>
          </ul>
        </div>
      </div>
      
      <div className="game-panel">
        <div className="panel-header">
          <h2>🏆 Leaderboard</h2>
        </div>
        
        <div className="leaderboard">
          <div className="leaderboard-header">
            <span>Rank</span>
            <span>King</span>
            <span>Reigns</span>
            <span>Earned</span>
          </div>
          
          {leaderboard.length > 0 ? (
            leaderboard.map((player, index) => (
              <div key={index} className="leaderboard-row">
                <span>#{index + 1}</span>
                <span>{shortenAddress(player.wallet)}</span>
                <span>{player.timesKing}</span>
                <span>{formatTokens(player.totalEarned)} $KING</span>
              </div>
            ))
          ) : (
            <div className="no-data">No kings yet. Be the first!</div>
          )}
        </div>
        
        <div className="info-section">
          <h3>Token Stats</h3>
          <div className="stats-grid">
            <div className="stat-card">
              <span className="stat-label">Total Supply</span>
              <span className="stat-value">1,000,000,000 $KING</span>
            </div>
            <div className="stat-card">
              <span className="stat-label">Burned</span>
              <span className="stat-value">0 $KING</span>
            </div>
            <div className="stat-card">
              <span className="stat-label">Total Players</span>
              <span className="stat-value">{leaderboard.length}</span>
            </div>
          </div>
        </div>
        
        <div className="contract-info">
          <div className="contract-row">
            <span>Token:</span>
            <a 
              href={`https://solscan.io/token/${TOKEN_MINT}`}
              target="_blank"
              rel="noopener noreferrer"
            >
              {shortenAddress(TOKEN_MINT.toBase58())}
            </a>
          </div>
          <div className="contract-row">
            <span>Program:</span>
            <a 
              href={`https://solscan.io/account/${PROGRAM_ID}`}
              target="_blank"
              rel="noopener noreferrer"
            >
              {shortenAddress(PROGRAM_ID.toBase58())}
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default KingOfTheHill;