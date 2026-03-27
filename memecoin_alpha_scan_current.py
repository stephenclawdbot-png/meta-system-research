#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def fetch_dexscreener_data():
    """Fetch comprehensive DexScreener data for analysis"""
    
    # Multiple search queries to catch various memecoin categories
    queries = ["solana", "meme", "dog", "cat", "pepe", "shib", "elon", "ai"]
    
    all_tokens = []
    
    for query in queries:
        url = f"https://api.dexscreener.com/latest/dex/search?q={query}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if data and 'pairs' in data:
                for token in data['pairs']:
                    mcap = token.get('fdv', 0)
                    
                    # Filter by market cap range
                    if 30000 <= mcap <= 200000:
                        token_info = {
                            'symbol': token.get('baseToken', {}).get('symbol', ''),
                            'name': token.get('baseToken', {}).get('name', ''),
                            'mcap': mcap,
                            'volume_24h': token.get('volume', {}).get('h24', 0),
                            'price': token.get('priceUsd', 0),
                            'price_change_24h': token.get('priceChange', {}).get('h24', 0),
                            'liquidity': token.get('liquidity', {}).get('usd', 0),
                            'txns': token.get('txns', {}),
                            'buy_ratio': None,
                            'url': token.get('url', ''),
                            'chain': token.get('chainId', ''),
                            'dex': token.get('dexId', ''),
                            'created_at': token.get('pairCreatedAt', '')
                        }
                        
                        # Calculate buy ratio if available
                        txns = token.get('txns', {})
                        buys = txns.get('h24', {}).get('buys', 0)
                        sells = txns.get('h24', {}).get('sells', 0)
                        total_txns = buys + sells
                        
                        if total_txns > 0:
                            token_info['buy_ratio'] = round((buys / total_txns) * 100, 1)
                        
                        all_tokens.append(token_info)
                        
        except Exception as e:
            print(f"Error fetching {query}: {e}")
    
    # Remove duplicates based on symbol+mcap
    seen = set()
    unique_tokens = []
    
    for token in all_tokens:
        identifier = f"{token['symbol']}-{token['mcap']}"
        if identifier not in seen:
            seen.add(identifier)
            unique_tokens.append(token)
    
    return unique_tokens

def calculate_composite_score(token):
    """Calculate comprehensive alpha score"""
    score = 0
    
    # Volume/MCap ratio (max 40 points)
    vol_mcap_ratio = (token['volume_24h'] / token['mcap']) * 100 if token['mcap'] > 0 else 0
    score += min(40, vol_mcap_ratio * 0.4)  # Scale down
    
    # Price momentum (max 25 points)
    momentum = max(-10, min(100, token['price_change_24h']))
    score += max(0, momentum * 0.25)  # Only reward positive momentum
    
    # Transaction activity (max 20 points)
    txns = token.get('txns', {}).get('h24', {})
    total_txns = txns.get('buys', 0) + txns.get('sells', 0)
    score += min(20, total_txns * 0.01)  # Scale based on transaction count
    
    # Buy pressure (max 15 points)
    if token.get('buy_ratio'):
        buy_pressure = max(0, token['buy_ratio'] - 50)  # Only count above 50%
        score += min(15, buy_pressure * 0.3)
    
    return min(100, round(score, 1))

def generate_report(tokens):
    """Generate comprehensive alpha report"""
    
    # Filter tokens with minimum volume
    filtered_tokens = [t for t in tokens if t['volume_24h'] >= 500]
    
    if not filtered_tokens:
        return "❌ No active memecoins detected in the 30k-200k range\nCurrent market appears quiet."
    
    # Calculate scores and sort
    for token in filtered_tokens:
        token['alpha_score'] = calculate_composite_score(token)
    
    filtered_tokens.sort(key=lambda x: x['alpha_score'], reverse=True)
    
    # Generate report
    report = f"🎯 MEMECOIN ALPHA SCANNER - CRON REPORT\n"
    report += "=" * 60 + "\n"
    report += f"Scan Time: {datetime.now().strftime('%A, %B %d, %Y — %I:%M %p')}\n"
    report += f"Market Cap Range: $30,000 - $200,000\n"
    report += f"Focus: Early alpha detection before mainstream attention\n\n"
    
    report += f"🔥 TOP ALPHA GEMS (Sorted by Alpha Score)\n"
    report += "-" * 50 + "\n\n"
    
    for i, token in enumerate(filtered_tokens[:10], 1):
        vol_mcap_ratio = (token['volume_24h'] / token['mcap']) * 100 if token['mcap'] > 0 else 0
        
        report += f"🎯 #{i} {token['symbol']} - Alpha Score: {token['alpha_score']}/100\n"
        report += f"   📈 24h Stats: ${token['volume_24h']:,.0f} vol • ${token['mcap']:,.0f} mcap • {vol_mcap_ratio:.1f}% ratio\n"
        if token.get('buy_ratio'):
            report += f"   📊 Sentiment: {token['price_change_24h']:.1f}% price • {token['buy_ratio']:.1f}% buy ratio\n"
        else:
            report += f"   📊 Sentiment: {token['price_change_24h']:.1f}% price • N/A buy ratio\n"
        
        txns = token.get('txns', {}).get('h24', {})
        buys = txns.get('buys', 0)
        sells = txns.get('sells', 0)
        total_txns = buys + sells
        
        report += f"   🔄 Activity: {total_txns} txns ({buys} buys/{sells} sells)\n"
        report += f"   💧 Liquidity: ${token['liquidity']:,.0f}\n"
        report += f"   🌐 Chain: {token['chain']}\n"
        report += f"   🔗 {token['url']}\n\n"
    
    # Market summary
    total_gems = len(filtered_tokens)
    avg_score = sum(t['alpha_score'] for t in filtered_tokens) / total_gems if total_gems > 0 else 0
    avg_mcap = sum(t['mcap'] for t in filtered_tokens) / total_gems if total_gems > 0 else 0
    avg_vol = sum(t['volume_24h'] for t in filtered_tokens) / total_gems if total_gems > 0 else 0
    avg_ratio = sum((t['volume_24h']/t['mcap']*100 if t['mcap']>0 else 0) for t in filtered_tokens) / total_gems if total_gems > 0 else 0
    
    report += f"📊 MARKET SUMMARY FOR {total_gems} GEMS\n"
    report += f"• Average Alpha Score: {avg_score:.1f}/100\n"
    report += f"• Average Market Cap: ${avg_mcap:,.0f}\n"
    report += f"• Average Volume: ${avg_vol:,.0f}\n"
    report += f"• Average Volume/MCap Ratio: {avg_ratio:.1f}%\n"
    
    if filtered_tokens:
        top_token = filtered_tokens[0]
        report += f"• Top Performer: {top_token['symbol']} ({top_token['alpha_score']}/100)\n"
    
    report += "\n💡 Key Alpha Signals:\n"
    report += "- Volume/Mcap ratio > 25% indicates strong interest\n"
    report += "- Buy ratio > 60% suggests accumulation phase\n"
    report += "- High transaction volume = active community\n"
    
    report += "\n⚠️ DISCLAIMER: High risk assets - DYOR required\n"
    report += "Next scan in 5 minutes"
    
    return report

def main():
    print("🔍 Scanning DexScreener for memecoin alpha...")
    tokens = fetch_dexscreener_data()
    report = generate_report(tokens)
    print(report)

if __name__ == "__main__":
    main()