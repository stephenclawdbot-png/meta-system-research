#!/usr/bin/env python3

import requests
import json
from datetime import datetime

def scan_memecoins_relaxed():
    """Scan DexScreener for memecoins with relaxed filters"""
    
    # Search for Solana tokens with recent activity
    url = "https://api.dexscreener.com/latest/dex/search"
    params = {
        "q": "solana",
        "limit": 100
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if "pairs" not in data:
            return "No token data available from DexScreener"
        
        # Filter for memecoins
        tokens = []
        
        for pair in data["pairs"]:
            # Check if it's Solana chain
            if "solana" not in pair.get("chainId", "").lower():
                continue
                
            # Get market cap
            market_cap = pair.get("marketCap", 0)
            
            # Check for reasonable volume
            volume_24h = pair.get("volume", {}).get("h24", 0)
            
            # Check age
            created_at = pair.get("pairCreatedAt", 0)
            age_hours = (datetime.now().timestamp() * 1000 - created_at) / (1000 * 60 * 60) if created_at else 0
            
            # Get transaction activity
            txns = pair.get("txns", {})
            
            token_data = {
                "symbol": pair.get("baseToken", {}).get("symbol", "Unknown"),
                "name": pair.get("baseToken", {}).get("name", "Unknown"),
                "market_cap": market_cap,
                "volume_24h": volume_24h,
                "age_hours": age_hours,
                "price_usd": pair.get("priceUsd", 0),
                "url": pair.get("url", ""),
                "chain": pair.get("chainId", ""),
                "created_at": created_at
            }
            
            tokens.append(token_data)
        
        # Sort by market cap
        tokens.sort(key=lambda x: x["market_cap"], reverse=True)
        
        return tokens
        
    except Exception as e:
        return f"Error scanning DexScreener: {str(e)}"

if __name__ == "__main__":
    result = scan_memecoins_relaxed()
    
    if isinstance(result, str):
        print(result)
    else:
        print(f"🎯 Market Scan Results - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"Found {len(result)} Solana tokens\n")
        
        # Show tokens in different ranges
        ranges = [
            (0, 50000, "Under $50k"),
            (50000, 200000, "$50k-$200k"),
            (200000, 500000, "$200k-$500k"),
            (500000, 1000000, "$500k-$1M")
        ]
        
        for min_cap, max_cap, label in ranges:
            matching_tokens = [t for t in result if min_cap <= t["market_cap"] <= max_cap]
            if matching_tokens:
                print(f"\n{label}:")
                for token in matching_tokens[:5]:
                    print(f"  {token['symbol']} - ${token['market_cap']:,.0f} | {token['age_hours']:.1f}h old | Vol: ${token['volume_24h']:,.0f}")
                    
        # Show newest tokens
        newest_tokens = sorted(result, key=lambda x: x.get("created_at", 0), reverse=True)[:5]
        if newest_tokens:
            print(f"\nNewest Tokens:")
            for token in newest_tokens:
                if token.get("created_at", 0):
                    age_mins = (datetime.now().timestamp() * 1000 - token["created_at"]) / (1000 * 60)
                    print(f"  {token['symbol']} - {age_mins:.0f} min old | MCap: ${token['market_cap']:,.0f}")