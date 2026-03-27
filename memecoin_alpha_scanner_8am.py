#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def fetch_dexscreener_tokens(search_queries):
    """Fetch tokens from DexScreener for multiple search queries"""
    all_tokens = []
    
    for query in search_queries:
        try:
            url = f"https://api.dexscreener.com/latest/dex/search?q={query}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if data and 'pairs' in data and data['pairs']:
                # Filter by market cap range
                for token in data['pairs']:
                    mcap = token.get('fdv', 0)
                    
                    # Focus on 30k-200k market cap range
                    if 30000 <= mcap <= 200000:
                        # Extract transaction data
                        txn_data = token.get('txns', {})
                        h24_buys = txn_data.get('h24', {}).get('buys', 0)
                        h24_sells = txn_data.get('h24', {}).get('sells', 0)
                        total_txns = h24_buys + h24_sells
                        
                        # Only include tokens with meaningful activity
                        if total_txns < 10:
                            continue
                            
                        token_info = {
                            'name': token.get('baseToken', {}).get('name', 'Unknown'),
                            'symbol': token.get('baseToken', {}).get('symbol', 'Unknown'),
                            'mcap': mcap,
                            'volume_24h': token.get('volume', {}).get('h24', 0),
                            'price': token.get('priceUsd', 0),
                            'price_change_24h': token.get('priceChange', {}).get('h24', 0),
                            'url': token.get('url', ''),
                            'dex': token.get('dexId', ''),
                            'chain': token.get('chainId', ''),
                            'pairAddress': token.get('pairAddress', ''),
                            'created_at': token.get('pairCreatedAt', None),
                            'h24_buys': h24_buys,
                            'h24_sells': h24_sells,
                            'total_txns': total_txns,
                            'buy_ratio': h24_buys / total_txns if total_txns > 0 else 0,
                            'search_term': query
                        }
                        all_tokens.append(token_info)
                        
        except Exception as e:
            print(f"Error fetching for query '{query}': {e}")
            continue
    
    return all_tokens

def calculate_alpha_score(token):
    """Calculate enhanced alpha score"""
    # Volume/MCap ratio (most important - shows high trading relative to size)
    vol_mcap_ratio = (token['volume_24h'] / token['mcap']) * 100 if token['mcap'] > 0 else 0
    vol_mcap_score = min(40, vol_mcap_ratio * 0.4)
    
    # Buy pressure (more buys than sells = accumulation)
    buy_pressure = min(25, max(0, (token['buy_ratio'] - 0.5) * 50))
    
    # Price momentum
    momentum = min(20, max(0, token['price_change_24h']) if token['price_change_24h'] else 0)
    
    # Age score (newer tokens are higher alpha)
    age_score = 0
    if token.get('created_at'):
        # If created timestamp is available, newer tokens get higher score
        age_seconds = datetime.now().timestamp() - (token['created_at'] / 1000)
        if age_seconds < 86400:  # Less than 24 hours old
            age_score = min(15, 100 * (86400 - age_seconds) / 86400) * 0.15
    
    # Transaction velocity
    txn_velocity = min(10, token['total_txns'] * 0.1)
    
    # Composite alpha score
    alpha_score = min(
        100,
        vol_mcap_score +      # Volume/MCap ratio (40 max)
        buy_pressure +        # Buy pressure (25 max)
        momentum +            # Price momentum (20 max)
        age_score +           # Newness bonus (15 max)
        txn_velocity          # Transaction activity (10 max)
    )
    
    return round(alpha_score, 1)

def remove_duplicates(tokens):
    """Remove duplicates by token symbol and mcap similarity"""
    unique_tokens = []
    seen_symbols = set()
    
    for token in tokens:
        symbol_key = f"{token['symbol']}_{round(token['mcap'] / 10000)}"
        if symbol_key not in seen_symbols:
            seen_symbols.add(symbol_key)
            unique_tokens.append(token)
    
    return unique_tokens

def format_report(tokens):
    """Create properly formatted report"""
    now = datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (Asia/Manila)")
    
    report = f"""🎯 MEMECOIN ALPHA SCANNER - CRON REPORT
{'=' * 60}
Scan Time: {now}
Market Cap Range: $30,000 - $200,000
Focus: Early alpha detection before mainstream attention

🔥 TOP ALPHA GEMS (Sorted by Alpha Score)
{'-' * 60}
"""
    
    for i, token in enumerate(tokens, 1):
        vol_mcap_ratio = (token['volume_24h'] / token['mcap']) * 100 if token['mcap'] > 0 else 0
        price_change = token['price_change_24h'] or 0
        
        report += f"""🎯 #{i} {token['symbol']} - Alpha Score: {token['alpha_score']}/100
   📈 24h Stats: ${token['volume_24h']:,.0f} vol • ${token['mcap']:,.0f} mcap • {vol_mcap_ratio:.1f}% ratio
   📊 Sentiment: {price_change:.1f}% price • {token['buy_ratio']:.1%} buy ratio
   🔄 Activity: {token['total_txns']} txns ({token['h24_buys']} buys/{token['h24_sells']} sells)
   💧 Liquidity: ${int(token['mcap'] * 0.7):,} (est.)
   🌐 Chain: {token['chain']}
   🔗 {token['url']}

"""
    
    # Summary
    if tokens:
        avg_score = sum(t['alpha_score'] for t in tokens) / len(tokens)
        avg_mcap = sum(t['mcap'] for t in tokens) / len(tokens)
        avg_ratio = sum((t['volume_24h']/t['mcap']*100 if t['mcap']>0 else 0) for t in tokens) / len(tokens)
        
        report += f"""📊 MARKET SUMMARY FOR {len(tokens)} GEMS
• Average Alpha Score: {avg_score:.1f}/100
• Average Market Cap: ${avg_mcap:,.0f}
• Average Volume/MCap Ratio: {avg_ratio:.1f}%
• Top Performer: {tokens[0]['symbol']} ({tokens[0]['alpha_score']}/100)

💡 Key Alpha Signals:
15+ transactions = active community
Vol/Mcap > 25% = strong interest
Buy ratio > 60% = accumulation phase

⚠️ DISCLAIMER: High risk assets - DYOR required"""
    else:
        report += "❌ No alpha gems detected in target range"
    
    return report

def main():
    # Search queries for memecoins
    search_queries = [
        "PEPE", "DOGE", "SHIB", "BONK", "FLOKI", "WIF", "BOME", "MEME",
        "GUAC", "PUDGY", "POPCAT", "MOOK", "HARAMBE", "HODL", "HONEY",
        "CAT", "FROG", "DOG", "SAFE", "RUG", "SOL", "ETH", "BTC",
        "AI", "PEPE", "DOG", "COIN", "STONKS", "MOON", "LAMBO"
    ]
    
    # Fetch tokens
    tokens = fetch_dexscreener_tokens(search_queries)
    tokens = remove_duplicates(tokens)
    
    if not tokens:
        print("❌ No memecoins found in 30k-200k range")
        return
    
    # Calculate alpha scores
    for token in tokens:
        token['alpha_score'] = calculate_alpha_score(token)
    
    # Filter for minimum quality
    tokens = [t for t in tokens if t['alpha_score'] >= 25]
    tokens.sort(key=lambda x: x['alpha_score'], reverse=True)
    
    # Create report
    report = format_report(tokens[:8])  # Top 8 tokens
    print(report)

if __name__ == "__main__":
    main()