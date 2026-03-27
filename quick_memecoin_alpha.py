#!/usr/bin/env python3
import requests
import json
from datetime import datetime

# Simple Alpha Scanner for sub-200k mcap memecoins

def fetch_solana_dexscreener():
    """Fetch trending Solana tokens from DexScreener"""
    print("🔍 Fetching trending Solana tokens...")
    url = "https://api.dexscreener.com/latest/dex/search?q=solana&limit=100"
    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            return data.get('pairs', [])
    except Exception as e:
        print(f"Error: {e}")
    
    return []

def analyze_token(token, index):
    """Quick analysis to see what's being filtered out"""
    mcap = token.get('fdv', token.get('marketCap', 0))
    volume = token.get('volume', {}).get('h24', 0)
    symbol = token.get('baseToken', {}).get('symbol', '').upper()
    
    # Skip major tokens
    major_tokens = {'SOL', 'ETH', 'BTC', 'USDC', 'USDT', 'WIF', 'BONK', 'TRUMP', 'DOGE', 'SHIB'}
    if symbol in major_tokens:
        return None
    
    # Check mcap range
    if not (30000 <= mcap <= 200000):
        return None
    
    # Skip low volume
    if volume < 1000:
        return None
    
    # Calculate age
    age_hours = 0
    created_at = token.get('pairCreatedAt')
    if created_at:
        created_dt = datetime.fromtimestamp(created_at / 1000)
        now = datetime.now()
        age_hours = (now - created_dt).total_seconds() / 3600
    
    return {
        'symbol': symbol,
        'name': token.get('baseToken', {}).get('name', 'Unknown'),
        'mcap': mcap,
        'volume': volume,
        'price_change': token.get('priceChange', {}).get('h24', 0),
        'url': token.get('url', ''),
        'age_hours': age_hours,
        'passed_filters': f"MCap ${mcap:,}, Vol ${volume:,}, Age {age_hours:.1f}h"
    }

def calculate_alpha_score(token):
    """Simple alpha scoring"""
    mcap = token['mcap']
    volume = token['volume']
    vol_mcap_ratio = (volume / mcap * 100) if mcap > 0 else 0
    
    score = min(80, vol_mcap_ratio * 0.8)  # Volume efficiency is key
    
    # Bonus for good metrics
    if token['price_change'] > 0:
        score += min(10, token['price_change'] * 0.1)
    
    if token['age_hours'] < 24:
        score += min(10, (24 - token['age_hours']) / 24 * 10)
    
    return min(100, score)

def run_scan():
    """Run quick memecoin scan"""
    tokens = fetch_solana_dexscreener()
    print(f"📍 Found {len(tokens)} tokens")
    
    filtered_tokens = []
    for i, token in enumerate(tokens):
        analysis = analyze_token(token, i)
        if analysis:
            analysis['alpha_score'] = calculate_alpha_score(analysis)
            filtered_tokens.append(analysis)
    
    # Sort by alpha score
    filtered_tokens.sort(key=lambda x: x['alpha_score'], reverse=True)
    
    return filtered_tokens[:10]  # Top 10

if __name__ == "__main__":
    print("🎯 QUICK MEMECOIN ALPHA SCANNER")
    print("="*50)
    print(f"Scan Time: {datetime.now().strftime('%A, %B %d, %Y — %I:%M %p (Asia/Manila)')}")
    print("Target Range: $30K - $200K Market Cap\n")
    
    tokens = run_scan()
    
    if tokens:
        print(f"🔥 Found {len(tokens)} Alpha Candidates:\n")
        for i, token in enumerate(tokens, 1):
            vol_mcap_ratio = (token['volume'] / token['mcap'] * 100) if token['mcap'] > 0 else 0
            print(f"#{i} {token['symbol']}")
            print(f"   Alpha Score: {token['alpha_score']:.1f}/100")
            print(f"   MCap: ${token['mcap']:,}")
            print(f"   Volume: ${token['volume']:,}")
            print(f"   Vol/MCap: {vol_mcap_ratio:.1f}%")
            print(f"   Price Δ: {token['price_change']:+.1f}%")
            print(f"   Age: {token['age_hours']:.1f}h")
            print(f"   URL: {token['url']}")
            print()
    else:
        print("📭 No tokens found matching criteria")
    
    print("⚠️  DISCLAIMER: High risk memecoins - Not financial advice")