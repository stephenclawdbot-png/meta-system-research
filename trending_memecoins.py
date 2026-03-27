#!/usr/bin/env python3

import requests
import json
from datetime import datetime

def get_trending_memecoins():
    """Get trending tokens that might be memecoins"""
    
    # Try different search terms
    search_terms = ["new", "meme", "coin", "dog", "cat", "ai", "pepe"]
    
    all_results = []
    
    for term in search_terms:
        url = "https://api.dexscreener.com/latest/dex/search"
        params = {"q": term, "limit": 20}
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            if "pairs" in data:
                for pair in data["pairs"]:
                    # Only include Solana tokens
                    if "solana" not in pair.get("chainId", "").lower():
                        continue
                        
                    market_cap = pair.get("marketCap", 0)
                    volume_24h = pair.get("volume", {}).get("h24", 0)
                    
                    # Check if it might be a memecoin (low market cap, recent creation)
                    created_at = pair.get("pairCreatedAt", 0)
                    age_hours = (datetime.now().timestamp() * 1000 - created_at) / (1000 * 60 * 60) if created_at else 0
                    
                    token_data = {
                        "symbol": pair.get("baseToken", {}).get("symbol", "Unknown"),
                        "name": pair.get("baseToken", {}).get("name", "Unknown"),
                        "market_cap": market_cap,
                        "volume_24h": volume_24h,
                        "age_hours": age_hours,
                        "price_usd": pair.get("priceUsd", 0),
                        "url": pair.get("url", ""),
                        "search_term": term,
                        "chain": pair.get("chainId", "")
                    }
                    
                    all_results.append(token_data)
        except Exception as e:
            print(f"Error searching for '{term}': {e}")
    
    # Remove duplicates by symbol
    unique_results = {}
    for result in all_results:
        symbol = result["symbol"]
        if symbol not in unique_results or result["age_hours"] < unique_results[symbol]["age_hours"]:
            unique_results[symbol] = result
    
    # Sort by market cap
    sorted_results = sorted(unique_results.values(), key=lambda x: x["market_cap"])
    
    return sorted_results

if __name__ == "__main__":
    results = get_trending_memecoins()
    
    print(f"🎯 Memecoin Scan Results - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Found {len(results)} unique Solana tokens\n")
    
    # Filter for tokens that could be interesting (low market cap, reasonable volume)
    promising_tokens = []
    
    for token in results:
        # Skip SOL itself and other major tokens
        if token["symbol"] == "SOL":
            continue
            
        # Show tokens under $1M market cap
        if token["market_cap"] < 1000000:
            promising_tokens.append(token)
    
    if promising_tokens:
        print("Promising Memecoins:")
        for token in promising_tokens[:15]:  # Top 15
            symbol_display = token["symbol"] if len(token["symbol"]) <= 10 else token["symbol"][:10] + "..."
            name_display = token["name"] if len(token["name"]) <= 20 else token["name"][:20] + "..."
            
            print(f"  {symbol_display:10} ({name_display:20})")
            print(f"    MCap: ${token['market_cap']:,.0f}")
            print(f"    Vol: ${token['volume_24h']:,.0f}")
            print(f"    Age: {token['age_hours']:.1f}h")
            if token['search_term']:
                print(f"    Found via: {token['search_term']}")
            print(f"    Link: {token['url']}")
            print()
    else:
        print("No promising memecoins found in the current scan.")
        print("This could mean:")
        print("- No new memecoins launched recently")
        print("- API search terms not matching current trends")
        print("- Market calm period")