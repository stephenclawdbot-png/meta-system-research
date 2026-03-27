# Perplexity Beta Bot for Telegram

An AI-powered Telegram bot that mimics Perplexity's search-first approach with source citations.

## Features

- 🔍 **Real-time web search** for current information
- 📚 **Source citations** on every factual answer
- 🧠 **Concise, direct responses** - no fluff
- ⚡ **Beta mode** - experimental features
- 💬 **Natural conversation** with follow-up suggestions

## Quick Start

### 1. Create the Bot

Message [@BotFather](https://t.me/BotFather) on Telegram:

```
/newbot
Perplexity Beta
perplexity_beta_bot (or your preferred username)
```

Copy the bot token (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 2. Set Up Environment

```bash
cd ~/.openclaw/workspace/bots/perplexity-beta
chmod +x setup.sh
./setup.sh
```

### 3. Configure Token

```bash
export PERPLEXITY_BOT_TOKEN='your_token_here'
```

Add to your `~/.zshrc` or `~/.bashrc` to make it permanent:
```bash
echo 'export PERPLEXITY_BOT_TOKEN="your_token_here"' >> ~/.zshrc
```

### 4. Run the Bot

```bash
source venv/bin/activate
python3 bot.py
```

## Bot Commands

- `/start` - Welcome message with beta features
- `/help` - Show available commands
- `/clear` - Clear conversation context
- `/feedback` - Send feedback about beta features

## Persona

The bot acts as **Perplexity Beta** - an AI assistant with:
- Search-first mindset
- Source citations on every claim
- Concise, bullet-point formatting
- Beta-specific language ("experimental", "beta mode")
- Professional but accessible tone

## Example Interactions

**User:** What's the weather in Tokyo?

**Bot:**
Currently 18°C and partly cloudy in Tokyo [1].

Expect light rain this evening around 8 PM.

Sources:
[1] [Open-Meteo Tokyo](https://open-meteo.com)

---

**User:** Who won the latest F1 race?

**Bot:**
Lando Norris won the 2026 Australian Grand Prix [1].

Key results:
• 1st: Lando Norris (McLaren)
• 2nd: Max Verstappen (Red Bull)
• 3rd: George Russell (Mercedes)

Sources:
[1] [Formula 1 Official](https://formula1.com)

---

**User:** Explain quantum computing

**Bot:**
Quantum computing uses quantum bits (qubits) that can exist in multiple states simultaneously [1].

Key concepts:
• **Superposition:** Qubits can be 0, 1, or both at once
• **Entanglement:** Linked qubits affect each other instantly
• **Interference:** Algorithms amplify correct answers

*Beta feature: Enhanced reasoning mode active*

Sources:
[1] [IBM Quantum](https://www.ibm.com/quantum-computing)

## Customization

Edit `persona.md` to adjust:
- Response style
- Beta features mentioned
- Tone and personality
- Source citation format

## Running as a Service

To keep the bot running 24/7:

### Option 1: Screen/Tmux
```bash
tmux new -s perplexity-bot
source venv/bin/activate
python3 bot.py
# Detach: Ctrl+B, then D
```

### Option 2: LaunchAgent (macOS)
Create `~/Library/LaunchAgents/com.perplexity.bot.plist`:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.perplexity.bot</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/clawdbot/.openclaw/workspace/bots/perplexity-beta/venv/bin/python3</string>
        <string>/Users/clawdbot/.openclaw/workspace/bots/perplexity-beta/bot.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/clawdbot/.openclaw/workspace/bots/perplexity-beta</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PERPLEXITY_BOT_TOKEN</key>
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
launchctl load ~/Library/LaunchAgents/com.perplexity.bot.plist
```

## Files

- `bot.py` - Main bot code
- `persona.md` - Bot personality configuration
- `requirements.txt` - Python dependencies
- `setup.sh` - Setup script
- `feedback.log` - User feedback (auto-created)

## Notes

- This is a **beta/preview** implementation
- Full LLM integration requires additional setup
- Web search uses OpenClaw's built-in capabilities
- Customize the persona in `persona.md` as needed

## Troubleshooting

**Bot not responding?**
- Check token is set: `echo $PERPLEXITY_BOT_TOKEN`
- Check bot is running: `ps aux | grep bot.py`
- Check logs for errors

**Dependencies issues?**
- Make sure virtual environment is activated: `source venv/bin/activate`
- Reinstall: `pip install -r requirements.txt`

**Token not working?**
- Regenerate via @BotFather: `/revoke`
- Make sure no extra spaces in token
- Export again: `export PERPLEXITY_BOT_TOKEN='...'`