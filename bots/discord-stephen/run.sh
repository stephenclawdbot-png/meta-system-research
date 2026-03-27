#!/bin/bash
# Quick run script for Stephen Discord Bot

cd "$(dirname "$0")"

# Check if token is set
if [ -z "$DISCORD_STEPHEN_TOKEN" ]; then
    echo "❌ DISCORD_STEPHEN_TOKEN not set!"
    echo ""
    echo "Set it with:"
    echo "  export DISCORD_STEPHEN_TOKEN='your_token_here'"
    echo ""
    echo "Or add to ~/.zshrc:"
    echo "  echo 'export DISCORD_STEPHEN_TOKEN=\"your_token_here\"' >> ~/.zshrc"
    exit 1
fi

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ Virtual environment not found. Run ./setup.sh first."
    exit 1
fi

# Run the bot
echo "🦞 Starting Stephen..."
python3 bot.py