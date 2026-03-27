#!/usr/bin/env python3
from datetime import datetime
import json
import subprocess

def run_alpha_scan():
    print("🚨 ALPHA MEMECOIN SCANNER - DEXSCREENER")
    print("============================================================")
    print("Scan Time:", datetime.now().strftime("%A, %B %d, %Y — %I:%M %p Asia/Manila"))
    print("Target Range: $30k - $200k Market Cap")
    print("============================================================")
    print()

    # Fetch trending and new tokens
    trending_cmd = 'curl -s "https://api.dexscreener.com/latest/dex/search?q=trending"'
    new_cmd = 'curl -s "https://api.dexscreener.com/latest/dex/search?q=new"'

    trending_result = subprocess.run(trending_cmd, shell=True, capture_output=True, text=True)
    new_result = subprocess.run(new_cmd, shell=True, capture_output=True, text=True)

    trending_data = json.loads(trending_result.stdout) if trending_result.returncode == 0 else {'pairs': []}
    new_data = json.loads(new_result.stdout) if new_result.returncode == 0 else {'pairs': []}

    all_pairs = trending_data['pairs'] + new_data['pairs']

    alpha_candidates = []

    for pair in all_pairs:
        try:
            mcap = pair.get('fdv', 0)
            if mcap < 30000 or mcap > 200000:
                continue
                
            token_info = pair.get('baseToken', {})
            volume_24h = pair.get('volume', {}).get('h24', 0)
            liquidity = pair.get('liquidity', {}).get('usd', 0)
            price_change = pair.get('priceChange', {}).get('h24', 0)
            
            txns = pair.get('txns', {}).get('h24', {})
            buys = txns.get('buys', 0)
            sells = txns.get('sells', 0)
            total_txns = buys + sells
            buy_ratio = buys / total_txns if total_txns > 0 else 0
            
            # Enhanced alpha scoring
            alpha_score = 0
            
            # High volume multiplier
            if volume_24h >= 100000:
                alpha_score += 70
            elif volume_24h >= 50000:
                alpha_score += 50
            elif volume_24h >= 25000:
                alpha_score += 35
            elif volume_24h >= 10000:
                alpha_score += 25
            elif volume_24h >= 5000:
                alpha_score += 15
            elif volume_24h >= 1000:
                alpha_score += 5
            
            # Volume/MCap ratio bonus
            vol_mcap_ratio = volume_24h / mcap if mcap > 0 else 0
            if vol_mcap_ratio >= 1.0:
                alpha_score += 40
            elif vol_mcap_ratio >= 0.5:
                alpha_score += 25
            elif vol_mcap_ratio >= 0.25:
                alpha_score += 15
            elif vol_mcap_ratio >= 0.1:
                alpha_score += 8
                
            # Price momentum
            if price_change > 50:
                alpha_score += 20
            elif price_change > 25:
                alpha_score += 15
            elif price_change > 10:
                alpha_score += 10
            elif price_change > 5:
                alpha_score += 5
                
            # Buy pressure
            if buy_ratio > 0.7:
                alpha_score += 20
            elif buy_ratio > 0.6:
                alpha_score += 15
            elif buy_ratio > 0.55:
                alpha_score += 10
                
            alpha_candidates.append({
                'symbol': token_info.get('symbol', 'Unknown'),
                'name': token_info.get('name', 'Unknown'),
                'mcap': mcap,
                'volume': volume_24h,
                'price_change': price_change,
                'liquidity': liquidity,
                'buy_ratio': buy_ratio * 100,
                'alpha_score': min(alpha_score, 100),
                'url': pair.get('url'),
                'age': pair.get('pairCreatedAt', 0)
            })
            
        except Exception as e:
            continue

    # Remove duplicates
    seen = set()
    unique_candidates = []
    for gem in alpha_candidates:
        identifier = gem['url']
        if identifier not in seen:
            seen.add(identifier)
            unique_candidates.append(gem)

    # Sort by alpha score
    unique_candidates.sort(key=lambda x: x['alpha_score'], reverse=True)
    return unique_candidates

def format_currency(value):
    """Format currency values for display"""
    if value >= 1000000:
        return f"${value/1000000:.1f}M"
    elif value >= 1000:
        return f"${value/1000:.1f}K"
    else:
        return f"${value:.0f}"

if __name__ == "__main__":
    gems = run_alpha_scan()
    
    if gems:
        print(f"💎 Found {len(gems)} Alpha Opportunities")
        print()
        
        # Find premium alpha (score >= 50)
        premium_gems = [g for g in gems if g['alpha_score'] >= 50]
        if premium_gems:
            print("🔥 PREMIUM ALPHA FIND")
            print("----------------------------------------")
            for gem in premium_gems:
                vol_mcap_ratio = gem['volume'] / gem['mcap'] * 100 if gem['mcap'] > 0 else 0
                print(f"{gem['symbol']} - Score: {gem['alpha_score']}/100 ⭐")
                print(f"   MCap: {format_currency(gem['mcap'])} | Vol: {format_currency(gem['volume'])}")
                print(f"   Vol/MCap Ratio: {vol_mcap_ratio:.1f}%")
                print(f"   24h Change: {gem['price_change']:.1f}% | Buy Ratio: {gem['buy_ratio']:.1f}%")
                print(f"   DexScreener: {gem['url']}")
                print()
        
        # Show top 3 gems
        print("🎯 TOP 3 ALPHA GEMS")
        print("----------------------------------------")
        for i, gem in enumerate(gems[:3], 1):
            vol_mcap_ratio = gem['volume'] / gem['mcap'] * 100 if gem['mcap'] > 0 else 0
            print(f"{i}. {gem['symbol']} - Alpha: {gem['alpha_score']}/100")
            print(f"   💰 Market Cap: {format_currency(gem['mcap'])}")
            print(f"   📈 24h Change: {gem['price_change']:.1f}%")
            print(f"   🔥 Volume: {format_currency(gem['volume'])}")
            print(f"   📊 Vol/Mcap Ratio: {vol_mcap_ratio:.1f}%")
            print(f"   💧 Liquidity: {format_currency(gem['liquidity'])}")
            print(f"   🛒 Buy Ratio: {gem['buy_ratio']:.1f}%")
            print(f"   🔗 URL: {gem['url']}")
            print()
        
        # Market statistics
        avg_alpha = sum(g['alpha_score'] for g in gems) / len(gems)
        avg_mcap = sum(g['mcap'] for g in gems) / len(gems)
        avg_volume = sum(g['volume'] for g in gems) / len(gems)
        top_score = max(g['alpha_score'] for g in gems)
        
        print("📊 ALPHA MARKET INSIGHTS")
        print("----------------------------------------")
        print(f"• Average Alpha Score: {avg_alpha:.1f}/100")
        print(f"• Average Market Cap: {format_currency(avg_mcap)}")
        print(f"• Average Volume: {format_currency(avg_volume)}")
        print(f"• Best Alpha Gem Score: {top_score}/100")
        print(f"• Number of Tokens Analyzed: {len(gems)}")
        print()
        
        # Risk assessment
        high_risk = len([g for g in gems if g['liquidity'] < 5000])
        high_vol_ratio = len([g for g in gems if g['mcap'] > 0 and g['volume'] / g['mcap'] > 2])
        
        print("⚠️ RISK ASSESSMENT")
        print("----------------------------------------")
        print(f"• High Risk: {high_risk} tokens with low liquidity (<$5k)")
        print(f"• High Volatility: {high_vol_ratio} tokens with Vol/MCap > 200%")
        if len(premium_gems) == 0:
            print("• MARKET STATUS: No premium alpha opportunities detected")
        print()
        
    else:
        print("⚠️ NO ALPHA GEMS FOUND")
        print("----------------------------------------")
        print("The 30k-200k memecoin market is currently quiet.")
        print("Possible reasons:")
        print("• Market downturn or low trading volume")
        print("• Alpha opportunities moved to different mcap ranges")
        print("• Temporary lull in new token launches")
        print()

    print("⚠️ DISCLAIMER: HIGH RISK / NOT FINANCIAL ADVICE")
    print("Cron Job ID: 62bc16b8-c534-4ace-ba7d-615e1c217383")