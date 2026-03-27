#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def fetch_solana_gems():
    """Fetch Solana tokens specifically with enhanced filtering"""
    url = "https://api.dexscreener.com/latest/dex/search?q=solana&results=100"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        solana_tokens = []
        
        if data and 'pairs' in data:
            for token in data['pairs']:
                # Only process Solana tokens
                if token.get('chainId') != 'solana':
                    continue
                    
                mcap = token.get('fdv', 0)
                volume_24h = token.get('volume', {}).get('h24', 0)
                
                # Enhanced filtering: $30k-$200k mcap + minimum volume
                if 30000 <= mcap <= 200000 and volume_24h >= 1000:
                    # Additional filter: avoid scam/low-quality tokens
                    liquidity = token.get('liquidity', {}).get('usd', 0)
                    
                    # Check transaction quality
                    txns = token.get('txns', {}).get('h24', {})
                    buys = txns.get('buys', 0)
                    sells = txns.get('sells', 0)
                    total_txns = buys + sells
                    
                    if total_txns < 10:  # Minimum transaction activity
                        continue
                        
                    # Calculate buy ratio
                    buy_ratio = round((buys / total_txns) * 100, 1) if total_txns > 0 else 0
                    
                    token_info = {
                        'symbol': token.get('baseToken', {}).get('symbol', ''),
                        'name': token.get('baseToken', {}).get('name', ''),
                        'mcap': mcap,
                        'volume_24h': volume_24h,
                        'price': token.get('priceUsd', 0),
                        'price_change_24h': token.get('priceChange', {}).get('h24', 0),
                        'liquidity': liquidity,
                        'txns': txns,
                        'buy_ratio': buy_ratio,
                        'total_txns': total_txns,
                        'url': token.get('url', ''),
                        'dex': token.get('dexId', ''),
                        'created_at': token.get('pairCreatedAt', '')
                    }
                    
                    solana_tokens.append(token_info)
        
        return solana_tokens
        
    except Exception as e:
        print(f"Error fetching Solana gems: {e}")
        return []

def calculate_solana_alpha_score(token):
    """Enhanced alpha scoring specifically for Solana tokens"""
    score = 0
    
    # Volume/MCap ratio (max 40 points)
    vol_mcap_ratio = (token['volume_24h'] / token['mcap']) * 100 if token['mcap'] > 0 else 0
    score += min(40, vol_mcap_ratio * 0.4)
    
    # Liquidity quality (max 20 points)
    if token['liquidity'] > 50000:
        score += 20
    elif token['liquidity'] > 20000:
        score += 15
    elif token['liquidity'] > 5000:
        score += 10
    elif token['liquidity'] > 1000:
        score += 5
    
    # Transaction activity (max 15 points)
    score += min(15, token['total_txns'] * 0.05)  # Scale down
    
    # Buy pressure (max 15 points)
    buy_pressure = max(0, token['buy_ratio'] - 50)  # Only count above 50%
    score += min(15, buy_pressure * 0.3)
    
    # Price momentum bonus (max 10 points)
    momentum = max(-10, min(100, token['price_change_24h']))
    score += max(0, momentum * 0.1)
    
    return min(100, round(score, 1))

def generate_solana_report(tokens):
    """Generate focused Solana alpha report"""
    
    if not tokens:
        return "❌ No high-quality Solana gems in the 30k-200k range at this time.\nMarket appears quiet or all tokens filtered out."
    
    # Calculate scores
    for token in tokens:
        token['alpha_score'] = calculate_solana_alpha_score(token)
    
    # Sort by alpha score
    tokens.sort(key=lambda x: x['alpha_score'], reverse=True)
    
    report = f"🚀 SOLANA MEMECOIN ALPHA SCANNER\n"
    report += "=" * 60 + "\n"
    report += f"Scan Time: {datetime.now().strftime('%A, %B %d, %Y — %I:%M %p (Asia/Manila)')}\n"
    report += f"Market Cap Range: $30,000 - $200,000\n"
    report += f"Focus: High-quality Solana alpha detection\n\n"
    
    report += f"💎 TOP SOLANA ALPHA GEMS\n"
    report += "-" * 50 + "\n\n"
    
    for i, token in enumerate(tokens[:8], 1):
        vol_mcap_ratio = (token['volume_24h'] / token['mcap']) * 100 if token['mcap'] > 0 else 0
        
        report += f"🎯 #{i} {token['symbol']} - Alpha Score: {token['alpha_score']}/100\n"
        report += f"   📈 24h Stats: ${token['volume_24h']:,.0f} vol • ${token['mcap']:,.0f} mcap • {vol_mcap_ratio:.1f}% ratio\n"
        report += f"   📊 Sentiment: {token['price_change_24h']:.1f}% price • {token['buy_ratio']:.1f}% buy ratio\n"
        report += f"   🔄 Activity: {token['total_txns']} total transactions\n"
        report += f"   💧 Liquidity: ${token['liquidity']:,.0f}\n"
        report += f"   🌐 DEX: {token['dex']}\n"
        report += f"   🔗 {token['url']}\n\n"
    
    # Market insights
    total_gems = len(tokens)
    avg_score = sum(t['alpha_score'] for t in tokens) / total_gems
    avg_mcap = sum(t['mcap'] for t in tokens) / total_gems
    avg_vol = sum(t['volume_24h'] for t in tokens) / total_gems
    avg_ratio = sum((t['volume_24h']/t['mcap']*100 if t['mcap']>0 else 0) for t in tokens) / total_gems
    
    report += f"📊 MARKET INSIGHTS FOR {total_gems} SOLANA GEMS\n"
    report += f"• Average Alpha Score: {avg_score:.1f}/100\n"
    report += f"• Average Market Cap: ${avg_mcap:,.0f}\n"
    report += f"• Average Volume: ${avg_vol:,.0f}\n"
    report += f"• Average Volume/MCap Ratio: {avg_ratio:.1f}%\n"
    
    if tokens:
        top_token = tokens[0]
        report += f"• Top Alpha Gem: {top_token['symbol']} ({top_token['alpha_score']}/100)\n"
    
    report += "\n💡 SOLANA ALPHA CRITERIA:\n"
    report += "- Volume/Mcap ratio > 20% = Strong interest\n"
    report += "- Liquidity > $20k = Healthy pool\n"
    report += "- Buy ratio > 55% = Accumulation phase\n"
    report += "- Txns > 20 = Active community\n"
    
    report += "\n⚠️ DISCLAIMER: High risk Solana memecoins - Always DYOR\n"
    
    return report

def main():
    print("🔍 Scanning Solana memecoins for alpha gems...")
    tokens = fetch_solana_gems()
    report = generate_solana_report(tokens)
    print(report)
    
    # Save report
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    filename = f"solana_alpha_report_{timestamp}.txt"
    with open(filename, 'w') as f:
        f.write(report)
    print(f"\n📁 Report saved to: {filename}")

if __name__ == "__main__":
    main()