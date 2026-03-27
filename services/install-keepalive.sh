#!/bin/bash
# Install keepalive services for Ollama and OpenClaw Gateway
# Run this before you leave town

echo "Installing keepalive services..."

# Create LaunchAgents directory if it doesn't exist
mkdir -p ~/Library/LaunchAgents

# Copy plist files
cp com.ollama.keepalive.plist ~/Library/LaunchAgents/
cp com.openclaw.gateway.keepalive.plist ~/Library/LaunchAgents/

# Load the services
launchctl load ~/Library/LaunchAgents/com.ollama.keepalive.plist
launchctl load ~/Library/LaunchAgents/com.openclaw.gateway.keepalive.plist

# Start them now
launchctl start com.ollama.keepalive
launchctl start com.openclaw.gateway.keepalive

echo "✅ Services installed and started"
echo ""
echo "They will:"
echo "- Check every 60 seconds if Ollama is running"
echo "- Check every 60 seconds if OpenClaw Gateway is running"
echo "- Auto-restart if either service goes down"
echo "- Start automatically on boot"
echo ""
echo "Logs:"
echo "  Ollama: /tmp/ollama-keepalive.log"
echo "  OpenClaw: /tmp/openclaw-keepalive.log"

# Show status
echo ""
echo "Current status:"
launchctl list | grep -E "(ollama|openclaw)"