#!/usr/bin/env python3
import requests
import json
from datetime import datetime

# Search for actual memecoins - expanded list
queries = ['memecoin', 'dog', 'cat', 'moon', 'mars', 'elon', 'pepe', 'floki', 'bonk', 'wif', 'tremp', 'zaki', 'osak', 'maga', 'turbo', 'myro', 'boden', 'mog', 'chad', 'baby', 'satoshi', 'doge', 'kitty', 'pig', 'bull', 'bear', 'pump', 'gems', 'rocket', 'animal', 'crypto', 'diamond']
all_tokens = []

for query in queries:
    try:
        response = requests.get(f'https://api.dexscreener.com/latest/dex/search?q={query}&limit=30', timeout=15)
        if response.status_code == 200:
            data = response.json()
            if data and 'pairs' in data:
                tokens = data['pairs']
                # Filter by mcap range and exclude generic/non-memecoin tokens
                filtered = []
                generic_names = ['bitcoin', 'ethereum', 'solana', 'bnb', 'matic', 'avax', 'arb', 'op']
                
                # Additional filtering for stronger alpha signals
                for token in tokens:
                    mcap = token.get('fdv', token.get('marketCap', 0))
                    name = token.get('baseToken', {}).get('name', '').lower()
                    symbol = token.get('baseToken', {}).get('symbol', '').lower()
                    vol = token.get('volume', {}).get('h24', 0)
                    txns = token.get('txns', {}).get('h24', {}).get('buys', 0) + token.get('txns', {}).get('h24', {}).get('sells', 0)
                    
                    # Broader criteria for alpha signals
                    if (30000 <= mcap <= 200000 and  # Original range
                        vol >= 500 and  # Lower volume threshold
                        vol/mcap >= 0.05 and  # Volume/Mcap ratio > 5%
                        txns >= 10 and  # Lower transaction threshold
                        name not in generic_names and
                        symbol not in generic_names and
                        len(name) > 2 and
                        'stable' not in name.lower() and
                        'usd' not in name.lower()):
                        filtered.append(token)
                all_tokens.extend(filtered)
    except Exception as e:
        pass

print('🐶 MEMECOIN ALPHA SCANNER - LIVE SCAN')
print('=' * 55)
print(f'Scan Time: {datetime.now().strftime("%A, March %d, %Y — %I:%M %p (Asia/Manila)")}')
print('Market Cap Range: $30k - $200k')
print()

if not all_tokens:
    print('❌ No specific memecoins found in target range')
else:
    # Enhanced deduplication and filtering
    seen_addresses = set()
    unique_tokens_enhanced = []
    
    for token in all_tokens:
        addr = token.get('pairAddress', '')
        if addr and addr not in seen_addresses:
            seen_addresses.add(addr)
            
            mcap = token.get('fdv', token.get('marketCap', 0))
            vol = token.get('volume', {}).get('h24', 0)
            ratio = vol / mcap * 100 if mcap > 0 else 0
            
            # Filter out suspicious tokens (likely bot manipulation)
            if ratio < 5000:  # Remove tokens with >5000% vol/mcap
                unique_tokens_enhanced.append(token)
    
    # Score all tokens and sort by alpha score
    scored_tokens = []
    for token in unique_tokens_enhanced:
        mcap = token.get('fdv', 0)
        vol = token.get('volume', {}).get('h24', 0)
        change = token.get('priceChange', {}).get('h24', 0)
        symbol = token.get('baseToken', {}).get('symbol', '??')
        name = token.get('baseToken', {}).get('name', 'Unknown')
        ratio = vol / mcap * 100 if mcap > 0 else 0
        
        # Get transaction data
        try:
            txns_url = f"https://api.dexscreener.com/latest/dex/tokens/{token.get('baseToken', {}).get('address', '')}"
            txn_response = requests.get(txns_url, timeout=5)
            if txn_response.status_code == 200:
                txn_data = txn_response.json()
                buy_txns = txn_data.get('pairs', [{}])[0].get('txns', {}).get('h24', {}).get('buys', 0)
                sell_txns = txn_data.get('pairs', [{}])[0].get('txns', {}).get('h24', {}).get('sells', 0)
                total_txns = buy_txns + sell_txns
                buy_ratio = (buy_txns / total_txns * 100) if total_txns > 0 else 50
            else:
                buy_txns = sell_txns = total_txns = 0
                buy_ratio = 50
        except:
            buy_txns = sell_txns = total_txns = 0
            buy_ratio = 50
        
        # Enhanced Alpha Score
        ratio_score = min(40, ratio * 0.8) if ratio > 0 else 0
        vol_score = min(20, vol / 5000)
        growth_score = min(15, max(0, change) * 0.3)
        buy_pressure_score = min(15, buy_ratio * 0.15)
        txn_velocity_score = min(10, total_txns / 100)
        
        alpha_score = min(100, ratio_score + vol_score + growth_score + buy_pressure_score + txn_velocity_score)
        
        scored_tokens.append({
            'token': token,
            'alpha_score': alpha_score,
            'buy_txns': buy_txns,
            'sell_txns': sell_txns,
            'total_txns': total_txns,
            'buy_ratio': buy_ratio
        })
    
    # Sort by alpha score
    scored_tokens.sort(key=lambda x: x['alpha_score'], reverse=True)
    
    # Take top tokens with reasonable metrics
    top_scored_tokens = []
    for token_data in scored_tokens:
        token = token_data['token']
        name = token.get('baseToken', {}).get('name', '').lower()
        symbol = token.get('baseToken', {}).get('symbol', '').lower()
        
        # Skip suspicious/repetitive names
        if len(set([name, symbol])) > len(set([name])):  # Different name/symbol
            top_scored_tokens.append(token_data)
        
        if len(top_scored_tokens) >= 7:
            break
    
    # Fallback if we don't have enough
    if len(top_scored_tokens) < 3:
        top_scored_tokens = scored_tokens[:7]
    
    top_tokens = [item['token'] for item in top_scored_tokens]
    
    print(f'💎 TOTAL GEMS FOUND: {len(unique_tokens_enhanced)} tokens')
    print('-' * 30)
    
    for i, token_data in enumerate(top_scored_tokens, 1):
        token = token_data['token']
        mcap = token.get('fdv', 0)
        vol = token.get('volume', {}).get('h24', 0)
        change = token.get('priceChange', {}).get('h24', 0)
        symbol = token.get('baseToken', {}).get('symbol', '??')
        name = token.get('baseToken', {}).get('name', 'Unknown')
        ratio = vol / mcap * 100 if mcap > 0 else 0
        
        # Use pre-calculated transaction data
        buy_txns = token_data['buy_txns']
        sell_txns = token_data['sell_txns']
        total_txns = token_data['total_txns']
        buy_ratio = token_data['buy_ratio']
        alpha_score = token_data['alpha_score']
        
        print(f'🎯 #{i} {symbol} ({name}) - Alpha: {alpha_score:.0f}/100')
        print(f'   💰 MCap: ${mcap:,.0f} | Vol: ${vol:,.0f}')
        print(f'   📈 24h Change: {change:+.1f}% | Txns: {total_txns}')
        print(f'   🤝 Buys/Sells: {buy_txns}/{sell_txns} ({buy_ratio:.1f}% buy ratio)')
        print(f'   🔥 Vol/MCap: {ratio:.1f}% (key alpha signal)')
        print(f'   🔗 {token.get("url", "")}')
        print()
    
    # Summary
    print('📊 MARKET INSIGHTS:')
    print('-' * 25)
    avg_ratio = sum(t.get('volume', {}).get('h24', 0) / max(1, t.get('fdv', 0)) * 100 for t in top_tokens if t.get('fdv', 0) > 0) / len(top_tokens)
    print(f'• Average Vol/MCap Ratio: {avg_ratio:.1f}%')
    print('• TARGET: Ratio > 25% = Strong alpha signal')
    print('• High ratio indicates efficient market capitalization')
    print()
    print('⚠️ DISCLAIMER: Extreme risk - DYOR required')