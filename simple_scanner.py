#!/usr/bin/env python3
import urllib.request
import json
from datetime import datetime

print("🔍 Simplest DexScreener Scanner")
print("=" * 40)

# Actually let me just use curl directly
import subprocess

try:
    print("📡 Testing direct curl to DexScreener...")
    
    # Try trending
    result1 = subprocess.run(['curl', '-s', 'https://api.dexscreener.com/latest/dex/tokens/trending'], 
                           capture_output=True, text=True)
    print(f"Trending API response: {result1.stdout[:200]}...")
    
    # Try Solana tokens
    result2 = subprocess.run(['curl', '-s', 'https://api.dexscreener.com/latest/dex/tokens/solana'], 
                           capture_output=True, text=True)
    print(f"Solana API response: {result2.stdout[:200]}...")
    
    # Try Ethereum tokens
    result3 = subprocess.run(['curl', '-s', 'https://api.dexscreener.com/latest/dex/tokens/ethereum'], 
                           capture_output=True, text=True)
    print(f"Ethereum API response: {result3.stdout[:200]}...")
    
    # Try new tokens
    result4 = subprocess.run(['curl', '-s', 'https://api.dexscreener.com/latest/dex/tokens/new'], 
                           capture_output=True, text=True)
    print(f"New tokens API response: {result4.stdout[:200]}...")

except Exception as e:
    print(f"❌ Error: {e}")