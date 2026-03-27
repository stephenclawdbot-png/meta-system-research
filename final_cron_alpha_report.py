#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def fetch_memecoins():
    """Fetch memecoins from DexScreener for 30k-200k mcap range"""
    url = "https://api.dexscreener.com/latest/dex/search?q=solana"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        filtered_tokens = []
        
        if not data or 'pairs' not in data:
            return filtered_tokens
        
        for token in data.get('pairs', []):
            mcap = token.get('fdv', 0)
            
            # Filter: 30k-200k mcap range
            if 30000 <= mcap <= 200000:
                # Skip generic tokens
                symbol = token.get('baseToken', {}).get('symbol', '').lower()
                name = token.get('baseToken', {}).get('name', '').lower()
                
                skip_patterns = ['wrapped', 'usdc', 'usdt', 'dai', 'eth', 'btc', 'solana', 'matic', 'chain']
                
                if not any(pattern in symbol or pattern in name for pattern in skip_patterns):
                    token_info = {
                        'symbol': token.get('baseToken', {}).get('symbol', 'Unknown'),
                        'name': token.get('baseToken', {}).get('name', 'Unknown'),
                        'mcap': mcap,
                        'volume_24h': token.get('volume', {}).get('h24', 0),
                        'price': token.get('priceUsd', 0),
                        'price_change_24h': token.get('priceChange', {}).get('h24', 0),
                        'url': token.get('url', ''),
                        'dex': token.get('dexId', ''),
                        'chain': token.get('chainId', ''),
                        'txns_24h': token.get('txns', {}).get('h24', 0),
                        'buy_ratio': token.get('buyRatio', 0),
                        'created_at': token.get('pairCreatedAt', 0)
                    }
                    filtered_tokens.append(token_info)
        
        return filtered_tokens
        
    except Exception as e:
        print(f"Error fetching DexScreener data: {e}")
        return []

def calculate_alpha_score(token):
    """Calculate alpha score based on memecoin-specific metrics"""
    
    # Calculate volume/mcap ratio
    vol_mcap_ratio = (token['volume_24h'] / token['mcap']) * 100 if token['mcap'] > 0 else 0
    
    # Calculate freshness bonus (newer coins get higher score)
    freshness_bonus = 0
    if token.get('created_at'):
        import time
        age_hours = max(1, (time.time() * 1000 - token['created_at']) / (1000 * 60 * 60))
        if age_hours < 24:
            freshness_bonus = min(25, (24 / age_hours) * 5)
    
    # Calculate alpha score weighted components
    alpha_score = min(
        100,
        (min(40, vol_mcap_ratio)) +  # Volume/MCap ratio (max 40pts)
        (min(20, max(0, token['price_change_24h']))) +  # Price momentum (max 20pts)
        (min(15, token['txns_24h'] / 20)) +  # Transaction volume (max 15pts)
        (min(10, token.get('buy_ratio', 0) * 10)) +  # Buy ratio (max 10pts)
        freshness_bonus  # Freshness bonus (max 25pts)
    )
    
    return round(max(0, alpha_score), 1)

def generate_alpha_report():
    report = []
    
    # Header
    report.append("🎯 MEMECOIN ALPHA SCANNER - EXECUTED REPORT")
    report.append("=" * 60)
    report.append(f"Execution Time: {datetime.now().strftime('%A, %B %d, %Y — %I:%M %p (Asia/Manila)')}")
    report.append("Market Cap Range: $30,000 - $200,000")
    report.append("Focus: Early alpha detection before mainstream attention")
    report.append("")
    
    # Fetch tokens
    tokens = fetch_memecoins()
    
    if not tokens:
        report.append("❌ No memecoins detected in the 30k-200k range at this time")
        report.append("• Market may be quiet")
        report.append("• Try scanning again in 15-30 minutes")
        report.append("• Broaden search parameters if needed")
        return "\n".join(report)
    
    # Calculate alpha scores
    for token in tokens:
        token['alpha_score'] = calculate_alpha_score(token)
    
    # Sort by alpha score
    tokens.sort(key=lambda x: x['alpha_score'], reverse=True)
    
    # Top gems section
    report.append("🔥 TOP ALPHA GEMS DETECTED")
    report.append("-" * 40)
    report.append("")
    
    for i, token in enumerate(tokens[:6], 1):
        vol_mcap_ratio = (token['volume_24h'] / token['mcap']) * 100 if token['mcap'] > 0 else 0
        
        # Age calculation
        age_text = ""
        if token.get('created_at'):
            import time
            age_hours = max(1, (time.time() * 1000 - token['created_at']) / (1000 * 60 * 60))
            age_text = f" | Age: {age_hours:.1f}h" if age_hours < 48 else f" | Age: {age_hours/24:.1f}d"
        
        report.append(f"🎯 #{i} {token['symbol']} - Alpha Score: {token['alpha_score']}/100")
        report.append(f"   📈 24h Stats: ${token['volume_24h']:,.0f} vol • ${token['mcap']:,.0f} mcap • {vol_mcap_ratio:.1f}% ratio")
        report.append(f"   📊 Sentiment: {token['price_change_24h']:.1f}% price • {token.get('buy_ratio', 0):.1f}% buy ratio")
        report.append(f"   🔄 Activity: {token['txns_24h']} txns{age_text}")
        report.append(f"   💧 Liquidity: ${token.get('liquidity', 'N/A')}")
        report.append(f"   🌐 Chain: {token['chain']}")
        report.append(f"   🔗 {token['url']}")
        report.append("")
    
    # Summary section
    report.append("📊 MARKET SUMMARY")
    report.append("-" * 18)
    report.append(f"• Total Gems Found: {len(tokens)}")
    if tokens:
        top_token = tokens[0]
        report.append(f"• Top Performer: {top_token['symbol']} ({top_token['alpha_score']}/100)")
        report.append(f"• Average Alpha Score: {sum(t['alpha_score'] for t in tokens)/len(tokens):.1f}/100")
        report.append(f"• Average Volume/MCap: {sum((t['volume_24h']/t['mcap']*100 if t['mcap']>0 else 0) for t in tokens)/len(tokens):.1f}%")
    
    report.append("")
    report.append("💡 Key Alpha Signals Evaluated:")
    report.append("- Volume/MCap ratio > 25% = strong interest")
    report.append("- Buy ratio > 60% = accumulation phase") 
    report.append("- Transaction volume > 50 = active community")
    report.append("- Age < 24h = fresh opportunity")
    report.append("")
    report.append("⚠️ DISCLAIMER: High risk asset scanning - DYOR required")
    report.append("Next scan available in 5 minutes")
    
    return "\n".join(report)

def main():
    print(generate_alpha_report())

if __name__ == "__main__":
    main()