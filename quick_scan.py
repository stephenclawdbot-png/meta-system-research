#!/usr/bin/env python3
import requests
from datetime import datetime

print('📡 DexScreener Memecoin Alpha Scan')
print('==================================')
print('Scan Time:', datetime.now().strftime('%A, %B %d, %Y — %I:%M %p (Asia/Manila)'))
print('Target MCAP Range: $30,000 - $200,000')
print()

try:
    response = requests.get('https://api.dexscreener.com/latest/dex/tokens/trending', timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        trending_tokens = data.get('pairs', [])
        
        memecoins_in_range = []
        
        for token in trending_tokens:
            mcap = token.get('marketCap', 0)
            symbol = token.get('baseToken', {}).get('symbol', 'Unknown')
            
            if 30000 <= mcap <= 200000:
                memecoins_in_range.append(token)
        
        memecoins_in_range.sort(key=lambda x: x.get('volume', {}).get('h24', 0), reverse=True)
        
        print(f'💰 Found {len(memecoins_in_range)} tokens in target range\n')
        
        if memecoins_in_range:
            print('🔥 TOP ALPHA GEMS:')
            print('--------------------------------------------------')
            
            for i, token in enumerate(memecoins_in_range[:8], 1):
                symbol = token.get('baseToken', {}).get('symbol', 'Unknown')
                mcap = token.get('marketCap', 0)
                volume_24h = token.get('volume', {}).get('h24', 0)
                price_change = token.get('priceChange', {}).get('h24', 0)
                liquidity = token.get('liquidity', {}).get('usd', 0)
                txns_24h = token.get('txns', {}).get('h24', {})
                buys = txns_24h.get('buys', 0)
                sells = txns_24h.get('sells', 0)
                total_txns = buys + sells
                buy_ratio = buys / total_txns if total_txns > 0 else 0
                
                vol_mcap_ratio = (volume_24h / mcap) * 100 if mcap > 0 else 0
                
                print(f'{i}. {symbol}')
                print(f'   MCAP: ${mcap:,} | Vol: ${volume_24h:,} ({vol_mcap_ratio:.1f}%)')
                print(f'   Price: {price_change:+.1f}% | Buys: {buy_ratio:.1%}')
                print(f'   Txns: {total_txns} ({buys}B/{sells}S) | Liquid: ${liquidity:}')
                print()
                
        else:
            print('📭 No trending memecoins found in the target range')
            
    else:
        print(f'❌ API Error: {response.status_code}')
        
except Exception as e:
    print(f'❌ Connection Error: {e}')
    print('\n⚠️ Using cached analysis from last successful scan')
    print('Check cron_memecoin_alpha_report_current.txt for recent data')