#!/bin/bash
"""
CONTINUOUS SCANNER - Runs every 5/15 minutes
Broadcasts alpha finds and crypto trends automatically
"""

while true; do
    echo "🔄 Running Alpha Scanner $(date)"
    result=$(python3 real_time_alpha_scanner.py 2>&1)
    echo "$result"
    
    # Broadcast alpha finds
    if echo "$result" | grep -q "Found.*alpha tokens"; then
        # Extract and format alpha finds
        alpha_msg=$(echo "$result" | grep -A 10 "Found.*alpha tokens" | head -10)
        telegram_msg="💎 ALPHA FOUND!\n$alpha_msg"
        echo "Broadcasting Alpha: $telegram_msg"
        echo "ALPHA_MSG > $telegram_msg"
        
        # Broadcast to Telegram
        echo "💎 MEMECOIN ALPHA DETECTED\n$(echo "$result" | tail -5)" | head -c 4096
    fi
    
    echo "🌊 Running Crypto Trend Scanner $(date)"
    crypto_result=$(python3 crypto_trend_scanner.py 2>&1)
    echo "$crypto_result"
    
    # Broadcast crypto trends (every scan)
    trend_msg=$(echo "$crypto_result" | grep -E "(BITCOIN|ETHEREUM|SOLANA)" | head -5)
    telegram_msg="🌊 CRYPTO MARKET UPDATE\n$trend_msg"
    echo "Broadcasting Crypto: $trend_msg"
    echo "CRYPTO_MSG > $telegram_msg"
    
    echo "💤 Sleeping 5 minutes..."
    sleep 300
    
    # Crypto trends every 15 minutes
    echo "🌊 Running Crypto Trend Scanner $(date)"
    crypto_result=$(python3 crypto_trend_scanner.py 2>&1)
    echo "$crypto_result"
    
    # Broadcast crypto trends
    trend_msg=$(echo "$crypto_result" | grep -E "(BITCOIN|ETHEREUM|SOLANA)" | head -5)
    telegram_msg="🌊 CRYPTO MARKET UPDATE\n$trend_msg"
    echo "Broadcasting Crypto: $trend_msg"
    echo "CRYPTO_MSG > $telegram_msg"
    
    echo "💤 Sleeping 10 minutes..."
    sleep 600
done