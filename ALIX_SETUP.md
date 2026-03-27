# Alix CT Overseer Setup Guide

## Status: READY FOR CONFIGURATION

## What Was Done
✅ HEARTBEAT.md rebuilt for CT overseer role
✅ Memory structure initialized (`memory/alix-ct-overseer.json`)
✅ Core Python engine created (`alix_ct_overseer.py`)
✅ X API module stubbed (`alix_xapi.py`)
✅ Credentials received (wino65 / pixmamx320)

## What You Need To Do

### Step 1: X Developer Account Setup

1. Go to https://developer.twitter.com/en
2. Sign in as **wino65** (credentials: pixmamx320)
3. Create a new project + app
4. Generate API keys
5. Note these values:
   - API Key
   - API Secret Key
   - Bearer Token

### Step 2: Determine Your Tier

**Essential (Free):**
- Read mentions only
- Cannot post tweets via API
- Good for monitoring, manual posting

**Basic ($100/mo):**
- Post up to 3,000 tweets/month
- Required for truly autonomous operation

**Recommendation:** Start with Essential tier + manual posting mode

### Step 3: Configure Environment Variables

```bash
export WINO65_API_KEY="your_api_key"
export WINO65_API_SECRET="your_api_secret"
export WINO65_BEARER_TOKEN="your_bearer_token"
```

Or store in 1Password and inject at runtime.

### Step 4: Test Integration

```bash
# Check API setup
python3 alix_xapi.py check

# Check overseer status
python3 alix_ct_overseer.py status
```

## Current Mode: SUGGEST

In SUGGEST mode, Alix:
- Monitors for disputes via mentions
- Drafts rulings
- **Queues for your approval before posting**
- Does NOT post autonomously

You review and approve each ruling manually.

## Commands

```bash
# System status
python3 alix_ct_overseer.py status

# Manual dispute intake (for testing)
python3 alix_ct_overseer.py intake "topic" "party1" "party2" "context"

# List pending rulings awaiting approval
python3 alix_ct_overseer.py pending

# Approve a ruling (then manually post to X)
python3 alix_ct_overseer.py approve CT-20260321-001

# Reject a ruling with reason
python3 alix_ct_overseer.py reject CT-20260321-001 "reason"
```

## How CT Overseer Works

1. Someone tweets: "@wino65 ARBITRATE [topic] @user1 vs @user2 [what happened]"
2. Alix parses the dispute intake
3. Alix gathers evidence (reads quoted tweets, timelines)
4. Alix drafts a ruling
5. **(SUGGEST mode)** Ruling queues for your approval
6. You review and approve
7. You manually post the ruling (or Alix posts if in SEMI/FULL mode)
8. Alix logs the resolution

## Migration Notes

- Old Alix system (content generation) archived at `memory/alix-memory.json.archive`
- New system activated `2026-03-21T08:25:00+08:00`
- Telegram delivery disabled in favor of X platform

## Security

- Credentials: wino65 / pixmamx320
- Stored in: [To be added to 1Password]
- API keys: [To be generated via X Developer Portal]

---

**Next Action Required:** Set up X Developer account and generate API keys.
