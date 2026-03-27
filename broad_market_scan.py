#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def fetch_top_tokens():
    """Fetch trending tokens on Solana"""
    
    # This endpoint gets trending/new tokens
    url = "https://api.dexscreener.com/latest/dex/search?q=solana&limit=200"
    
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        tokens = []
        
        if data and 'pairs' in data:
            for token in data['pairs']:
                mcap = token.get('fdv', 0)
                
                # Filter for our target range
                if 30000 <= mcap <= 200000:
                    # Get transaction data
                    h24_txns = token.get('txns', {}).get('h24', {})
                    buys = h24_txns.get('buys', 0)
                    sells = h24_txns.get('sells', 0)
                    total_txns = buys + sells
                    
                    # Skip tokens with minimal activity
                    if total_txns < 10:
                        continue
                    
                    token_info = {
                        'symbol': token.get('baseToken', {}).get('symbol', 'Unknown'),
                        'name': token.get('baseToken', {}).get('name', 'Unknown'),
                        'mcap': mcap,
                        'volume_24h': token.get('volume', {}).get('h24', 0),
                        'price_change_24h': token.get('priceChange', {}).get('h24', 0),
                        'liquidity': token.get('liquidity', {}).get('usd', 0),
                        'url': token.get('url', ''),
                        'dex': token.get('dexId', ''),
                        'chain': token.get('chainId', ''),
                        'buys': buys,
                        'sells': sells,
                        'total_txns': total_txns,
                        'buy_ratio': buys / total_txns if total_txns > 0 else 0,
                        'created_at': token.get('pairCreatedAt', 0)
                    }
                    tokens.append(token_info)
        
        return tokens
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

def calculate_potential_score(token):
    """Calculate potential score based on multiple factors"""
    
    # Volume/Market Cap ratio (trading intensity)
    vol_mcap = (token['volume_24h'] / token['mcap']) * 100 if token['mcap'] > 0 else 0
    
    # Buy pressure
    buy_pressure = max(0, (token['buy_ratio'] - 0.5) * 100)
    
    # Transaction velocity
    txn_velocity = min(20, token['total_txns'] / 15)
    
    # Liquidity health
    liquidity_score = min(15, token['liquidity'] / 10000)
    
    # Age score (newer tokens score higher)
    age_score = 0
    if token['created_at']:
        age_hours = (datetime.now().timestamp() * 1000 - token['created_at']) / (1000 * 3600)
        if age_hours < 24:
            age_score = min(15, 15 * (24 - age_hours) / 24)
    
    # Composite score
    score = min(100,
        (vol_mcap * 0.35) +        # Trading intensity 35%
        (buy_pressure * 0.25) +    # Buy pressure 25%
        (txn_velocity * 0.20) +    # Transaction velocity 20%
        (liquidity_score * 0.10) + # Liquidity health 10%
        (age_score * 0.10)         # Age bonus 10%
    )
    
    return round(score, 1)

def main():
    print("🎯 BROAD MARKET SCAN - SUB 30K-200K MCAP")
    print("=" * 50)
    print("Scan Time:", datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (Asia/Manila)"))
    print("Market Cap Range: $30,000 - $200,000")
    print("Chain: Solana")
    print()
    
    print("🔍 Scanning broad Solana market...")
    tokens = fetch_top_tokens()
    
    if not tokens:
        print("❌ No active tokens found in target range")
        return
    
    # Calculate potential scores
    for token in tokens:
        token['score'] = calculate_potential_score(token)
    
    # Sort by score
    tokens.sort(key=lambda x: x['score'], reverse=True)
    
    # Filter for high-potential tokens
    high_potential = [t for t in tokens if t['score'] >= 25]
    
    print(f"✅ Found {len(tokens)} tokens, {len(high_potential)} high-potential")
    print()
    print("🔥 TOP POTENTIAL ALPHA PICKS:")
    print("-" * 50)
    
    for i, token in enumerate(high_potential[:8], 1):
        vol_mcap = (token['volume_24h'] / token['mcap']) * 100 if token['mcap'] > 0 else 0
        
        print(f"{i}. {token['symbol']} - Score: {token['score']}/100")
        print(f"   📛 Name: {token['name']}")
        print(f"   💰 MCap: ${token['mcap']:,}")
        print(f"   📈 24h Vol: ${token['volume_24h']:,} ({vol_mcap:.1f}% ratio)")
        print(f"   🟢 Buy/Sell: {token['buys']}/{token['sells']} ({token['buy_ratio']:.1%})")
        print(f"   📊 Price Δ: {token['price_change_24h'] or 0:.1f}%")
        print(f"   💧 Liquidity: ${token['liquidity']:,.0f}")
        print(f"   🌐 Dex: {token['dex']}")
        print(f"   🔗 {token['url']}")
        print()
    
    # Market summary
    print("📊 SCAN SUMMARY:")
    print(f"• Total Active Tokens: {len(tokens)}")
    print(f"• High Potential Tokens: {len(high_potential)}")
    if high_potential:
        print(f"• Avg MCap: ${sum(t['mcap'] for t in high_potential)/len(high_potential):,.0f}")
        print(f"• Avg Vol/MCap Ratio: {sum((t['volume_24h']/t['mcap']*100 if t['mcap']>0 else 0) for t in high_potential)/len(high_potential):.1f}%")
        print(f"• Avg Buy Ratio: {sum(t['buy_ratio'] for t in high_potential)/len(high_potential):.1%}")
    
    print()
    print("💡 Alpha Detection based on: Volume/MCap ratio, Buy Pressure, Transaction Velocity")
    print("DYOR - These are high-risk crypto assets")

if __name__ == "__main__":
    main()