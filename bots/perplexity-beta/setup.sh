#!/bin/bash
# Setup script for Perplexity Beta Bot

echo "🤖 Setting up Perplexity Beta Bot..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Create a bot via @BotFather on Telegram"
echo "2. Copy the bot token"
echo "3. Set the token: export PERPLEXITY_BOT_TOKEN='your_token_here'"
echo "4. Run the bot: python3 bot.py"
echo ""
echo "To create the bot:"
echo "  1. Open Telegram and message @BotFather"
echo "  2. Send /newbot"
echo "  3. Name it 'Perplexity Beta'"
echo "  4. Choose username like 'perplexity_beta_bot'"
echo "  5. Copy the token and set it as PERPLEXITY_BOT_TOKEN"