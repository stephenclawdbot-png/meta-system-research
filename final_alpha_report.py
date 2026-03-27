#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def alpha_scanner_final():
    """Comprehensive alpha scanner for memecoins in 30k-200k mcap range"""
    
    print("🚀 MEMECOIN ALPHA SCANNER - DexScreener Analysis")
    print("=" * 80)
    print(f"Scan Time: {datetime.now().strftime('%A, %B %d, %Y — %I:%M %p (Asia/Manila)')}")
    print("Target Range: $30K - $200K Market Cap")
    print("Criteria: High volume/mcap ratio + memecoin pattern")
    print()
    
    # Strategy: Use multiple search approaches
    searches = [
        "https://api.dexscreener.com/latest/dex/search?q=memecoin",
        "https://api.dexscreener.com/latest/dex/search?q=solana",
        "https://api.dexscreener.com/latest/dex/search?q=meme",
    ]
    
    memecoin_keywords = ["pepe", "doge", "bonk", "wif", "cat", "frog", "inu", "hamster"]
    all_tokens = []
    
    # Search by keyword
    for keyword in memecoin_keywords:
        try:
            url = f"https://api.dexscreener.com/latest/dex/search?q={keyword}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data and 'pairs' in data:
                    for token in data['pairs']:
                        mcap = token.get('marketCap', token.get('fdv', 0))
                        symbol = token.get('baseToken', {}).get('symbol', '').upper()
                        
                        # Apply filters
                        if (30000 <= mcap <= 200000 and
                            token.get('volume', {}).get('h24', 0) >= 500 and
                            token.get('priceUsd', 0) > 0):
                            
                            vol_mcap_ratio = token.get('volume', {}).get('h24', 0) / mcap * 100 if mcap > 0 else 0
                            
                            token_info = {
                                'symbol': symbol,
                                'keyword': keyword,
                                'mcap': mcap,
                                'volume': token.get('volume', {}).get('h24', 0),
                                'vol_ratio': vol_mcap_ratio,
                                'price': token.get('priceUsd', 0),
                                'price_change': token.get('priceChange', {}).get('h24', 0),
                                'liquidity': token.get('liquidity', {}).get('usd', 0),
                                'txns': sum(token.get('txns', {}).get('h24', {}).values()) if token.get('txns', {}).get('h24') else 0,
                                'url': token.get('url', ''),
                                'chain': token.get('chainId', '')
                            }
                            
                            # Avoid duplicates
                            if not any(t['symbol'] == symbol and t['chain'] == token_info['chain'] for t in all_tokens):
                                all_tokens.append(token_info)
        except:
            continue
    
    print(f"Found {len(all_tokens)} qualifying tokens\n")
    
    if not all_tokens:
        print("❌ No alpha gems detected")
        return
    
    # Sort by volume/mcap ratio (highest first)
    all_tokens.sort(key=lambda x: x['vol_ratio'], reverse=True)
    top_5 = all_tokens[:5]
    
    print("🔥 TOP 5 ALPHA PICKS (Highest Volume/MCap Ratio)")
    print("-" * 80)
    
    for i, token in enumerate(top_5, 1):
        print(f"🎯 #{i} {token['symbol']}")
        print(f"   📊 ${token['mcap']:,.0f} mcap • ${token['volume']:,.0f} vol • {token['vol_ratio']:.1f}% ratio")
        print(f"   📈 Price: ${token['price']:.8f} ({token['price_change']:+.1f}%)")
        print(f"   💧 Liquidity: ${token['liquidity']:,.0f} • Txns: {token['txns']}")
        print(f"   🌐 Chain: {token['chain']}")
        print(f"   🔗 {token['url']}")
        print()
    
    # Alpha detection logic
    if top_5:
        best_token = top_5[0]
        
        print("💡 ALPHA SIGNALS DETECTED")
        print("-" * 80)
        
        signals = []
        
        if best_token['vol_ratio'] > 50:
            signals.append("🚀 STRONG VOLUME: Volume > 50% of MCap (high efficiency)")
        elif best_token['vol_ratio'] > 25:
            signals.append("📈 GOOD VOLUME: Volume > 25% of MCap")
        
        if best_token['price_change'] > 10:
            signals.append(f"📈 BULLISH PRICE: +{best_token['price_change']:.1f}% momentum")
        elif best_token['price_change'] > 5:
            signals.append(f"📊 POSITIVE PRICE: +{best_token['price_change']:.1f}%")
        
        if best_token['txns'] > 500:
            signals.append(f"🔄 HIGH ACTIVITY: {best_token['txns']} transactions")
        elif best_token['txns'] > 100:
            signals.append(f"🔄 GOOD ACTIVITY: {best_token['txns']} transactions")
        
        # Risk assessment
        if best_token['liquidity'] < 5000:
            signals.append("⚠️ LOW LIQUIDITY: High slippage risk")
        elif best_token['liquidity'] < 20000:
            signals.append("⚠️ MODERATE LIQUIDITY") 
        else:
            signals.append("✅ GOOD LIQUIDITY")
        
        for signal in signals:
            print(f"• {signal}")
        
        # Overall assessment
        alpha_score = min(100, (
            min(30, best_token['vol_ratio'] * 0.3) +
            min(25, max(0, best_token['price_change']) * 2.5) +
            min(20, best_token['txns'] / 50 * 20) +
            min(15, best_token['liquidity'] / 2000 * 15) +
            min(10, len(best_token['symbol']) * 2)  # Short symbols tend to perform better
        ))
        
        print(f"\n🧠 ALPHA SCORE: {alpha_score:.0f}/100")
        
        if alpha_score > 70:
            print("💎 HIGH ALPHA: Strong buy signals detected")
        elif alpha_score > 50:
            print("📈 MEDIUM ALPHA: Good opportunity")
        else:
            print("📊 MODERATE ALPHA: Requires further research")
    
    print(f"\n⚠️ DISCLAIMER: Memecoins are high risk. DYOR required.")
    print(f"   Scanned at {datetime.now().strftime('%I:%M %p')} Asia/Manila")

if __name__ == "__main__":
    alpha_scanner_final()