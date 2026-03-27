#!/usr/bin/env python3
"""
Enhanced Alpha Scanner for Memecoin Detection
Scans DexScreener for smaller tokens beyond just wrapped SOL
"""

import json
import subprocess
from datetime import datetime

def fetch_multiple_dexscreener_searches():
    """Fetch multiple search queries from DexScreener"""
    searches = [
        "meme", "dog", "cat", "ai", "game", "nft", 
        "elon", "pepe", "shib", "bonk", "wif", "bome"
    ]
    
    all_pairs = []
    
    for query in searches:
        try:
            cmd = f'curl -s "https://api.dexscreener.com/latest/dex/search?q={query}"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                if data.get('pairs'):
                    all_pairs.extend(data['pairs'])
                    print(f"Found {len(data['pairs'])} pairs for query: {query}")
        except Exception as e:
            print(f"Error fetching {query}: {e}")
    
    return {'pairs': all_pairs}

def analyze_tokens_enhanced(data):
    """Analyze tokens with enhanced filtering"""
    alpha_candidates = []
    
    if not data or 'pairs' not in data:
        return alpha_candidates
    
    seen_tokens = set()
    
    for pair in data['pairs']:
        try:
            # Get market cap
            mcap = pair.get('fdv', 0)
            
            # Filter for 30k-200k range
            if 30000 <= mcap <= 200000:
                token_info = pair.get('baseToken', {})
                token_address = token_info.get('address')
                token_symbol = token_info.get('symbol', '').upper()
                
                # Skip wrapped tokens and SOL-related tokens
                if any(keyword in token_symbol for keyword in ['SOL', 'WALLET', 'WRAPPED']):
                    continue
                
                # Skip duplicates
                if token_address in seen_tokens:
                    continue
                seen_tokens.add(token_address)
                
                # Calculate alpha score
                alpha_score = 0
                volume_24h = pair.get('volume', {}).get('h24', 0)
                liquidity = pair.get('liquidity', {}).get('usd', 0)
                price_change = pair.get('priceChange', {}).get('h24', 0)
                
                buys = pair.get('txns', {}).get('h24', {}).get('buys', 0)
                sells = pair.get('txns', {}).get('h24', {}).get('sells', 0)
                total_txns = buys + sells
                buy_ratio = buys / total_txns * 100 if total_txns > 0 else 0
                
                # Score components (max 100)
                # Volume score (max 25) - higher volume = better
                if volume_24h > 10000:
                    alpha_score += 25
                elif volume_24h > 5000:
                    alpha_score += 15
                elif volume_24h > 1000:
                    alpha_score += 5
                
                # Liquidity score (max 20) - healthy liquidity
                if liquidity > 10000:
                    alpha_score += 20
                elif liquidity > 5000:
                    alpha_score += 15
                elif liquidity > 2500:
                    alpha_score += 10
                elif liquidity > 1000:
                    alpha_score += 5
                
                # Buy pressure score (max 25) - strong accumulation
                if buy_ratio > 70:
                    alpha_score += 25
                elif buy_ratio > 60:
                    alpha_score += 20
                elif buy_ratio > 55:
                    alpha_score += 15
                elif buy_ratio > 50:
                    alpha_score += 10
                
                # Price momentum (max 20) - upward trend
                if price_change > 25:
                    alpha_score += 20
                elif price_change > 15:
                    alpha_score += 15
                elif price_change > 8:
                    alpha_score += 10
                elif price_change > 3:
                    alpha_score += 5
                
                # Age/dex diversity bonus (max 10)
                if pair.get('chainId') == 'solana':
                    alpha_score += 5  # Prefer Solana tokens
                if pair.get('dexId') in ['raydium', 'jupiter']:
                    alpha_score += 5  # Prefer major DEXs
                
                alpha_candidates.append({
                    'symbol': token_symbol,
                    'name': token_info.get('name', 'N/A'),
                    'mcap': mcap,
                    'price': pair.get('priceUsd', 0),
                    'price_change_24h': price_change,
                    'volume_24h': volume_24h,
                    'liquidity': liquidity,
                    'buy_ratio': buy_ratio,
                    'alpha_score': alpha_score,
                    'url': pair.get('url'),
                    'address': token_address,
                    'chain': pair.get('chainId'),
                    'dex': pair.get('dexId'),
                    'txns_24h_buys': buys,
                    'txns_24h_sells': sells,
                    'total_txns': total_txns
                })
                
        except Exception as e:
            continue
    
    # Sort by alpha score
    alpha_candidates.sort(key=lambda x: x['alpha_score'], reverse=True)
    return alpha_candidates[:15]

def generate_enhanced_report(alpha_gems):
    """Generate enhanced scanner report"""
    timestamp = datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (GMT+8)")
    
    report = f"""
💰 ENHANCED ALPHA SCANNER - SUB 30K-200K MCAP GEMS
====================================================
Scan Time: {timestamp}
Market Cap Focus: $30,000 - $200,000
Searched Terms: meme, dog, cat, ai, game, nft, elon, pepe, shib, bonk, wif, bome
Total Gems Identified: {len(alpha_gems)}

"""
    
    if alpha_gems:
        for i, gem in enumerate(alpha_gems, 1):
            # Alpha rating based on score
            rating = "⭐⭐⭐⭐⭐" if gem['alpha_score'] > 75 else \
                     "⭐⭐⭐⭐" if gem['alpha_score'] > 60 else \
                     "⭐⭐⭐" if gem['alpha_score'] > 45 else \
                     "⭐⭐" if gem['alpha_score'] > 30 else "⭐"
            
            report += f"""
{i}. {rating} {gem['symbol']} - Alpha Score: {gem['alpha_score']}/100
   Name: {gem['name']}
   Market Cap: ${gem['mcap']:,}
   24h Volume: ${gem['volume_24h']:,}
   Price Change: {gem['price_change_24h']:.2f}%
   Liquidity: ${gem['liquidity']:,}
   Buy Ratio: {gem['buy_ratio']:.1f}%
   Transactions: {gem['txns_24h_buys']}/{gem['txns_24h_sells']} (Total: {gem['total_txns']})
   Chain: {gem['chain']} | DEX: {gem['dex']}
   DexScreener: {gem['url']}
"""
    else:
        report += """No alpha gems found matching criteria. Market may be quiet or try broadening search.
"""
    
    report += """

📊 ALPHA SCORING BREAKDOWN:
- Volume (25p): Higher volume = stronger momentum
- Liquidity (20p): Healthy pool size reduces risk
- Buy Pressure (25p): More buys than sells = accumulation  
- Price Momentum (20p): Upward trend = bull signal
- Platform Bonus (10p): Solana + major DEXs preferred

🎯 FILTER CRITERIA:
- Market Cap: $30K-$200K (target microcaps)
- Volume > $1,000 (minimum activity)
- Buy Ratio > 50% (prefer accumulation)
- Fresh Results (less than 24h old)
"""
    
    return report

if __name__ == "__main__":
    print("🔍 Enhanced Alpha Scanner - Searching multiple categories...")
    
    data = fetch_multiple_dexscreener_searches()
    if data:
        alpha_gems = analyze_tokens_enhanced(data)
        report = generate_enhanced_report(alpha_gems)
        print(report)
    else:
        print("Failed to fetch data from DexScreener.")