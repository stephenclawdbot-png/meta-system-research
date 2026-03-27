#!/usr/bin/env python3
import requests
import time
from datetime import datetime

def fetch_solana_memecoins():
    """Broad Solana memecoin search"""
    # Search for various token patterns
    searches = [
        "https://api.dexscreener.com/latest/dex/search?q=sol",
        "https://api.dexscreener.com/latest/dex/search?q=memecoin", 
        "https://api.dexscreener.com/latest/dex/search?q=WIF",
        "https://api.dexscreener.com/latest/dex/search?q=BONK"
    ]
    
    all_tokens = []
    seen_addresses = set()
    
    for url in searches:
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if not data or 'pairs' not in data:
                continue
            
            for token in data.get('pairs', []):
                address = token.get('pairAddress', '')
                mcap = token.get('fdv', 0)
                
                if address in seen_addresses:
                    continue
                seen_addresses.add(address)
                
                # Target range: 30K-200K
                if 30000 <= mcap <= 200000:
                    token_info = {
                        'name': token.get('baseToken', {}).get('name', 'Unknown'),
                        'symbol': token.get('baseToken', {}).get('symbol', 'Unknown'),
                        'mcap': mcap,
                        'volume_24h': token.get('volume', {}).get('h24', 0),
                        'price_change_24h': token.get('priceChange', {}).get('h24', 0),
                        'url': token.get('url', ''),
                        'dex': token.get('dexId', ''),
                        'chain': token.get('chainId', ''),
                        'address': address,
                        'txns_24h': token.get('txns', {}).get('h24', 0),
                        'pairCreatedAt': token.get('pairCreatedAt', '')
                    }
                    
                    all_tokens.append(token_info)
            
            time.sleep(0.5)  # Rate limiting
            
        except Exception as e:
            print(f"Search error for {url}: {e}")
            continue
    
    return all_tokens

def calculate_comprehensive_score(token):
    """Enhanced scoring including volume momentum and age"""
    vol_mcap_ratio = (token['volume_24h'] / token['mcap']) * 100 if token['mcap'] > 0 else 0
    momentum = max(0, token['price_change_24h']) if token['price_change_24h'] else 0
    
    # Transaction velocity bonus
    txns_data = token.get('txns_24h', {})
    buy_count = txns_data.get('buys', 0) if isinstance(txns_data, dict) else txns_data
    txn_bonus = min(10, (buy_count or 0) / 50) 
    
    # Age bonus (newer tokens get more points)
    age_bonus = 0
    if token.get('pairCreatedAt'):
        # Very rough age estimation based on timestamp
        age_bonus = min(10, 10 - ((time.time() - get_timestamp(token['pairCreatedAt'])) / 3600))  # Points degrade over hours
    
    score = min(
        100,
        (min(40, vol_mcap_ratio * 2)) +           # Volume/MCap ratio
        (min(30, momentum * 2)) +                 # Price momentum  
        (min(15, token['volume_24h'] / 1000)) +   # Absolute volume
        txn_bonus +                               # Transaction velocity
        age_bonus                                 # Age freshness
    )
    
    return round(score, 1)

def get_timestamp(dt_string):
    """Convert ISO timestamp to Unix timestamp"""
    try:
        from datetime import datetime
        dt = datetime.fromisoformat(dt_string.replace('Z', '+00:00'))
        return dt.timestamp()
    except:
        return time.time() - 86400  # Default to 24h ago

def categorize_gems(tokens):
    """Categorize gems by scoring tiers"""
    tiers = {
        "🚀 HIGH ALPHA (50+)": [],
        "💎 MEDIUM ALPHA (30-49)": [],
        "⚡ GROWTH ALPHA (15-29)": [],
        "🟡 DEVELOPING ALPHA (5-14)": [],
        "🔴 EARLY STAGE (0-4)": []
    }
    
    for token in tokens:
        score = token['alpha_score']
        if score >= 50:
            tiers["🚀 HIGH ALPHA (50+)"].append(token)
        elif score >= 30:
            tiers["💎 MEDIUM ALPHA (30-49)"].append(token)
        elif score >= 15:
            tiers["⚡ GROWTH ALPHA (15-29)"].append(token)
        elif score >= 5:
            tiers["🟡 DEVELOPING ALPHA (5-14)"].append(token)
        else:
            tiers["🔴 EARLY STAGE (0-4)"].append(token)
    
    return tiers

def main():
    print("🧠 COMPREHENSIVE ALPHA SCAN - MEMECOINS 30K-200K")
    print("=" * 60)
    print("Scan Time:", datetime.now().strftime("%A, %B %d, %Y — %I:%M %p (Asia/Manila)"))
    print("Source: DexScreener Multiple Searches")
    print("Focus: Solana ecosystem with volume momentum")
    print()
    
    tokens = fetch_solana_memecoins()
    
    if not tokens:
        print("❌ MARKET QUIET: No memecoins found in target range")
        print("Market conditions suggest extremely low activity")
        print("This could indicate:")
        print("  • Early morning market lull (2:30 AM Asia)")
        print("  • Server/maintenance issues")
        print("  • Genuine market-wide quiet period")
        return
    
    # Calculate scores
    for token in tokens:
        token['alpha_score'] = calculate_comprehensive_score(token)
    
    # Sort by score
    tokens.sort(key=lambda x: x['alpha_score'], reverse=True)
    
    tiers = categorize_gems(tokens)
    
    total_found = sum(len(tier) for tier in tiers.values())
    print(f"📊 MARKET OVERVIEW: {total_found} tokens total")
    print("-" * 40)
    
    # Display tiers
    for tier_name, tier_tokens in tiers.items():
        if tier_tokens:
            print(f"\n{tier_name}: {len(tier_tokens)} tokens")
            print("-" * len(tier_name))
            
            for token in tier_tokens:
                vol_mcap_ratio = (token['volume_24h'] / token['mcap']) * 100 if token['mcap'] > 0 else 0
                score_emoji = "🚀" if token['alpha_score'] >= 60 else "💎" if token['alpha_score'] >= 40 else "⚡" if token['alpha_score'] >= 20 else "🟡"
                
                print(f"{score_emoji} {token['symbol']} - Score: {token['alpha_score']}/100")
                print(f"   📛 {token['name']}")
                print(f"   💰 MCap: ${token['mcap']:,}")
                print(f"   📈 24h Vol: ${token['volume_24h']:,}")
                print(f"   📊 Vol/MCp: {vol_mcap_ratio:.1f}%")
                print(f"   🎯 24h Change: {token['price_change_24h'] or 0:.1f}%")
                print(f"   🔗 Dex: {token['dex']}")
                print(f"   👁️ {token['url']}")
                if token.get('txns_24h'):
                    print(f"   🔄 24h Txns: {token['txns_24h']}")
                print()
    
    # Market analytics
    print("💡 MARKET ANALYTICS:")
    print("-" * 20)
    print(f"• Total Alpha Gems: {total_found}")
    
    if tokens:
        avg_score = sum(t['alpha_score'] for t in tokens) / len(tokens)
        avg_mcap = sum(t['mcap'] for t in tokens) / len(tokens)
        avg_vol = sum(t['volume_24h'] for t in tokens) / len(tokens)
        
        print(f"• Average Alpha Score: {avg_score:.1f}/100")
        print(f"• Average Market Cap: ${avg_mcap:,.0f}")
        print(f"• Average Volume: ${avg_vol:,.0f}")
    
    # Trading insights
    print("\n🎯 TRADING INSIGHTS:")
    print("-" * 18)
    if tokens:
        top_gem = tokens[0]
        if top_gem['alpha_score'] >= 40:
            print(f"• TOP PLAY: {top_gem['symbol']} shows strong fundamentals")
        elif top_gem['alpha_score'] >= 20:
            print(f"• MONITOR: {top_gem['symbol']} worth watching")
        else:
            print("• MARKET QUIET: Low alpha scores suggest waiting")
    
    print("\n⚠️ DISCLAIMER: High-risk memecoin analysis - DYOR essential")

if __name__ == "__main__":
    main()