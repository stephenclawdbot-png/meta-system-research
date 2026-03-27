#!/usr/bin/env python3
import json
import requests
from datetime import datetime

print("🧠 MEMECOIN ALPHA SCANNER - 30K-200K MCAP")
print("="*60)
print("Filter: Market Cap $30,000 - $200,000")
print("Time:", datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (%Z)"))
print()

def fetch_meme_coins():
    """Fetch multiple meme coin categories from DexScreener"""
    meme_search_terms = ["memecoin", "meme", "coin", "token", "degens"]
    all_results = []
    
    for term in meme_search_terms:
        try:
            response = requests.get(f"https://api.dexscreener.com/latest/dex/search?q={term}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data and 'pairs' in data:
                    all_results.extend(data['pairs'])
        except Exception as e:
            print(f"Error fetching {term}: {e}")
    
    return all_results

def filter_alpha_gems(tokens):
    """Filter tokens based on alpha criteria"""
    alpha_candidates = []
    
    for token in tokens:
        if not token.get('marketCap'):
            continue
            
        mcap = token['marketCap']
        volume_24h = token.get('volume', {}).get('h24', 0)
        
        # Filter: 30k-200k market cap
        if 30000 <= mcap <= 200000:
            # Calculate alpha score components
            score = 0
            
            # Volume/mcap ratio (max 25 pts)
            if volume_24h > 0:
                vol_ratio = volume_24h / mcap
                score += min(25, vol_ratio * 100)
            
            # Buy/Sell ratio (max 20 pts) - estimate from recent transactions
            txns = token.get('txns', {})
            h1_buys = txns.get('h1', {}).get('buys', 0)
            h1_sells = txns.get('h1', {}).get('sells', 0)
            if h1_buys + h1_sells > 0:
                buy_ratio = h1_buys / (h1_buys + h1_sells)
                score += min(20, buy_ratio * 20)
            
            # Price momentum (max 15 pts)
            price_change = token.get('priceChange', {})
            h1_change = abs(price_change.get('h1', 0))
            score += min(15, h1_change * 0.5)
            
            # Liquidity (max 10 pts)
            liquidity = token.get('liquidity', {}).get('usd', 0)
            score += min(10, liquidity / 5000)
            
            # Transaction velocity (max 10 pts)
            h24_txns_total = txns.get('h24', {}).get('buys', 0) + txns.get('h24', {}).get('sells', 0)
            score += min(10, h24_txns_total / 50)
            
            # Social presence (max 10 pts)
            has_socials = bool(token.get('info', {}).get('socials'))
            has_website = bool(token.get('info', {}).get('websites'))
            score += 5 if has_socials else 0
            score += 5 if has_website else 0
            
            # Age freshness (max 10 pts) - tokens created more recently score higher
            created_at = token.get('pairCreatedAt')
            if created_at:
                age_days = (datetime.now().timestamp() - created_at / 1000) / 86400
                age_score = max(0, 10 - min(age_days, 10))
                score += age_score
            
            alpha_candidates.append({
                'symbol': token.get('baseToken', {}).get('symbol', 'Unknown'),
                'name': token.get('baseToken', {}).get('name', 'Unknown'),
                'mcap': mcap,
                'volume': volume_24h,
                'price': token.get('priceUsd'),
                'change_h1': price_change.get('h1', 0),
                'buy_ratio': h1_buys / max(1, h1_buys + h1_sells),
                'txns_24h': h24_txns_total,
                'liquidity': liquidity,
                'url': token.get('url'),
                'score': round(score, 2),
                'filter_score': calculate_filter_score(token)
            })
    
    return sorted(alpha_candidates, key=lambda x: x['score'], reverse=True)

def calculate_filter_score(token):
    """Calculate filter-specific score (alpha criteria)"""
    score = 0
    
    # Market cap in sweet spot
    mcap = token.get('marketCap', 0)
    if 50000 <= mcap <= 150000:  # Sweet spot
        score += 25
    elif 30000 <= mcap <= 200000:  # Acceptable range
        score += 15
    
    # High volume/mcap ratio
    volume_24h = token.get('volume', {}).get('h24', 0)
    if volume_24h > 0:
        vol_ratio = volume_24h / max(mcap, 1)
        if vol_ratio > 5:  # Very high ratio
            score += 30
        elif vol_ratio > 2:  # High ratio
            score += 20
        elif vol_ratio > 1:  # Good ratio
            score += 10
    
    # Strong buy pressure
    txns = token.get('txns', {})
    h1_buys = txns.get('h1', {}).get('buys', 0)
    h1_sells = txns.get('h1', {}).get('sells', 0)
    if h1_buys + h1_sells > 10:
        buy_ratio = h1_buys / (h1_buys + h1_sells)
        if buy_ratio > 0.7:  # Strong buying
            score += 20
        elif buy_ratio > 0.6:  # Good buying
            score += 15
        elif buy_ratio > 0.55:  # Above average
            score += 10
    
    # Good liquidity
    liquidity = token.get('liquidity', {}).get('usd', 0)
    if liquidity > 50000:
        score += 15
    elif liquidity > 10000:
        score += 10
    elif liquidity > 5000:
        score += 5
    
    # Recent creation (freshness)
    created_at = token.get('pairCreatedAt')
    if created_at:
        age_days = (datetime.now().timestamp() - created_at / 1000) / 86400
        if age_days < 1:  # Less than 1 day old
            score += 15
        elif age_days < 3:  # Less than 3 days old
            score += 10
        elif age_days < 7:  # Less than 7 days old
            score += 5
    
    return min(100, score)

def main():
    try:
        print("🔍 Scanning DexScreener for memecoins...")
        tokens = fetch_meme_coins()
        
        if not tokens:
            print("❌ No tokens found")
            return
        
        alpha_gems = filter_alpha_gems(tokens)
        
        print(f"📊 Scan Complete: Found {len(alpha_gems)} alpha candidates")
        
        if not alpha_gems:
            print("\n🎯 No gems found in 30k-200k mcap range")
            print("⚠️ The market may be quiet or criteria too strict")
            return
        
        print(f"\n🔥 TOP ALPHA GEMS (30K-200K MCAP)")
        print("-" * 60)
        
        for i, gem in enumerate(alpha_gems[:10], 1):
            print(f"\n{i}. 💎 {gem['symbol']} - Alpha Score: {gem['score']:.1f}/100")
            print(f"   📛 Name: {gem['name']}")
            print(f"   💰 MCap: ${gem['mcap']:,}")
            print(f"   📈 24h Volume: ${gem['volume']:,}")
            print(f"   🔥 Vol/MCap Ratio: {(gem['volume']/gem['mcap']):.1f}x")
            print(f"   📊 1h Change: {gem['change_h1']:.1f}%")
            print(f"   🔄 Buy Ratio: {gem['buy_ratio']:.1%}")
            print(f"   💧 Transactions 24h: {gem['txns_24h']}")
            print(f"   🏦 Liquidity: ${gem['liquidity']:,}")
            print(f"   🌐 Filter Score: {gem['filter_score']}/100")
            print(f"   🔗 DexScreener: {gem['url']}")
        
        print("\n📈 ALPHA ANALYSIS")
        print("-" * 25)
        
        high_scorers = [g for g in alpha_gems if g['score'] >= 60]
        if high_scorers:
            print(f"• High Alpha ({len(high_scorers)} gems): Score ≥ 60")
            for gem in high_scorers:
                print(f"  - {gem['symbol']}: {gem['score']:.1f} (${gem['mcap']:,})")
        
        medium_scorers = [g for g in alpha_gems if 40 <= g['score'] < 60]
        if medium_scorers:
            print(f"• Medium Alpha ({len(medium_scorers)} gems): Score 40-59")
        
        print(f"• Total Alpha Gems: {len(alpha_gems)}")
        print(f"• Market Status: {'Active' if len(alpha_gems) > 5 else 'Quiet'}")
        
        print("\n⚠️ DISCLAIMER: This is alpha detection only - DYOR")
        
    except Exception as e:
        print(f"❌ Error during scan: {e}")
        print("\n🔧 Manual Verification Required:")
        print("- Check DexScreener.com manually")
        print("- Filter by market cap: $30K-$200K")
        print("- Look for high volume/price momentum")

if __name__ == "__main__":
    main()