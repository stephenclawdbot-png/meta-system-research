# R05: Systems Architect - Cycle 0

## System Integration Blueprint

### Distributed vs Centralized

**Centralized (Single Emitter)**
- Pros: Precise synchronization
- Cons: Limited field of view
- Best for: Personal volumetric displays

**Distributed (Array)**
- Pros: 360° viewing, scalability
- Cons: Calibration complexity
- Best for: Room-scale installations

### Proposed Architecture: "Aether Lattice"

**Core Components:**
1. **Edge Emitters:** Wall/ceiling mounted laser arrays
2. **Control Plane:** Real-time voxel computation engine
3. **Safety Layer:** Eye-tracking + beam blocking
4. **Calibration:** Continuous auto-alignment

**Safety System:**
- Eye tracking cameras detect viewers
- Active beam steering avoids eyes
- Emergency shutdown < 1ms

### Control Protocol

**Data Flow:**
3D Scene (NeRF/Voxel) → Wavefront Computation → SLM Patterns → Laser Array → Voxel Space

**Timing Requirements:**
- End-to-end latency: < 5ms
- Beam steering: MHz rates
- Eye tracking: kHz rates

### Integration Challenges
- Alignment of multiple emitters
- Voxel overlap from different angles
- Ambient light rejection

### Breakthrough
Combine filamentation (volumetric) with smart dust (persistent pixels)?
