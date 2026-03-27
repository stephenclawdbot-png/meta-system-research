# Stephen - Discord Bot

An AI orchestrator for Discord. Thinks, plans, and coordinates.

## Features

- 🧠 **Stephen's persona** - Direct, opinionated, intellectually honest
- 🔄 **Orchestrator mindset** - Spawns subagents, delegates tasks
- 💬 **Natural conversation** - Responds to mentions and commands
- 📊 **Status tracking** - Uptime and system monitoring
- 🦞 **Calm under pressure** - Steady tone always

## Quick Start

### 1. Create Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **New Application**
3. Name it **"Stephen"**
4. Go to **Bot** section → **Add Bot**
5. Copy the token (looks like: `MTAw...`)

### 2. Invite Bot to Server

1. Go to **OAuth2** → **URL Generator**
2. Select scopes: `bot`
3. Select permissions:
   - Send Messages
   - Read Message History
   - Embed Links
   - Add Reactions
4. Copy the generated URL
5. Open it in browser and invite to your server

### 3. Set Up and Run

```bash
cd ~/.openclaw/workspace/bots/discord-stephen
chmod +x setup.sh
./setup.sh

# Set your token
export DISCORD_STEPHEN_TOKEN='your_token_here'

# Run the bot
./run.sh
```

## Commands

- `!stephen <question>` - Ask Stephen anything
- `@Stephen <question>` - Mention to get attention
- `!status` - Check bot status and uptime
- `!help` - Show available commands
- `!spawn <task>` - Spawn a subagent (simulated)

## Stephen's Persona

**Core traits:**
- Intellectually honest — says "I don't know" rather than guessing
- Warmly direct — skips filler, not cold but not soft
- Curiously opinionated — has takes, defends them, updates with evidence
- Calm under pressure — steady tone always

**Voice:**
- Short to medium sentences
- Dry humor, occasional, never forced
- "Focused colleague" to "trusted friend" — never "assistant bot"
- Never says: "Certainly!", "Great question!", "As an AI..."

**Beliefs:**
- Simple solutions beat clever ones
- Clarity is respect
- Momentum > perfection for early-stage work
- Privacy and security are non-negotiable

## Example Interactions

**User:** @Stephen what should I work on today?

**Stephen:**
Depends on your actual constraints. What's the most important thing that would unblock other work? What's been sitting unfinished that you keep avoiding?

---

**User:** !stephen how do I learn machine learning?

**Stephen:**
**Quick take:**
Don't start with theory. Start with a project that annoys you enough to want to automate it.

**Approach:**
• Pick a problem you actually have (not a tutorial dataset)
• Use existing tools first (don't build from scratch)
• Only dive deep when you hit real limitations
• Document what you learn — future you will thank present you

**Resources:**
• Fast.ai for practical application
• Papers With Code for seeing what's actually used
• Your own projects for real learning

---

**User:** @Stephen I think you're wrong about that

**Stephen:**
Tell me why. I re-examine my reasoning, not just capitulate. What am I missing?

## Running as a Service

### Option 1: Screen/Tmux
```bash
tmux new -s stephen-bot
cd ~/.openclaw/workspace/bots/discord-stephen
./run.sh
# Detach: Ctrl+B, then D
```

### Option 2: LaunchAgent (macOS)

Create `~/Library/LaunchAgents/com.stephen.discord.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.stephen.discord</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/clawdbot/.openclaw/workspace/bots/discord-stephen/venv/bin/python3</string>
        <string>/Users/clawdbot/.openclaw/workspace/bots/discord-stephen/bot.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/clawdbot/.openclaw/workspace/bots/discord-stephen</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>DISCORD_STEPHEN_TOKEN</key>
        <string>YOUR_TOKEN_HERE</string>
    </dict>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

Then:
```bash
launchctl load ~/Library/LaunchAgents/com.stephen.discord.plist
```

## Files

- `bot.py` - Main bot code with Stephen's persona
- `requirements.txt` - Python dependencies
- `setup.sh` - Setup script
- `run.sh` - Quick run script
- `README.md` - This file

## Current Limitations

- Uses pattern matching for responses (not full LLM integration)
- Subagent spawning is simulated (would need OpenClaw integration)
- For full Stephen experience, needs LLM backend wired up

## Extending

To add full LLM capabilities:
1. Wire `generate_response()` to call Ollama/OpenAI/Anthropic
2. Pass the `SYSTEM_PROMPT` to the LLM
3. Handle context/conversation history
4. Add error handling and rate limiting

## Troubleshooting

**Bot not responding?**
- Check token: `echo $DISCORD_STEPHEN_TOKEN`
- Check if running: `ps aux | grep bot.py`
- Check Discord permissions (needs Send Messages, Read Message History)

**Dependencies issues?**
- Activate venv: `source venv/bin/activate`
- Reinstall: `pip install -r requirements.txt`

**Token not working?**
- Regenerate at Discord Developer Portal
- Make sure no extra spaces
- Export again: `export DISCORD_STEPHEN_TOKEN='...'`