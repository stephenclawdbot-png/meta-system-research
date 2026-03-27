#!/usr/bin/env python3
import requests
import json
from datetime import datetime

def fetch_memecoins():
    searches = ['dog', 'cat', 'meme', 'ai', 'pepe', 'wif', 'bonk', 'elon', 'doge']
    all_tokens = []
    
    for search_term in searches:
        url = f'https://api.dexscreener.com/latest/dex/search?q={search_term}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if not data or 'pairs' not in data:
                continue
            
            for token in data.get('pairs', []):
                mcap = token.get('fdv', 0)
                if 30000 <= mcap <= 200000:
                    token_info = {
                        'name': token.get('baseToken', {}).get('name', 'Unknown'),
                        'symbol': token.get('baseToken', {}).get('symbol', 'Unknown'),
                        'mcap': mcap,
                        'volume_24h': token.get('volume', {}).get('h24', 0),
                        'price': token.get('priceUsd', 0),
                        'price_change_24h': token.get('priceChange', {}).get('h24', 0),
                        'url': token.get('url', ''),
                        'dex': token.get('dexId', ''),
                        'chain': token.get('chainId', '')
                    }
                    
                    # Calculate alpha score
                    vol_mcap_ratio = (token_info['volume_24h'] / token_info['mcap']) * 100 if token_info['mcap'] > 0 else 0
                    momentum = max(0, token_info['price_change_24h']) if token_info['price_change_24h'] else 0
                    alpha_score = min(100, (vol_mcap_ratio * 0.6) + (momentum * 0.3) + (min(100, token_info['volume_24h'] / 1000) * 0.1))
                    token_info['alpha_score'] = round(alpha_score, 1)
                    
                    if alpha_score >= 30:  # Only keep high alpha gems
                        all_tokens.append(token_info)
                        
        except Exception:
            continue
    
    return all_tokens

def main():
    tokens = fetch_memecoins()
    tokens.sort(key=lambda x: x['alpha_score'], reverse=True)
    
    print(f'🔥 HIGHEST ALPHA GEMS (30+ SCORE)')
    print('='*60)
    print(f"Scan Time: {datetime.now().strftime('%A, %B %d, %Y — %I:%M %p (GMT+8)')}")
    print('Target Range: $30k - $200k Market Cap')
    print()
    
    for i, token in enumerate(tokens[:5], 1):
        vol_mcap_ratio = (token['volume_24h'] / token['mcap']) * 100 if token['mcap'] > 0 else 0
        print(f'🎯 #{i} {token["symbol"]} - Alpha Score: {token["alpha_score"]}/100')
        print(f'💎 MCap: ${token["mcap"]:,} | Vol: ${token["volume_24h"]:,}')
        print(f'📈 24h Change: {token["price_change_24h"]:.1f}%')
        print(f'🔥 Vol/MCap Ratio: {vol_mcap_ratio:.1f}%')
        print(f'🌐 Dex: {token["dex"]} | Chain: {token["chain"]}')
        print(f'🔗 {token["url"]}')
        print()
        
    if not tokens:
        print('❌ No high alpha gems found (score ≥ 30)')
    
    print('⚠️ DISCLAIMER: High risk memecoin scanning - NFA')

if __name__ == '__main__':
    main()