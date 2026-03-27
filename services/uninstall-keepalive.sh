#!/bin/bash
# Uninstall keepalive services

echo "Uninstalling keepalive services..."

# Unload services
launchctl unload ~/Library/LaunchAgents/com.ollama.keepalive.plist 2>/dev/null
launchctl unload ~/Library/LaunchAgents/com.openclaw.gateway.keepalive.plist 2>/dev/null

# Remove plist files
rm -f ~/Library/LaunchAgents/com.ollama.keepalive.plist
rm -f ~/Library/LaunchAgents/com.openclaw.gateway.keepalive.plist

echo "✅ Services uninstalled"

# Show status
echo ""
echo "Remaining services:"
launchctl list | grep -E "(ollama|openclaw)" || echo "None"