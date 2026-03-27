#!/usr/bin/env python3
import json
from datetime import datetime

print('🧠 MEMECOIN ALPHA SCANNER - COMPREHENSIVE REPORT')
print('='*60)
print('Filter: Market Cap $30,000 - $200,000')
print('Time:', datetime.now().strftime("%A, March %d, %Y — %I:%M %p (%Z)"))
print()

# From the first scan
alpha_results = [
    {
        'symbol': 'TOK', 'name': 'Token', 'mcap': 33068, 'volume': 6940.37,
        'score': 51.7, 'filter_score': 15, 'url': 'https://dexscreener.com/bsc/0xe8c0efb703f23d4e024c4b776784a49d2b9b85f2',
        'change': -2.4, 'buy_ratio': 0.714, 'txns': 486, 'liquidity': 2684.38
    },
    {
        'symbol': 'memecoin', 'name': 'Memecoin', 'mcap': 47854, 'volume': 6956.42,
        'score': 51.5, 'filter_score': 45, 'url': 'https://dexscreener.com/solana/8fyvrgzr6xcas2t5exfccwzjv9us51ttgn5befq4cety',
        'change': 3.0, 'buy_ratio': 0.818, 'txns': 60, 'liquidity': 39631.42
    },
    {
        'symbol': 'Coin', 'name': 'Coin', 'mcap': 42234, 'volume': 4842.12,
        'score': 43.5, 'filter_score': 25, 'url': 'https://dexscreener.com/solana/fjt1dpbreuesu2r1dqfhxfatk9uitwau4bdvnnvm4c4w',
        'change': 3.9, 'buy_ratio': 0.478, 'txns': 167, 'liquidity': 35697.82
    },
    {
        'symbol': 'WSOD', 'name': 'World Series of Degens', 'mcap': 155581, 'volume': 1642.83,
        'score': 40.5, 'filter_score': 25, 'url': 'https://dexscreener.com/solana/dj7hbqokom2yhnbjnvapxlntddrqmxeevesjwijv3r8l',
        'change': 1.6, 'buy_ratio': 1.0, 'txns': 14, 'liquidity': 41532.18
    }
]

# Sort by highest alpha score
alpha_results.sort(key=lambda x: x['score'], reverse=True)

print('🔥 TOP ALPHA GEMS (Alpha Score ≥ 40)')
print('=' * 40)

for i, gem in enumerate(alpha_results, 1):
    print(str(i) + '. 💎 ' + gem['symbol'] + ' - ' + gem['name'])
    print('   ⭐ Alpha Score: ' + str(gem['score']) + '/100')
    print('   📊 Market Cap: ${:,}'.format(gem['mcap']))
    print('   📈 24h Volume: ${:,}'.format(gem['volume']))
    print('   🔥 Volume/MCap Ratio: ' + str(round(gem['volume']/gem['mcap'], 1)) + 'x')
    print('   📊 1h Change: ' + str(gem['change']) + '%')
    print('   🔄 Buy Ratio: {:.1%}'.format(gem['buy_ratio']))
    print('   💧 Transactions 24h: ' + str(gem['txns']))
    print('   🏦 Liquidity: ${:,}'.format(gem['liquidity']))
    print('   🌐 Filter Score: ' + str(gem['filter_score']) + '/100')
    print('   🔗 ' + gem['url'])
    print()

# Market summary
print('📈 MARKET SUMMARY')
print('=' * 25)
print('• Total Alpha Gems Found: ' + str(len(alpha_results)))
market_status = 'Yes' if len(alpha_results) > 0 else 'No'
print('• Active Market: ' + market_status)
volume_text = alpha_results[0]['symbol'] + ' ($' + str('{:,}'.format(alpha_results[0]['volume'])) + ')'
print('• Volume Leaders: ' + volume_text)
score_text = alpha_results[0]['symbol'] + ' (' + str(alpha_results[0]['score']) + ')'
print('• Best Alpha Score: ' + score_text)

print()
print('⚠️ DISCLAIMER: This is alpha detection only - DYOR')
print('High-risk assets - only invest what you can afford to lose')