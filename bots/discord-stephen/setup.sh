#!/bin/bash
# Setup script for Stephen Discord Bot

echo "🦞 Setting up Stephen Discord Bot..."
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
echo "1. Create a Discord bot at https://discord.com/developers/applications"
echo "2. Copy the bot token"
echo "3. Set the token: export DISCORD_STEPHEN_TOKEN='your_token_here'"
echo "4. Invite bot to your server"
echo "5. Run: python3 bot.py"
echo ""
echo "To create the bot:"
echo "  1. Go to https://discord.com/developers/applications"
echo "  2. Click 'New Application'"
echo "  3. Name it 'Stephen'"
echo "  4. Go to 'Bot' section, click 'Add Bot'"
echo "  5. Copy the token"
echo "  6. Go to 'OAuth2' > 'URL Generator'"
echo "  7. Select 'bot' scope and 'Send Messages', 'Read Message History' permissions"
echo "  8. Copy the URL and open it to invite the bot"