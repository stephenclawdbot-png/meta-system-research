# R07: Computational Theorist - Cycle 0

## Computation Requirements

### Inverse Holography Problem

**Given:** Desired 3D scene (voxels)
**Find:** Wavefront patterns for each emitter

**Complexity:**
- Direct simulation: O(N²) per frame
- N = number of voxels (1M for 1080p equivalent)
- At 60Hz: 60M inversions/second

### Current Approaches

**1. Iterative Optimization**
- Gerchberg-Saxton algorithm variants
- Requires 20-100 iterations per frame
- Too slow for real-time

**2. Neural Radiance Fields (NeRF)**
- Train MLP to map 3D position → color
- Render via volume ray marching
- Inference time: ~100ms on modern GPU
- Too slow by 6x

**3. Tensor Approximation**
- Low-rank decomposition of wavefield
- Exploit scene sparsity
- Parallelizable on tensor cores

### Acceleration Strategies

**Temporal Coherence:**
- Don't recompute unchanged regions
- Delta encoding between frames

**Spatial Partitioning:**
- Divide space into independent regions
- Process in parallel

**Pre-computed Lookup:**
- Common patterns cached
- Composition of base patterns

### Hardware Requirements

**Current Estimates:**
- 1M voxels @ 60Hz = 60G voxel-ops/second
- Each voxel-op: float64 complex multiply
- Need: ~1 PFLOPS sustained
- RTX 4090: ~80 TFLOPS → Need 12+ GPUs

### Breakthrough
Use wavelet transforms or compressed sensing to reduce effective resolution needed
