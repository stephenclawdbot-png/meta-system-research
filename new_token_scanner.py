#!/usr/bin/env python3
"""
New Token Alpha Scanner
Finds freshly created Solana tokens that could be memecoins
"""

import requests
import json
from datetime import datetime, timedelta

print("🚀 NEW TOKEN ALPHA SCANNER")
print("=" * 60)
print(f"📅 Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("🎯 Target: Freshly created Solana tokens (potential memecoins)")
print("💰 Focus: Early alpha detection before mainstream attention")
print("")

def scan_new_tokens():
    """Scan for newly created tokens on DexScreener"""
    try:
        # Fetch token profiles
        response = requests.get('https://api.dexscreener.com/token-profiles/latest/v1', timeout=15)
        profiles = response.json()
        
        if not isinstance(profiles, list):
            print("❌ Unexpected response format")
            return []
        
        # Filter for Solana tokens created recently (last 24 hours)
        recent_tokens = []
        cutoff_time = datetime.now() - timedelta(hours=24)
        
        for profile in profiles:
            if profile.get('chainId') != 'solana':
                continue
                
            created_time = profile.get('createdAt')
            if created_time:
                try:
                    # Convert timestamp to datetime
                    created_dt = datetime.fromtimestamp(created_time / 1000)
                    
                    # Check if created within last 24 hours
                    if created_dt >= cutoff_time:
                        recent_tokens.append(profile)
                        
                except Exception:
                    continue
        
        print(f"🔍 Found {len(recent_tokens)} Solana tokens created in last 24 hours")
        
        # Enrich with pair data
        enriched_tokens = []
        for token in recent_tokens:
            token_address = token.get('tokenAddress')
            if not token_address:
                continue
            
            # Get pair data for this token
            pair_response = requests.get(f'https://api.dexscreener.com/tokens/v1/solana/{token_address}', timeout=10)
            pair_data = pair_response.json()
            
            if isinstance(pair_data, list) and len(pair_data) > 0:
                # Take the highest volume pair
                best_pair = max(pair_data, key=lambda x: x.get('volume', {}).get('h24', 0))
                
                token_info = {
                    'symbol': token.get('symbol', 'Unknown'),
                    'name': token.get('name', 'Unknown'),
                    'address': token_address,
                    'pair_address': best_pair.get('pairAddress', ''),
                    'market_cap': best_pair.get('marketCap', 0),
                    'volume_24h': best_pair.get('volume', {}).get('h24', 0),
                    'price': best_pair.get('priceUsd', 0),
                    'price_change_24h': best_pair.get('priceChange', {}).get('h24', 0),
                    'liquidity': best_pair.get('liquidity', {}).get('usd', 0),
                    'created_at': token.get('createdAt', 0),
                    'age_hours': None
                }
                
                # Calculate age
                if token_info['created_at']:
                    created_dt = datetime.fromtimestamp(token_info['created_at'] / 1000)
                    token_info['age_hours'] = (datetime.now() - created_dt).total_seconds() / 3600
                
                enriched_tokens.append(token_info)
        
        print(f"✅ Successfully enriched {len(enriched_tokens)} tokens\n")
        
        # Filter by our target criteria
        target_tokens = [t for t in enriched_tokens 
                        if 1000 <= t['market_cap'] <= 500000  # Broader range since they're new
                        and t['volume_24h'] > 100  # Some volume activity
                        and t['age_hours'] < 24]   # Under 24 hours old
        
        # Sort by age (newest first)
        target_tokens.sort(key=lambda x: x['age_hours'] or 999)
        
        return target_tokens
        
    except Exception as e:
        print(f"❌ Scan error: {e}")
        return []

def main():
    tokens = scan_new_tokens()
    
    if tokens:
        print("🎉 ALPHA OPPORTUNITIES DETECTED!")
        print("=" * 80)
        
        for i, token in enumerate(tokens, 1):
            print(f"{i}. 🚨 {token['symbol']}: {token['name']}")
            print(f"   💰 Market Cap: ${token['market_cap']:,}")
            print(f"   📈 24h Volume: ${token['volume_24h']:,}")
            print(f"   📊 Price: ${token['price']:.6f}")
            print(f"   📈 24h Change: {token['price_change_24h']:+.2f}%")
            print(f"   💧 Liquidity: ${token['liquidity']:,}")
            print(f"   ⏱️ Age: {token['age_hours']:.1f} hours")
            
            if token['pair_address']:
                print(f"   🔗 DexScreener: https://dexscreener.com/solana/{token['pair_address']}")
            
            # Alpha Score calculation
            alpha_score = 0
            if token['volume_24h'] / max(token['market_cap'], 1) > 0.1:
                alpha_score += 25  # High vol/mcap ratio
            if token['age_hours'] < 6:
                alpha_score += 30  # Very fresh
            elif token['age_hours'] < 12:
                alpha_score += 20
            elif token['age_hours'] < 24:
                alpha_score += 10
            
            print(f"   ⚡ Alpha Score: {alpha_score}/100")
            print("-" * 60)
    else:
        print("📭 No new token alpha opportunities detected")
        print("")
        print("💡 Tips for future scans:")
        print("- Scan more frequently for fresher opportunities")
        print("- Check Pump.fun for newly launched tokens")
        print("- Monitor DexScreener trending/popular sections")

if __name__ == "__main__":
    main()