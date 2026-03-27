#!/usr/bin/env python3
import subprocess
import json
from datetime import datetime

def search_memecoins():
    """Search for memecoins using DexScreener"""
    search_terms = ["meme", "pepe", "dog", "cat", "bonk", "wif", "ordi", "slerf", "kitty", "bome", "popcat", "peng"]
    all_pairs = []
    
    for term in search_terms:
        try:
            cmd = f"curl -s 'https://api.dexscreener.com/latest/dex/search?q={term}'"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                pairs = data.get('pairs', [])
                
                # Filter for USD pairs and reasonable targets
                for pair in pairs:
                    quote_symbol = pair.get('quoteToken', {}).get('symbol', '')
                    # Look for USD pairs, especially USDC/USDT, or SOL pairs which are common
                    if quote_symbol in ['USDC', 'USDT', 'USD', 'SOL']:
                        all_pairs.append(pair)
                        
        except Exception as e:
            continue
    
    return all_pairs

def calculate_mcap(pair):
    """Estimate market cap from volume and price"""
    try:
        # Try to get fdv first
        fdv = pair.get('fdv', 0)
        if fdv > 0:
            return fdv
        
        # Fallback: estimate from price and liquidity
        price = pair.get('priceUsd', 0)
        liquidity = pair.get('liquidity', {}).get('usd', 0)
        
        # Very rough estimate - liquidity * multiplier
        if liquidity > 0:
            return liquidity * 10  # Assume 10x liquidity factor
        
        return 0
        
    except:
        return 0

def analyze_for_alpha(pairs):
    """Analyze pairs for alpha potential"""
    alpha_gems = []
    
    for pair in pairs:
        try:
            # Calculate market cap
            mcap = calculate_mcap(pair)
            
            # Skip if out of range
            if not (30000 <= mcap <= 200000):
                continue
            
            # Get basic metrics
            volume_24h = pair.get('volume', {}).get('h24', 0)
            price_change = pair.get('priceChange', {}).get('h24', 0)
            liquidity = pair.get('liquidity', {}).get('usd', 0)
            symbol = pair.get('baseToken', {}).get('symbol', 'Unknown')
            name = pair.get('baseToken', {}).get('name', 'Unknown')
            dex_url = pair.get('url', '')
            chain = pair.get('chainId', '')
            
            # Filter by minimum volume
            if volume_24h < 1000:
                continue
            
            # Calculate alpha score (0-80)
            alpha_score = 0
            
            # Volume/mcap ratio (0-40)
            if mcap > 0:
                vol_ratio = volume_24h / mcap
                alpha_score += min(int(vol_ratio * 20), 40)
            
            # Price momentum (0-20)
            if price_change > 0:
                alpha_score += min(int(price_change * 0.5), 20)
            elif price_change < -30:  # Oversold potential
                alpha_score += 5
            
            # Liquidity health (0-10)
            if liquidity > 10000:
                alpha_score += 10
            elif liquidity > 5000:
                alpha_score += 7
            elif liquidity > 2000:
                alpha_score += 4
            
            # Transaction activity (0-10)
            txns_24h = pair.get('txns', {}).get('h24', {})
            buy_count = txns_24h.get('buys', 0)
            sell_count = txns_24h.get('sells', 0)
            total_txns = buy_count + sell_count
            
            if total_txns > 100:
                alpha_score += 10
            elif total_txns > 50:
                alpha_score += 6
            elif total_txns > 20:
                alpha_score += 3
            
            if alpha_score >= 20:  # Minimum threshold
                alpha_gems.append({
                    'symbol': symbol,
                    'name': name,
                    'mcap': mcap,
                    'volume_24h': volume_24h,
                    'price_change': price_change,
                    'liquidity': liquidity,
                    'alpha_score': alpha_score,
                    'dex_url': dex_url,
                    'chain': chain,
                    'buys_24h': buy_count,
                    'sells_24h': sell_count
                })
                
        except Exception as e:
            continue
    
    # Sort by alpha score
    alpha_gems.sort(key=lambda x: x['alpha_score'], reverse=True)
    return alpha_gems

def main():
    timestamp = datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (Asia/Manila)")
    
    print("🎯 MEMECOIN ALPHA SCANNER - CRON JOB EXECUTION")
    print("=" * 70)
    print(f"Scan Time: {timestamp}")
    print("Market Cap Range: $30,000 - $200,000")
    print("Min Volume: $1,000")
    print("Alpha Score >= 20/80 required")
    print("Search Terms: meme, pepe, dog, cat, bonk, wif, ordi, slerf, kitty, bome, popcat, peng")
    print()
    
    # Fetch data
    print("🔍 Scanning DexScreener for memecoin data...")
    pairs = search_memecoins()
    
    if not pairs:
        print("❌ No memecoin data found")
        return
    
    print(f"✓ Found {len(pairs)} total pairs across all search terms")
    
    # Analyze for alpha
    alpha_gems = analyze_for_alpha(pairs)
    
    if not alpha_gems:
        print("💰 No alpha gems found matching criteria")
        print("   Market may be consolidating during off-peak hours")
        print()
        print("⚠️ Scanner Status: Operational, Market Data Returned")
        return
    
    print(f"\n💎 ALPHA GEMS DETECTED: {len(alpha_gems)}")
    print("=" * 70)
    
    for i, gem in enumerate(alpha_gems[:10], 1):
        print(f"\n{i}. ⭐⭐⭐ {gem['symbol']} - Alpha Score: {gem['alpha_score']}/80")
        print(f"   Name: {gem['name']}")
        print(f"   Chain: {gem['chain']}")
        print(f"   Market Cap: ${gem['mcap']:,}")
        print(f"   24h Volume: ${gem['volume_24h']:,}")
        print(f"   Volume/MCap: {(gem['volume_24h']/gem['mcap']):.1%}" if gem['mcap'] > 0 else "   Volume/MCap: N/A")
        print(f"   Price Change: {gem['price_change']:.1f}%")
        print(f"   Liquidity: ${gem['liquidity']:,}")
        print(f"   Buys/Sells: {gem['buys_24h']}/{gem['sells_24h']}")
        print(f"   DexScreener: {gem['dex_url']}")
    
    print(f"\n📊 SCANNER SUMMARY")
    print("=" * 70)
    print(f"✓ DexScreener API: Responsive")
    print(f"✓ Total Pairs Scanned: {len(pairs)}")
    print(f"✓ Alpha Gems Identified: {len(alpha_gems)}")
    print(f"✓ Scan Time: {timestamp}")

if __name__ == "__main__":
    main()