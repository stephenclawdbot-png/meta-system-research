#!/usr/bin/env python3
import requests
import json

def fetch_solana_memecoins():
    """Fetch Solana memecoins from DexScreener with various searches"""
    
    # Try different search queries for memecoins
    queries = ['solana', 'meme', 'pump', 'coin', 'token', 'so', 'inu']
    all_pairs = []
    
    for query in queries:
        try:
            url = f"https://api.dexscreener.com/latest/dex/search/?q={query}"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if 'pairs' in data:
                all_pairs.extend(data['pairs'])
                print(f"Found {len(data['pairs'])} pairs for query '{query}'")
            
        except Exception as e:
            print(f"Error fetching {query}: {e}")
    
    return all_pairs

def filter_30k_200k_mcap(pairs):
    """Filter pairs with market cap between 30k and 200k"""
    filtered = []
    
    for pair in pairs:
        # Only Solana tokens
        if pair.get('chainId') != 'solana':
            continue
            
        mcap = pair.get('marketCap')
        if mcap and 30000 <= mcap <= 200000:
            filtered.append(pair)
    
    return filtered

def analyze_alpha_potential(pairs):
    """Analyze alpha potential based on various metrics"""
    alpha_gems = []
    
    for pair in pairs:
        mcap = pair.get('marketCap', 0)
        volume_24h = pair.get('volume', {}).get('h24', 0)
        txns_24h = pair.get('txns', {}).get('h24', {})
        buy_count = txns_24h.get('buys', 0)
        sell_count = txns_24h.get('sells', 0)
        total_txns = buy_count + sell_count
        
        buy_ratio = buy_count / total_txns if total_txns > 0 else 0
        price_change_24h = pair.get('priceChange', {}).get('h24', 0)
        
        # Alpha Score Calculation (0-100)
        alpha_score = 0
        
        # Volume/Mcap ratio - undervalued tokens (max 30 points)
        if volume_24h > 0:
            volume_mcap_ratio = volume_24h / mcap
            if volume_mcap_ratio > 2.0:
                alpha_score += 30
            elif volume_mcap_ratio > 1.0:
                alpha_score += 20
            elif volume_mcap_ratio > 0.5:
                alpha_score += 10
        
        # Buy pressure (max 25 points)
        if buy_ratio > 0.7:
            alpha_score += 25
        elif buy_ratio > 0.6:
            alpha_score += 15
        elif buy_ratio > 0.55:
            alpha_score += 10
        
        # Transaction velocity (max 20 points)
        if total_txns > 1000:
            alpha_score += 20
        elif total_txns > 500:
            alpha_score += 15
        elif total_txns > 200:
            alpha_score += 10
        elif total_txns > 100:
            alpha_score += 5
        
        # Price momentum (max 15 points)
        if price_change_24h > 50:
            alpha_score += 15
        elif price_change_24h > 25:
            alpha_score += 10
        elif price_change_24h > 10:
            alpha_score += 5
        elif price_change_24h > 0:
            alpha_score += 2
        
        # Liquidity depth (max 10 points)
        liquidity = pair.get('liquidity', {}).get('usd', 0)
        if liquidity > mcap * 0.5:  # Good liquidity relative to mcap
            alpha_score += 10
        elif liquidity > mcap * 0.2:
            alpha_score += 5
        
        alpha_gems.append({
            'symbol': pair.get('baseToken', {}).get('symbol'),
            'name': pair.get('baseToken', {}).get('name'),
            'mcap': mcap,
            'price': pair.get('priceUsd'),
            'volume_24h': volume_24h,
            'price_change_24h': price_change_24h,
            'buy_ratio': buy_ratio,
            'total_txns': total_txns,
            'url': pair.get('url'),
            'dex': pair.get('dexId'),
            'liquidity': liquidity,
            'alpha_score': alpha_score
        })
    
    # Sort by alpha score descending
    alpha_gems.sort(key=lambda x: x['alpha_score'], reverse=True)
    return alpha_gems

def main():
    print("🔍 Scanning DexScreener for Solana memecoins...")
    
    pairs = fetch_solana_memecoins()
    print(f"Total pairs found: {len(pairs)}")
    
    filtered = filter_30k_200k_mcap(pairs)
    print(f"Filtered to 30k-200k MCap: {len(filtered)} tokens")
    
    alpha_gems = analyze_alpha_potential(filtered)
    
    print(f"\n🎯 Alpha Scanner Results - {len(alpha_gems)} potential alpha gems\n")
    
    if alpha_gems:
        print("Top Alpha Candidates (sorted by alpha score):")
        print("=" * 100)
        
        for i, gem in enumerate(alpha_gems[:20], 1):
            print(f"\n{i}. {gem['symbol']} - {gem['name']}")
            print(f"   Alpha Score: {gem['alpha_score']}/100")
            print(f"   Market Cap: ${gem['mcap']:,}")
            print(f"   24h Volume: ${gem['volume_24h']:,.2f}")
            print(f"   Volume/MCap Ratio: {gem['volume_24h']/gem['mcap']:.2f}")
            print(f"   Buy Ratio: {gem['buy_ratio']:.1%}")
            print(f"   Total Transactions (24h): {gem['total_txns']}")
            print(f"   24h Price Change: {gem['price_change_24h']}%" if gem['price_change_24h'] is not None else "   24h Price Change: N/A")
            print(f"   Liquidity: ${gem['liquidity']:,.2f}")
            print(f"   DEX: {gem['dex']}")
            print(f"   URL: {gem['url']}")
    else:
        print("No alpha gems found in the 30k-200k range")

if __name__ == "__main__":
    main()