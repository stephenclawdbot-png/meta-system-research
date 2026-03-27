# R03: Optical Engineer - Cycle 0

## Optical System Design

### Femtosecond Filamentation Approach

**Architecture:**
- Ti:Sapphire laser, 800nm, 50fs pulses
- Chirped pulse amplification (CPA) for safety
- Beam shaping via spatial light modulator (SLM)
- Multiple filament generation from single pulse

**Voxel Addressing:**
- Time-of-flight delay lines
- Rotating mirrors + synchronization
- Holographic beam reconstruction

**Color Generation:**
- Filament plasma is white (broadband)
- Post-processing via fluorescence?
- RGB via different ionization energies

### Alternative: Holographic Volumetric

**Concept:** Reference beam interference creating standing wave nodes
- Requires extremely stable optical path
- Sensitive to air currents

### Engineering Constraints
- 1M voxels at 60Hz = 60M voxels/sec
- Current SLMs: 1kHz update rates
- Parallelization needed

### Potential Innovation
Femtosecond pulse trains at different focal lengths create multiple voxels simultaneously (axial multiplexing)
