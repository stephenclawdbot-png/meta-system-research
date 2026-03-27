#!/bin/bash
# Install Stephen Discord Bot as a LaunchAgent service

PLIST_NAME="com.stephen.discord.plist"
PLIST_PATH="$HOME/Library/LaunchAgents/$PLIST_NAME"
BOT_DIR="$HOME/.openclaw/workspace/bots/discord-stephen"

echo "🦞 Installing Stephen Discord Bot as a service..."

# Check if token is set
if [ ! -f "$BOT_DIR/.env" ]; then
    echo "❌ .env file not found. Create it first with your token."
    exit 1
fi

# Create LaunchAgents directory if needed
mkdir -p "$HOME/Library/LaunchAgents"

# Create the plist file
cat > "$PLIST_PATH" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.stephen.discord</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>$BOT_DIR/venv/bin/python3</string>
        <string>$BOT_DIR/bot.py</string>
    </array>
    
    <key>WorkingDirectory</key>
    <string>$BOT_DIR</string>
    
    <key>EnvironmentVariables</key>
    <dict>
        <key>DISCORD_STEPHEN_TOKEN</key>
        <string>6db046e48c2bb08363463541581b20399f69d69f5072e42ac9c18bb956ce9b1b</string>
        <key>PYTHONPATH</key>
        <string>$BOT_DIR/venv/lib/python3.x/site-packages</string>
    </dict>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>KeepAlive</key>
    <true/>
    
    <key>StandardOutPath</key>
    <string>/tmp/stephen-discord.log</string>
    
    <key>StandardErrorPath</key>
    <string>/tmp/stephen-discord.error.log</string>
</dict>
</plist>
EOF

# Load the service
launchctl load "$PLIST_PATH"

echo "✅ Stephen Discord Bot installed as a service!"
echo ""
echo "The bot will:"
echo "  • Start automatically on boot"
echo "  • Restart if it crashes"
echo "  • Log to /tmp/stephen-discord.log"
echo ""
echo "Commands:"
echo "  launchctl start com.stephen.discord    # Start manually"
echo "  launchctl stop com.stephen.discord     # Stop"
echo "  launchctl unload $PLIST_PATH  # Uninstall"
echo ""
echo "View logs:"
echo "  tail -f /tmp/stephen-discord.log"