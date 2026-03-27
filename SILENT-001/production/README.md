# SILENT-001 Production Package

**Project:** SILENT-001 Subvocalization Interface  
**Revision:** 1.0  
**Generated:** 2026-03-28

---

## 🚀 Quick Start

This folder contains everything needed to order fabricated PCBs with assembly from JLCPCB.

**Upload these 3 files to JLCPCB:**
1. `gerbers/SILENT-001_Gerbers.zip` - PCB fabrication files
2. `SILENT-001_BOM_JLCPCB.csv` - Component list with LCSC part numbers
3. `SILENT-001_CPL_JLCPCB.csv` - Component placement coordinates

**See:** `JLCPCB_ORDER_PACKAGE.md` for detailed ordering instructions

---

## 📁 File Inventory

| File | Purpose |
|------|---------|
| `JLCPCB_ORDER_PACKAGE.md` | Complete ordering guide with timeline and settings |
| `README.md` | This file - quick reference |
| `SILENT-001_Gerbers.zip` | All Gerber layers + drill file for PCB fab |
| `SILENT-001_BOM_JLCPCB.csv` | JLCPCB-formatted BOM with 57 components |
| `SILENT-001_CPL_JLCPCB.csv` | Pick & place file for SMT assembly |
| `SILENT-001_BOM_Full.csv` | Complete BOM with pricing info |
| `gerbers/` | Individual Gerber layer files |
| `generate_gerbers.py` | Python script used to generate Gerbers |

---

## 📊 Board Specs

- **Size:** 50mm × 35mm
- **Layers:** 4 (Top, In1, In2, Bottom)
- **Thickness:** 1.6mm
- **Finish:** ENIG
- **Solder Mask:** Green
- **Silkscreen:** White

### Key Components
- U1: STM32L476RGT6 (MCU Core) - `C152425`
- U2-U9: INA333AIDGKR (8 EMG Preamps) - `C48659`
- U10: ADS131M08IPBSR (ADC) - `C2939338`

---

## ⚡ Ordering Steps

1. Go to [jlcpcb.com](https://jlcpcb.com)
2. Upload `SILENT-001_Gerbers.zip`
3. Select: 4-layer, 1.6mm, ENIG finish
4. Enable PCB Assembly
5. Upload `SILENT-001_BOM_JLCPCB.csv` and `SILENT-001_CPL_JLCPCB.csv`
6. Review component placements
7. Place order

**Estimated Cost:** $90-120 for 10 assembled boards
**Lead Time:** 9-14 business days + shipping

---

## ⚠️ Important Notes

- **Headers (J1-J5)** are NOT included in assembly - solder manually after receipt
- **Bottom-side crystal (U15)** placement verified
- All components verified with JLCPCB parts library LCSC numbers
- See `JLCPCB_ORDER_PACKAGE.md` Section "Assembly Notes" for full details

---

## 📞 Support

JLCPCB Help: support@jlcpcb.com  
Project Location: `/Users/clawdbot/.openclaw/workspace/SILENT-001/`
