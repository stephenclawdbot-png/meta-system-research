#!/usr/bin/env python3
import requests
from datetime import datetime

def generate_alpha_report():
    """Generate comprehensive alpha report for memecoins"""
    print("🧠 MEMECOIN ALPHA SCAN REPORT")
    print("=" * 60)
    print("Filter: Market Cap $30,000 - $200,000")
    print(f"Scan Time: {datetime.now().strftime('%A, %B %d, %Y — %I:%M %p (%Z)')}")
    print()
    
    search_terms = ["doge", "pepe", "moon", "shib", "bonk", "floki", "elon", "musk", "coin", "meme"]
    tokens = []
    
    for term in search_terms:
        try:
            url = f"https://api.dexscreener.com/latest/dex/search?q={term}"
            response = requests.get(url, timeout=8)
            
            if response.status_code == 200:
                data = response.json()
                if 'pairs' in data:
                    for token in data['pairs']:
                        mcap = token.get('marketCap', 0)
                        if 30000 <= mcap <= 200000:
                            txns = token.get('txns', {}).get('h24', {})
                            buys = txns.get('buys', 0)
                            sells = txns.get('sells', 0)
                            total_txns = buys + sells
                            buy_ratio = buys / total_txns if total_txns > 0 else 0
                            
                            tokens.append({
                                'symbol': token.get('baseToken', {}).get('symbol', 'Unknown'),
                                'name': token.get('baseToken', {}).get('name', 'Unknown'),
                                'mcap': mcap,
                                'volume': token.get('volume', {}).get('h24', 0),
                                'txns_24h': buys + sells,
                                'buy_ratio': buy_ratio,
                                'price_change': token.get('priceChange', {}).get('h24', 0),
                                'liquidity': token.get('liquidity', {}).get('usd', 0),
                                'chain': token.get('chainId', 'Unknown'),
                                'url': token.get('url')
                            })
        except:
            continue
    
    # Remove duplicates and calculate alpha scores
    unique_tokens = {}
    for token in tokens:
        key = token['symbol'].upper() + token['chain']
        if key not in unique_tokens:
            unique_tokens[key] = token
    
    token_list = list(unique_tokens.values())
    
    # Calculate alpha scores
    for token in token_list:
        vol_ratio = token['volume'] / token['mcap'] if token['mcap'] > 0 else 0
        alpha_score = (
            min(40, vol_ratio * 100) +  # Volume/mcap ratio (max 40)
            token['buy_ratio'] * 30 +   # Buy pressure (max 30)
            min(20, token['txns_24h'] / 10) +  # Transaction volume (max 20)
            min(10, max(0, token['price_change']) / 2)  # Positive price momentum (max 10)
        )
        token['alpha_score'] = min(100, alpha_score)
    
    token_list.sort(key=lambda x: x['alpha_score'], reverse=True)
    
    print(f"📊 SUMMARY STATISTICS")
    print("-" * 40)
    print(f"• Total Tokens Found: {len(token_list)}")
    
    if token_list:
        # Market analysis
        avg_score = sum(t['alpha_score'] for t in token_list) / len(token_list)
        high_alpha = len([t for t in token_list if t['alpha_score'] > 30])
        medium_alpha = len([t for t in token_list if 15 <= t['alpha_score'] <= 30])
        
        print(f"• Average Alpha Score: {avg_score:.1f}/100")
        print(f"• High Alpha Tokens (score >30): {high_alpha}")
        print(f"• Medium Alpha Tokens (score 15-30): {medium_alpha}")
        print(f"• Best Vol/MCap Ratio: {max(t['volume']/t['mcap'] for t in token_list if t['mcap'] > 0):.2f}x")
        print(f"• Best Buy Ratio: {max(t['buy_ratio'] for t in token_list if t['buy_ratio'] > 0):.1%}")
        print()
        
        print("🎯 TOP ALPHA CANDIDATES (Score >20)")
        print("-" * 40)
        
        alpha_tokens = [t for t in token_list if t['alpha_score'] > 20]
        
        if alpha_tokens:
            for i, token in enumerate(alpha_tokens[:5]):
                vol_ratio = token['volume'] / token['mcap'] if token['mcap'] > 0 else 0
                print(f"\n{i+1}. 💎 {token['symbol']}")
                print(f"   📛 {token['name']}")
                print(f"   ⛓️  {token['chain']}")
                print(f"   💰 MCap: ${token['mcap']:,}")
                print(f"   📈 24h Vol: ${token['volume']:,}")
                print(f"   🔥 Vol/MCap: {vol_ratio:.2f}x")
                print(f"   📊 Txns: {token['txns_24h']}")
                print(f"   🟢 Buy Ratio: {token['buy_ratio']:.1%}")
                print(f"   📈 Price Chg: {token['price_change']:.1f}%")
                print(f"   🎯 Alpha Score: {token['alpha_score']:.1f}/100")
                print(f"   🔗 {token['url']}")
        else:
            print("❌ No tokens with significant alpha detected")
            print("💡 Market appears quiet in this range")
            
            # Show top 3 by volume/mcap ratio instead
            if token_list:
                top_by_ratio = sorted(token_list, 
                                    key=lambda x: x['volume']/x['mcap'] if x['mcap'] > 0 else 0, 
                                    reverse=True)[:3]
                print("\n📈 TOP BY VOLUME/MCAP RATIO:")
                for token in top_by_ratio:
                    print(f"   • {token['symbol']}: {token['volume']/token['mcap']:.2f}x")
                    
        # Market sentiment
        print("\n📈 MARKET SENTIMENT")
        print("-" * 25)
        if high_alpha >= 3:
            print("• 🔥 BULLISH - Multiple alpha opportunities")
        elif medium_alpha >= 5:
            print("• 📊 MODERATE - Decent activity")
        else:
            print("• 🐻 QUIET - Low alpha detection")
            
    print("\n⚠️ ALPHA SCREENING NOTES")
    print("• Alpha Score = Volume/MCap (40%) + Buy Pressure (30%) + Txns (20%) + Momentum (10%)")
    print("• Score >30 = Strong alpha signal")
    print("• Score 15-30 = Moderate potential")
    print("• Always DYOR - memecoins are extremely high risk")

if __name__ == "__main__":
    generate_alpha_report()