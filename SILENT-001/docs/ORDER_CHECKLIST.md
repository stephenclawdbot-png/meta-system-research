# SILENT-001 Order Checklist

## Quick Order Summary
- **PCB + Assembly:** JLCPCB (~$70-90)
- **Remaining Components:** Digi-Key (~$20-30)
- **Total Estimated:** $90-120
- **Lead Time:** 5-7 days (PCB), 2-3 days (Digi-Key)

---

## Step 1: JLCPCB Order (PCB + Assembly)

### ✅ Order Link
<https://jlcpcb.com>

### ✅ Required Files
Upload these files from `/SILENT-001/pcb/`:
- [ ] Gerber files (zip all .gtl, .gbl, .gto, etc.)
- [ ] JLCPCB CPL file (`jlcpcb_pos.csv`)
- [ ] BOM file (`jlcpcb_bom.xlsx` - combine CSV into their Excel format)

### ✅ PCB Specifications
| Parameter | Setting |
|-----------|---------|
| Layer | 4 layers |
| Dimensions | 50 x 35 mm |
| Quantity | 5 or 10 |
| Thickness | 1.6mm |
| Color | Green |
| Surface Finish | ENIG (Electroless Nickel Immersion Gold) |
| Copper Weight | 1oz outer, 0.5oz inner |
| Min Hole Size | 0.3mm |
| Impedance Control | Optional (for USB) |

### ✅ Assembly Specifications
| Parameter | Setting |
|-----------|---------|
| Assembly Side | Top only |
| Placement File Format | CPL (pick-and-place) |

### ✅ Components to Assemble (JLCPCB)
See `bom/` folder for full list. Key automated assembly parts:
- U1: STM32L476RGT6
- U2-U9: INA333AIDGKR (8x)
- U10: ADS131M08
- U11-U12: AMS1117 regulators
- Passive components: Resistors, capacitors

**Quantity:** 5 boards minimum for good price break

---

## Step 2: Digi-Key Order (Remaining Parts)

### ✅ Order Link
<https://digikey.com>

### ✅ Part Number Quick List

| Qty | Part Number | Description | Est. Price |
|-----|-------------|-------------|------------|
| 1 | 887-X49SM8SM8MSD2SC-ND | 8MHz crystal | $0.15 |
| 1 | SE3203-ND | 32.768kHz crystal | $0.25 |
| 8 | 296-INA333AIDGKR-ND | INA333 preamp | $2.35/ea |
| 1 | ADS131M08IPBSR-ND | 24-bit ADC | $6.95 |
| 2 | CKN10363-ND | Tactile switches | $0.15/ea |
| 1 | 360-JS202011SCQN-ND | Power slide switch | $0.45 |
| 5 | 952-2269-ND | Headers 1x4 | $0.08/ea |
| 2 | 952-2273-ND | Headers 1x8 | $0.15/ea |
| 1 | 952-2267-ND | Header 1x2 | $0.05 |
| 2 | 5000K-ND | Test points | $0.15/ea |

### ✅ Create BOM Import
Save as `SILENT-001_digikey_bom.csv` and upload to Digi-Key BOM Manager for instant cart creation.

---

## Step 3: Tools & Equipment Check

### ✅ Required Soldering Tools
- [ ] Soldering iron (temperature controlled, 60W+)
- [ ] Solder wire: 63/37 leaded, 0.5mm or 0.8mm
- [ ] Flux: No-clean paste flux
- [ ] Tweezers: Fine-point (ESD-safe)
- [ ] Magnification: Head-mounted magnifier or microscope
- [ ] Desoldering: Copper braid/wick

### ✅ Required Testing Equipment
- [ ] Multimeter (Fluke or equivalent)
- [ ] Oscilloscope (50MHz+ for EMG signal verification)
- [ ] USB-to-Serial adapter (3.3V logic)
- [ ] ST-Link V2 debugger/programmer

### ✅ Consumables
- [ ] Isopropyl alcohol 99% (cleaning)
- [ ] Kimwipes or lint-free cloth
- [ ] Kapton tape (masking during assembly)

---

## Step 4: Pre-Order Verification

### ✅ Design Review
- [ ] Review PCB files in KiCad
- [ ] Check component footprints match datasheets
- [ ] Verify placement files match PCB layout
- [ ] Confirm crystal loading capacitors are correct

### ✅ BOM Verification
- [ ] Cross-check all LCSC part numbers
- [ ] Verify Digi-Key part numbers are active
- [ ] Check for alternatives/components approaching EOL
- [ ] Confirm all passives are in stock

### ✅ Mechanical Check
- [ ] Verify physical dimensions (50x35mm)
- [ ] Confirm connector positions
- [ ] Check mounting hole spacing
- [ ] Validate USB-C mid-mount position

---

## Order Confirmation Log

| Item | Status | Date | Tracking # |
|------|--------|------|------------|
| JLCPCB PCB + Assembly | ⬜ ORDERED | | |
| JLCPCB Shipped | ⬜ | | |
| JLCPCB Received | ⬜ | | |
| Digi-Key Order | ⬜ ORDERED | | |
| Digi-Key Received | ⬜ | | |
| Inspection Complete | ⬜ | | |

---

## Post-Order Actions

1. **After ordering:** Update tracking numbers above
2. **After receiving:** Update build log in `/build-log/`
3. **Issues:** Contact suppliers immediately for any shortages

## Contact Information

**JLCPCB**
- Support: support@jlcpcb.com

**Digi-Key**
- Support: Sales/Service Team
- Live chat available on website
