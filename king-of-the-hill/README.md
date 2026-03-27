# 👑 King of the Hill

A Pump.fun compatible degen game built on Solana. Dethrone the King, claim the Treasury, or watch the timer tick down.

## 🎮 How It Works

1. **Claim the Throne** — Pay the current price to dethrone the King
2. **Splits** — 80% to previous King, 15% to Treasury, 5% burned
3. **Escalate** — Price increases 10% with every claim
4. **Win** — If no one claims for 24h, the King wins the entire Treasury

## 📊 Tokenomics

| Action | Distribution |
|--------|-------------|
| To Previous King | 80% |
| To Treasury Pot | 15% |
| Burned | 5% |
| Price Escalation | +10% |
| Victory Timer | 24 hours |

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- Rust 1.76+
- Solana CLI 1.18+
- Anchor CLI 0.30+

### Install Dependencies

```bash
# Program dependencies
cd program
cargo build

# Frontend dependencies
cd ../app
npm install
```

### Deploy to Devnet

```bash
# 1. Build the program
cd program
anchor build

# 2. Deploy
anchor deploy --provider.cluster devnet

# 3. Update program ID in lib.rs and anchorClient.js
# Replace "Your_Program_ID_Here" with actual ID

# 4. Initialize the game
anchor run initialize --provider.cluster devnet
```

### Run Frontend

```bash
cd app
npm start
```

Then open http://localhost:3000

## 📁 Project Structure

```
king-of-the-hill/
├── Anchor.toml              # Anchor configuration
├── program/
│   ├── Cargo.toml           # Rust dependencies
│   └── src/
│       └── lib.rs             # Smart contract
├── app/                     # React frontend
│   ├── package.json
│   └── src/
│       ├── App.js
│       ├── components/
│       │   └── KingOfTheHill.js
│       └── utils/
│           └── anchorClient.js
└── README.md
```

## 🧪 Testing

```bash
cd program
anchor test
```

## 📝 Contract Functions

| Function | Description |
|----------|-------------|
| `initialize_game` | Creates new game with initial price |
| `claim_throne` | Pay to become the new King |
| `claim_victory` | Winner claims Treasury (after 24h) |
| `start_new_round` | Begin new round after victory |

## 🎯 Pump.fun Integration

To launch on Pump.fun:

1. Create token on Pump.fun
2. Update `TOKEN_MINT` in frontend
3. Deploy program to mainnet
4. Initialize game with Pump.fun token
5. Launch game UI

## 🔒 Security

- Contract uses PDAs for deterministic addresses
- Treasury is controlled by program, not dev wallet
- Player stats tracked per-wallet
- Events emitted for all actions

## 📈 Success Metrics

- **King Claims** — Price escalates, creates buy pressure
- **Victory Claims** — Big single payouts, viral moments
- **Burn Mechanics** — Deflationary pressure on token
- **Leaderboard** — Social competition drives engagement

## 🤝 Contributing

1. Fork the repo
2. Create feature branch
3. Submit PR

## 📄 License

MIT License — see LICENSE file

## ⚠️ Disclaimer

This is a degen game. Play responsibly. Not financial advice. Code is provided as-is.

---

**Built for Pump.fun degens. May the best King win.** 👑
