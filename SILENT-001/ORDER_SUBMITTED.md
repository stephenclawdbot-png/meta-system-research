# SILENT-001 PCB Order Submission Status

**Submission Date:** 2026-03-28  
**Status:** ⏳ **PENDING_MANUAL_SUBMISSION**  
**Order Type:** Real hardware requiring manual website submission

---

## 📦 Order Package Validation: ✅ PASSED

```bash
$ python3 procurement/jlcpcb_order.py --validate
============================================================
SILENT-001 JLCPCB Order Validation
============================================================
✅ Loaded BOM: 70 components
✅ Loaded CPL: 70 placements
   - Top side: 69 placements
   - Bottom side: 1 placements
✅ Loaded Digi-Key sourcing list: 6 parts
✅ Gerber archive verified: 11 layers
✅ BOM/CPL cross-reference: MATCHED
============================================================
✅ Order package validation: PASSED
============================================================
```

---

## 🌐 Order Submission Method: MANUAL (No API Available)

**Findings:** JLCPCB does not offer a public REST API for programmatic order submission. All orders must be placed through their web interface at [jlcpcb.com](https://jlcpcb.com).

---

## 📋 Step-by-Step Submission Instructions

### Step 1: Prepare JLCPCB Account
1. Visit [jlcpcb.com](https://jlcpcb.com)
2. Sign in or create free account
3. Verify email if new account

### Step 2: Upload Gerbers
**File:** `production/gerbers/SILENT-001_Gerbers.zip`

1. Click "Quote Now" or "Order Now"
2. Upload: `production/gerbers/SILENT-001_Gerbers.zip`
3. Wait for auto-analysis (takes ~10-30 seconds)

### Step 3: Configure PCB Settings
| Parameter | Setting |
|-----------|---------|
| Base Material | FR-4 |
| Layers | **4** |
| Dimensions | 50mm × 35mm (auto-detected) |
| Qty | **10** (or 20 if budget allows) |
| Thickness | **1.6mm** |
| Surface Finish | **ENIG** |
| Copper Weight | 1oz (35μm) |
| Solder Mask Color | Green (default) |
| Silkscreen | White |
| Via Covering | Tented |
| Impedance Control | No |
| Material Type | TG155-160 |

**Expected PCB Cost:** $20-25 for 10pcs

### Step 4: Enable PCB Assembly
1. Check "**PCB Assembly**" option
2. Assembly Side: **Top Side**
3. Tooling Holes: **Yes** (recommended - 4 holes)
4. Click "Confirm"

### Step 5: Upload BOM
**File:** `production/SILENT-001_BOM_JLCPCB.csv`

**Upload Link:** `jlcpcb.com` → Order page BOM section

After upload, wait for JLCPCB to validate all LCSC part numbers. Verify:
- ✅ All parts show as "Matched" or "Extended/Basic Library"
- ✅ No parts listed as "Not Found"

### Step 6: Upload CPL
**File:** `production/SILENT-001_CPL_JLCPCB.csv`

**Upload Link:** `jlcpcb.com` → Order page CPL section

### Step 7: Review Component Placement
This is CRITICAL - visually verify every component:

**Components to verify in 3D previewer:**

| Designator | Part Type | Rotation Check |
|------------|-----------|----------------|
| U1 | STM32L476 LQFP-64 | Pin 1 at top-left (0°) |
| U2-U9 | INA333 VSSOP-8 | Verify orientation |
| U10 | ADS131M08 TQFP-32 | Pin 1 position |
| U11-U12 | AMS1117 SOT-223 | Tab alignment |
| **U13** | **USB-C Mid-Mount** | **⚠️ MOST CRITICAL - verify pins face board** |
| U14 | USBLC6-2 SOT23-6 | Standard orientation |
| U15 | Crystal HC-49S | On BOTTOM layer - verify |

**Fix rotations if needed:** JLCPCB allows adjusting rotation in the previewer before checkout.

### Step 8: Review Assembly Quote
After component matching:

| Cost Component | Estimated |
|----------------|-----------|
| PCB Fabrication (10x) | $20-25 |
| Assembly Fee | ~$10-15 |
| Component Parts | ~$35-45 |
| Engineering Fee | Included |
| **Subtotal** | **~$65-85** |
| Shipping (DHL Express) | ~$20-30 |
| **TOTAL** | **~$85-115** |

### Step 9: Checkout
1. Enter shipping address
2. Select "DHL Express" for speed (~3-7 days)
3. Or use "JLCPCB Standard" for economy (~15-30 days)
4. Complete payment (Credit Card, PayPal, etc.)
5. Save Order Confirmation Number

---

## 🔌 Digi-Key Through-Hole Connector Order

These connectors are **NOT** included in JLCPCB assembly (through-hole, user-assembled).

### Shopping Cart Links
**Digi-Key URL:** https://www.digikey.com

### Parts to Order

| Designator | Digi-Key PN | Description | Qty | Est. Unit $ |
|------------|-------------|-------------|-----|-------------|
| J1 (SWD) | 952-2269-ND | Header 1x4 TH 2.54mm | 20 | $0.15 |
| J2,J3 (EMG) | 952-2273-ND | Header 1x8 TH 2.54mm | 40 (2 per board) | $0.25 |
| J4 (UART) | 952-2269-ND | Header 1x4 TH 2.54mm | 20 | $0.15 |
| J5 (Power) | 952-2267-ND | Header 1x2 TH 2.54mm | 20 | $0.12 |
| TP1,TP2 | 5000K-ND | Test Point SMD Red | 40 (2 per board) | $0.18 |

**Digi-Key Order Total:** ~$35-45 (includes spares)

**Direct Digi-Key Search Links:**
- 952-2269-ND: https://www.digikey.com/en/products/detail/952-2269-ND
- 952-2273-ND: https://www.digikey.com/en/products/detail/952-2273-ND
- 952-2267-ND: https://www.digikey.com/en/products/detail/952-2267-ND
- 5000K-ND: https://www.digikey.com/en/products/detail/5000K-ND

**Shipping:** Standard Digi-Key shipping ~3-5 days to most locations.

---

## 📅 Expected Delivery Timeline

```
T+0 days    → Order submitted (manual submission)
T+1 day     → JLCPCB engineering review
T+2-6 days  → PCB fabrication
T+7-10 days → Component sourcing + SMT assembly
T+11-14 days→ Testing & QC
T+14-21 days→ DHL Express delivery
─────────────────────────────────
Total Lead Time: ~2-3 weeks
```

**Digi-Key components:** ~3-5 days shipping (order separately)

**Recommended Order:** Place both orders same day. Digi-Key parts often arrive before JLCPCB boards.

---

## 📊 Order Files Reference

### JLCPCB Upload Package
```
/Users/clawdbot/.openclaw/workspace/SILENT-001/production/
├── gerbers/SILENT-001_Gerbers.zip    ← Gerber files (11 layers)
├── SILENT-001_BOM_JLCPCB.csv         ← Bill of Materials (70 components)
└── SILENT-001_CPL_JLCPCB.csv         ← Component Placement
```

### Supporting Documents
```
/Users/clawdbot/.openclaw/workspace/SILENT-001/
├── PROCUREMENT.md                    ← Full procurement guide
├── production/JLCPCB_ORDER_PACKAGE.md  ← Detailed order specs
└── procurement/order_summary.html    ← Visual order summary
```

---

## ✅ Pre-Order Checklist (Complete Before Submitting)

- [ ] Reviewed PCB settings (4-layer, 1.6mm, ENIG)
- [ ] Gerbers uploaded without errors
- [ ] All 4 copper layers detected by JLCPCB
- [ ] BOM uploaded, all components matched
- [ ] CPL uploaded, coordinates valid
- [ ] Component rotations verified in 3D preview
- [ ] USB-C connector (U13) orientation DOUBLE-CHECKED
- [ ] Crystal (U15) confirmed on bottom layer
- [ ] Shipping address correct
- [ ] Payment method ready
- [ ] Digi-Key cart prepared with connectors

---

## 📸 Screenshot Requirements

**When submitting order, capture:**
1. PCB settings screenshot (all parameters)
2. BOM match success screenshot (all parts green)
3. Component placement 3D view screenshot
4. Order confirmation page with order number

**Save screenshots to:** `SILENT-001/docs/order_screenshots/`

---

## 📝 Order Confirmation Template

Once submitted, fill in:

| Field | Value |
|-------|-------|
| JLCPCB Order Number | _______________ |
| Order Date | _______________ |
| Quantity Ordered | _______________ |
| Total Cost USD | _______________ |
| Shipping Method | _______________ |
| Expected Delivery | _______________ |
| Digi-Key Order # | _______________ |

---

## 🚨 Important Notes

1. **USB-C Connector (U13):** This is a MID-MOUNT connector. JLCPCB's automated placement may get rotation wrong. **Triple-check in 3D preview.**

2. **Crystal (U15):** Placed on bottom layer - verify it's assigned correctly in CPL.

3. **Assembly Verification:** After receiving boards, visually inspect U1 (STM32) and U10 (ADC) soldering - these have fine-pitch leads prone to bridging.

4. **Quantity Recommendation:** Order 10 boards minimum. First 2-3 may have issues; having spares is critical for bring-up testing.

5. **Order Window:** JLCPCB often has sales. Check for promotions before ordering - can save 10-20%.

---

## 🔗 Quick Links

| Resource | URL |
|----------|-----|
| JLCPCB Home | https://jlcpcb.com |
| JLCPCB Assembly Guide | https://jlcpcb.com/help/article/PCB-Assembly-SMT-Service |
| Digi-Key Home | https://www.digikey.com |
| LCSC Parts Search | https://lcsc.com |
| Order Status | Sign in at jlcpcb.com → Order History |

---

## 🎯 Next Steps After Manual Submission

1. **Place JLCPCB order** via website (following steps above)
2. **Place Digi-Key order** for connectors
3. **Update this file** with actual order numbers
4. **Create daily/heartbeat reminder** to check order status
5. **Prepare assembly station** for through-hole soldering
6. **On delivery:** Run post-assembly verification tests

---

**Order Package Generated:** 2026-03-28T05:26:00+08:00  
**Validation Status:** ✅ PASSED  
**Submission Status:** ⏳ AWAITING MANUAL SUBMISSION

---

*This order is for real hardware. All files are validated and ready. Awaiting human completion of web order forms.*
