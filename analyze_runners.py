#!/usr/bin/env python3
import requests
import json
from datetime import datetime

# Get token profiles (trending/new)
profiles_url = "https://api.dexscreener.com/token-profiles/latest/v1"
response = requests.get(profiles_url)
profiles = response.json()

# Get top pairs for Solana
search_url = "https://api.dexscreener.com/latest/dex/search?q=solana"
response = requests.get(search_url)
search_data = response.json()
pairs = search_data.get('pairs', [])

print('🏃 FINDING ACTUAL RUNNERS')
print('=' * 70)
print(f'Data timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print()

# Find pump.fun tokens from profiles with links to pairs
if pairs:
    print(f'Found {len(pairs)} Solana pairs')
    
    # Filter for high activity
    active_tokens = []
    for pair in pairs[:50]:
        mcap = pair.get('marketCap', 0) or 0
        volume = pair.get('volume', {}).get('h24', 0) or 0
        change = pair.get('priceChange', {}).get('h24', 0) or 0
        
        if mcap > 50000 and volume > 100000:
            active_tokens.append({
                'symbol': pair.get('baseToken', {}).get('symbol', 'Unknown'),
                'mcap': mcap,
                'volume': volume,
                'change': change,
                'address': pair.get('baseToken', {}).get('address', ''),
                'pair': pair
            })
    
    # Sort by volume
    active_tokens.sort(key=lambda x: x['volume'], reverse=True)
    
    print(f'\n🔥 TOP {min(10, len(active_tokens))} BY VOLUME:')
    print('-' * 70)
    
    for i, t in enumerate(active_tokens[:10], 1):
        vol_mcap = (t['volume'] / t['mcap'] * 100) if t['mcap'] > 0 else 0
        print(f"\n{i}. {t['symbol']}")
        print(f"   MCap: ${t['mcap']:,.0f} | Vol: ${t['volume']:,.0f}")
        print(f"   Vol/MCap: {vol_mcap:.1f}% | 24h: {t['change']:+.1f}%")
        print(f"   CA: {t['address']}")

# Check profiles for narrative/themes
print('\n\n📊 TOKEN PROFILES (Narrative Analysis):')
print('=' * 70)

# Get token addresses from profiles
pump_profiles = [p for p in profiles if p.get('chainId') == 'solana' and 'pump' in p.get('tokenAddress', '').lower()]

for p in pump_profiles[:8]:
    desc = p.get('description', 'No description')[:80]
    addr = p.get('tokenAddress', '')
    links = p.get('links', [])
    
    social_score = 0
    for link in links:
        if link.get('type') == 'twitter':
            social_score += 2
        if link.get('type') == 'telegram':
            social_score += 1
        if link.get('type') == 'website':
            social_score += 1
    
    print(f"\n{desc}...")
    print(f"   Social Score: {social_score}/5 | CA: {addr[:25]}...")
