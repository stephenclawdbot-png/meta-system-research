#!/usr/bin/env python3
import requests

url = 'https://api.dexscreener.com/latest/dex/search?q=solana'
response = requests.get(url, timeout=10)
data = response.json()

print('Total pairs:', len(data['pairs']))

# Check all chains present
chains = set()
for pair in data['pairs']:
    chain = pair.get('chainId', 'unknown')
    chains.add(chain)

print('Chains found:', chains)

# Show first few pairs by chain
for chain in chains:
    chain_pairs = [p for p in data['pairs'] if p.get('chainId') == chain]
    print(f'\n{chain} pairs ({len(chain_pairs)}):')
    for i, pair in enumerate(chain_pairs[:3]):
        base_token = pair.get('baseToken', {})
        print(f'  {i+1}. {base_token.get("symbol", "N/A")} - MCap: ${pair.get("fdv", 0):,}')