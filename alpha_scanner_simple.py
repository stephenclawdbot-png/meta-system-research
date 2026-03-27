import json
import subprocess
from datetime import datetime

search_terms = ['dog', 'cat', 'pepe', 'shib', 'bonk', 'floki', 'elon', 'meme', 'baby', 'wojak']
results = []

for term in search_terms:
    try:
        cmd = f'curl -s "https://api.dexscreener.com/latest/dex/search/?q={term}&limit=50"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if 'pairs' in data:
                for pair in data['pairs']:
                    mcap = pair.get('marketCap', 0)
                    if 30000 <= mcap <= 200000:
                        results.append({
                            'symbol': pair['baseToken']['symbol'],
                            'name': pair['baseToken'].get('name', ''),
                            'mcap': mcap,
                            'volume24h': pair.get('volume', {}).get('h24', 0),
                            'priceChange': pair.get('priceChange', {}).get('h24', 0),
                            'chain': pair.get('chainId', ''),
                            'url': pair['url']
                        })
    except Exception as e:
        print(f'Error {term}: {e}')

# Sort by volume descending
results.sort(key=lambda x: x['volume24h'], reverse=True)

print('MEMECOIN ALPHA SCANNER SUMMARY')
print('===============================')
print(f"Time: {datetime.now().strftime('%A, %B %d, %Y — %I:%M %p (Asia/Manila)')}")
print(f'Market Cap Range: $30k-$200k')
print(f'Total Found: {len(results)}')
print('')

for i, token in enumerate(results[:10], 1):
    # Calculate alpha score
    volume_score = min(token['volume24h'] / max(token['mcap'], 1) * 100, 100) if token['mcap'] > 0 else 0
    momentum_score = min(abs(token['priceChange'] or 0) * 5, 100) if (token['priceChange'] or 0) > 0 else 0
    alpha_score = (volume_score * 0.6) + (momentum_score * 0.4)
    
    print(f'{i}. {token["symbol"]} ({token["name"]})')
    print(f'   💰 MCap: ${token["mcap"]:,} | 📊 Vol24h: ${token["volume24h"]:.0f}')
    print(f'   📈 Change: {token["priceChange"] or 0}% | 🔗 Chain: {token["chain"]}')
    print(f'   🔥 Alpha Score: {alpha_score:.1f}/100 | Vol/MCap: {volume_score:.1f}%')
    print(f'   🌐 {token["url"]}')
    print('')