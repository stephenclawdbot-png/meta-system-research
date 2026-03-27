#!/usr/bin/env python3
import json
import requests
from datetime import datetime
import time

print("🧠 MEMECOIN ALPHA SCANNER - REAL TIME ANALYSIS")
print("="*60)
print("Filter: Market Cap $30,000 - $200,000")
print("Time:", datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (%Z)"))
print()

def search_meme_categories():
    """Search multiple meme coin categories"""
    categories = [
        "dog", "cat", "meme", "coin", "pepe", "shib", "elon", "musk",
        "doge", "floki", "bonk", "woof", "moon", "mars", "satoshi",
        "test", "token", "degens", "alpha", "gem", "diamond"
    ]
    
    all_tokens = []
    
    for category in categories:
        try:
            response = requests.get(
                f"https://api.dexscreener.com/latest/dex/search?q={category}",
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                if data and 'pairs' in data:
                    for token in data['pairs']:
                        if 'marketCap' in token:
                            all_tokens.append(token)
            # Rate limiting
            time.sleep(0.1)
        except Exception as e:
            print(f"❌ Error searching {category}: {e}")
    
    return all_tokens

def filter_alpha_gems(tokens):
    """Filter tokens based on alpha criteria"""
    alpha_candidates = []
    
    for token in tokens:
        try:
            mcap = token['marketCap']
            
            # Primary filter: Market cap range
            if not (30000 <= mcap <= 200000):
                continue
                
            # Secondary filters
            volume_24h = token.get('volume', {}).get('h24', 0)
            txns_24h = token.get('txns', {}).get('h24', {})
            buys_24h = txns_24h.get('buys', 0)
            sells_24h = txns_24h.get('sells', 0)
            total_txns_24h = buys_24h + sells_24h
            
            # Skip if completely dead
            if total_txns_24h < 5:
                continue
                
            # Calculate alpha score
            score = 0
            
            # Volume/MCap ratio (max 40 pts)
            if volume_24h > 0:
                vol_ratio = volume_24h / mcap
                score += min(40, vol_ratio * 100)
            
            # Buy pressure (max 30 pts)
            if total_txns_24h > 0:
                buy_ratio = buys_24h / total_txns_24h
                score += buy_ratio * 30
            
            # Transaction velocity (max 20 pts)
            score += min(20, total_txns_24h / 10)
            
            # Price momentum (max 10 pts)
            price_change_24h = abs(token.get('priceChange', {}).get('h24', 0))
            score += min(10, price_change_24h * 0.5)
            
            # Age freshness (negative score for old tokens)
            if 'pairCreatedAt' in token:
                age_hours = (datetime.now().timestamp() - token['pairCreatedAt'] / 1000) / 3600
                if age_hours > 24:  # Penalize old tokens
                    score -= min(20, (age_hours - 24) / 24 * 10)
            
            score = max(0, score)
            
            alpha_candidates.append({
                'symbol': token.get('baseToken', {}).get('symbol', 'Unknown'),
                'name': token.get('baseToken', {}).get('name', 'Unknown'),
                'mcap': mcap,
                'volume': volume_24h,
                'vol_ratio': volume_24h / mcap if mcap > 0 else 0,
                'buy_ratio': buy_ratio if total_txns_24h > 0 else 0,
                'txns_24h': total_txns_24h,
                'liquidity': token.get('liquidity', {}).get('usd', 0),
                'price_change_24h': token.get('priceChange', {}).get('h24', 0),
                'url': token.get('url'),
                'score': round(score, 1),
                'chain': token.get('chainId', 'Unknown')
            })
            
        except Exception as e:
            continue
    
    return sorted(alpha_candidates, key=lambda x: x['score'], reverse=True)

def main():
    print("🔍 Scanning multiple meme coin categories...")
    
    try:
        tokens = search_meme_categories()
        print(f"📊 Found {len(tokens)} total tokens")
        
        alpha_gems = filter_alpha_gems(tokens)
        print(f"🎯 Alpha candidates in range: {len(alpha_gems)}")
        
        if not alpha_gems:
            print("\n❌ No alpha gems found in 30k-200k range")
            print("🔧 Try searching manually on DexScreener:")
            print("  - Filter by: Market Cap $30K-$200K")
            print("  - Sort by: Volume/MCap Ratio")
            print("  - Look for: High transaction volume")
            print("  - Check: Recent price momentum")
            return
        
        # Show top gems
        print(f"\n🔥 TOP ALPHA GEMS - SCORE > 20")
        print("-" * 60)
        
        high_alpha = [g for g in alpha_gems if g['score'] > 25]
        medium_alpha = [g for g in alpha_gems if 15 <= g['score'] <= 25]
        
        for gem in high_alpha[:10]:
            print(f"\n💎 {gem['symbol']} - Alpha Score: {gem['score']}/100")
            print(f"   📛 Name: {gem['name']}")
            print(f"   ⛓️  Chain: {gem['chain']}")
            print(f"   💰 MCap: ${gem['mcap']:,}")
            print(f"   📈 24h Volume: ${gem['volume']:,}")
            print(f"   🔥 Vol/MCap Ratio: {gem['vol_ratio']:.2f}x")
            print(f"   📊 Buy Ratio: {gem['buy_ratio']:.1%}")
            print(f"   🔄 Transactions 24h: {gem['txns_24h']}")
            print(f"   💧 Liquidity: ${gem['liquidity']:,}")
            print(f"   📈 24h Price Change: {gem['price_change_24h']:.1f}%")
            print(f"   🔗 DexScreener: {gem['url']}")
        
        print(f"\n📈 MARKET ANALYSIS")
        print("-" * 25)
        print(f"• High Alpha Gems: {len(high_alpha)}")
        print(f"• Medium Alpha Gems: {len(medium_alpha)}")
        print(f"• Total Candidates: {len(alpha_gems)}")
        
        # Market sentiment
        if len(high_alpha) >= 3:
            print("• Sentiment: 🔥 BULLISH - Good alpha opportunities")
        elif len(alpha_gems) > 5:
            print("• Sentiment: 📊 MODERATE - Some activity")
        else:
            print("• Sentiment: 🐻 QUIET - Low alpha detection")
        
        print("\n⚠️ RISK DISCLAIMER: This is alpha screening only")
        print("   Always do your own research (DYOR)")
        print("   Memecoins are extremely high risk")
        
    except Exception as e:
        print(f"❌ Scanner error: {e}")
        print("\n🔧 Manual scan required - DexScreener.com")

if __name__ == "__main__":
    main()