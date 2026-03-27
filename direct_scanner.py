#!/usr/bin/env python3
import subprocess
import json
from datetime import datetime

def search_dexscreener(query):
    """Search DexScreener for tokens"""
    try:
        cmd = f"curl -s 'https://api.dexscreener.com/latest/dex/search/?q={query}'"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data
    except Exception as e:
        print(f"Error searching DexScreener: {e}")
    return None

def analyze_pairs(data):
    """Analyze pairs for alpha gems"""
    alpha_gems = []
    
    if not data or 'pairs' not in data or not data['pairs']:
        return alpha_gems
    
    for pair in data['pairs']:
        try:
            # Market cap filtering (30k-200k range)
            mcap = pair.get('fdv', 0)
            if not (30000 <= mcap <= 200000):
                continue
            
            # Volume filtering
            volume_24h = pair.get('volume', {}).get('h24', 0)
            if volume_24h < 1000:
                continue
                
            # Get basic info
            symbol = pair.get('baseToken', {}).get('symbol', 'Unknown')
            name = pair.get('baseToken', {}).get('name', 'Unknown')
            price_change = pair.get('priceChange', {}).get('h24', 0)
            liquidity = pair.get('liquidity', {}).get('usd', 0)
            dex_url = pair.get('url', '')
            
            # Transaction data
            tx_24h = pair.get('txns', {}).get('h24', {})
            buys_24h = tx_24h.get('buys', 0)
            sells_24h = tx_24h.get('sells', 0)
            total_tx = buys_24h + sells_24h
            buy_ratio = buys_24h / total_tx if total_tx > 0 else 0
            
            # Calculate alpha score (simplified)
            alpha_score = 0
            
            # Volume/mcap ratio
            vol_mcap_ratio = volume_24h / mcap if mcap > 0 else 0
            if vol_mcap_ratio > 1.0:
                alpha_score += 40
            elif vol_mcap_ratio > 0.5:
                alpha_score += 30
            elif vol_mcap_ratio > 0.2:
                alpha_score += 20
            elif vol_mcap_ratio > 0.1:
                alpha_score += 10
                
            # Price momentum
            if price_change > 0:
                if price_change > 50:
                    alpha_score += 30
                elif price_change > 20:
                    alpha_score += 20
                elif price_change > 10:
                    alpha_score += 10
                    
            # Buy ratio bonus
            if buy_ratio > 0.6:
                alpha_score += 15
            elif buy_ratio > 0.55:
                alpha_score += 10
            elif buy_ratio > 0.5:
                alpha_score += 5
                
            # Liquidity bonus
            if liquidity > 5000:
                alpha_score += 10
            elif liquidity > 2000:
                alpha_score += 5
                
            alpha_gems.append({
                'symbol': symbol,
                'name': name,
                'mcap': mcap,
                'volume_24h': volume_24h,
                'price_change': price_change,
                'liquidity': liquidity,
                'alpha_score': alpha_score,
                'buy_ratio': buy_ratio * 100,
                'total_tx': total_tx,
                'buys': buys_24h,
                'sells': sells_24h,
                'dex_url': dex_url,
                'chain': dex_url.split('/')[3] if dex_url else 'unknown'
            })
            
        except Exception as e:
            continue
    
    # Sort by alpha score
    alpha_gems.sort(key=lambda x: x['alpha_score'], reverse=True)
    return alpha_gems

def search_common_memecoin_patterns():
    """Search for common memecoin patterns"""
    patterns = ["meme", "coin", "token", "pepe", "doge", "shib", "elon", "moon", "pump", "gem", "alpha"]
    all_gems = []
    
    for pattern in patterns:
        print(f"Searching for: {pattern}")
        data = search_dexscreener(pattern)
        if data:
            gems = analyze_pairs(data)
            all_gems.extend(gems)
    
    # Remove duplicates by symbol
    seen_symbols = set()
    unique_gems = []
    for gem in all_gems:
        if gem['symbol'] not in seen_symbols:
            seen_symbols.add(gem['symbol'])
            unique_gems.append(gem)
    
    unique_gems.sort(key=lambda x: x['alpha_score'], reverse=True)
    return unique_gems

def main():
    timestamp = datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (Asia/Manila)")
    
    print("🎯 DIRECT MEMECOIN SCANNER")
    print("=" * 60)
    print(f"Scan Time: {timestamp}")
    print("Market Cap Range: $30,000 - $200,000")
    print("Search Method: Direct search for common memecoin patterns")
    print()
    
    alpha_gems = search_common_memecoin_patterns()
    
    if not alpha_gems:
        print("❌ No memecoin gems found matching criteria")
        print("   Market is currently quiet for small-cap memecoins")
        print("   This is normal during late hours - check again during active trading")
        return
    
    print(f"💎 MEMECOIN GEMS FOUND: {len(alpha_gems)}")
    print("=" * 60)
    
    for i, gem in enumerate(alpha_gems[:10], 1):
        print(f"\n🎯 #{i} {gem['symbol']} - Alpha Score: {gem['alpha_score']}/100")
        print(f"   📈 24h Stats: ${gem['volume_24h']:,} vol • ${gem['mcap']:,} mcap • {gem['volume_24h']/gem['mcap']:.1%} ratio")
        print(f"   📊 Sentiment: {gem['price_change']:.1f}% price • {gem['buy_ratio']:.1f}% buy ratio")
        print(f"   🔄 Activity: {gem['total_tx']} txns ({gem['buys']} buys/{gem['sells']} sells)")
        print(f"   💧 Liquidity: ${gem['liquidity']:,}")
        print(f"   🌐 Chain: {gem['chain']}")
        print(f"   🔗 {gem['dex_url']}")
    
    print(f"\n📊 MARKET SUMMARY")
    print("=" * 60)
    print(f"• Total Gems Found: {len(alpha_gems)}")
    print(f"• Top Alpha Score: {alpha_gems[0]['alpha_score']}/100" if alpha_gems else "None")
    print(f"• Search Coverage: Common memecoin keywords")
    
    print(f"\n⚠️ DISCLAIMER: High risk assets - DYOR required")
    print("Market is currently in quiet phase - check during peak hours")

if __name__ == "__main__":
    main()