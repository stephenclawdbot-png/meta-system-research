#!/bin/bash

API_KEY="cope_7uc1tj8RAB0a6Ucg5esBAiTud0r3duzhIu99nokxBo0qpQEi"
BASE_URL="https://api.cope.capital"

# Calculate timestamp for last 2 hours
SINCE_TIMESTAMP=$(( $(date +%s) - 7200 ))000

# Check convergence events (parallel buying of same tokens)
echo "🔍 Checking convergence events..."
convergences=$(curl -s "$BASE_URL/v1/convergence?limit=5" -H "Authorization: Bearer $API_KEY")
echo "Recent convergences:"
echo "$convergences" | jq -r '.convergences[]? | "Token: \(.token_symbol) | Wallets: \(.wallets | length) | Max Gain: \(.max_gain_pct)%"' 2>/dev/null || echo "No recent convergences"

# Check what our watchlist is doing
echo -e "\n📊 Watchlist activity (last 2 hours):"
activity=$(curl -s "$BASE_URL/v1/activity?limit=10" -H "Authorization: Bearer $API_KEY")
echo "$activity" | jq -r '.activity[]? | "\(.fomo_handle): \(.action) \(.token_symbol) $\(.usd_amount)"' 2>/dev/null || echo "No recent activity"