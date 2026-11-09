# Research & Engineering Progress Log

## Session: 2026-11-09 — Phase 1 Foundations & QEC Infrastructure (COMPLETE)

### 1. Mathematical Grounding & Circuit Implementation
- **Module:** `src/circuits/bivariate_bicycle.py` & `src/utils/gf2.py`
- Implemented cyclic permutation representation of $A(x, y) = x^3 + y + y^2$ and $B(x, y) = y^3 + x + x^2$ over $\mathbb{F}_2[x, y] / (x^\ell - 1, y^m - 1)$.
- Formally verified CSS commutativity $H_X H_Z^T = 0 \pmod 2$.
- Derived binary ranks and canonical symplectic logical basis ($k=12$ for both $[[72,12,6]]$ and $[[144,12,12]]$).
- Implemented Bravyi et al. (Nature 2024) depth-7 syndrome extraction circuit in Stim.
- **Empirical Size Check:**
  - 12-round $[[144, 12, 12]]$ gross code: **1,728 detectors** and **67,752 error mechanisms** (100% exact match with published literature).
  - 6-round $[[72, 12, 6]]$ code: **432 detectors** and **16,164 error mechanisms**.

### 2. Automorphism Symmetry Orbit Extraction & Invariance Verifier
- **Module:** `src/decoder/orbits.py`
- Extracted torus translation group $G = \mathbb{Z}_\ell \times \mathbb{Z}_m$ ($|G|=36$ for $[[72,12,6]]$, $|G|=72$ for $[[144,12,12]]$).
- Built automated verifier: proved that **36/36 shifts** are strict graph automorphisms of the circuit-level DEM (exact symptom matching and $|p' - p| < 10^{-10}$).
- Partitioned 10,260 fault mechanisms into **285 symmetry orbits** ($36\times$ parameter reduction).
- Implemented window boundary class classification (`open_left=0`, `interior=1`, `open_right=2`).

### 3. Graph Bridge (Stim to PyTorch / PyG)
- **Module:** `src/data/dem_graph.py`
- Converted DEM into bipartite graph tensor representations (detector check nodes, fault variable nodes, prior LLRs, and observable incidence matrix).
- Verified that node and edge counts strictly match DEM detectors and fault mechanisms.
- Exported PyTorch Geometric `HeteroData` graph.

### 4. Classical Min-Sum Baselines (A0 & A1)
- **Module:** `src/decoder/baselines.py`
- Implemented vectorized Min-Sum Belief Propagation decoder with Min-1 and Min-2 CNU.
- Configured baseline A0 (unweighted min-sum, $\alpha=1.0$) and baseline A1 (normalized min-sum, $\alpha=0.75$).
- Verified immediate convergence on noiseless syndrome (1 iteration) and deterministic single-fault correction.

### 5. Orbit-Tied Quantized Neural BP Core (QNBP)
- **Module:** `src/decoder/qnbp.py` & `src/decoder/quantization.py`
- Implemented unfolded Neural BP architecture with orbit-tied $\alpha_{o, t}$ and signed memory damping $\gamma_{o, t}$.
- Implemented straight-through estimator (STE) power-of-two quantization $\Delta = 2^{-\text{round}(\tilde{b})}$.
- Implemented Canonical Signed Digit (CSD) projection for multiplier-free shift-and-add arithmetic ($\pm 2^{-a} \pm 2^{-b}$).
- Implemented multi-iteration supervised log-domain observable loss $\mathcal{L}_{\text{obs}} = \sum_k \text{BCE}(q_k, y_k) + \lambda \sum_c \text{BCE}(\hat{s}_c, s_c)$ using stable $\ln \tanh(x/2)$ formula.
- Verified complete forward pass and finite backward gradient flow across all parameters.

### 6. Sliding Window Manager & Margin-Gated Fast Path
- **Module:** `src/decoder/sliding_window.py`
- Implemented temporal sliding window state machine (width $W$, commit stride $F$).
- Implemented fast-path confidence margin gates: G1 (syndrome matched), G2 (min flipped LLR $\ge \tau$), G3 (observable-specific margin $\ge \tau$), and conservative control.
- Implemented trace-driven sequential queue backlog simulator: verified expected service time $\mathbb{E}[S]$ and buffer capacity boundary.

### 7. Test Suite Status
- **19/19 pytest unit tests passed** across all 7 test suites (`test_gf2`, `test_bivariate_bicycle`, `test_orbits`, `test_dem_graph`, `test_baselines`, `test_qnbp`, `test_sliding_window`).
