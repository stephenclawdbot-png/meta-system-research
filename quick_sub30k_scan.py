import json
import requests
from datetime import datetime

print('🎯 SUB-30K MEMECOIN ALPHA SCAN')
print('Time:', datetime.now().strftime('%A, %B %d, %Y — %I:%M %p (%Z)'))
print()

def search_low_mcap_memes():
    categories = ['doge', 'pepe', 'shib', 'elon', 'bonk', 'floki', 'moon', 'mars', 'gem']
    low_mcap_gems = []
    
    for category in categories:
        try:
            response = requests.get(f'https://api.dexscreener.com/latest/dex/search?q={category}', timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data and 'pairs' in data:
                    for token in data['pairs']:
                        if 'marketCap' in token and token['marketCap'] < 30000:
                            mcap = token['marketCap']
                            volume = token.get('volume', {}).get('h24', 0)
                            txns = token.get('txns', {}).get('h24', {})
                            
                            # Ignore completely dead tokens
                            if txns.get('buys', 0) + txns.get('sells', 0) < 3:
                                continue
                                
                            score = 0
                            # Volume/MCap ratio
                            if mcap > 0:
                                score += min(40, volume / mcap * 100)
                            
                            # Transaction velocity
                            total_txns = txns.get('buys', 0) + txns.get('sells', 0)
                            score += min(20, total_txns / 10)
                            
                            low_mcap_gems.append({
                                'symbol': token.get('baseToken', {}).get('symbol', 'Unknown'),
                                'mcap': mcap,
                                'volume': volume,
                                'txns': total_txns,
                                'score': score,
                                'url': token.get('url')
                            })
        except:
            pass
    
    return sorted(low_mcap_gems, key=lambda x: x['score'], reverse=True)

gems = search_low_mcap_memes()
if gems:
    print(f'💎 Found {len(gems)} sub-30k market cap memecoins:')
    for gem in gems[:15]:
        print(f"{gem['symbol']}: ${gem['mcap']:,} mcap, {gem['txns']} txns, score: {gem['score']:.1f}")
else:
    print('❌ No sub-30k market cap memecoins found with activity')