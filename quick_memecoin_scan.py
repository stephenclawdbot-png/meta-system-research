#!/usr/bin/env python3
import json
import requests
from datetime import datetime

def search_dexscreener(query):
    """Search DexScreener"""
    url = f"https://api.dexscreener.com/latest/dex/search?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def filter_tokens(data, min_mcap=30000, max_mcap=200000):
    candidates = []
    if not data or 'pairs' not in data or not data['pairs']:
        return candidates
    
    for token in data['pairs']:
        market_cap = token.get('marketCap', 0)
        if min_mcap <= market_cap <= max_mcap and token.get('chainId') == 'solana':
            volume_24h = token.get('volume', {}).get('h24', 0)
            txns = token.get('txns', {}).get('h24', {})
            buys = txns.get('buys', 0)
            sells = txns.get('sells', 0)
            total = buys + sells
            buy_ratio = (buys / total * 100) if total > 0 else 0
            price_change = token.get('priceChange', {}).get('h24', 0)
            liquidity = token.get('liquidity', {}).get('usd', 0)
            
            # Basic filters
            if volume_24h < 500 or total < 10 or buy_ratio < 50:
                continue
            
            vol_mcap_ratio = (volume_24h / market_cap * 100) if market_cap > 0 else 0
            
            # Simple alpha score
            alpha_score = min(vol_mcap_ratio * 0.3 + buy_ratio * 0.3 + max(0, price_change) * 0.4, 100)
            
            candidate = {
                'symbol': token.get('baseToken', {}).get('symbol', 'Unknown'),
                'market_cap': market_cap,
                'volume': volume_24h,
                'buy_ratio': buy_ratio,
                'price_change': price_change,
                'liquidity': liquidity,
                'alpha_score': alpha_score,
                'url': token.get('url', ''),
                'pair_address': token.get('pairAddress', ''),
                'symbol': token.get('baseToken', {}).get('symbol', 'Unknown')
            }
            candidates.append(candidate)
    
    return sorted(candidates, key=lambda x: x['alpha_score'], reverse=True)

def main():
    print("🧠 Quick Memecoin Alpha Scanner - Sub 30k-200k MCap")
    print("="*60)
    current_time = datetime.now().strftime('%A, March 4, 2026 — %I:%M %p (Asia/Manila)')
    print(f"Scan Time: {current_time}\n")
    
    # Try popular memecoin keywords
    keywords = ["bonk", "wif", "pepe", "doge", "shib", "harambe", "floki", "coin"]
    all_candidates = []
    
    for keyword in keywords:
        print(f"Searching '{keyword}'...")
        data = search_dexscreener(keyword)
        if data:
            candidates = filter_tokens(data)
            all_candidates.extend(candidates)
    
    # Remove duplicates
    unique = {}
    for c in all_candidates:
        key = c['pair_address']
        if key not in unique or c['alpha_score'] > unique[key]['alpha_score']:
            unique[key] = c
    
    final_candidates = list(unique.values())
    final_candidates.sort(key=lambda x: x['alpha_score'], reverse=True)
    
    if not final_candidates:
        print("❌ No alpha gems found")
        print("The memecoin market may be quiet right now")
        return
    
    print(f"\n🔥 Top {min(5, len(final_candidates))} Alpha Gems:")
    print("-"*40)
    
    for i, candidate in enumerate(final_candidates[:5], 1):
        print(f"\n{i}. {candidate['symbol']} - Score: {candidate['alpha_score']:.1f}/100")
        print(f"   Market Cap: ${candidate['market_cap']:,}")
        print(f"   24h Volume: ${candidate['volume']:,}")
        print(f"   Buy Ratio: {candidate['buy_ratio']:.1f}%")
        print(f"   Price Change: {candidate['price_change']:.1f}%")
        print(f"   Liquidity: ${candidate['liquidity']:,}")
    
    # Market summary
    print(f"\n📊 Summary:")
    print(f"• Found {len(final_candidates)} tokens in range")
    if final_candidates:
        top_score = max(c['alpha_score'] for c in final_candidates)
        avg_mcap = sum(c['market_cap'] for c in final_candidates) / len(final_candidates)
        print(f"• Top Alpha Score: {top_score:.1f}")
        print(f"• Avg Market Cap: ${avg_mcap:,.0f}")
    
    print("\n⚠️ High risk - Not financial advice")

if __name__ == "__main__":
    main()