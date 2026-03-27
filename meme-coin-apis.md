# MEME COIN EXTERNAL APIs - REAL-TIME DATA

## ✅ WORKING APIS (NO API KEYS REQUIRED)

### 1. DexScreener API
**URL:** `https://api.dexscreener.com/latest/dex/search?q=meme`
**Features:**
- Real-time trading data, volume, price, liquidity
- Buy/sell transaction ratios
- Market cap and trading activity
- Filtering by chain and token type

### 2. CoinGecko API  
**URL:** `https://api.coingecko.com/api/v3/search?query=meme`
**Features:**
- Broad meme coin database with rankings
- Market cap, volume, price movements
- Historical data and trends
- Categories for Solana, Base memes, etc

### 3. DexScreener Trending Tokens
**URL:** `https://api.dexscreener.com/latest/dex/tokens/solana`
**Features:**
- Solana-specific meme coin data
- Trending tokens by volume
- Real-time price and volume data

### 4. Custom DexScreener Filters
**Example:** `https://api.dexscreener.com/latest/dex/search?q=meme&limit=50`
- Filter by chain (solana, base, ethereum)
- Sort by volume, market cap, age
- Get comprehensive trading analytics

## 🚀 API USAGE EXAMPLES

### Basic Meme Coin Scan
```bash
curl -s "https://api.dexscreener.com/latest/dex/search?q=meme&limit=20"
```

### Solana-Specific Scan
```bash
curl -s "https://api.dexscreener.com/latest/dex/search?q=solana+meme"
```

### Market Cap Filtering
```bash
curl -s "https://api.dexscreener.com/latest/dex/search?q=meme" | jq '[.pairs[] | select((.fdv // .marketCap) >= 30000 and (.fdv // .marketCap) <= 200000)]'
```

### Trending Analysis
```bash
curl -s "https://api.coingecko.com/api/v3/search?query=meme" | jq '.coins[0:10]'
```

## 🔧 INTEGRATION WITH ALPHA SCANNER

These APIs can be integrated into our alpha scanner directly:
- Replace local scanner service with real-time API calls
- Automated filtering for 30k-200k mcap range
- Real-time buy/sell ratio analysis
- Volume momentum detection

## 📊 DATA METRICS AVAILABLE
- Real-time price and volume
- Market cap and liquidity
- Transaction counts and ratios
- Chain-specific data
- Historical performance

**Status:** Ready for immediate integration into continuous scanning system!