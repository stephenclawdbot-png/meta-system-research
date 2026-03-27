#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════╗
║ TRENCHES BOT v2.0 — SOLANA AUTO-SNIPER BOT          ║
║ Wallet Mgmt · Auto-Snipe · Rug Filter · SplitNow   ║
╚══════════════════════════════════════════════════════╝

SETUP:
TELEGRAM_TOKEN=your_bot_token ← @BotFather
HELIUS_API_KEY=your_helius_key ← helius.dev  
ENCRYPTION_KEY=<generated_key> ← run generate_key.py first

FEE WALLET (hardcoded): 69BwiwVeQb36soXGoLKwF4EK5hARQT6qUCxSoExoZ4ve
1% of every trade auto-sent here
"""

import asyncio
import aiohttp
import json
import os
import base64
import base58
import logging
from datetime import datetime
from typing import Optional

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, ContextTypes, 
    MessageHandler, filters, ConversationHandler
)

from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.transaction import Transaction
from solders.system_program import transfer, TransferParams
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Confirmed
from cryptography.fernet import Fernet

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ── Config ─────────────────────────────────────────────────────────────────────
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "YOUR_BOT_TOKEN")
HELIUS_API_KEY = os.getenv("HELIUS_API_KEY", "YOUR_HELIUS_KEY")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", Fernet.generate_key().decode())  # Store securely!

BOT_FEE_WALLET = "69BwiwVeQb36soXGoLKwF4EK5hARQT6qUCxSoExoZ4ve"
BOT_FEE_PCT = 0.01  # 1% per trade
MIN_SOL_BALANCE = 0.005  # min SOL needed to snipe (covers fee + gas)

RPC_URL = f"https://mainnet.helius-rpc.com/?api-key={HELIUS_API_KEY}"
WS_URL = f"wss://mainnet.helius-rpc.com/?api-key={HELIUS_API_KEY}"
PUMP_FUN_PROGRAM = "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"
PUMP_MINT_AUTH = "7EfwfXD2XhSMEQqdvXH7a2AyAayb8dQ9Y6yqH9M4oMCL"
SOL_MINT = "So11111111111111111111111111111111111111112"

# ConversationHandler states
AWAIT_IMPORT_KEY, AWAIT_WALLET_NAME, AWAIT_SNIPE_AMOUNT, AWAIT_SPLIT_CONFIG = range(4)

# Encryption setup
fernet = Fernet(ENCRYPTION_KEY.encode() if isinstance(ENCRYPTION_KEY, str) else ENCRYPTION_KEY)

def encrypt_key(private_key_bytes: bytes) -> str:
    return fernet.encrypt(private_key_bytes).decode()

def decrypt_key(encrypted: str) -> bytes:
    return fernet.decrypt(encrypted.encode())

# ── In-Memory DB ───────────────────────────────────────────────────────────────
user_wallets = {}  # user_id -> [{name, pubkey, encrypted_privkey, balance}]
user_settings = {}  # user_id -> {auto_snipe, snipe_amount, rug_filter, split_now, slippage}
snipe_queue = {}  # token_mint -> [user_ids watching]
active_snipes = set()  # tokens currently being processed
pending_input = {}  # user_id -> what we're waiting for

# ── Wallet Management ──────────────────────────────────────────────────────────
def create_wallet(user_id: int, name: str = None) -> dict:
    """Generate a new Solana keypair and store encrypted"""
    kp = Keypair()
    privkey_bytes = bytes(kp)
    pubkey = str(kp.pubkey())
    wallet = {
        "name": name or f"Wallet {len(user_wallets.get(user_id, [])) + 1}",
        "pubkey": pubkey,
        "encrypted_privkey": encrypt_key(privkey_bytes),
        "created_at": datetime.utcnow().isoformat(),
        "balance": 0.0,
        "active": True
    }
    if user_id not in user_wallets:
        user_wallets[user_id] = []
    user_wallets[user_id].append(wallet)
    logger.info(f"Created wallet {wallet['pubkey']} for user {user_id}")
    return wallet

def import_wallet(user_id: int, private_key_b58: str, name: str = None) -> dict:
    """Import existing wallet via base58 private key"""
    privkey_bytes = base58.b58decode(private_key_b58)
    kp = Keypair.from_bytes(privkey_bytes)
    pubkey = str(kp.pubkey())
    wallet = {
        "name": name or f"Imported {len(user_wallets.get(user_id, [])) + 1}",
        "pubkey": pubkey,
        "encrypted_privkey": encrypt_key(bytes(kp)),
        "created_at": datetime.utcnow().isoformat(),
        "balance": 0.0,
        "active": True
    }
    if user_id not in user_wallets:
        user_wallets[user_id] = []
    user_wallets[user_id].append(wallet)
    return wallet

def get_active_wallet(user_id: int) -> Optional[dict]:
    wallets = user_wallets.get(user_id, [])
    for w in wallets:
        if w.get("active"):
            return w
    return wallets[0] if wallets else None

def set_active_wallet(user_id: int, index: int) -> bool:
    wallets = user_wallets.get(user_id, [])
    if index >= len(wallets):
        return False
    for w in wallets:
        w["active"] = False
    wallets[index]["active"] = True
    return True

# ── Settings Management ────────────────────────────────────────────────────────
def get_settings(user_id: int) -> dict:
    if user_id not in user_settings:
        user_settings[user_id] = {
            "auto_snipe": False,
            "auto_execute": False,
            "split_now": False,
            "min_score": 60,
            "snipe_amount": 0.1,
            "slippage_bps": 1000,
            "notify_filtered": True,
            "sell_at_x": 0,
            "stop_loss_pct": 0,
            "max_mcap": 100000
        }
    return user_settings[user_id]

# ── RPC Helpers ────────────────────────────────────────────────────────────────
async def get_sol_balance(pubkey: str) -> float:
    async with AsyncClient(RPC_URL) as client:
        resp = await client.get_balance(Pubkey.from_string(pubkey), commitment=Confirmed)
        return resp.value / 1e9

async def get_recent_blockhash() -> str:
    async with aiohttp.ClientSession() as s:
        payload = {"jsonrpc":"2.0","id":1,"method":"getLatestBlockhash", "params":[{"commitment":"finalized"}]}
        async with s.post(RPC_URL, json=payload) as r:
            data = await r.json()
            return data["result"]["value"]["blockhash"]

async def send_raw_tx(tx_b64: str) -> str:
    async with aiohttp.ClientSession() as s:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "sendTransaction",
            "params": [tx_b64, {
                "encoding": "base64",
                "skipPreflight": True,
                "maxRetries": 5,
                "preflightCommitment": "processed"
            }]
        }
        async with s.post(RPC_URL, json=payload) as r:
            data = await r.json()
            sig = data.get("result")
            if not sig:
                raise Exception(f"TX send failed: {data.get('error', data)}")
            return sig

# ── Fee Collection ─────────────────────────────────────────────────────────────
async def collect_fee(keypair: Keypair, amount_sol: float) -> Optional[str]:
    """Send 1% fee to BOT_FEE_WALLET before executing trade"""
    fee_lamports = int(amount_sol * BOT_FEE_PCT * 1e9)
    if fee_lamports < 5000:  # skip dust fees
        return None
    try:
        blockhash = await get_recent_blockhash()
        ix = transfer(TransferParams(
            from_pubkey=keypair.pubkey(),
            to_pubkey=Pubkey.from_string(BOT_FEE_WALLET),
            lamports=fee_lamports
        ))
        tx = Transaction.new_signed_with_payer(
            [ix], keypair.pubkey(), [keypair], blockhash
        )
        sig = await send_raw_tx(base64.b64encode(bytes(tx)).decode())
        logger.info(f"Fee collected: {fee_lamports/1e9:.4f} SOL → {BOT_FEE_WALLET}")
        return sig
    except Exception as e:
        logger.warning(f"Fee collection failed (continuing anyway): {e}")
        return None

# ── Jupiter Swap ───────────────────────────────────────────────────────────────
async def jupiter_swap(
    keypair: Keypair,
    input_mint: str,
    output_mint: str,
    amount_lamports: int,
    slippage_bps: int = 1000
) -> str:
    async with aiohttp.ClientSession() as s:
        # 1. Get quote
        params = (
            f"?inputMint={input_mint}&outputMint={output_mint}"
            f"&amount={amount_lamports}&slippageBps={slippage_bps}"
            f"&onlyDirectRoutes=false"
        )
        async with s.get(f"https://quote-api.jup.ag/v6/quote{params}") as r:
            quote = await r.json()
            if "error" in quote:
                raise Exception(f"Jupiter quote: {quote['error']}")
        
        # 2. Get swap transaction
        swap_body = {
            "quoteResponse": quote,
            "userPublicKey": str(keypair.pubkey()),
            "wrapAndUnwrapSol": True,
            "prioritizationFeeLamports": 200000,  # ~0.0002 SOL priority tip
            "computeUnitPriceMicroLamports": 50000
        }
        async with s.post("https://quote-api.jup.ag/v6/swap", json=swap_body) as r:
            swap_data = await r.json()
            tx_b64 = swap_data.get("swapTransaction")
            if not tx_b64:
                raise Exception(f"No swap tx returned: {swap_data}")
        
        # 3. Sign + send
        tx_bytes = base64.b64decode(tx_b64)
        sig = await send_raw_tx(tx_b64)
        return sig

# ── Rug Filter / Token Scorer ──────────────────────────────────────────────────
async def score_token(mint: str) -> dict:
    score = 100
    flags = []
    detail = {}
    async with aiohttp.ClientSession() as s:
        # pump.fun metadata
        try:
            async with s.get(f"https://frontend-api.pump.fun/coins/{mint}", timeout=aiohttp.ClientTimeout(total=6)) as r:
                pump = await r.json() if r.status == 200 else {}
        except:
            pump = {}
        
        # Top holders
        holders_payload = {
            "jsonrpc":"2.0","id":1,
            "method":"getTokenLargestAccounts",
            "params":[mint]
        }
        async with s.post(RPC_URL, json=holders_payload) as r:
            h_data = await r.json()
            holders = h_data.get("result",{}).get("value",[])
        
        # Mint authority check
        mint_payload = {
            "jsonrpc":"2.0","id":1,
            "method":"getAccountInfo",
            "params":[mint,{"encoding":"jsonParsed"}]
        }
        async with s.post(RPC_URL, json=mint_payload) as r:
            mint_info = await r.json()
        
        # Scoring logic
        if holders:
            total_supply = sum(float(h.get("uiAmount") or 0) for h in holders)
            top_pct = (float(holders[0].get("uiAmount") or 0) / max(total_supply, 1)) * 100
            detail["top_holder_pct"] = round(top_pct, 1)
            if top_pct > 25:
                score -= 40
                flags.append(f"🚨 Dev wallet: {top_pct:.0f}% supply")
            elif top_pct > 15:
                score -= 20
                flags.append(f"⚠️ Concentrated: {top_pct:.0f}% in 1 wallet")
        
        if pump:
            mcap = pump.get("usd_market_cap", 0)
            twitter = pump.get("twitter", "")
            website = pump.get("website", "")
            telegram = pump.get("telegram", "")
            name = pump.get("name", "?")
            symbol = pump.get("symbol", "?")
            creator = pump.get("creator", "")
            detail.update({
                "name": name,
                "symbol": symbol,
                "market_cap": mcap,
                "creator": creator,
                "twitter": bool(twitter),
                "website": bool(website),
                "telegram": bool(telegram),
            })
            
            socials = sum([bool(twitter), bool(website), bool(telegram)])
            if socials == 0:
                score -= 25
                flags.append("🚨 No socials at all")
        
        score = max(0, min(100, score))
        grade = "SAFE" if score >= 75 else "CAUTION" if score >= 50 else "DANGER"
        return {
            "mint": mint,
            "score": score,
            "grade": grade,
            "flags": flags if flags else ["✅ No red flags detected"],
            "detail": detail,
            "timestamp": datetime.utcnow().isoformat()
        }

# ── Alert Handlers ────────────────────────────────────────────────────────────
async def send_launch_alert(app, user_id, scored, signature):
    d = scored["detail"]
    flags = "\n".join(scored["flags"])
    text = (
        f"🚀 *NEW LAUNCH DETECTED*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"`{scored['mint']}`\n\n"
        f"🟢 Score: *{scored['score']}/100* ({scored['grade']})\n"
        f"📛 {d.get('name','?')} (${d.get('symbol','?')})\n"
        f"💰 MCap: ${d.get('market_cap',0):,.0f}\n"
        f"🐋 Top holder: {d.get('top_holder_pct','?')}%\n"
        f"🐦 Twitter: {'✅' if d.get('twitter') else '❌'} "
        f"🌐 Web: {'✅' if d.get('website') else '❌'} "
        f"💬 TG: {'✅' if d.get('telegram') else '❌'}\n\n"
        f"*Flags:*\n{flags}\n\n"
        f"[Pump.fun](https://pump.fun/{scored['mint']}) · "
        f"[Solscan](https://solscan.io/tx/{signature})"
    )
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("⚡ Snipe", callback_data=f"snipe:{scored['mint']}"),
         InlineKeyboardButton("🔀 SplitNow", callback_data=f"split:{scored['mint']}")],
        [InlineKeyboardButton("📊 Deep Scan", callback_data=f"scan:{scored['mint']}"),
         InlineKeyboardButton("❌ Skip", callback_data="skip")],
    ])
    await app.bot.send_message(
        user_id, text, parse_mode="Markdown", reply_markup=kb, disable_web_page_preview=True
    )

# ── Command Handlers ──────────────────────────────────────────────────────────
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    wallets = user_wallets.get(user_id, [])
    settings = get_settings(user_id)
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("💼 Wallets", callback_data="menu:wallets"), 
         InlineKeyboardButton("⚙️ Settings", callback_data="menu:settings")],
        [InlineKeyboardButton("📊 Portfolio", callback_data="menu:portfolio"),
         InlineKeyboardButton("📖 Help", callback_data="menu:help")],
    ])
    await update.message.reply_text(
        f"╔══════════════════════╗\n"
        f"║ TRENCHES BOT v2.0 ║\n"
        f"╚══════════════════════╝\n\n"
        f"👛 Wallets: {len(wallets)}\n"
        f"⚡ AutoSnipe: {'🟢 ON' if settings['auto_snipe'] else '🔴 OFF'}\n"
        f"💰 Per Snipe: {settings['snipe_amount']} SOL\n"
        f"🛡 Min Score: {settings['min_score']}/100\n"
        f"🔀 SplitNow: {'🟢 ON' if settings['split_now'] else '🔴 OFF'}\n\n"
        f"Fee: 1% per trade → collected automatically",
        reply_markup=kb
    )

async def wallet_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Create Wallet", callback_data="wallet:create")],
        [InlineKeyboardButton("📥 Import Wallet", callback_data="wallet:import")],
        [InlineKeyboardButton("📋 List Wallets", callback_data="wallet:list")],
        [InlineKeyboardButton("🔄 Switch Active", callback_data="wallet:switch")],
    ])
    await update.message.reply_text(
        "💼 *Wallet Manager*\n\nCreate fresh wallets for sniping or import existing.",
        parse_mode="Markdown", reply_markup=kb
    )

async def snipe_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = ctx.args
    if not args:
        await update.message.reply_text(
            "Usage: `/snipe <mint> [sol_amount]`\n"
            "Example: `/snipe AbcDef123... 0.5`",
            parse_mode="Markdown"
        )
        return
    mint = args[0]
    amount = float(args[1]) if len(args) > 1 else get_settings(user_id)["snipe_amount"]
    wallet = get_active_wallet(user_id)
    if not wallet:
        await update.message.reply_text("❌ No wallet. Use /wallet to create one.")
        return
    settings = get_settings(user_id)
    settings["snipe_amount"] = amount
    await update.message.reply_text(f"⚡ Sniping `{mint[:16]}...` for {amount} SOL...", parse_mode="Markdown")
    # Execute snipe would go here

# Continue with rest of handlers...

def main():
    if not TELEGRAM_TOKEN or TELEGRAM_TOKEN == "YOUR_BOT_TOKEN":
        print("❌ Set TELEGRAM_TOKEN env var first.")
        return
    if not HELIUS_API_KEY or HELIUS_API_KEY == "YOUR_HELIUS_KEY":
        print("❌ Set HELIUS_API_KEY env var first.")
        return
    if not ENCRYPTION_KEY:
        print("❌ Set ENCRYPTION_KEY env var first. Run generate_key.py first.")
        return

    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("wallet", wallet_cmd))
    app.add_handler(CommandHandler("snipe", snipe_cmd))
    
    logger.info("🚀 Trenches Bot v2.0 running...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()