#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def proper_alpha_analysis():
    """Proper alpha scanner with better data handling"""
    
    def fetch_and_filter(keyword):
        """Fetch tokens for a keyword and filter by criteria"""
        try:
            url = f"https://api.dexscreener.com/latest/dex/search?q={keyword}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data and 'pairs' in data and data['pairs']:
                    tokens = []
                    for token in data['pairs']:
                        mcap = token.get('marketCap', token.get('fdv', 0))
                        
                        # Apply filters
                        if (30000 <= mcap <= 200000 and
                            token.get('priceUsd', 0) > 0 and
                            token.get('volume', {}).get('h24', 0) > 0):
                            
                            volume = token.get('volume', {}).get('h24', 0)
                            liquidity = token.get('liquidity', {}).get('usd', 0)
                            price_change = token.get('priceChange', {}).get('h24', 0)
                            symbol = token.get('baseToken', {}).get('symbol', '').upper()
                            
                            tokens.append({
                                'symbol': symbol,
                                'keyword': keyword,
                                'mcap': mcap,
                                'volume': volume,
                                'liquidity': liquidity,
                                'price_change': price_change,
                                'url': token.get('url', ''),
                                'chain': token.get('chainId', '')
                            })
                    
                    return tokens
            return []
        except:
            return []
    
    # Search for multiple memecoin patterns
    keywords = ["pepe", "doge", "bonk", "wif", "cat", "frog", "inu", "hamster", "sam", "based", "maga", "trump"]
    all_tokens = []
    
    for keyword in keywords:
        tokens = fetch_and_filter(keyword)
        all_tokens.extend(tokens)
        print(f"✓ {keyword}: {len(tokens)} tokens")
    
    print(f"\nTotal tokens found: {len(all_tokens)}\n")
    
    if not all_tokens:
        print("❌ No alpha gems detected")
        return "No memecoins found in target range $30K-$200K"
    
    # Remove duplicates
    unique_tokens = []
    seen = set()
    for token in all_tokens:
        key = f"{token['symbol']}-{token['chain']}"
        if key not in seen:
            seen.add(key)
            unique_tokens.append(token)
    
    print(f"Unique tokens after dedupe: {len(unique_tokens)}\n")
    
    # Calculate volume/mcap ratio
    for token in unique_tokens:
        token['vol_ratio'] = token['volume'] / token['mcap'] * 100 if token['mcap'] > 0 else 0
    
    # Sort by volume/mcap ratio
    unique_tokens.sort(key=lambda x: x['vol_ratio'], reverse=True)
    top_tokens = unique_tokens[:10]
    
    # Generate report
    report = []
    report.append("🚀 MEMECOIN ALPHA SCANNER REPORT")
    report.append("=" * 60)
    report.append(f"Scan Time: {datetime.now().strftime('%A, %B %d, %Y — %I:%M %p')} (Asia/Manila)")
    report.append(f"Target Range: $30K - $200K Market Cap")
    report.append(f"")
    
    if top_tokens:
        report.append("🔥 TOP ALPHA PICKS (Sorted by Volume/MCap Ratio)")
        report.append("-" * 60)
        
        for i, token in enumerate(top_tokens, 1):
            report.append(f"🎯 #{i} {token['symbol']} (via '{token['keyword']}')")
            report.append(f"   💰 MCap: ${token['mcap']:,.0f}")
            report.append(f"   📈 Volume: ${token['volume']:,.0f} ({token['vol_ratio']:.1f}% ratio)")
            report.append(f"   📊 Price: {token['price_change']:+.1f}%")
            report.append(f"   💧 Liquidity: ${token['liquidity']:,.0f}")
            report.append(f"   🌐 Chain: {token['chain']}")
            report.append(f"")
        
        # Stats
        avg_mcap = sum(t['mcap'] for t in top_tokens) / len(top_tokens)
        avg_volume = sum(t['volume'] for t in top_tokens) / len(top_tokens)
        avg_ratio = sum(t['vol_ratio'] for t in top_tokens) / len(top_tokens)
        
        report.append("📊 MARKET OVERVIEW")
        report.append("-" * 60)
        report.append(f"• Tokens Found: {len(unique_tokens)}")
        report.append(f"• Avg MCap: ${avg_mcap:,.0f}")
        report.append(f"• Avg Volume: ${avg_volume:,.0f}")
        report.append(f"• Avg Volume Ratio: {avg_ratio:.1f}%")
        
        # Alpha signals
        best_token = top_tokens[0]
        report.append(f"")
        report.append("💡 BEST ALPHA SIGNAL")
        report.append("-" * 60)
        report.append(f"• Token: {best_token['symbol']}")
        report.append(f"• Volume Efficiency: {best_token['vol_ratio']:.1f}%")
        report.append(f"• Price Momentum: {best_token['price_change']:+.1f}%")
        report.append(f"• Liquidity Score: ${best_token['liquidity']:,.0f}")
        
    report.append(f"")
    report.append("⚠️ DISCLAIMER: High risk memecoins. Do Your Own Research.")
    
    return "\n".join(report)

if __name__ == "__main__":
    result = proper_alpha_analysis()
    print(result)