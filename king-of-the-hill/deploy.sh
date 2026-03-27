#!/bin/bash

# King of the Hill Deployment Script
# Usage: ./deploy.sh [devnet|mainnet]

set -e

NETWORK="${1:-devnet}"

echo "🚀 Deploying King of the Hill to $NETWORK..."

# Check prerequisites
command -v anchor >/dev/null 2>&1 || { echo "❌ Anchor CLI not installed"; exit 1; }
command -v solana >/dev/null 2>&1 || { echo "❌ Solana CLI not installed"; exit 1; }

solana config set --url https://api.$NETWORK.solana.com

echo "📦 Building program..."
cd program
anchor build

echo "🚀 Deploying..."
anchor deploy --provider.cluster $NETWORK

echo "📝 Program deployed!"
echo ""
echo "⚠️ IMPORTANT:"
echo "1. Update PROGRAM_ID in app/src/utils/anchorClient.js"
echo "2. Update TOKEN_MINT in app/src/utils/anchorClient.js"
echo "3. Run: cd app && npm install && npm start"
echo ""
echo "🎮 Game is ready to play!"
