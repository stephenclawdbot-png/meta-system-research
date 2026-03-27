#!/bin/bash
# Quick run script for Perplexity Beta Bot

cd "$(dirname "$0")"

# Check if token is set
if [ -z "$PERPLEXITY_BOT_TOKEN" ]; then
    echo "❌ PERPLEXITY_BOT_TOKEN not set!"
    echo ""
    echo "Set it with:"
    echo "  export PERPLEXITY_BOT_TOKEN='your_token_here'"
    echo ""
    echo "Or add to ~/.zshrc:"
    echo "  echo 'export PERPLEXITY_BOT_TOKEN=\"your_token_here\"' >> ~/.zshrc"
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
echo "🤖 Starting Perplexity Beta Bot..."
python3 bot.py