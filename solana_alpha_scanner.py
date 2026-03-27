#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def fetch_solana_memecoins():
    """Fetch Solana memecoins directly"""
    url = "https://api.dexscreener.com/latest/dex/tokens/solana"
    
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        return data.get('pairs', [])
    except Exception as e:
        print(f"Error fetching Solana data: {e}")
        return []

def analyze_solana_gems(pairs):
    """Analyze Solana memecoins for alpha potential"""
    gems = []
    wrapped_tokens = ['wbtc', 'weth', 'wsol', 'wmatic', 'wbnb', 'usdc', 'usdt']
    
    for pair in pairs:
        mcap = pair.get('fdv', 0)
        volume_24h = pair.get('volume', {}).get('h24', 0)
        base_token = pair.get('baseToken', {})
        name = base_token.get('name', '').lower()
        symbol = base_token.get('symbol', '').lower()
        
        # Filter by market cap
        if mcap < 30000 or mcap > 200000:
            continue
        
        # Skip wrapped tokens and stablecoins
        if any(wrapped in name for wrapped in wrapped_tokens):
            continue
        if any(wrapped in symbol for wrapped in wrapped_tokens):
            continue
        
        # Skip if no volume
        if volume_24h < 100:
            continue
        
        # Calculate metrics
        vol_mcap_ratio = (volume_24h / mcap) * 100 if mcap > 0 else 0
        momentum = max(0, pair.get('priceChange', {}).get('h24', 0))
        txn_h24 = pair.get('txns', {}).get('h24', {})
        buys = txn_h24.get('buys', 0)
        sells = txn_h24.get('sells', 0)
        buy_ratio = buys / max(1, buys + sells)
        
        # Alpha score calculation
        vol_mcap_score = min(40, vol_mcap_ratio * 1.5)
        momentum_score = min(25, momentum * 2)
        volume_score = min(20, volume_24h / 500)
        buy_ratio_score = buy_ratio * 15
        
        alpha_score = min(100, vol_mcap_score + momentum_score + volume_score + buy_ratio_score)
        
        gem = {
            'name': base_token.get('name', 'Unknown'),
            'symbol': symbol.upper(),
            'mcap': mcap,
            'volume_24h': volume_24h,
            'price_change_24h': pair.get('priceChange', {}).get('h24', 0),
            'url': pair.get('url', ''),
            'dex': pair.get('dexId', ''),
            'liquidity': pair.get('liquidity', {}).get('usd', 0),
            'txns': buys + sells,
            'buys': buys,
            'sells': sells,
            'buy_ratio': buy_ratio,
            'vol_mcap_ratio': vol_mcap_ratio,
            'alpha_score': alpha_score
        }
        gems.append(gem)
    
    return gems

def main():
    print("🚀 SOLANA MEMECOIN ALPHA SCANNER")
    print("=" * 65)
    print("Scan Time:", datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (Asia/Manila)"))
    print("Target Range: $30k - $200k Market Cap (Solana chain only)")
    print("Filters: $100+ 24h volume, excludes wrapped tokens")
    print()
    
    print("🔍 Fetching Solana token data...")
    pairs = fetch_solana_memecoins()
    
    if not pairs:
        print("❌ No Solana tokens fetched")
        return
    
    print(f"📊 Found {len(pairs)} Solana tokens")
    gems = analyze_solana_gems(pairs)
    
    if not gems:
        print("❌ No Solana gems meet alpha criteria")
        return
    
    gems.sort(key=lambda x: x['alpha_score'], reverse=True)
    
    print(f"\n🔥 SOLANA ALPHA GEMS ({len(gems)} total)")
    print("=" * 60)
    
    for i, gem in enumerate(gems[:10], 1):
        sentiment = "🟢" if gem['price_change_24h'] > 0 else "🔴"
        
        print(f"🎯 #{i} {gem['symbol']} - Alpha Score: {gem['alpha_score']:.1f}/100")
        print(f"   📛 Name: {gem['name']}")
        print(f"   💰 MCap: ${gem['mcap']:,.0f} | Vol: ${gem['volume_24h']:,.0f}")
        print(f"   {sentiment} 24h Change: {gem['price_change_24h'] or 0:.1f}%")
        print(f"   🔥 Vol/MCap Ratio: {gem['vol_mcap_ratio']:.1f}%")
        print(f"   🤝 Buy Ratio: {gem['buy_ratio']*100:.1f}% ({gem['buys']}/{gem['sells']})")
        print(f"   🔄 Transactions: {gem['txns']}")
        print(f"   💧 Liquidity: ${gem['liquidity']:,.0f}")
        print(f"   🌐 Dex: {gem['dex']}")
        print(f"   🔗 {gem['url']}")
        print()
    
    # Detailed analysis
    print("📊 ANALYSIS SUMMARY:")
    print("-" * 20)
    print(f"Total Solana Gems: {len(gems)}")
    print(f"Average Alpha Score: {sum(g['alpha_score'] for g in gems)/len(gems):.1f}/100")
    print(f"Average MCap: ${sum(g['mcap'] for g in gems)/len(gems):,.0f}")
    print(f"Average Volume: ${sum(g['volume_24h'] for g in gems)/len(gems):,.0f}")
    print(f"Average Vol/MCap Ratio: {sum(g['vol_mcap_ratio'] for g in gems)/len(gems):.1f}%")
    print(f"Average Buy Ratio: {sum(g['buy_ratio']*100 for g in gems)/len(gems):.1f}%")
    print()
    
    # Highlight key findings
    top_gem = gems[0] if gems else None
    if top_gem:
        print("🎯 TOP ALPHA IDENTIFIED:")
        print(f"Token: {top_gem['symbol']} ({top_gem['name']})")
        print(f"Alpha Score: {top_gem['alpha_score']}/100")
        print(f"Volume/MCap Ratio: {top_gem['vol_mcap_ratio']:.1f}% (Excellent)")
        print(f"Buy Pressure: {top_gem['buy_ratio']*100:.1f}% (Strong)")
        print(f"Transactions: {top_gem['txns']} (Healthy activity)")
        print(f"DexScreener Link: {top_gem['url']}")
    
    print("\n⚠️ DISCLAIMER: High risk investment - Research before trading")

if __name__ == "__main__":
    main()