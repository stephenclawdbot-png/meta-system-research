# Auto-Restart Services (launchd)

Keep Ollama and OpenClaw Gateway running 24/7 with auto-restart.

## Quick Install

```bash
cd ~/.openclaw/workspace/services
chmod +x install-keepalive.sh
./install-keepalive.sh
```

## What It Does

- **Checks every 60 seconds** if Ollama is running
- **Checks every 60 seconds** if OpenClaw Gateway is running
- **Auto-restarts** any service that crashes or stops
- **Starts on boot** — survives restarts

## Logs

```bash
# Watch Ollama keepalive logs
tail -f /tmp/ollama-keepalive.log

# Watch OpenClaw keepalive logs
tail -f /tmp/openclaw-keepalive.log

# Watch error logs
tail -f /tmp/ollama-keepalive.error.log
tail -f /tmp/openclaw-keepalive.error.log
```

## Check Status

```bash
# See if services are loaded
launchctl list | grep -E "(ollama|openclaw)"

# Check specific service
launchctl print gui/$(id - u)/com.ollama.keepalive
launchctl print gui/$(id - u)/com.openclaw.gateway.keepalive
```

## Manual Control

```bash
# Stop monitoring (services keep running)
launchctl stop com.ollama.keepalive
launchctl stop com.openclaw.gateway.keepalive

# Start monitoring again
launchctl start com.ollama.keepalive
launchctl start com.openclaw.gateway.keepalive

# Unload completely
launchctl unload ~/Library/LaunchAgents/com.ollama.keepalive.plist
launchctl unload ~/Library/LaunchAgents/com.openclaw.gateway.keepalive.plist
```

## Uninstall

```bash
cd ~/.openclaw/workspace/services
chmod +x uninstall-keepalive.sh
./uninstall-keepalive.sh
```

## Before You Leave Town

1. **Install the services** (run install script above)
2. **Test it**: Stop Ollama manually, wait 60 seconds, verify it restarts
3. **Check logs** to make sure everything looks good
4. **Leave the Mac mini on** and connected to internet

## Troubleshooting

**Services not starting?**
- Check permissions: `chmod +x install-keepalive.sh`
- Check if plist files were copied: `ls ~/Library/LaunchAgents/`

**Ollama not found?**
- Make sure Ollama is installed: `which ollama`
- Update the path in the plist if needed

**Gateway not restarting?**
- Check OpenClaw is installed: `which openclaw`
- Check logs: `cat /tmp/openclaw-keepalive.error.log`