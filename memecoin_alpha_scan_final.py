#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def fetch_dexscreener_tokens(min_mcap=30000, max_mcap=200000):
    """Fetch tokens from DexScreener API with market cap filtering"""
    tokens = []
    
    # Search for trending memecoins
    trending_url = "https://api.dexscreener.com/latest/dex/tokens/trending"
    try:
        response = requests.get(trending_url)
        if response.status_code == 200:
            data = response.json()
            tokens.extend(data.get('pairs', []))
    except Exception as e:
        pass
    
    # Search for specific memecoin keywords
    keywords = ['memecoin', 'dog', 'cat', 'pepe', 'inu', 'sats', 'bonk']
    
    for keyword in keywords:
        try:
            search_url = f"https://api.dexscreener.com/latest/dex/search?q={keyword}"
            response = requests.get(search_url)
            if response.status_code == 200:
                data = response.json()
                search_tokens = data.get('pairs', [])
                tokens.extend(search_tokens)
        except Exception as e:
            pass
    
    # Remove duplicates
    seen_addresses = set()
    unique_tokens = []
    for token in tokens:
        addr = token.get('pairAddress')
        if addr and addr not in seen_addresses:
            mcap = token.get('fdv', 0)
            # Filter by market cap
            if min_mcap <= mcap <= max_mcap:
                seen_addresses.add(addr)
                unique_tokens.append(token)
    
    return unique_tokens

def calculate_alpha_score(token):
    """Calculate alpha score for a token"""
    mcap = token.get('fdv', 0)
    volume_24h = token.get('volume', {}).get('h24', 0)
    price_change = token.get('priceChange', {}).get('h24', 0)
    
    # Volume/MCap ratio (most important)
    vol_mcap_ratio = (volume_24h / mcap * 100) if mcap > 0 else 0
    vol_score = min(50, max(0, vol_mcap_ratio * 0.5))
    
    # Price momentum
    momentum_score = min(30, max(0, price_change * 0.3))
    
    # Transaction activity
    txns = token.get('txns', {}).get('h24', {})
    total_txns = txns.get('buys', 0) + txns.get('sells', 0)
    activity_score = min(10, total_txns / 100)
    
    # Liquidity
    liquidity = token.get('liquidity', {}).get('usd', 0)
    liquidity_score = min(10, liquidity / 5000)
    
    total_score = vol_score + momentum_score + activity_score + liquidity_score
    return min(100, total_score)

def main():
    print("🚀 MEMECOIN ALPHA SCANNER - SUB 30K-200K MCAP")
    print("=" * 60)
    print("Scan Time:", datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (Asia/Manila)"))
    print("Target Range: $30k - $200k Market Cap")
    print()
    
    # Fetch tokens
    tokens = fetch_dexscreener_tokens()
    
    if not tokens:
        print("❌ No memecoins found in target range")
        return
    
    # Calculate scores
    scored_tokens = []
    for token in tokens:
        symbol = token.get('baseToken', {}).get('symbol', 'Unknown')
        name = token.get('baseToken', {}).get('name', 'Unknown')
        
        # Skip wrapped tokens and SOL derivatives
        if 'SOL' in symbol.upper() or 'solana' in name.lower():
            continue
            
        mcap = token.get('fdv', 0)
        volume_24h = token.get('volume', {}).get('h24', 0)
        price_change = token.get('priceChange', {}).get('h24', 0)
        
        # Skip tokens with unrealistic data
        if volume_24h > mcap * 100:  # Volume > 100x mcap is unrealistic
            continue
            
        alpha_score = calculate_alpha_score(token)
        
        scored_tokens.append({
            'symbol': symbol,
            'name': name,
            'mcap': mcap,
            'volume_24h': volume_24h,
            'price_change': price_change,
            'alpha_score': alpha_score,
            'chain': token.get('chainId', ''),
            'url': token.get('url', ''),
            'txns': token.get('txns', {}).get('h24', {})
        })
    
    # Sort by alpha score
    scored_tokens.sort(key=lambda x: x['alpha_score'], reverse=True)
    
    print("🔥 TOP ALPHA MEMECOINS DETECTED:")
    print("-" * 50)
    
    for i, token in enumerate(scored_tokens[:10], 1):
        vol_mcap_ratio = (token['volume_24h'] / token['mcap'] * 100) if token['mcap'] > 0 else 0
        txns = token['txns']
        buys = txns.get('buys', 0)
        sells = txns.get('sells', 0)
        buy_ratio = (buys / (buys + sells) * 100) if (buys + sells) > 0 else 0
        
        print(f"🎯 #{i} {token['symbol']} ({token['name']})")
        print(f"   Alpha Score: {token['alpha_score']:.1f}/100")
        print(f"   Market Cap: ${token['mcap']:,.0f} | Vol: ${token['volume_24h']:,.0f}")
        print(f"   Vol/MCap Ratio: {vol_mcap_ratio:.1f}%")
        print(f"   24h Change: {token['price_change']:.1f}%")
        print(f"   Buy Ratio: {buy_ratio:.1f}% ({buys} buys, {sells} sells)")
        print(f"   Chain: {token['chain']}")
        print(f"   URL: {token['url']}")
        print()
    
    # Summary
    print("📊 SCAN SUMMARY:")
    print("-" * 20)
    print(f"Total Gems Found: {len(scored_tokens)} tokens")
    if scored_tokens:
        print(f"Highest Alpha: {scored_tokens[0]['symbol']} ({scored_tokens[0]['alpha_score']:.1f}/100)")
        avg_mcap = sum(t['mcap'] for t in scored_tokens) / len(scored_tokens)
        avg_vol = sum(t['volume_24h'] for t in scored_tokens) / len(scored_tokens)
        avg_ratio = sum((t['volume_24h']/t['mcap']*100 if t['mcap']>0 else 0) for t in scored_tokens) / len(scored_tokens)
        print(f"Average Market Cap: ${avg_mcap:,.0f}")
        print(f"Average Volume: ${avg_vol:,.0f}")
        print(f"Average Vol/MCap Ratio: {avg_ratio:.1f}%")
    
    print("\n🔍 KEY INSIGHTS:")
    print("• High Volume/MCap ratio signals strong interest")
    print("• Positive price momentum indicates bullish sentiment")
    print("• Buy ratio >50% suggests accumulation")
    print("\n⚠️ DISCLAIMER: High risk memecoin scanning - NFA")

if __name__ == "__main__":
    main()