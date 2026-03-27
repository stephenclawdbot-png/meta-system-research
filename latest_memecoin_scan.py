#!/usr/bin/env python3
import requests
from datetime import datetime
import time

def scan_memecoins_30k_200k():
    """Scan DexScreener for memecoins with $30k-$200k market cap"""
    
    # Popular meme search terms
    search_terms = ["meme", "doge", "pepe", "shib", "bonk", "floki", "elon", "moon", "coin"]
    
    alpha_opportunities = []
    
    for term in search_terms:
        try:
            url = f"https://api.dexscreener.com/latest/dex/search?q={term}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                pairs = data.get('pairs', [])
                
                for pair in pairs:
                    # Extract basic info
                    mcap = pair.get('marketCap', 0)
                    fdv = pair.get('fdv', 0)
                    
                    # Use market cap if available, otherwise FDV
                    effective_mcap = mcap if mcap > 0 else fdv
                    
                    # Filter for our target range
                    if 30000 <= effective_mcap <= 200000:
                        # Get volume data
                        volume_data = pair.get('volume', {})
                        if isinstance(volume_data, dict):
                            volume_24h = volume_data.get('h24', 0)
                        else:
                            volume_24h = volume_data
                        
                        # Get price change
                        price_change_data = pair.get('priceChange', {})
                        if isinstance(price_change_data, dict):
                            price_change_24h = price_change_data.get('h24', 0)
                        else:
                            price_change_24h = price_change_data
                        
                        # Get transaction data
                        txns_24h = pair.get('txns', {}).get('h24', {})
                        buys = txns_24h.get('buys', 0)
                        sells = txns_24h.get('sells', 0)
                        total_txns = buys + sells
                        buy_ratio = buys / total_txns if total_txns > 0 else 0
                        
                        # Get liquidity
                        liquidity_data = pair.get('liquidity', {})
                        if isinstance(liquidity_data, dict):
                            liquidity = liquidity_data.get('usd', 0)
                        else:
                            liquidity = liquidity_data
                        
                        # Calculate alpha score
                        volume_mcap_ratio = volume_24h / effective_mcap if effective_mcap > 0 else 0
                        momentum_score = max(0, price_change_24h) * 0.5
                        liquidity_score = min(1, liquidity / 50000) * 0.3
                        volume_score = min(0.1, volume_24h / 100000) * 0.2
                        
                        alpha_score = volume_mcap_ratio + momentum_score + liquidity_score + volume_score
                        alpha_score = min(100, alpha_score * 20)  # Scale to 100
                        
                        # Only include tokens with meaningful activity
                        if volume_24h > 1000:
                            alpha_opportunities.append({
                                'name': pair.get('baseToken', {}).get('name', 'Unknown'),
                                'symbol': pair.get('baseToken', {}).get('symbol', 'Unknown'),
                                'market_cap': effective_mcap,
                                'volume_24h': volume_24h,
                                'price_change_24h': price_change_24h,
                                'liquidity': liquidity,
                                'buys': buys,
                                'sells': sells,
                                'total_txns': total_txns,
                                'buy_ratio': buy_ratio,
                                'alpha_score': alpha_score,
                                'chain': pair.get('chainId', ''),
                                'exchange': pair.get('dexId', ''),
                                'url': pair.get('url', '')
                            })
                            
        except Exception as e:
            print(f"Error searching '{term}': {e}")
    
    # Remove duplicates and sort by alpha score
    seen = set()
    unique_opportunities = []
    
    for opp in alpha_opportunities:
        key = opp['symbol'] + opp['chain']
        if key not in seen:
            seen.add(key)
            unique_opportunities.append(opp)
    
    unique_opportunities.sort(key=lambda x: x['alpha_score'], reverse=True)
    return unique_opportunities

def generate_report(opportunities):
    """Generate a comprehensive alpha scanner report"""
    
    report_lines = []
    
    report_lines.append("🚨 ALPHA MEMECOIN SCANNER - DEXSCREENER")
    report_lines.append("=" * 60)
    report_lines.append(f"Scan Time: {datetime.now().strftime('%A, %B %d, %Y — %I:%M %p (%Z)')}")
    report_lines.append("Market Cap Range: $30,000 - $200,000")
    report_lines.append(f"Qualifying Tokens Found: {len(opportunities)}")
    report_lines.append("")
    
    if opportunities:
        report_lines.append("🔥 TOP ALPHA OPPORTUNITIES")
        report_lines.append("-" * 40)
        
        for i, opp in enumerate(opportunities[:5]):
            score_emoji = "⚡" if opp['alpha_score'] > 80 else "🚀" if opp['alpha_score'] > 60 else "💪" if opp['alpha_score'] > 40 else "📊"
            
            report_lines.append(f"{i+1}. {opp['symbol']} - Alpha: {opp['alpha_score']:.1f}/100 {score_emoji}")
            report_lines.append(f"   💰 Market Cap: ${opp['market_cap']:,.0f}")
            report_lines.append(f"   📈 24h Change: {opp['price_change_24h']:.1f}%")
            report_lines.append(f"   🔥 Volume: ${opp['volume_24h']:,.0f}")
            report_lines.append(f"   📊 Vol/Mcap Ratio: {(opp['volume_24h']/opp['market_cap']*100):.1f}%")
            report_lines.append(f"   💧 Liquidity: ${opp['liquidity']:,.0f}")
            report_lines.append(f"   🛒 Buy Ratio: {opp['buy_ratio']:.1%}")
            report_lines.append(f"   🌐 Chain: {opp['chain']}")
            report_lines.append(f"   🏦 Exchange: {opp['exchange']}")
            report_lines.append(f"   🔗 URL: {opp['url']}")
            report_lines.append("")
    else:
        report_lines.append("❌ No high-potential alpha memecoins detected in target range")
        report_lines.append("")
    
    # Market summary
    if opportunities:
        report_lines.append("📊 MARKET OVERVIEW")
        report_lines.append("-" * 20)
        avg_score = sum(opp['alpha_score'] for opp in opportunities) / len(opportunities)
        avg_mcap = sum(opp['market_cap'] for opp in opportunities) / len(opportunities)
        avg_volume = sum(opp['volume_24h'] for opp in opportunities) / len(opportunities)
        avg_vol_ratio = sum((opp['volume_24h']/opp['market_cap']) for opp in opportunities) / len(opportunities) * 100
        
        report_lines.append(f"• Average Alpha Score: {avg_score:.1f}/100")
        report_lines.append(f"• Average Market Cap: ${avg_mcap:,.0f}")
        report_lines.append(f"• Average Volume: ${avg_volume:,.0f}")
        report_lines.append(f"• Avg Vol/MCap Ratio: {avg_vol_ratio:.1f}%")
        report_lines.append(f"• Solana Tokens: {len([o for o in opportunities if o['chain'] == 'solana'])}")
        report_lines.append(f"• Ethereum Tokens: {len([o for o in opportunities if o['chain'] == 'ethereum'])}")
        report_lines.append("")
    
    # Risk assessment
    report_lines.append("⚠️ RISK ASSESSMENT")
    if opportunities:
        low_liquidity = len([o for o in opportunities if o['liquidity'] < 5000])
        high_vol_ratio = len([o for o in opportunities if (o['volume_24h']/o['market_cap']) > 2])
        
        report_lines.append(f"• High Risk: {low_liquidity} tokens with low liquidity")
        report_lines.append(f"• Volatile: {high_vol_ratio} tokens with >200% vol/mcap ratio")
    else:
        report_lines.append("• Market appears quiet - no significant alpha opportunities")
        
    report_lines.append("")
    report_lines.append("⚠️ DISCLAIMER: HIGH RISK / NOT FINANCIAL ADVICE")
    
    return "\n".join(report_lines)

if __name__ == "__main__":
    print("Scanning DexScreener for alpha memecoins...")
    opportunities = scan_memecoins_30k_200k()
    report = generate_report(opportunities)
    print(report)