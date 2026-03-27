# SILENT-001 Assembly Guide

**Document Version:** 1.0  
**Date:** 2026-03-28  
**Skill Level:** Intermediate SMD Soldering  
**Estimated Time:** 2-3 hours

---

## Safety First

⚠️ **Read Before Starting**
- Use ESD-safe workspace (grounded mat, wrist strap)
- Ensure adequate ventilation (soldering fumes)
- Wear eye protection when working with small parts
- Work in well-lit area with magnification available

---

## Required Tools

### Soldering
| Tool | Specification | Purpose |
|------|--------------|---------|
| Soldering Iron | 60W+, temperature controlled | SMD assembly |
| Solder | 63/37 or SAC305, 0.5-0.8mm | General soldering |
| Flux | No-clean paste flux | QFP soldering |
| Desolder Braid | 2-3mm width | Removing excess solder |
| Tweezers | Fine point, ESD-safe | Component handling |
| Magnification | 3-10x minimum | Visual inspection |

### Testing
- Multimeter (continuity, resistance, voltage)
- ST-Link V2 programmer
- USB-C cable
- Oscilloscope (for EMG signal verification)

---

## Assembly Sequence

**CRITICAL:** Do NOT skip steps. Each section must be completed and tested before proceeding.

### Phase 1: Power Section ⏱️ 20 min

#### 1.1 Mount Low-Dropout Regulators (U11, U12)
**Components:**
- U11: AMS1117-3.3 (SOT-223)
- U12: AMS1117-5.0 (SOT-223)
- C5, C6: 4.7µF (0805)
- C7, C8: 10µF (0805)
- L1, L2: Ferrite bead 600Ω (0805)

**Procedure:**
1. Apply flux to pads
2. Tin one pad on each IC footprint
3. Position U11, reflow tinned pad
4. Solder remaining pins (4 pins each)
5. Repeat for U12
6. Mount input/output capacitors

**Inspection:**
- [ ] No bridges between pins
- [ ] Proper orientation (tab matches silkscreen)
- [ ] Capacitors have correct polarity

#### 1.2 Test Power Rails
Connect power input (J5) to 5V supply:

| Test Point | Expected Voltage | Tolerance |
|------------|------------------|-----------|
| TP1 (3V3) | 3.30V | ±0.15V |
| TP2 (5V) | 5.00V | ±0.25V |

**If voltages incorrect:** STOP - debug before proceeding

---

### Phase 2: MCU Section ⏱️ 30 min

#### 2.1 Mount STM32 MCU (U1)
**Component:** STM32L476RGT6 (LQFP-64)

**Procedure (Drag Soldering Method):**
1. Align pin 1 corner marker (dot/triangle)
2. Flux ALL pads generously
3. Solder two diagonal corner pins
4. Apply solder to one row, drag iron across pins
5. Use desolder braid to remove excess/bridges
6. Repeat for all four sides

**Inspection:**
- [ ] All 64 pins soldered (no tombstoning)
- [ ] No solder bridges between pins
- [ ] Pin 1 correctly oriented

#### 2.2 Mount Supporting Components
**Components:**
- C1-C4: 100nF decoupling (0605, 4x)
- C9-C10: 12pF (0605, 2x) - HSE load caps
- C11-C12: 6.8pF (0402, 2x) - LSE load caps
- Y1: 8MHz crystal (HC-49S) - HSE
- Y2: 32.768kHz crystal (FC-135) - LSE

**Procedure:**
1. Mount crystals first (largest components)
2. Mount load capacitors (check values!)
3. Mount decoupling capacitors

**Critical:** Double-check load capacitor values
- HSE: 12pF
- LSE: 6.8pF

#### 2.3 Mount USB Section
**Components:**
- U13: USB-C connector (mid-mount)
- U14: USBLC6-2SC6 (ESD protection)
- R9-R16: 10kΩ pull-ups (0605)

**Procedure:**
1. Apply solder to anchor pads on USB connector
2. Position connector, tack solder one pin
3. Check alignment, adjust if needed
4. Solder all pins
5. Mount ESD protection IC

**Inspection:**
- [ ] USB connector sits flat on board
- [ ] No solder bridges on tiny USBLC6 pins

---

### Phase 3: Analog Front-End ⏱️ 45 min

#### 3.1 Mount Instrumentation Amplifiers (U2-U9)
**Components:** INA333AIDGKR (8x, VSSOP-8)

**Procedure:**
1. Mount U2 first as practice (easiest to access)
2. Apply flux to all pads
3. Position IC, solder one corner pin
4. Check orientation (pin 1 marking)
5. Solder remaining pins
6. Repeat for U3-U9

**Gain Setting:**
Each INA needs gain resistor (R17-R24):
```
Gain = 1 + (100kΩ / Rg)
For Gain = 10: Rg = 11.1kΩ
For Gain = 100: Rg = 1.01kΩ
Use 1kΩ (R17-R24) for Gain = 101
```

#### 3.2 Mount ADC (U10)
**Component:** ADS131M08 (TQFP-32)

This is the most difficult component. Consider:
- Hot air station (ideal)
- Preheater
- Drag soldering with magnification

**Procedure:**
1. Preheat board if available
2. Flux all pads
3. Position IC, tack two corners
4. Solder all pins carefully
5. Check with microscope for bridges

#### 3.3 Mount Passive Components for Analog
**Components:**
- R1-R8: 10kΩ bias (0605)
- R25-R32: 1kΩ protection (0605)
- R33: 10MΩ high-Z bias (0605)
- Filter capacitors as per schematic

---

### Phase 4: Connectors & Mechanical ⏱️ 20 min

#### 4.1 Mount Through-Hole Headers
**Components:**
- J1: SWD debug (1x4 pin header)
- J2: EMG Inputs Ch1-4 (1x8)
- J3: EMG Inputs Ch5-8 (1x8)
- J4: Expansion (I2C/SPI/UART) (1x4)
- J5: Power input (1x2)

**Procedure:**
1. Insert headers from top side
2. Solder on bottom side
3. Cut legs if too long

#### 4.2 Mount User Interface
**Components:**
- SW1, SW2: Tactile switches (reset/user)
- SW3: Slide switch (power)
- D1: Green LED (status)
- D2: Red LED (error)
- TP1, TP2: Test points

**Procedure:**
1. Mount LEDs (check polarity!):
   - Pad with chamfer = CATHODE (-)
   - Cathode usually marked on silkscreen
2. Mount switches (flat side alignment)
3. Mount test points (easy soldering)

#### 4.4 Final Component (D3)
**Component:** Schottky diode (SMA package)

**Procedure:**
- Check polarity (cathode band marked)
- Position per silkscreen
- Solder both ends

---

## Phase 5: Initial Testing ⏱️ 30 min

### 5.1 Visual Inspection
- [ ] No solder bridges on ICs
- [ ] Pin 1 orientations correct
- [ ] Component alignments good
- [ ] No damaged components

### 5.2 Continuity Tests
Use multimeter to check:
- [ ] No shorts between VCC and GND
- [ ] USB D+/D- not shorted
- [ ] Power rails isolated

### 5.3 Power-Up Test
1. Connect 5V to J5
2. Measure voltage at:
   - VCC_3V3 rail: 3.30V ±5%
   - VCC_5V rail: 5.00V ±5%
3. Check USB_VBUS when USB connected

**DO NOT CONNECT USB** if power rails incorrect!

---

## Phase 6: Programming & Verification ⏱️ 45 min

### 6.1 Connect ST-Link
Wire to J1 (SWD header):
| Pin | Signal | Color | ST-Link |
|-----|--------|-------|---------|
| 1 | VCC | Red | 3.3V |
| 2 | GND | Black | GND |
| 3 | SWDIO | Blue | SWDIO |
| 4 | SWCLK | Yellow | SWCLK |

### 6.2 Program Firmware
```bash
# Using OpenOCD
openocd -f interface/stlink.cfg -f target/stm32l4.cfg

# Program using STM32CubeProgrammer
STM32_Programmer_CLI -c port=SWD -w firmware.elf 0x8000000 -v -s
```

### 6.3 Blink Test
First firmware should:
- Blink status LED (D1)
- Output "Hello" on UART
- Initialize ADC

---

## Phase 7: EMG Signal Path Verification ⏱️ 30 min

### 7.1 Inject Test Signal
Connect function generator to EMG input:
- 10mV sine wave
- 100Hz frequency

### 7.2 Verify ADC Operation
Expected readings (via USB CDC or UART):
- Signal present on all channels
- Noise floor < 1mV RMS
- No crosstalk between channels

### 7.3 Channel Crosstalk Test
- Inject signal into Ch1 only
- Verify Ch2-Ch8 show <1% of Ch1 amplitude

---

## Troubleshooting Guide

### Power Section Issues
| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| No 3.3V output | U11 defective | Replace AMS1117 |
| 3.3V low/high | Wrong resistor | Check feedback resistors |
| Excessive heat | Short circuit | Check polarity of caps |

### Programming Issues
| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| No device detected | SWD wiring | Check pinout on J1 |
| Read fails | MCU not powered | Verify 3.3V to MCU |
| Erased but won't program | Protection bits | Mass erase first |

### Analog Section Issues
| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| High noise | Poor grounding | Check ground connections |
| Signal clipping | Wrong gain | Check Rg value |
| No signal | INA defective | Replace instrumentation amp |
| Saturation | DC offset | Check bias resistors |

---

## Assembly Completion Checklist

- [ ] All components soldered per BOM
- [ ] Visual inspection complete
- [ ] Power rails tested and within spec
- [ ] MCU programmed successfully
- [ ] LED blink test passed
- [ ] UART output verified
- [ ] EMG signal path tested
- [ ] All 8 channels functional
- [ ] USB communication working
- [ ] Final visual/documentation photos taken

---

## Next Steps After Assembly

1. **Firmware Development**
   - Implement EMG sampling at 1kHz/channel
   - Add digital filtering (bandpass 10-500Hz)
   - Implement USB CDC for data streaming

2. **Mechanical Integration**
   - Design enclosure for 50x35mm PCB
   - Add electrode attachment mechanism
   - Strain relief for USB cable

3. **Calibration**
   - Calibrate each channel gain
   - Measure noise floor per channel
   - Verify CMRR (Common Mode Rejection Ratio)

---

*Assembly complete. Move to build log for documentation.*
