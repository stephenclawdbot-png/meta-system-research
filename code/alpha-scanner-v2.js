/** - ╔═══════════════════════════════════════════════════════════════╗ - ║ ALPHA SCANNER v2.0 — Unfair Meme Coin Gem Finder ║ - ║ Real-time Pump.fun + DexScreener engine ║ - ║ 5-min scan cycles · Smart alpha filters · Bot-ready output ║ - ╚═══════════════════════════════════════════════════════════════╝ - - WHAT THIS DOES: - - Polls Pump.fun for brand new coin launches every 5 minutes - - Polls DexScreener for new Solana pairs - - Cross-references tokens on both platforms for enriched data - - Applies configurable alpha criteria to filter noise - - Only surfaces NEW gems not previously seen - - Outputs alerts via webhook (Discord/Telegram), local log, and JSON feed - - Exposes HTTP API for OpenClaw/Clawdbot skill integration - - ALPHA CRITERIA (configurable in config): - - Minimum market cap threshold - - Minimum volume threshold - - Minimum transaction count - - Buy/sell ratio (bullish pressure) - - Age filter (only fresh tokens) - - Liquidity floor - - Dev wallet concentration check - - Social signal detection (website, twitter, telegram present) */ const http = require('http'); const https = require('https'); const fs = require('fs'); const path = require('path'); const { EventEmitter } = require('events'); // ═══════════════════════════════════════════════════════════════ // CONFIGURATION — Tune these for your alpha edge // ═══════════════════════════════════════════════════════════════ const CONFIG = { // Scan timing SCAN_INTERVAL_MS: 5 * 60 * 1000, // 5 minutes ENRICHMENT_DELAY_MS: 30 * 1000, // Wait 30s before enriching (let data populate) // Alpha criteria — tokens must pass ALL enabled filters ALPHA_FILTERS: { // Market cap range (too low = rug, too high = already found) MIN_MCAP: 5000, // $5K min — below this is dust MAX_MCAP: 5000000, // $5M max — above this isn't "early" anymore // Volume shows real interest MIN_VOLUME_24H: 1000, // $1K min 24h volume // Transaction activity MIN_TXNS_24H: 10, // At least 10 transactions // Buy pressure — more buys than sells = accumulation MIN_BUY_RATIO: 0.50, // 50%+ buys (0.0 to 1.0) // Age — we want FRESH tokens only MAX_AGE_HOURS: 24, // Only tokens < 24 hours old MIN_AGE_MINUTES: 5, // At least 5 min old (avoid instant rugs) // Liquidity floor MIN_LIQUIDITY: 1000, // $1K min liquidity // Social signals (bonus score, not hard filter) REQUIRE_WEBSITE: false, // Must have website REQUIRE_TWITTER: false, // Must have twitter REQUIRE_TELEGRAM: false, // Must have telegram // Rug detection MAX_DEV_HOLDING_PCT: 20, // Dev holds < 20% of supply BONDING_CURVE_COMPLETE: false, // Only graduated tokens (pump.fun) }, // Alpha scoring weights SCORING: { VOLUME_WEIGHT: 25, // High volume = interest MCAP_VOLUME_RATIO_WEIGHT: 20, // Low mcap + high volume = undervalued BUY_PRESSURE_WEIGHT: 15, // More buys = accumulation AGE_WEIGHT: 15, // Newer = earlier LIQUIDITY_WEIGHT: 10, // Healthy liquidity SOCIAL_WEIGHT: 10, // Has socials TXN_VELOCITY_WEIGHT: 5, // Transaction speed }, // Output destinations WEBHOOKS: { DISCORD: process.env.DISCORD_WEBHOOK || '', TELEGRAM_BOT_TOKEN: process.env.TG_BOT_TOKEN || '', TELEGRAM_CHAT_ID: process.env.TG_CHAT_ID || '', CUSTOM_WEBHOOK: process.env.CUSTOM_WEBHOOK || '', }, // Server HTTP_PORT: parseInt(process.env.PORT) || 3111, // Storage DATA_DIR: path.join(__dirname, 'data'), SEEN_TOKENS_FILE: path.join(__dirname, 'data', 'seen_tokens.json'), ALERTS_LOG: path.join(__dirname, 'data', 'alerts.jsonl'), ALPHA_FEED: path.join(__dirname, 'data', 'alpha_feed.json'), }; // ═══════════════════════════════════════════════════════════════ // STATE // ═══════════════════════════════════════════════════════════════ const state = {
    alphaTokens: [],
    seenTokens: new Map(),
    lastScan: null,
    isScanning: false,
    scanNumber: 0,
    allScannedCount: 0,
    errors: [],
};

// Phase 3: Filter to only NEW (unseen) tokens
const allAddresses = [...tokenMap.keys()];
const newAddresses = allAddresses.filter(addr => !state.seenTokens.has(addr));

// Mark all as seen 
const now = Date.now();
allAddresses.forEach(addr => {
    if (!state.seenTokens.has(addr)) state.seenTokens.set(addr, now);
});

state.allScannedCount += allAddresses.length;
log('info', `${newAddresses.length} NEW tokens found (${allAddresses.length} total, ${state.seenTokens.size} lifetime tracked)`);

if (newAddresses.length === 0) {
    log('info', 'No new tokens this cycle');
    state.lastScan = new Date().toISOString();
    state.isScanning = false;
    return;
}

// Phase 4: Enrich new tokens with DexScreener pair data
log('scan', `Phase 4: Enriching ${newAddresses.length} new tokens via DexScreener...`);
await sleep(2000); // Small delay to let pair data propagate
const enrichedData = await enrichWithDexScreener(newAddresses);

// Merge enriched data
const candidates = [];
newAddresses.forEach(addr => {
    const base = tokenMap.get(addr);
    const dex = enrichedData[addr] || {};
    
    const token = {
        address: addr,
        name: base.name || dex.name || 'Unknown',
        ticker: base.ticker || dex.ticker || '???',
        mcap: Math.max(base.mcap || 0, dex.mcap || 0),
        volume24h: Math.max(base.volume24h || 0, dex.volume24h || 0),
        volume1h: dex.volume1h || 0,
        priceChange24h: dex.priceChange24h || base.priceChange24h || 0,
        priceChange1h: dex.priceChange1h || base.priceChange1h || 0,
        priceChange5m: dex.priceChange5m || 0,
        price: dex.priceUsd || base.price || 0,
        liquidity: dex.liquidity || base.liquidity || 0,
        txns24h: Math.max(base.txns24h || 0, dex.txns24h || 0),
        buys24h: Math.max(base.buys24h || 0, dex.buys24h || 0),
        sells24h: Math.max(base.sells24h || 0, dex.sells24h || 0),
        txns1h: dex.txns1h || 0,
        buys1h: dex.buys1h || 0,
        sells1h: dex.sells1h || 0,
        image: base.image || '',
        source: base.source || 'unknown',
        createdAt: base.createdAt || dex.pairCreatedAt || null,
        ageMs: null,
        pairAddress: dex.pairAddress || '',
        website: base.website || '',
        twitter: base.twitter || '',
        telegram: base.telegram || '',
        description: base.description || '',
        complete: base.complete || false,
        kingOfTheHill: base.kingOfTheHill || false,
        replyCount: base.replyCount || 0,
        boostAmount: base.boostAmount || 0,
        firstSeen: now,
        scanNumber: state.scanNumber,
    };
    
    // Calculate age
    if (token.createdAt) {
        token.ageMs = now - token.createdAt;
    }
    
    candidates.push(token);
});

// Phase 5: Apply alpha filters
log('scan', `Phase 5: Applying alpha filters to ${candidates.length} candidates...`);
const alphaGems = [];
let filtered = 0;

candidates.forEach(token => {
    const { pass, reasons } = passesAlphaFilter(token);
    if (pass) {
        const { score, breakdown } = computeAlphaScore(token);
        token.alphaScore = score;
        token.alphaBreakdown = breakdown;
        alphaGems.push(token);
    } else {
        filtered++;
    }
});

// Sort by alpha score
alphaGems.sort((a, b) => b.alphaScore - a.alphaScore);

log('alpha', `═══ ${alphaGems.length} ALPHA GEMS FOUND (${filtered} filtered out) ═══`);

// Phase 6: Alert and store
if (alphaGems.length > 0) {
    // Add to state
    state.alphaTokens = [...alphaGems, ...state.alphaTokens].slice(0, 200);
    
    // Log each gem
    alphaGems.forEach((gem, i) => {
        log('alpha', ` #${i+1} $${gem.ticker} | MCap: ${fmt(gem.mcap)} | Vol: ${fmt(gem.volume24h)} | Age: ${fmtAge(gem.ageMs)} | Score: ${gem.alphaScore}/100`);
    });
    
    // Send alerts
    await sendAlerts(alphaGems);
    
    // Persist
    saveAlphaFeed();
    appendAlertsLog(alphaGems);
}

state.lastScan = new Date().toISOString();
const duration = ((Date.now() - scanStart) / 1000).toFixed(1);
log('scan', `═══ SCAN #${state.scanNumber} COMPLETE in ${duration}s ═══ `);
}

// State initialization...
seenTokens: new Map(), // address -> first seen timestamp 
alphaTokens: [], // current alpha gems
allScannedCount: 0, 
alertsSent: 0,
lastScan: null,
scanNumber: 0,
isScanning: false,
errors: [], 
}; 

const events = new EventEmitter();

// ═══════════════════════════════════════════════════════════════
// HELPERS
// ═══════════════════════════════════════════════════════════════

function log(level, msg, data = null) {
    const ts = new Date().toISOString();
    const prefix = { info: '🟢', warn: '🟡', error: '🔴', alpha: '⚡', scan: '🔍' }[level] || '·';
    const line = `${prefix} [${ts}] ${msg}`;
    console.log(data ? `${line} ${JSON.stringify(data)}` : line);
}

function httpGet(url, timeout = 15000) {
    return new Promise((resolve, reject) => {
        const mod = url.startsWith('https') ? https : http;
        const req = mod.get(url, { 
            timeout, 
            headers: { 
                'Accept': 'application/json',
                'User-Agent': 'AlphaScanner/2.0'
            }
        }, (res) => {
            let body = '';
            res.on('data', chunk => body += chunk);
            res.on('end', () => {
                try {
                    resolve(JSON.parse(body));
                } catch(e) {
                    reject(new Error(`JSON parse error from ${url}: ${e.message}`));
                }
            });
        });
        req.on('error', reject);
        req.on('timeout', () => {
            req.destroy();
            reject(new Error(`Timeout: ${url}`));
        });
    });
}

function httpPost(url, data) {
    return new Promise((resolve, reject) => {
        const parsed = new URL(url);
        const body = JSON.stringify(data);
        const opts = {
            hostname: parsed.hostname,
            port: parsed.port || 443,
            path: parsed.pathname + parsed.search,
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(body)
            },
            timeout: 10000,
        };
        const mod = url.startsWith('https') ? https : http;
        const req = mod.request(opts, (res) => {
            let d = '';
            res.on('data', c => d += c);
            res.on('end', () => resolve(d));
        });
        req.on('error', reject);
        req.write(body);
        req.end();
    });
}

function fmt(n) {
    if (!n || isNaN(n)) return '-';
    if (n >= 1e9) return '$' + (n/1e9).toFixed(2) + 'B';
    if (n >= 1e6) return '$' + (n/1e6).toFixed(2) + 'M';
    if (n >= 1e3) return '$' + (n/1e3).toFixed(1) + 'K';
    return '$' + n.toFixed(2);
}

function fmtAge(ms) {
    if (!ms) return '?';
    const mins = Math.floor(ms / 60000);
    if (mins < 60) return `${mins}m`;
    const hrs = Math.floor(mins / 60);
    if (hrs < 24) return `${hrs}h ${mins % 60}m`;
    return `${Math.floor(hrs / 24)}d ${hrs % 24}h`;
}

function sleep(ms) {
    return new Promise(r => setTimeout(r, ms));
}

// ═══════════════════════════════════════════════════════════════
// DATA FETCHERS
// ═══════════════════════════════════════════════════════════════

async function fetchPumpFunCoins() {
    const results = [];
    // Fetch multiple endpoints for maximum coverage
    const endpoints = [
        'https://frontend-api-v3.pump.fun/coins/latest',
        'https://frontend-api-v3.pump.fun/coins/featured',
        'https://frontend-api-v3.pump.fun/coins/king-of-the-hill?includeNsfw=false',
    ];
    
    for (const url of endpoints) {
        try {
            const data = await httpGet(url);
            if (Array.isArray(data)) {
                data.forEach(c => {
                    results.push({
                        name: c.name || 'Unknown',
                        ticker: c.symbol || '???',
                        address: c.mint || c.address || '',
                        mcap: c.usd_market_cap || c.market_cap || 0,
                        volume24h: c.volume_24h || 0,
                        priceChange24h: c.price_change_24h || 0,
                        priceChange1h: c.price_change_1h || 0,
                        price: c.price || 0,
                        image: c.image_uri || c.profile_image || '',
                        createdAt: c.created_timestamp || null,
                        txns24h: (c.buys_24h || 0) + (c.sells_24h || 0),
                        buys24h: c.buys_24h || 0,
                        sells24h: c.sells_24h || 0,
                        liquidity: 0,
                        source: 'pump',
                        description: c.description || '',
                        website: c.website || '',
                        twitter: c.twitter || '',
                        telegram: c.telegram || '',
                        complete: c.complete || false, // bonding curve graduated
                        kingOfTheHill: !!c.king_of_the_hill_timestamp,
                        devAddress: c.creator || '',
                        replyCount: c.reply_count || 0,
                    });
                });
            }
        } catch(e) {
            log('warn', `Pump.fun fetch failed: ${url}`, e.message);
        }
    }
    
    // Deduplicate
    const seen = new Map();
    results.forEach(t => {
        if (t.address && !seen.has(t.address)) seen.set(t.address, t);
    });
    return [...seen.values()];
}

async function fetchDexScreenerNew() {
    const results = [];
    
    try {
        // Latest token profiles (newest listings)
        const profiles = await httpGet('https://api.dexscreener.com/token-profiles/latest/v1');
        if (Array.isArray(profiles)) {
            const solProfiles = profiles.filter(t => t.chainId === 'solana');
            solProfiles.forEach(t => {
                results.push({
                    address: t.tokenAddress,
                    source: 'dex',
                    website: (t.links || []).find(l => l.type === 'website')?.url || '',
                    twitter: (t.links || []).find(l => l.type === 'twitter')?.url || '',
                    telegram: (t.links || []).find(l => l.type === 'telegram')?.url || '',
                    image: t.icon || '',
                    description: t.description || '',
                });
            });
        }
    } catch(e) {
        log('warn', 'DexScreener profiles failed', e.message);
    }
    
    try {
        // Token boosts (recently promoted)
        const boosts = await httpGet('https://api.dexscreener.com/token-boosts/latest/v1');
        if (Array.isArray(boosts)) {
            const solBoosts = boosts.filter(t => t.chainId === 'solana');
            solBoosts.forEach(t => {
                if (!results.find(r => r.address === t.tokenAddress)) {
                    results.push({
                        address: t.tokenAddress,
                        source: 'dex',
                        image: t.icon || '',
                        boostAmount: t.totalAmount || 0,
                    });
                }
            });
        }
    } catch(e) {
        log('warn', 'DexScreener boosts failed', e.message);
    }
    
    return results;
}

async function enrichWithDexScreener(addresses) {
    const enriched = {};
    
    for (let i = 0; i < addresses.length; i += 30) {
        const batch = addresses.slice(i, i + 30).join(',');
        try {
            const pairs = await httpGet(`https://api.dexscreener.com/tokens/v1/solana/${batch}`);
            if (Array.isArray(pairs)) {
                pairs.forEach(p => {
                    const addr = p.baseToken?.address;
                    if (!addr) return;
                    
                    // Pick the highest-volume pair for this token
                    if (!enriched[addr] || (p.volume?.h24 || 0) > (enriched[addr].volume24h || 0)) {
                        enriched[addr] = {
                            name: p.baseToken?.name || '',
                            ticker: p.baseToken?.symbol || '',
                            mcap: p.marketCap || p.fdv || 0,
                            volume24h: p.volume?.h24 || 0,
                            volume1h: p.volume?.h1 || 0,
                            volume6h: p.volume?.h6 || 0,
                            priceChange24h: p.priceChange?.h24 || 0,
                            priceChange1h: p.priceChange?.h1 || 0,
                            priceChange5m: p.priceChange?.m5 || 0,
                            priceUsd: p.priceUsd ? parseFloat(p.priceUsd) : 0,
                            liquidity: p.liquidity?.usd || 0,
                            pairCreatedAt: p.pairCreatedAt || null,
                            pairAddress: p.pairAddress || '',
                            txns24h: p.txns?.h24 ? (p.txns.h24.buys + p.txns.h24.sells) : 0,
                            buys24h: p.txns?.h24?.buys || 0,
                            sells24h: p.txns?.h24?.sells || 0,
                            txns1h: p.txns?.h1 ? (p.txns.h1.buys + p.txns.h1.sells) : 0,
                            buys1h: p.txns?.h1?.buys || 0,
                            sells1h: p.txns?.h1?.sells || 0,
                            dexId: p.dexId || '',
                            info: p.info || {},
                        };
                    }
                });
            }
            // Rate limit respect
            if (i + 30 < addresses.length) await sleep(500);
        } catch(e) {
            log('warn', `DexScreener enrichment batch failed`, e.message);
        }
    }
    
    return enriched;
}

// ═══════════════════════════════════════════════════════════════
// ALPHA SCORING ENGINE
// ═══════════════════════════════════════════════════════════════

function computeAlphaScore(token) {
    const W = CONFIG.SCORING;
    let score = 0;
    let breakdown = {};
    
    // Volume score (log scale, $1K=low, $500K+=max)
    if (token.volume24h > 0) {
        const volScore = Math.min(1, Math.log10(token.volume24h / 1000) / Math.log10(500));
        score += volScore * W.VOLUME_WEIGHT;
        breakdown.volume = +(volScore * W.VOLUME_WEIGHT).toFixed(1);
    }
    
    // MCap/Volume ratio — undervalued = low mcap + high volume
    if (token.mcap > 0 && token.volume24h > 0) {
        const ratio = token.volume24h / token.mcap;
        const ratioScore = Math.min(1, ratio / 2); // 200% vol/mcap = max
        score += ratioScore * W.MCAP_VOLUME_RATIO_WEIGHT;
        breakdown.mcapVolRatio = +(ratioScore * W.MCAP_VOLUME_RATIO_WEIGHT).toFixed(1);
    }
    
    // Buy pressure
    if (token.buys24h + token.sells24h > 0) {
        const buyRatio = token.buys24h / (token.buys24h + token.sells24h);
        const buyScore = Math.max(0, (buyRatio - 0.5) * 2); // 50%=0, 100%=1
        score += buyScore * W.BUY_PRESSURE_WEIGHT;
        breakdown.buyPressure = +(buyScore * W.BUY_PRESSURE_WEIGHT).toFixed(1);
    }
    
    // Age freshness
    if (token.ageMs > 0) {
        const hoursOld = token.ageMs / 3600000;
        const ageScore = Math.max(0, 1 - (hoursOld / 24)); // 0h=1.0, 24h=0.0
        score += ageScore * W.AGE_WEIGHT;
        breakdown.age = +(ageScore * W.AGE_WEIGHT).toFixed(1);
    }
    
    // Liquidity health
    if (token.liquidity > 0) {
        const liqScore = Math.min(1, Math.log10(token.liquidity / 1000) / Math.log10(100));
        score += liqScore * W.LIQUIDITY_WEIGHT;
        breakdown.liquidity = +(liqScore * W.LIQUIDITY_WEIGHT).toFixed(1);
    }
    
    // Social signals
    let socialCount = 0;
    if (token.website) socialCount++;
    if (token.twitter) socialCount++;
    if (token.telegram) socialCount++;
    const socialScore = socialCount / 3;
    score += socialScore * W.SOCIAL_WEIGHT;
    breakdown.social = +(socialScore * W.SOCIAL_WEIGHT).toFixed(1);
    
    // Transaction velocity (more txns in last hour vs 24h avg = accelerating)
    if (token.txns1h > 0 && token.txns24h > 0) {
        const hourlyAvg = token.txns24h / 24;
        const velocity = token.txns1h / Math.max(hourlyAvg, 1);
        const velScore = Math.min(1, velocity / 3); // 3x avg = max
        score += velScore * W.TXN_VELOCITY_WEIGHT;
        breakdown.velocity = +(velScore * W.TXN_VELOCITY_WEIGHT).toFixed(1);
    }
    
    return { 
        score: Math.round(Math.min(score, 100)), 
        breakdown 
    };
}

function passesAlphaFilter(token) {
    const F = CONFIG.ALPHA_FILTERS;
    const reasons = [];
    
    // MCap range
    if (token.mcap < F.MIN_MCAP) reasons.push(`mcap ${fmt(token.mcap)} < ${fmt(F.MIN_MCAP)}`);
    if (token.mcap > F.MAX_MCAP) reasons.push(`mcap ${fmt(token.mcap)} > ${fmt(F.MAX_MCAP)}`);
    
    // Volume
    if (token.volume24h < F.MIN_VOLUME_24H) reasons.push(`vol ${fmt(token.volume24h)} < ${fmt(F.MIN_VOLUME_24H)}`);
    
    // Transactions
    if (token.txns24h < F.MIN_TXNS_24H) reasons.push(`txns ${token.txns24h} < ${F.MIN_TXNS_24H}`);
    
    // Buy ratio
    if (token.buys24h + token.sells24h > 0) {
        const buyRatio = token.buys24h / (token.buys24h + token.sells24h);
        if (buyRatio < F.MIN_BUY_RATIO) reasons.push(`buy ratio ${(buyRatio*100).toFixed(0)}% < ${(F.MIN_BUY_RATIO*100)}%`);
    }
    
    // Age
    if (token.ageMs !== null) {
        const ageHours = token.ageMs / 3600000;
        if (ageHours > F.MAX_AGE_HOURS) reasons.push(`age ${fmtAge(token.ageMs)} > ${F.MAX_AGE_HOURS}h`);
        const ageMins = token.ageMs / 60000;
        if (ageMins < F.MIN_AGE_MINUTES) reasons.push(`age ${ageMins.toFixed(0)}m < ${F.MIN_AGE_MINUTES}m (too new)`);
    }
    
    // Liquidity
    if (token.liquidity < F.MIN_LIQUIDITY) reasons.push(`liq ${fmt(token.liquidity)} < ${fmt(F.MIN_LIQUIDITY)}`);
    
    // Social requirements
    if (F.REQUIRE_WEBSITE && !token.website) reasons.push('no website');
    if (F.REQUIRE_TWITTER && !token.twitter) reasons.push('no twitter');
    if (F.REQUIRE_TELEGRAM && !token.telegram) reasons.push('no telegram');
    
    return { 
        pass: reasons.length === 0, 
        reasons 
    };
}

// ═══════════════════════════════════════════════════════════════
// MAIN SCAN CYCLE
// ═══════════════════════════════════════════════════════════════

async function runScan() {
    if (state.isScanning) {
        log('warn', 'Scan already in progress, skipping');
        return;
    }
    
    state.isScanning = true;
    state.scanNumber++;
    const scanStart = Date.now();
    
    log('scan', `═══ SCAN #${state.scanNumber} STARTED ═══`);
    
    try {
        // Phase 1: Fetch raw data from both sources
        log('scan', 'Phase 1: Fetching Pump.fun + DexScreener…');
        const [pumpTokens, dexTokens] = await Promise.all([
            fetchPumpFunCoins(),
            fetchDexScreenerNew(),
        ]);
        
        log('info', `Fetched ${pumpTokens.length} pump.fun tokens, ${dexTokens.length} dexscreener tokens`);
        
        // Phase 2: Merge and deduplicate
        const tokenMap = new Map();
        
        // Add pump.fun tokens
        pumpTokens.forEach(t => {
            if (t.address) tokenMap.set(t.address, t);
        });
        
        // Merge dexscreener social data into pump tokens, add new ones
        dexTokens.forEach(d => {
            if (!d.address) return;
            if (tokenMap.has(d.address)) {
                const existing = tokenMap.get(d.address);
                existing.website = existing.website || d.website || '';
                existing.twitter = existing.twitter || d.twitter || '';
                existing.telegram = existing.telegram || d.telegram || '';
                existing.image = existing.image || d.image || '';
                existing.boostAmount = d.boostAmount || 0;
            } else {
                tokenMap.set(d.address, {
                    ...d,
                    name: '',
                    ticker: '',
                    mcap: 0,
                    volume24h: 0
                });
            }
        });