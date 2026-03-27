# SILENT-001 PCB Design

## Board Specifications
- **Dimensions:** 50mm x 35mm
- **Layers:** 4 (Signal/Power/Power/Signal)
- **Thickness:** 1.6mm
- **Surface Finish:** ENIG (Electroless Nickel Immersion Gold)
- **Impedance Control:** Yes, 90Ω differential for USB
- **Min Via:** 0.3mm drill
- **Min Trace:** 0.1mm (4mil)

## Stackup
| Layer | Type | Thickness |
|-------|------|-----------|
| Top | Signal | 0.035mm Cu |
| Dielectric 1 | Prepreg | 0.1mm |
| Internal 1 | Power Plane | 0.035mm Cu |
| Dielectric 2 | Core | 1.2mm |
| Internal 2 | Ground Plane | 0.035mm Cu |
| Dielectric 3 | Prepreg | 0.1mm |
| Bottom | Signal | 0.035mm Cu |

## Key Components Placement
1. **MCU (U1):** Center - STM32L476RGT6 (LQFP-64)
2. **ADC (U10):** Top edge - ADS131M08
3. **INAs (U2-U9):** Left/right edges - 8x INA333 for EMG
4. **USB (U13):** Left edge - USB-C mid-mount
5. **Regulators (U11-U12):** Bottom right - 3.3V & 5V
6. **Crystal (Y1):** Bottom center - 8MHz HSE

## PCB Ordering Instructions (JLCPCB)

1. Go to <https://jlcpcb.com>
2. Upload `SILENT-001.zip` (gerbers + pos file + bom)
3. PCB Settings:
   - Layers: 4
   - Dimensions: 50 x 35 mm
   - Quantity: 5 (or 10 for better price)
   - Thickness: 1.6mm
   - Color: Green (or choose preference)
   - Surface Finish: ENIG
   - Cu Weight: 1oz outer / 0.5oz inner
4. PCB Assembly:
   - Enable "PCB Assembly"
   - Assembly Side: Top only
   - Upload BOM_CPL.xlsx (combined from jlcpcb_pos.csv + BOM)
5. Expected cost: ~$70-90 including shipping (5 boards assembled)

## Gerber Files Included
- `SILENT-001.GTL` - Top layer
- `SILENT-001.G1` - Internal layer 1 (power)
- `SILENT-001.G2` - Internal layer 2 (ground)
- `SILENT-001.GBL` - Bottom layer
- `SILENT-001.GTS` - Top solder mask
- `SILENT-001.GBS` - Bottom solder mask
- `SILENT-001.GTO` - Top silkscreen
- `SILENT-001.GBO` - Bottom silkscreen
- `SILENT-001.GKO` - Board outline
- `SILENT-001.drl` - Drill file

## Design Notes
- Keep high-speed traces (USB) away from analog inputs
- EMG traces are routed differentially with 10mil spacing
- Ground vias placed every 10mm around RF-sensitive areas
- Shielding option: Can add grounded copper pour under EMG inputs
