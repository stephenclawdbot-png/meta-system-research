# COLLABORATION DIRECTIVE: R02 (Materials) + R06 (Energy)
**Cycle 2 Mission: Smart Dust Specification & Power Architecture**

---

## Objective
Design the optimal passive retroreflective particle for AETHER-S and validate the acoustic levitation power budget.

---

## Background from Cycle 1

**The Visibility Crisis:**
- Initial target: 10^6 particles/m³ = visible fog
- AETHER-S revision: 10^4 particles/m³ (100x reduction)

**The New Requirements:**
1. **Passive particles** - No onboard power (eliminates complexity)
2. **Retroreflective** - Return light to source regardless of angle
3. **Small** - <50 microns to minimize visibility
4. **Levitate-able** - Must work with acoustic standing wave

---

## Your Collaboration Tasks

### R02 (Materials Lead): Particle Design

**Task 1: Size Optimization**

**The trade-off:**
| Size | Visibility | Retroreflection efficiency | Levitation stability |
|------|-----------|---------------------------|---------------------|
| 10μm | Low | Poor (diffraction) | Poor |
| 50μm | Medium | Good | Good |
| 100μm | High | Excellent | Excellent |

**Calculate:**
- Scattering cross-section vs size
- At 10^4 particles/m³, what size maintains acceptable visibility?
- Reference: <1% scattering for "invisible" perception

**Deliverable:** Recommended size range with justification

---

**Task 2: Retroreflector Geometry**

**Options:**
1. **Corner cube reflectors** (glass prism) - 100% efficiency theoretical
2. **Microspheres** (glass beads) - Cat's eye reflectors, ~50% efficiency
3. **Holographic film** - Diffractive, angle-dependent
4. **Photonic crystal** - Wavelength selective, complex fabrication

**Evaluate:**
- Efficiency at small scale (50μm)
- Fabrication complexity
- Cost per particle
- Broadband vs narrowband response

**Deliverable:** Recommended geometry + material stack

---

**Task 3: Mass Density & Acoustic Response**

**Critical:** Particles must be able to levitate in kHz acoustic field.
- Typical acoustic levitation: 20-40 kHz
- Optimal particle size: comparable to acoustic wavelength/2
- Acoustic wavelength at 28kHz: ~12mm (in air)
- Particle size: 50μm = 1/240th of wavelength

**Question:** Can 50μm particles levitate at 28kHz?

**Research:** Acoustic radiation pressure on small particles
```
F_rad ≈ (πr²)(E_acoustic)/c × Q_factor
```
Where:
- r = particle radius
- E = acoustic energy density
- c = speed of sound
- Q = quality factor (geometry dependent)

**Deliverable:** Minimum acoustic intensity required for levitation

---

**Task 4: Particle Manufacturing**

**Scale requirements:**
- 10^4 particles/m³ × 40m³ room = 400,000 particles per room
- Need: Mass production method

**Options:**
1. **Glass microspheres** (commercially available, reflective coating added)
2. **MEMS fabrication** (corners cubes in silicon, expensive)
3. **Polymer molding** (inexpensive, lower quality)

**Deliverable:** Manufacturing recommendation + cost estimate

---

### R06 (Energy Lead): Power & Delivery

**Task 1: Acoustic Levitation Power Budget**

**Calculate for room-scale:**
- Room: 4m × 4m × 2.5m = 40m³
- Acoustic field: standing wave at 28kHz
- Particles: 10^4/m³ = 400,000 total
- Position: pressure nodes (antinodes? check physics)

**Parameters to determine:**
1. Acoustic intensity needed per particle: ? W/m²
2. Total acoustic power: ? W
3. Transducer efficiency: ~50% (electrical to acoustic)
4. **Total electrical power: ? W**

**Reference data:**
- Typical lab acoustic levitation: 10-30W for single object
- Ultrasonic cleaning baths: 50-100W/L
- But: Only need to maintain position, not agitate

**Deliverable:** Power requirement for levitation field

---

**Task 2: Emitter Power Budget**

**From R01/R03 analysis:**
- ~100 emitters needed
- Each emitter delivers light to particles
- Reflected light must be visible against ambient

**Calculate:** Optical power per emitter
- Assume: 10% retroreflectivity, 10mW reflected = visible
- Then: 100mW per emitter needed
- With 100 emitters: **10W optical total**

**Add:**
- Scanner/servo power: ~1W per emitter
- Control electronics: ~1W per emitter
- **Total per emitter: ~2W**
- **100 emitters: ~200W total**

**Deliverable:** Complete system power budget

---

**Task 3: Power Distribution Strategy**

**Challenge:** 100 emitters around room perimeter need power

**Options:**
1. **Wired:** Install power rails along ceiling perimeter
   - Pros: Reliable, no battery maintenance
   - Cons: Installation complexity, aesthetic impact

2. **PoE (Power over Ethernet):** Each emitter on network + power
   - Pros: Single cable, data + power
   - Cons: Requires Ethernet infrastructure

3. **Local power + wireless data:** Battery/small supply at each emitter
   - Pros: Minimal wiring
   - Cons: Battery maintenance, power constraints

4. **Wireless power beaming:** IR laser to photovoltaic receivers
   - Pros: Zero wiring
   - Cons: Efficiency losses, alignment challenges

**Deliverable:** Recommended power architecture with trade-offs

---

**Task 4: Energy Storage (Optional)**

**If particles need energy:**
- Capacitors for burst modulation
- Photovoltaic cells on particles
- Energy harvesting from acoustic field

**Note:** AETHER-S uses passive particles, but may need active in future.
**Evaluate:** Energy harvesting feasibility anyway (for future cycles).

---

## Joint Deliverables

### 1. Particle Specification Sheet

| Parameter | Value | Tolerance |
|-----------|-------|-----------|
| Size | ? μm | ±? μm |
| Material | ? | - |
| Geometry | ? | - |
| Retroreflectivity | ? % | ±? % |
| Mass | ? μg | ±? % |
| Cost per particle | $? | - |

### 2. Acoustic System Specification

| Parameter | Value |
|-----------|-------|
| Frequency | ? kHz |
| Intensity at particle | ? W/m² |
| Total acoustic power | ? W |
| Electrical power | ? W |
| Transducer count | ? |
| Transducer placement | ? |

### 3. Full System Power Budget

| Component | Power | Notes |
|-----------|-------|-------|
| Acoustic levitation | ? W | ? |
| Laser emitters (100) | ? W | ? |
| Scanner servos | ? W | ? |
| Control electronics | ? W | ? |
| Computation | ? W | Assume 1 PC |
| **TOTAL** | **? W** | Target: <1kW |

### 4. Cost Estimate

| Component | Unit Cost | Quantity | Total |
|-----------|-----------|----------|-------|
| Particles | $? | 400,000 | $? |
| Emitters | $? | 100 | $? |
| Transducers | $? | ? | $? |
| Infrastructure | $? | 1 | $? |
| **TOTAL** | | | **$?** |

---

## Open Questions

- Can particles survive long-term in acoustic field (degradation)?
- How to introduce/remove particles from room?
- What happens when particles accumulate on surfaces?
- Environmental factors: humidity, dust, air currents?

---

## Success Criteria

✅ Particle size/material selected  
✅ Retroreflector efficiency quantified  
✅ Acoustic levitation power calculated  
✅ Full system power budget ≤1kW  
✅ Cost estimate for prototype  

---

## Coordination with R01/R03

**Need from R01/R03:**
- Required reflected light intensity for visibility
- Emitter count and placement
- Scanning frequency requirements

**Provide to R01/R03:**
- Particle reflectivity coefficient
- Recommended emitter wavelength
- Particle distribution stability over time

**Deliver findings to:** CYCLE_LOG.md (update with "R02-R06 Results")

**Time limit:** 15 minutes (Cycle 2 duration)
