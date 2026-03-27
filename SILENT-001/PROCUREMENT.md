# SILENT-001 Procurement Documentation

**Project:** SILENT-001 Subvocalization Interface  
**Date:** 2026-03-28  
**Status:** ⏳ Order Ready - Awaiting Placement  

---

## 📋 Overview

This document outlines the complete procurement process for the SILENT-001 hardware prototype, including PCB fabrication, component sourcing, and assembly coordination.

## 💰 Budget Summary

| Category | Estimated Cost (USD) |
|----------|---------------------|
| PCB Fabrication (10x) | $20-25 |
| JLCPCB SMT Assembly | $55-65 |
| Shipping (DHL Express) | $20-30 |
| **JLCPCB Subtotal** | **~$100-120** |
| Digi-Key Connectors* | $5-10 |
| **Grand Total** | **~$110-130** |

*Through-hole connectors shipped separately and assembled manually

---

## 🏭 PCB Fabrication

### Supplier: JLCPCB (jlcpcb.com)

**Board Specifications:**
- **Dimensions:** 50mm × 35mm
- **Layer Count:** 4-layer
- **Material:** FR-4 TG155-160
- **Thickness:** 1.6mm
- **Copper Weight:** 1oz (35μm) all layers
- **Surface Finish:** ENIG (Electroless Nickel Immersion Gold)
- **Solder Mask:** Green
- **Silkscreen:** White
- **Via Treatment:** Tented

### Order Files Location
```
SILENT-001/production/
├── gerbers/SILENT-001_Gerbers.zip    # Gerber RS-274X + Drill
├── SILENT-001_BOM_JLCPCB.csv         # Bill of Materials
└── SILENT-001_CPL_JLCPCB.csv         # Component Placement
```

### Ordering Steps

1. **Visit** [jlcpcb.com](https://jlcpcb.com)
2. **Upload Gerbers:** `production/gerbers/SILENT-001_Gerbers.zip`
3. **Configure PCB:**
   - Base Material: FR-4
   - Layers: 4
   - Quantity: 10 (or preferred)
   - Thickness: 1.6mm
   - Surface Finish: ENIG
   - Copper Weight: 1oz
4. **Enable PCB Assembly**
5. **Upload BOM:** `production/SILENT-001_BOM_JLCPCB.csv`
6. **Upload CPL:** `production/SILENT-001_CPL_JLCPCB.csv`
7. **Review Placement** in online previewer
8. **Submit Order**

---

## 🔧 Component Sourcing

### JLCPCB Assembly (SMT Components)

All surface-mount components are available from JLCPCB's Basic/Extended parts library.

| Component | LCSC | Qty | Notes |
|-----------|------|-----|-------|
| MCU U1 | C152425 | 1 | STM32L476RGT6 |
| INA333 U2-U9 | C48659 | 8 | 8-channel preamps |
| ADC U10 | C2939338 | 1 | ADS131M08 |
| LDO U11, U12 | C6186, C6185 | 2 | 3.3V and 5V regulators |
| USB-C U13 | C168688 | 1 | Mid-mount connector |
| ESD U14 | C2828234 | 1 | USB protection |
| Passives | Various | ~40 | Caps, resistors, ferrites |

### Digi-Key Supplement (User Assembly)

These through-hole components are **not** included in JLCPCB assembly and must be ordered separately.

| Designator | Digi-Key PN | Description | Qty |
|------------|-------------|-------------|-----|
| J1 | 952-2269-ND | SWD Header 1x4 TH | 1 |
| J2, J3 | 952-2273-ND | EMG Headers 1x8 TH | 2 |
| J4 | 952-2269-ND | UART/I2C Header 1x4 TH | 1 |
| J5 | 952-2267-ND | Power Header 1x2 TH | 1 |
| TP1, TP2 | 5000K-ND | Test Points Red | 2 |

**Digi-Key Order Link:**  
https://www.digikey.com (search by part numbers above)

---

## 🤖 Automation

### Order Generator Script

The `jlcpcb_order.py` script automates order validation and generation.

**Usage:**
```bash
cd /Users/clawdbot/.openclaw/workspace/SILENT-001

# Validate order package
python3 procurement/jlcpcb_order.py --validate

# Generate order JSON + HTML summary
python3 procurement/jlcpcb_order.py --generate --quantity 10
```

**Output Files:**
- `procurement/jlcpcb_order.json` - Order data for API submission
- `procurement/order_summary.html` - Human-readable summary

---

## 📦 Delivery Timeline

| Stage | Duration |
|-------|----------|
| JLCPCB - Engineering Review | 1-2 days |
| JLCPCB - PCB Fabrication | 3-5 days |
| JLCPCB - Assembly | 2-4 days |
| JLCPCB - Shipping (DHL) | 3-7 days |
| Digi-Key - Shipping | 3-5 days |
| **Total Lead Time** | **~10-20 days** |

---

## ✅ Order Checklist

### Pre-Order Verification
- [ ] Gerber ZIP uploads without errors
- [ ] All 4 copper layers detected
- [ ] Drill file parses correctly
- [ ] BOM uploaded successfully
- [ ] All components found in JLCPCB library
- [ ] CPL uploaded without coordinate errors
- [ ] Component rotations verified in 3D preview
- [ ] Board outline visible
- [ ] Silkscreen legible

### Post-Assembly Verification
- [ ] Visual inspection of solder joints
- [ ] Continuity test (no shorts)
- [ ] Power-on test (3.3V rail present)
- [ ] Crystal oscillation verified
- [ ] USB enumeration test
- [ ] Solder headers J1-J5
- [ ] Solder test points TP1-TP2

---

## 🔗 External Links

- **JLCPCB:** https://jlcpcb.com
- **Digi-Key:** https://www.digikey.com
- **LCSC Parts:** https://lcsc.com
- **Order Package:** `production/JLCPCB_ORDER_PACKAGE.md`

---

## 📝 Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-03-28 | Initial procurement documentation | OpenClaw Labs |

---

## 📞 Support Contacts

- **JLCPCB Support:** support@jlcpcb.com / Live Chat
- **Digi-Key Support:** 1-800-344-4539
- **Project Lead:** Check PROJECT_REGISTRY.json

---

**Document Generated:** 2026-03-28T05:26:00+08:00  
**Order Status:** READY FOR PLACEMENT
