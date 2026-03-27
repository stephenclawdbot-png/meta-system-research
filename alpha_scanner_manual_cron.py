#!/usr/bin/env python3
"""
Manual Alpha Scanner for Memecoins (30k-200k mcap)
Scans DexScreener API directly
"""

import requests
import json
from datetime import datetime

def fetch_memecoins():
    """Fetch trending memecoins from DexScreener"""
    # Try multiple searches for memecoin patterns
    searches = ["meme", "cat", "doge", "elon", "pepe", "floki", "shib"]
    all_pairs = []
    
    for search_term in searches:
        url = f"https://api.dexscreener.com/latest/dex/search/?q={search_term}"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                all_pairs.extend(data.get('pairs', []))
        except Exception as e:
            print(f"⚠️ Search '{search_term}' failed: {e}")
    
    # Remove duplicates by pair address
    unique_pairs = {}
    for pair in all_pairs:
        address = pair.get('pairAddress')
        if address and address not in unique_pairs:
            unique_pairs[address] = pair
    
    return {"pairs": list(unique_pairs.values())}

def filter_memecoins(data):
    """Filter for memecoins in the 30k-200k mcap range"""
    alpha_tokens = []
    
    for pair in data.get('pairs', [])[:50]:
        try:
            # Skip major tokens
            symbol = pair.get('baseToken', {}).get('symbol', '').upper()
            if symbol in ['SOL', 'ETH', 'BTC', 'USDC', 'USDT', 'WETH', 'WBTC']:
                continue
                
            # Get key metrics
            fdv = pair.get('fdv', 0)
            volume = pair.get('volume', {}).get('h24', 0)
            
            # Calculate buy ratio
            h24_txns = pair.get('txns', {}).get('h24', {})
            buys = h24_txns.get('buys', 0)
            sells = h24_txns.get('sells', 0)
            total_txns = buys + sells
            buy_ratio = buys / total_txns if total_txns > 0 else 0
            
            # Filter criteria
            if (fdv >= 20000 and fdv <= 200000 and
                volume >= 500 and
                total_txns >= 10 and
                buy_ratio >= 0.5):
                
                alpha_tokens.append({
                    "symbol": symbol,
                    "name": pair.get('baseToken', {}).get('name', 'Unknown'),
                    "mcap": int(fdv),
                    "volume": round(volume, 2),
                    "buy_ratio": round(buy_ratio * 100, 1),
                    "price_change": pair.get('priceChange', {}).get('h24', 0),
                    "liquidity": pair.get('liquidity', {}).get('usd', 0),
                    "chain": pair.get('chainId', 'unknown'),
                    "url": pair.get('url', '')
                })
                
        except Exception as e:
            continue
    
    return alpha_tokens

def generate_report(memecoins):
    """Generate summary report"""
    report = f"MEMECOIN ALPHA SCANNER REPORT\n"
    report += f"Time: {datetime.now().strftime('%A, %B %d, %Y — %I:%M %p (Asia/Manila)')}\n"
    report += f"Filter: Market Cap $30,000 - $200,000\n"
    report += "="*60 + "\n"
    
    if memecoins:
        report += f"Found {len(memecoins)} potential alpha tokens:\n\n"
        
        for i, token in enumerate(memecoins[:10], 1):  # Max 10 tokens
            report += f"🎯 {i}. {token['symbol']}\n"
            report += f"   📛 {token['name']}\n"
            report += f"   💰 Market Cap: ${token['mcap']:,}\n"
            report += f"   📈 24h Volume: ${token['volume']:,}\n"
            report += f"   📊 Price Change: {token['price_change']:.2f}%\n"
            report += f"   📈 Buy Ratio: {token['buy_ratio']}%\n"
            report += f"   💧 Liquidity: ${token['liquidity']:,.2f}\n"
            report += f"   🌐 Chain: {token['chain']}\n"
            report += "\n"
    else:
        report += "No alpha tokens found in target range.\n"
    
    report += "\n⚠️ DISCLAIMER: High risk investment - DYOR only\n"
    return report

if __name__ == "__main__":
    print("🔄 Scanning DexScreener for memecoins...")
    
    data = fetch_memecoins()
    
    if "error" in data:
        print(f"❌ Error: {data['error']}")
        exit(1)
    
    alpha_tokens = filter_memecoins(data)
    report = generate_report(alpha_tokens)
    
    print(report)
    
    # Save report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"cron_memecoin_alpha_report_{timestamp}.txt"
    
    with open(filename, 'w') as f:
        f.write(report)
    
    print(f"✅ Report saved as {filename}")