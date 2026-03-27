#!/bin/bash
# Alpha Scanner Test Script

ALPHA_API="http://localhost:3111"

# Check if scanner is running
echo "🧪 Testing Alpha Scanner connectivity..."
status_response=$(curl -s "$ALPHA_API/api/status")

if [ $? -ne 0 ]; then
    echo "❌ Alpha Scanner not responding at $ALPHA_API"
    echo "Make sure the service is running on port 3111"
    exit 1
fi

echo "✅ Alpha Scanner is running"
echo "🎯 Service Status:"
echo "$status_response" | jq .

# Get some gems
echo ""
echo "💎 Fetching top 3 alpha gems..."
gems_response=$(curl -s "$ALPHA_API/api/gems?limit=3")
if [ $? -eq 0 ]; then
    echo "$gems_response" | jq '.[] | {ticker: .ticker, score: .alphaScore, mcap: .mcap, volume: .volume24h}'
else
    echo "❌ Failed to fetch gems"
fi