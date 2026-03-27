#!/usr/bin/env python3
import requests
from datetime import datetime

def fetch_alpha_overview():
    """Broader scan for alpha detection"""
    queries = ["solana", "meme", "ai", "elon", "dog", "cat", "pepe", "shib"]
    
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
                    volume_24h = token.get('volume', {}).get('h24', 0)
                    
                    # Broader range with minimum activity
                    if 20000 <= mcap <= 300000 and volume_24h >= 500:
                        txns = token.get('txns', {}).get('h24', {})
                        buys = txns.get('buys', 0)
                        sells = txns.get('sells', 0)
                        total_txns = buys + sells
                        
                        if total_txns < 5:  # Minimum transaction threshold
                            continue
                            
                        buy_ratio = round((buys / total_txns) * 100, 1) if total_txns > 0 else 0
                        liquidity = token.get('liquidity', {}).get('usd', 0)
                        
                        token_info = {
                            'symbol': token.get('baseToken', {}).get('symbol', ''),
                            'name': token.get('baseToken', {}).get('name', ''),
                            'mcap': mcap,
                            'volume_24h': volume_24h,
                            'price_change_24h': token.get('priceChange', {}).get('h24', 0),
                            'liquidity': liquidity,
                            'buy_ratio': buy_ratio,
                            'total_txns': total_txns,
                            'chain': token.get('chainId', ''),
                            'dex': token.get('dexId', ''),
                            'url': token.get('url', ''),
                            'created_at': token.get('pairCreatedAt', '')
                        }
                        
                        all_tokens.append(token_info)
                        
        except Exception as e:
            print(f"Error fetching {query}: {e}")
    
    # Remove duplicates
    seen = set()
    unique_tokens = []
    
    for token in all_tokens:
        identifier = f"{token['chain']}-{token['symbol']}"
        if identifier not in seen:
            seen.add(identifier)
            unique_tokens.append(token)
    
    return unique_tokens

def calculate_alpha_score(token):
    """Alpha score calculation"""
    score = 0
    
    # Volume/ Mcap efficiency
    vol_mcap_ratio = (token['volume_24h'] / token['mcap']) * 100 if token['mcap'] > 0 else 0
    score += min(40, vol_mcap_ratio)
    
    # Buy pressure
    buy_score = max(0, token['buy_ratio'] - 50)
    score += min(20, buy_score)
    
    # Transaction activity
    score += min(15, token['total_txns'] * 0.05)
    
    # Price momentum (reward positive only)
    if token['price_change_24h'] > 0:
        score += min(15, token['price_change_24h'])
    
    # Liquidity bonus
    if token['liquidity'] > 20000:
        score += 10
    
    return min(100, round(score))

def generate_summary_report(tokens):
    """Generate alpha summary for cron"""
    
    if not tokens:
        return "❌ No alpha gems detected across major chains\nCurrent market activity appears limited."
    
    # Calculate scores
    for token in tokens:
        token['alpha_score'] = calculate_alpha_score(token)
    
    # Sort by score
    tokens.sort(key=lambda x: x['alpha_score'], reverse=True)
    
    # Top 5 overall
    top_tokens = tokens[:5]
    
    report = f"🎯 MEMECOIN ALPHA SCANNER - SUMMARY REPORT\n"
    report += "=" * 65 + "\n"
    report += f"Scan Time: {datetime.now().strftime('%A, %B %d, %Y — %I:%M %p (Asia/Manila)')}\n"
    report += f"Market Range: $20k-$300k with minimum activity\n"
    report += f"Total Tokens Scanned: {len(tokens)}\n\n"
    
    if top_tokens:
        report += f"🔥 TOP 5 ALPHA GEMS ACROSS ALL CHAINS\n"
        report += "-" * 55 + "\n\n"
        
        for i, token in enumerate(top_tokens, 1):
            report += f"🎯 #{i} [{token['chain'].upper()}] {token['symbol']} - {token['alpha_score']}/100\n"
            report += f"   📊 ${token['mcap']:,} mcap • ${token['volume_24h']:,} vol • {token['price_change_24h']:.1f}% Δ\n"
            report += f"   📈 {token['buy_ratio']}% buys • {token['total_txns']} txns • ${token['liquidity']:,} liquidity\n"
            report += f"   🔗 {token['url'][:80]}...\n\n"
    
    # Chain breakdown
    chain_stats = {}
    for token in tokens:
        chain = token['chain']
        if chain not in chain_stats:
            chain_stats[chain] = {'count': 0, 'avg_score': 0, 'total_tokens': []}
        
        chain_stats[chain]['count'] += 1
        chain_stats[chain]['total_tokens'].append(token['alpha_score'])
    
    report += f"🌐 MARKET BREAKDOWN BY CHAIN\n"
    report += "-" * 35 + "\n"
    
    for chain, stats in chain_stats.items():
        avg_score = sum(stats['total_tokens']) / stats['count']
        report += f"• {chain.upper()}: {stats['count']} gems • Avg α: {avg_score:.1f}/100\n"
    
    # Market health indicators
    total_gems = len(tokens)
    avg_mcap = sum(t['mcap'] for t in tokens) / total_gems if total_gems > 0 else 0
    avg_vol = sum(t['volume_24h'] for t in tokens) / total_gems if total_gems > 0 else 0
    avg_score = sum(t['alpha_score'] for t in tokens) / total_gems if total_gems > 0 else 0
    
    report += f"\n📊 MARKET HEALTH INDICATORS\n"
    report += f"• Average MCap: ${avg_mcap:,.0f}\n"
    report += f"• Average Volume: ${avg_vol:,.0f}\n"
    report += f"• Average Alpha Score: {avg_score:.1f}/100\n"
    report += f"• Total Active Gems: {total_gems}\n"
    
    if tokens:
        top_token = tokens[0]
        report += f"• Top Alpha Gem: {top_token['symbol']} ({top_token['alpha_score']}/100)\n"
    
    report += "\n💡 ALPHA SIGNALS TO WATCH:\n"
    report += "- Volume/Mcap ratio > 30% = Strong interest\n"
    report += "- Buy ratio > 55% = Potential accumulation\n"
    report += "- High transaction count = Active community\n"
    report += "- Recent token creation + volume = Momentum\n"
    
    report += "\n⚠️ HIGH RISK DISCLAIMER: Always conduct your own research\n"
    
    return report

def main():
    print("🔍 Scanning cross-chain memecoins for alpha opportunities...")
    tokens = fetch_alpha_overview()
    report = generate_summary_report(tokens)
    print(report)

if __name__ == "__main__":
    main()