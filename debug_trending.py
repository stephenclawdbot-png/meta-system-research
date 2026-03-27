#!/usr/bin/env python3
import requests

print('🔍 DEBUG TRENDING TOKENS')
print('='*30)
print()

# Fetch trending memecoins
response = requests.get('https://api.dexscreener.com/latest/dex/tokens/trending')
print('Status Code:', response.status_code)
print('Response Headers:', response.headers)

try:
    data = response.json()
    print('Response Keys:', data.keys() if data else 'Empty response')
    if data and 'pairs' in data:
        print('Number of pairs:', len(data['pairs']))
        if data['pairs']:
            first_token = data['pairs'][0]
            print('First token keys:', first_token.keys())
    else:
        print('No pairs found')
except Exception as e:
    print('JSON Error:', e)
    print('Raw response text:', response.text[:500])