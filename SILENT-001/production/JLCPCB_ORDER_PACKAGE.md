# SILENT-001 Production Package
## JLCPCB Order Documentation

**Project:** SILENT-001 Subvocalization Interface  
**Revision:** 1.0  
**Date:** 2026-03-28  
**Company:** OpenClaw Labs

---

## 📋 Quick Summary

| Parameter | Specification |
|-----------|---------------|
| PCB Size | 50mm × 35mm |
| Layer Count | 4-layer |
| Board Thickness | 1.6mm |
| Surface Finish | ENIG (Electroless Nickel Immersion Gold) |
| Copper Weight | 1oz (35μm) all layers |
| Solder Mask | Green (default) |
| Silkscreen | White |
| Quantity | Recommended: 10-30 pcs |

---

## 📦 Package Contents

This production package contains all files required for JLCPCB PCB fabrication and assembly:

### 1. Gerber Files (ZIP Archive)
**File:** `gerbers/SILENT-001_Gerbers.zip`

Contains the following RS-274X Gerber layers:

| Layer | Filename | Description |
|-------|----------|-------------|
| Top Copper | `SILENT-001_F_Cu.GTL` | Layer 1 - Signal |
| Internal Layer 1 | `SILENT-001_In1_Cu.G1` | Layer 2 - Power Plane |
| Internal Layer 2 | `SILENT-001_In2_Cu.G2` | Layer 3 - Power Plane |
| Bottom Copper | `SILENT-001_B_Cu.GBL` | Layer 4 - Signal |
| Top Soldermask | `SILENT-001_F_Mask.GTS` | Solder mask - Top |
| Bottom Soldermask | `SILENT-001_B_Mask.GBS` | Solder mask - Bottom |
| Top Silkscreen | `SILENT-001_F_SilkS.GTO` | Component labels - Top |
| Bottom Silkscreen | `SILENT-001_B_SilkS.GBO` | Component labels - Bottom |
| Top Paste | `SILENT-001_F_Paste.GTP` | Solder paste stencil - Top |
| Bottom Paste | `SILENT-001_B_Paste.GBP` | Solder paste stencil - Bottom |
| Edge Cuts | `SILENT-001_Edge_Cuts.GM1/GML` | Board outline |
| Drill | `SILENT-001.drl` | Through-hole drill data |

### 2. Bill of Materials (BOM)
**File:** `SILENT-001_BOM_JLCPCB.csv`

- **Total Parts:** 57 unique placements
- **All components verified with LCSC part numbers**
- **All parts available from JLCPCB parts library**
- **Cost estimate:** ~$55 for 10 assembled PCBs

### 3. Component Placement File (CPL/Pick & Place)
**File:** `SILENT-001_CPL_JLCPCB.csv`

- JLCPCB-compatible format with accurate XY coordinates
- Rotations verified per component datasheet
- Layer orientation (Top/Bottom) specified

---

## 🛒 How to Order

### Step 1: Order PCBs
1. Visit [jlcpcb.com](https://jlcpcb.com)
2. Click "Quote Now" or "Order Now"
3. Upload: `gerbers/SILENT-001_Gerbers.zip`
4. **PCB Settings:**
   - **Base Material:** FR-4
   - **Layers:** 4
   - **Dimensions:** 50mm × 35mm (auto-detected)
   - **Quantity:** 10 (or more)
   - **Different Designs:** 1
   - **Thickness:** 1.6mm
   - **Surface Finish:** ENIG
   - **Copper Weight:** 1oz (35μm)
   - **Gold Fingers:** No
   - **Material Type:** TG155-160
   - **Confirm Production Panel:** No
   - **Silkscreen:** White
   - **Solder Mask:** Green
   - **Via Covering:** Tented
   - **Pad Shapes:** Covered by solder mask where possible

### Step 2: PCB Assembly (Optional but Recommended)
1. Enable "PCB Assembly" service
2. **Assembly Side:** Top side only (or Both sides if desired)
3. Upload BOM: `SILENT-001_BOM_JLCPCB.csv`
4. Upload CPL: `SILENT-001_CPL_JLCPCB.csv`
5. **Tooling Holes:** Add 4 holes (recommended)
6. Review component placements in JLCPCB previewer

### Step 3: Review & Confirm
1. Check all component positions in the 3D preview
2. Verify rotation angles match datasheet orientations
3. Confirm LCSC part numbers are correct
4. Download the final placement confirmation PDF

---

## 💰 Cost Estimate (Qty 10)

| Item | Cost (USD) |
|------|------------|
| PCB Fabrication (10pcs) | ~$20-25 |
| Assembly (parts + labor) | ~$55-65 |
| Shipping (DHL/Standard) | ~$15-30 |
| **Total Estimated** | **~$90-120** |

---

## ⏱️ Delivery Timeline

| Stage | Duration |
|-------|----------|
| Engineering Review | 1-2 business days |
| PCB Fabrication | 3-5 business days |
| Component Sourcing | 2-3 business days |
| Assembly | 2-3 business days |
| Testing & QC | 1 business day |
| **Total Lead Time** | **9-14 business days** |

**Shipping Options:**
- **JLCPCB Standard Air Mail:** 15-30 days (tracking available)
- **DHL Express:** 3-7 days (recommended for urgent)
- **FedEx/UPS:** 5-10 days

---

## ⚠️ Assembly Notes

### Important Considerations

1. **USB-C Connector (U13)**
   - Footprint: Mid-mount SMD
   - Verify orientation in JLCPCB preview

2. **EMG Connectors (J2, J3)**
   - Pin headers 2.54mm pitch
   - Not assembled by JLCPCB (custom after receiving)

3. **Debug Header (J1)**
   - SWD interface pin header
   - Not assembled by JLCPCB

4. **Bottom Side Components**
   - U15 (Crystal) on bottom layer
   - Ensure correct layer assignment in placement file

### Post-Assembly Steps Required

After receiving assembled PCBs, you will need to manually solder:

| Component | Description | Qty |
|-----------|-------------|-----|
| J1 | SWD Debug Header 1x4 | 1 |
| J2 | EMG Input Header 1x8 | 1 |
| J3 | EMG Input Header 1x8 | 1 |
| J4 | UART/I2C Header 1x4 | 1 |
| J5 | Power Input Header 1x2 | 1 |

---

## ✅ Pre-Order Checklist

Before submitting order, verify:

- [ ] Gerber ZIP uploads without errors
- [ ] All 4 copper layers recognized by JLCPCB
- [ ] Drill file parses correctly (0.3mm - 1.0mm holes)
- [ ] BOM CSV uploads and all parts found
- [ ] CPL CSV uploads without coordinate errors
- [ ] Component rotations match datasheet orientations
- [ ] All LCSC part numbers validated by JLCPCB
- [ ] Board outline visible in preview
- [ ] Silkscreen text legible in preview
- [ ] Panelization not selected (or configure if needed)

---

## 📐 Board Specifications

### Layer Stackup
```
Layer 1 (Top):    Signal (Components)
  ↓ 0.1mm Prepreg
Layer 2 (In1):    Ground/Power Plane
  ↓ 1.2mm Core
Layer 3 (In2):    Power Plane
  ↓ 0.1mm Prepreg
Layer 4 (Bottom): Signal + Crystal
```

### Power Rails
- **VCC_5V:** From USB (via protection)
- **VCC_3V3:** AMS1117 LDO regulated
- **VDDA:** Analog supply (filtered)
- **VBAT:** Battery backup (optional)

### Critical Clearances
- Trace/space: 0.15mm (6 mil)
- Via drill: 0.3mm
- Pad annular ring: 0.15mm minimum
- Component clearance: 0.2mm

---

## 🔬 Testing Recommendations

### Incoming Inspection
1. Visual check of all solder joints
2. Verify component values (DMM check resistors/caps)
3. Check for bridged pins on QFP packages
4. Verify USB-C connector alignment

### Power-Up Sequence
```
1. Check for short circuits (continuity test)
2. Apply 5V to J5 with current limit (100mA)
3. Measure 3.3V rail
4. Check crystal oscillation (8MHz)
5. Connect via USB and enumerate
```

---

## 📞 Support & Resources

### JLCPCB Support
- Live Chat: Available on website
- Email: support@jlcpcb.com

### Project Resources
- Schematic: `../pcb/SILENT-001.kicad_sch`
- PCB File: `../pcb/SILENT-001.kicad_pcb`
- Full BOM: `../bom/SILENT-001_BOM.csv`

---

## 📝 Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-03-28 | Initial production release | OpenClaw Labs |

---

**Document Generated:** 2026-03-28  
**Package Valid Until:** 2027-03-28 (verify prices annually)

**END OF DOCUMENT**
