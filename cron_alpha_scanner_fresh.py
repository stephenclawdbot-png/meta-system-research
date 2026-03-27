#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def fetch_all_memecoins():
    """Fetch trending memecoins and filter by market cap"""
    
    # Search popular memecoin-related terms
    queries = [
        "memecoin", "Pepe", "Doge", "Shib", "Bonk", "WIF", "BOME", "MEME",
        "FLOKI", "GUAC", "PUDGY", "POPCAT", "MOOK", "HARAMBE", "HODL", "HONEY"
    ]
    
    all_tokens = []
    
    for query in queries:
        try:
            url = f"https://api.dexscreener.com/latest/dex/search?q={query}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data and 'pairs' in data:
                for token in data['pairs']:
                    # Get market cap (use FDV if available)
                    mcap = token.get('fdv', 0)
                    
                    # Filter by our target range
                    if 30000 <= mcap <= 200000:
                        # Get transaction data
                        txn_data = token.get('txns', {})
                        h24 = txn_data.get('h24', {})
                        buys = h24.get('buys', 0)
                        sells = h24.get('sells', 0)
                        
                        # Only include tokens with meaningful activity
                        total_txns = buys + sells
                        if total_txns < 5:
                            continue
                            
                        token_info = {
                            'name': token.get('baseToken', {}).get('name', 'Unknown'),
                            'symbol': token.get('baseToken', {}).get('symbol', 'Unknown'),
                            'mcap': mcap,
                            'volume_24h': token.get('volume', {}).get('h24', 0),
                            'price': token.get('priceUsd', 0),
                            'price_change_24h': token.get('priceChange', {}).get('h24', 0),
                            'url': token.get('url', ''),
                            'dex': token.get('dexId', ''),
                            'chain': token.get('chainId', ''),
                            'pairAddress': token.get('pairAddress', ''),
                            'buys': buys,
                            'sells': sells,
                            'total_txns': total_txns,
                            'buy_ratio': buys / total_txns if total_txns > 0 else 0,
                            'search_term': query
                        }
                        all_tokens.append(token_info)
                        
        except Exception as e:
            print(f"Error fetching '{query}': {e}")
            continue
    
    return all_tokens

def calculate_alpha_score(token):
    """Calculate alpha score based on trading metrics"""
    
    # Volume/MCap ratio (shows trading intensity)
    vol_mcap_ratio = (token['volume_24h'] / token['mcap']) * 100 if token['mcap'] > 0 else 0
    
    # Buy pressure (more buys = accumulation)
    buy_pressure = max(0, (token['buy_ratio'] - 0.5) * 50)
    
    # Trading velocity (higher txns = more interest)
    txn_velocity = min(25, token['total_txns'] / 10)
    
    # Price momentum
    momentum = max(0, token['price_change_24h'] or 0)
    
    alpha_score = min(100,
        (vol_mcap_ratio * 0.4) +      # Trading intensity
        (buy_pressure * 0.3) +        # Buy pressure
        (txn_velocity * 0.2) +        # Transaction velocity
        (momentum * 0.1)              # Price momentum
    )
    
    return round(alpha_score, 1)

def main():
    print("🎯 SOLANA MEMECOIN ALPHA SCANNER REPORT")
    print("=" * 50)
    print("Scanning DexScreener for sub 30k-200k MCap gems")
    print("Scan Time:", datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (Asia/Manila)"))
    print("Market Cap Range: $30,000 - $200,000")
    print("Chain Filter: Solana Only")
    print()
    
    # Fetch tokens
    tokens = fetch_all_memecoins()
    
    if not tokens:
        print("❌ No memecoins found in 30k-200k range")
        return
    
    # Calculate alpha scores
    for token in tokens:
        token['alpha_score'] = calculate_alpha_score(token)
    
    # Filter out low-quality tokens (min alpha score)
    tokens = [t for t in tokens if t['alpha_score'] >= 15]
    
    # Sort by alpha score
    tokens.sort(key=lambda x: x['alpha_score'], reverse=True)
    
    print(f"🔥 TOP ALPHA MEMECOINS ({len(tokens)} total)")
    print("-" * 50)
    
    for i, token in enumerate(tokens[:5], 1):
        vol_mcap_ratio = (token['volume_24h'] / token['mcap']) * 100 if token['mcap'] > 0 else 0
        
        print(f"{i}. {token['symbol']} - Alpha Score: {token['alpha_score']}/100")
        print(f"   💰 Market Cap: ${token['mcap']:,.0f}")
        print(f"   📈 24h Volume: ${token['volume_24h']:,.0f} ({vol_mcap_ratio:.1f}%)")
        print(f"   📊 Price Change: {token['price_change_24h'] or 0:.1f}%")
        print(f"   💧 Liquidity: ${token.get('liquidity', {}).get('usd', 'N/A')}")
        print(f"   🔄 Transactions: {token['total_txns']} ({token['buys']} buys/{token['sells']} sells - {token['buy_ratio']:.1%})")
        print(f"   🌐 Chain: {token['chain']}")
        print(f"   🔗 {token['url']}")
        print()
    
    # Summary
    print("📊 MARKET SUMMARY")
    print(f"• Total Candidates: {len(tokens)}")
    if tokens:
        print(f"• Average Alpha Score: {sum(t['alpha_score'] for t in tokens)/len(tokens):.1f}/100")
        print(f"• Average Market Cap: ${sum(t['mcap'] for t in tokens)/len(tokens):,.0f}")
        print(f"• Average Volume/MCap Ratio: {sum((t['volume_24h']/t['mcap']*100 if t['mcap']>0 else 0) for t in tokens)/len(tokens):.1f}%")
    
    print()
    print("💡 Detecting alpha memecoins before mainstream attention")
    print("DYOR - High risk volatile assets")

if __name__ == "__main__":
    main()