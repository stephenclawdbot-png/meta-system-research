#!/usr/bin/env python3
import json
import subprocess
from datetime import datetime
import time

# Enhanced search terms covering more meme trends
search_terms = [
    'memecoin', 'solana', 'pepe', 'doge', 'bonk', 'wif', 'slerf', 'cat', 
    'ai', 'trump', 'maga', 'based', 'sam', 'rocket', 'baby', 'inu', 'frog', 
    'hamster', 'money', 'cash', 'elon', 'shib', 'meme', 'wojak', 'dog'
]

results = []
seen_addresses = set()

for term in search_terms:
    try:
        cmd = f'curl -s "https://api.dexscreener.com/latest/dex/search/?q={term}&limit=100"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if 'pairs' in data:
                for pair in data['pairs']:
                    base_address = pair.get('baseToken', {}).get('address')
                    if base_address and base_address in seen_addresses:
                        continue
                    seen_addresses.add(base_address)
                    
                    mcap = pair.get('marketCap', 0)
                    if 30000 <= mcap <= 200000:
                        # Get more detailed metrics
                        fdv = pair.get('fdv', 0)
                        liquidity = pair.get('liquidity', {}).get('usd', 0)
                        volume_5m = pair.get('volume', {}).get('m5', 0)
                        volume_1h = pair.get('volume', {}).get('h1', 0)
                        volume_6h = pair.get('volume', {}).get('h6', 0)
                        volume_24h = pair.get('volume', {}).get('h24', 0)
                        price_change_5m = pair.get('priceChange', {}).get('m5', 0)
                        price_change_1h = pair.get('priceChange', {}).get('h1', 0)
                        price_change_6h = pair.get('priceChange', {}).get('h6', 0)
                        price_change_24h = pair.get('priceChange', {}).get('h24', 0)
                        
                        results.append({
                            'symbol': pair['baseToken']['symbol'],
                            'name': pair['baseToken'].get('name', ''),
                            'mcap': mcap,
                            'fdv': fdv,
                            'liquidity': liquidity,
                            'price': pair.get('priceUsd', 0),
                            'volume_5m': volume_5m,
                            'volume_1h': volume_1h,
                            'volume_6h': volume_6h,
                            'volume_24h': volume_24h,
                            'price_change_5m': price_change_5m,
                            'price_change_1h': price_change_1h,
                            'price_change_6h': price_change_6h,
                            'price_change_24h': price_change_24h,
                            'chain': pair.get('chainId', ''),
                            'pair_address': pair.get('pairAddress', ''),
                            'created_at': pair.get('pairCreatedAt', ''),
                            'url': pair['url']
                        })
                        
        time.sleep(0.5)  # Rate limiting
    except Exception as e:
        print(f'Error searching {term}: {e}')

print(f'Total tokens found: {len(results)}')

# Enhanced alpha scoring
for token in results:
    # Volume/MCap ratio (0-25 pts)
    vol_mcap_ratio = token['volume_24h'] / max(token['mcap'], 1)
    vol_score = min(vol_mcap_ratio * 100, 25)
    
    # Price momentum (0-25 pts)
    momentum_weights = {'5m': 0.1, '1h': 0.3, '6h': 0.4, '24h': 0.2}
    momentum_score = 0
    for timeframe, weight in momentum_weights.items():
        change = token.get(f'price_change_{timeframe}', 0)
        if change > 0:
            momentum_score += min(change * 0.5, 25) * weight
    
    # Volume acceleration (0-20 pts)
    recent_vol = token['volume_1h'] / 3600  # hourly rate
    avg_vol = token['volume_24h'] / 24
    vol_accel = min((recent_vol / max(avg_vol, 1)) * 20, 20)
    
    # Liquidity health (0-15 pts)
    liq_score = min((token['liquidity'] / max(token['mcap'], 1)) * 15, 15)
    
    # Market efficiency (0-15 pts) - high MCap/volume ratio = good
    mcap_eff_score = min((token['mcap'] / max(token['volume_24h'], 1)) * 0.3, 15)
    
    alpha_score = vol_score + momentum_score + vol_accel + liq_score + mcap_eff_score
    token['alpha_score'] = round(alpha_score, 1)
    token['score_breakdown'] = {
        'volume_score': round(vol_score, 1),
        'momentum_score': round(momentum_score, 1),
        'volume_acceleration': round(vol_accel, 1),
        'liquidity_score': round(liq_score, 1),
        'market_efficiency': round(mcap_eff_score, 1)
    }

# Sort by alpha score descending
results.sort(key=lambda x: x['alpha_score'], reverse=True)

print('\n' + '='*80)
print('🎯 ENHANCED MEMECOIN ALPHA SCANNER - SUB $30K-$200K MCAP')
print('='*80)
print(f"Time: {datetime.now().strftime('%A, %B %d, %Y — %I:%M %p (Asia/Manila)')}")
print(f"Market Cap Range: ${30000:,}-${200000:,}")
print(f"Unique Tokens Found: {len(results)}")
print('='*80)

# Print top 15 results
for i, token in enumerate(results[:15], 1):
    print(f"\n{i}. {token['symbol']} ({token['name']})")
    print(f"   💰 MCap: ${token['mcap']:,} | 📊 Vol24h: ${token['volume_24h']:,.0f}")
    print(f"   📈 Momentum: 5m:{token['price_change_5m']}% 1h:{token['price_change_1h']}% 6h:{token['price_change_6h']}% 24h:{token['price_change_24h']}%")
    print(f"   💧 Liquidity: ${token['liquidity']:,} | 🔗 Chain: {token['chain']}")
    print(f"   🔥 ALPHA SCORE: {token['alpha_score']}/100")
    print(f"   Breakdown: Vol:{token['score_breakdown']['volume_score']} | Mom:{token['score_breakdown']['momentum_score']} | Accel:{token['score_breakdown']['volume_acceleration']}")
    print(f"   🌐 {token['url']}")

print('\n' + '='*80)
print("💡 Scanner complete. Focusing on high volume/mcap ratio and positive momentum.")
print("Alpha Score Breakdown: Volume(25) + Momentum(25) + Acceleration(20) + Liquidity(15) + Market Efficiency(15)")
print('='*80)