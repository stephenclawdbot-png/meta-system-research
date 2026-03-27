#!/usr/bin/env python3
import re
import sys

data = """24H Volume:
$22.56B

24H Txns:
37,516,814

Trending
https://docs.dexscreener.com/trending
[#1house/SOLwhat's inside that house 50$0.0021751d56,020$4.8M8,991-4.96%-27.79%217%1,312%$134K$2.1M](/solana/dmzalghgnhbqjjnpks7gr2wrnzm2o54pasdlkbx5d2kr)[#2Punch/SOLパンチ 50$0.0116211d69,570$9.5M10,3403.95%11.19%-13.59%-30.06%$374K$11.6M](/solana/a6khmifzn9am7vkbtvp4fzny9bco2jp63r9dphaw1vrq)[#3MOG/SOLMog Coin 100$0.000512616h40,787$2.3M7,8347.53%117%-26.26%1,328%$62K$512K](/solana/9twd2us5bx5swevkjbfcwk9uhv57mh61sza2e8osh3nv)[#4MUSHU/SOLMushu$0.029471y41,985$6.8M3,9152.29%6.83%74.55%107%$476K$24.8M](/solana/hxh2wp1nq2ico2rv5hqzmcirh7tvjsgwykchy8zjbbr7)[#5丙午/SOLbǐngwǔ 500$0.0013901mo64,704$351K14,584-0.93%-3.72%-15.48%-11.45%$127K$1.3M](/solana/2y8qhdp4zox3mtkijnpcqifqunchde69lkzntyvfjeqg)[#6NOBODY/SOLa nobody$0.0494486h19,800$2.1M3,623-7.61%-51.07%-71.72%165%$26K$94K](/solana/gmgkxdmqwxvplf1vc77ss3szpyni4td4185wwra9nwru)[#7Jellycat/SOLJellycat 10$0.000480620h68,373$3.9M21,324-8.52%7.82%-1.24%1,226%$61K$480K](/solana/5bhphfpnbojjsfndaou2b3httb8nspntvzyxdaxwecbr)[#8SmokinCrow/SOLCrow with cigarette 100$0.00068789h31,046$805K4,11018.53%-0.99%175%1,817%$66K$687K](/solana/aeecjn71skryekyvkqo1uw4z78zgrgwy5hlaabqbrd7u)[#9Dreamcore/SOLDreamcore$0.00011922h17,708$778K3,430-21.18%28.01%238%238%$28K$117K](/solana/czdjho2yivz1z9ldpix9q4rvpsiu8hjzwxoy5n19yhnp)[#10LABUBU/SOLLABUBU$0.0022071y10,325$1.5M1,3477.29%16.86%110%256%$522K$2.2M](/solana/fyanfcdjkcfakbtzqixntqnvlodjjft82l5ffgpaswe3)"""

# Extract token entries
pattern = r'\[#\d+([^\]]+)\]\([^\)]+\)'
entries = re.findall(pattern, data)

def parse_token_data(text):
    """Parse token data from DexScreener format"""
    # Extract components: name, price, age, volume, mcap
    parts = text.split('$')
    if len(parts) < 3:
        return None
    
    # First part contains name info
    name_part = parts[0]
    # Price is second part
    price = parts[1].split()[0] if parts[1] else None
    # Age and volume/mcap info in subsequent parts
    
    # Extract market cap and volume using regex
    mcap_match = re.search(r'([\d\.]+[KM])\s*(?:[\d,]*)%.*?\$(\d+[KM])', text)
    if mcap_match:
        mcap = mcap_match.group(1)
        volume = mcap_match.group(2)
    else:
        # Fallback: look for $XK or $XM patterns
        mcap_matches = re.findall(r'\$(\d+[\.\d]*[KM])', text)
        if len(mcap_matches) >= 2:
            volume = mcap_matches[0]
            mcap = mcap_matches[1]
        else:
            return None
    
    # Extract name - look for pattern like "something/SOLsomething"
    name_match = re.search(r'([^/]+)/SOL([^$]+)', name_part)
    if name_match:
        ticker = name_match.group(1)
        name = name_match.group(2).strip()
    else:
        # Fallback: extract from beginning
        parts_before_sol = name_part.split('/SOL')
        if len(parts_before_sol) > 1:
            ticker = parts_before_sol[0]
            name = parts_before_sol[1]
        else:
            ticker = name_part[:20]
            name = name_part
    
    # Clean up name
    name = re.sub(r'^\d+', '', name).strip()
    
    return {
        'ticker': ticker.strip(),
        'name': name,
        'price': price,
        'market_cap': mcap,
        'volume': volume
    }

# Parse all tokens
tokens = []
for entry in entries:
    token_data = parse_token_data(entry)
    if token_data:
        tokens.append(token_data)

# Filter for sub 30k-200k market cap
def mcap_to_num(mcap_str):
    """Convert $XK/$XM to numeric"""
    if not mcap_str:
        return 0
    mcap_str = mcap_str.replace('$', '')
    if 'K' in mcap_str:
        return float(mcap_str.replace('K', '')) * 1000
    elif 'M' in mcap_str:
        return float(mcap_str.replace('M', '')) * 1000000
    else:
        return float(mcap_str)

filtered_tokens = []
for token in tokens:
    mcap_num = mcap_to_num(token['market_cap'])
    if 30000 <= mcap_num <= 200000:
        filtered_tokens.append(token)

# Sort by market cap
filtered_tokens.sort(key=lambda x: mcap_to_num(x['market_cap']))

print(f"Total tokens parsed: {len(tokens)}")
print(f"Filtered tokens (30k-200k mcap): {len(filtered_tokens)}")
print("\nAlpha Candidates:")
print("-" * 60)

for token in filtered_tokens:
    print(f"Ticker: {token['ticker']}")
    print(f"Name: {token['name']}")
    print(f"Price: ${token['price']}")
    print(f"Market Cap: ${token['market_cap']}")
    print(f"Volume: ${token['volume']}")
    print("-" * 40)