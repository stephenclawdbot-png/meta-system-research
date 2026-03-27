#!/usr/bin/env python3
import requests
import json
from datetime import datetime
import sys

def search_memecoins():
    """Search DexScreener for memecoins across multiple queries"""
    queries = ["meme", "pepe", "doge", "shiba", "bonk", "elon", "trump", "cat", "dog", "coin", "token"]
    
    all_pairs = []
    seen_addresses = set()
    
    for query in queries:
        url = f"https://api.dexscreener.com/latest/dex/search?q={query}"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'pairs' in data:
                for pair in data['pairs']:
                    address = pair.get('baseToken', {}).get('address', '')
                    if address and address not in seen_addresses:
                        seen_addresses.add(address)
                        all_pairs.append(pair)
            
            print(f"✓ Queried '{query}': {len(data.get('pairs', [])) if 'pairs' in data else 0} tokens")
            
        except Exception as e:
            print(f"✗ Query '{query}' failed: {e}")
            continue
    
    return all_pairs

def filter_candidates(pairs):
    """Filter tokens based on evaluation criteria"""
    candidates = []
    wrapped_tokens = ['wbtc', 'weth', 'wsol', 'wmatic', 'wbnb']
    blockchain_names = ['solana', 'ethereum', 'bitcoin', 'cardano', 'polygon', 'base', 'avax', 'arbitrum']
    
    for pair in pairs:
        mcap = pair.get('fdv', 0)
        volume_24h = pair.get('volume', {}).get('h24', 0)
        base_token = pair.get('baseToken', {})
        name = base_token.get('name', '').lower()
        symbol = base_token.get('symbol', '').lower()
        
        # Skip if no market cap data
        if mcap == 0:
            continue
        
        # Filter by market cap range
        if mcap < 30000 or mcap > 200000:
            continue
        
        # Exclude wrapped tokens and blockchain names
        if any(wrapped in name for wrapped in wrapped_tokens):
            continue
        if any(wrapped in symbol for wrapped in wrapped_tokens):
            continue
        if any(chain in name for chain in blockchain_names):
            continue
        
        # Calculate metrics
        vol_mcap_ratio = (volume_24h / mcap) * 100 if mcap > 0 else 0
        
        # Additional filtering for quality
        if vol_mcap_ratio < 5:  # Minimum 5% volume/mcap ratio
            continue
        if volume_24h < 100:  # Minimum $100 volume
            continue
        
        # Calculate alpha score
        momentum = max(0, pair.get('priceChange', {}).get('h24', 0))
        txn_h24 = pair.get('txns', {}).get('h24', {})
        buys = txn_h24.get('buys', 0)
        sells = txn_h24.get('sells', 0)
        buy_ratio = buys / max(1, buys + sells)
        
        vol_mcap_score = min(40, vol_mcap_ratio * 1.5)
        momentum_score = min(25, momentum * 2)
        volume_score = min(20, volume_24h / 500)
        buy_ratio_score = buy_ratio * 15
        
        alpha_score = min(100, vol_mcap_score + momentum_score + volume_score + buy_ratio_score)
        
        candidate = {
            'name': base_token.get('name', 'Unknown'),
            'symbol': symbol.upper(),
            'mcap': mcap,
            'volume_24h': volume_24h,
            'price': pair.get('priceUsd', 0),
            'price_change_24h': pair.get('priceChange', {}).get('h24', 0),
            'url': pair.get('url', ''),
            'dex': pair.get('dexId', ''),
            'chain': pair.get('chainId', ''),
            'liquidity': pair.get('liquidity', {}).get('usd', 0),
            'txns': buys + sells,
            'buys': buys,
            'sells': sells,
            'buy_ratio': buy_ratio,
            'vol_mcap_ratio': vol_mcap_ratio,
            'alpha_score': alpha_score
        }
        candidates.append(candidate)
    
    return candidates

def main():
    print("🧠 MEMECOIN ALPHA SCANNER")
    print("=" * 60)
    print("Scan Time:", datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (Asia/Manila)"))
    print("Target Range: $30k - $200k Market Cap")
    print("Filters: Vol/MCap ratio > 5%, $100+ 24h volume")
    print()
    
    print("🔍 Fetching DexScreener data...")
    pairs = search_memecoins()
    
    if not pairs:
        print("❌ No data fetched from DexScreener")
        return
    
    print(f"\n📊 Found {len(pairs)} unique tokens")
    candidates = filter_candidates(pairs)
    
    if not candidates:
        print("❌ No tokens meet alpha criteria")
        print("Market may be quiet or stricter filtering needed")
        return
    
    # Sort by alpha score
    candidates.sort(key=lambda x: x['alpha_score'], reverse=True)
    
    print(f"🔥 TOP ALPHA GEMS DETECTED ({len(candidates)} total)")
    print("=" * 50)
    
    for i, gem in enumerate(candidates[:8], 1):
        sentiment_emoji = "🟢" if gem['price_change_24h'] > 0 else "🔴"
        
        print(f"🎯 #{i} {gem['symbol']} - Alpha Score: {gem['alpha_score']:.1f}/100")
        print(f"   📛 Name: {gem['name']}")
        print(f"   💰 MCap: ${gem['mcap']:,.0f} | Vol: ${gem['volume_24h']:,.0f}")
        print(f"   {sentiment_emoji} 24h Change: {gem['price_change_24h'] or 0:.1f}%")
        print(f"   🔥 Vol/MCap Ratio: {gem['vol_mcap_ratio']:.1f}%")
        print(f"   🤝 Buy Ratio: {gem['buy_ratio']*100:.1f}% ({gem['buys']}/{gem['sells']})")
        print(f"   🔄 Transactions: {gem['txns']}")
        print(f"   💧 Liquidity: ${gem['liquidity']:,.0f}")
        print(f"   🌐 Dex: {gem['dex']} | Chain: {gem['chain']}")
        print(f"   🔗 {gem['url']}")
        print()
    
    # Summary
    print("📊 SCAN SUMMARY:")
    print("-" * 20)
    print(f"Total Alpha Gems: {len(candidates)}")
    print(f"Top Alpha Score: {candidates[0]['alpha_score']:.1f}/100")
    if len(candidates) > 1:
        print(f"Bottom Alpha Score: {candidates[-1]['alpha_score']:.1f}/100")
    print(f"Average MCap: ${sum(g['mcap'] for g in candidates)/len(candidates):,.0f}")
    print(f"Average Volume: ${sum(g['volume_24h'] for g in candidates)/len(candidates):,.0f}")
    print(f"Average Vol/MCap Ratio: {sum(g['vol_mcap_ratio'] for g in candidates)/len(candidates):.1f}%")
    print()
    print("⚠️ DISCLAIMER: High risk memecoin scanning - Do your own research!")

if __name__ == "__main__":
    main()