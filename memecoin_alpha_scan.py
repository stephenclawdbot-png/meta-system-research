#!/usr/bin/env python3
import json
import subprocess
from datetime import datetime

def fetch_memecoin_data():
    """Fetch memecoin data from DexScreener with better filtering"""
    
    # Try multiple search queries for memecoins
    searches = ["new", "solana", "meme", "dog", "cat", "pepe", "shib"]
    
    all_pairs = []
    
    for query in searches:
        cmd = f'curl -s "https://api.dexscreener.com/latest/dex/search?q={query}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        try:
            data = json.loads(result.stdout)
            if data and 'pairs' in data:
                all_pairs.extend(data['pairs'])
        except:
            continue
    
    return all_pairs

def analyze_memecoins(pairs):
    """Analyze memecoins for alpha signals"""
    
    alpha_gems = []
    
    for pair in pairs:
        try:
            mcap = pair.get('fdv', 0)
            
            # Filter by market cap (30k-200k)
            if mcap < 30000 or mcap > 200000:
                continue
            
            # Filter by token name/symbol for memecoin characteristics
            symbol = pair.get('baseToken', {}).get('symbol', '').lower()
            name = pair.get('baseToken', {}).get('name', '').lower()
            
            # Skip if it looks like SOL/WETH etc
            if symbol in ['sol', 'eth', 'usdc', 'usdt', 'btc']:
                continue
            
            volume_24h = pair.get('volume', {}).get('h24', 0)
            liquidity = pair.get('liquidity', {}).get('usd', 0)
            price_change = pair.get('priceChange', {}).get('h24', 0)
            
            txns = pair.get('txns', {}).get('h24', {})
            buys = txns.get('buys', 0)
            sells = txns.get('sells', 0)
            total_txns = buys + sells
            buy_ratio = buys / total_txns if total_txns > 0 else 0
            
            # Alpha scoring focused on memecoins
            alpha_score = 0
            
            # Volume/Price momentum (max 30)
            vol_mcap_ratio = (volume_24h / mcap) * 100
            if vol_mcap_ratio > 25: alpha_score += 15
            elif vol_mcap_ratio > 10: alpha_score += 10
            elif vol_mcap_ratio > 5: alpha_score += 5
            
            if price_change > 20: alpha_score += 15
            elif price_change > 10: alpha_score += 8
            elif price_change > 5: alpha_score += 2
            
            # Buy pressure (max 20)
            if buy_ratio > 0.7: alpha_score += 20
            elif buy_ratio > 0.6: alpha_score += 15
            elif buy_ratio > 0.55: alpha_score += 10
            elif buy_ratio > 0.5: alpha_score += 5
            
            # Transaction velocity (max 15)
            if total_txns > 200: alpha_score += 15
            elif total_txns > 100: alpha_score += 10
            elif total_txns > 50: alpha_score += 5
            
            # Liquidity strength (max 15)
            if liquidity > 10000: alpha_score += 15
            elif liquidity > 5000: alpha_score += 10
            elif liquidity > 1000: alpha_score += 5
            
            # Memecoin pattern bonus (max 10)
            meme_keywords = ['dog', 'cat', 'pepe', 'shib', 'inu', 'bonk', 'woof', 'meow', 'meme']
            if any(keyword in symbol.lower() or keyword in name.lower() for keyword in meme_keywords):
                alpha_score += 10
            
            # Minimum transaction activity filter
            if total_txns < 10:
                continue
                
            # Minimum volume filter
            if volume_24h < 500:
                continue
            
            alpha_gems.append({
                'symbol': symbol.upper(),
                'name': pair.get('baseToken', {}).get('name', ''),
                'mcap': mcap,
                'volume_24h': volume_24h,
                'vol_mcap_ratio': vol_mcap_ratio,
                'price_change': price_change,
                'liquidity': liquidity,
                'buy_ratio': buy_ratio * 100,
                'total_txns': total_txns,
                'alpha_score': alpha_score,
                'chain': pair.get('chainId', ''),
                'url': pair.get('url', ''),
                'age': pair.get('pairCreatedAt', 0)
            })
            
        except Exception as e:
            continue
    
    # Sort by alpha score
    alpha_gems.sort(key=lambda x: x['alpha_score'], reverse=True)
    return alpha_gems

def main():
    print("🎯 MEMECOIN ALPHA SCANNER")
    print("=" * 60)
    print("Scan Time:", datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (Asia/Manila)"))
    print("Market Cap Range: $30,000 - $200,000")
    print("Target: Memecoins with alpha signals before mainstream attention")
    print()
    
    print("🔍 Fetching memecoin data from DexScreener...")
    pairs = fetch_memecoin_data()
    
    print(f"📊 Found {len(pairs)} total pairs")
    
    gems = analyze_memecoins(pairs)
    
    print(f"✅ Filtered to {len(gems)} qualifying memecoins\n")
    
    if gems:
        print("🔥 TOP ALPHA MEMECOINS")
        print("-" * 40)
        
        for i, gem in enumerate(gems[:5], 1):
            print(f"{i}. {gem['symbol']} - Alpha Score: {gem['alpha_score']}/90")
            print(f"   💰 Market Cap: ${gem['mcap']:,}")
            print(f"   📈 24h Vol/Mcap: {gem['vol_mcap_ratio']:.1f}%")
            print(f"   🔼 Price Change: {gem['price_change']:.1f}%")
            print(f"   💧 Liquidity: ${gem['liquidity']:,}")
            print(f"   🛒 Buy Ratio: {gem['buy_ratio']:.1f}%")
            print(f"   🔄 Transactions: {gem['total_txns']}")
            print(f"   🌐 Chain: {gem['chain']}")
            print(f"   🔗 DexScreener: {gem['url']}")
            print()
    else:
        print("⚠️ No alpha memecoins found in target range")
        print("Market conditions suggest either:")
        print("- No undervalued gems available")
        print("- Scanning limitations (API limitations)")
        print("- Market consolidation period")
    
    print("ℹ️ DISCLAIMER: High-risk memecoins, do your own research")

if __name__ == "__main__":
    main()