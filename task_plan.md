# Task Plan: Orbit-Tied Quantized Neural BP for BB Codes

**Goal:** Implement, verify, and benchmark a 3D sliding-window neural belief propagation (QNBP) decoder with automorphism orbit weight-tying and multiplier-free power-of-two quantization for Bivariate-Bicycle quantum LDPC codes ($[[72,12,6]]$ and $[[144,12,12]]$), targeting top-tier publication (IEEE TQE / QST).

---

## 🏗️ Phase 1: Foundations & QEC Infrastructure (Week 1 Milestones)

- [x] **Task 1.1: Bivariate Bicycle Code Generator & Circuit Builder (`src/circuits/bivariate_bicycle.py`)**
  - Implement polynomial cyclic matrices $A(x, y), B(x, y)$ over $\mathbb{F}_2[x, y] / (x^\ell - 1, y^m - 1)$.
  - Construct check matrices $H_X = [A, B]$ and $H_Z = [B^T, A^T]$; verify CSS commutativity $H_X H_Z^T = 0 \pmod 2$.
  - Implement full Stim syndrome-extraction circuit with Bravyi et al. depth-7 schedule for $R$ rounds.
  - Generate Detector Error Models (DEM) for $p \in \{0.001, 0.002, 0.003, 0.005\}$.
  - Run Size Check: verified detector (1,728) and error mechanism (67,752) counts for $[[144,12,12]]$.
  - **Status:** Complete (Verified with automated tests in `tests/test_bivariate_bicycle.py`)

- [x] **Task 1.2: DEM Automorphism Orbit Extraction & Invariance Verifier (`src/decoder/orbits.py`)**
  - Extract the torus group action $G = \mathbb{Z}_\ell \times \mathbb{Z}_m$ ($|G|=36$ for $[[72,12,6]]$, $|G|=72$ for $[[144,12,12]]$).
  - Apply translation shifts to the DEM graph nodes (detectors, faults) and check for invariant priors and observable memberships.
  - Partition DEM elements into symmetry orbits and classify boundary effects (open-left, interior, open-right rounds).
  - Automated verifier: 36/36 shifts verified as strict automorphisms; confirmed $36\times$ parameter reduction.
  - **Status:** Complete (Verified with automated tests in `tests/test_orbits.py`)

- [x] **Task 1.3: Stim DEM-to-PyTorch/PyG Graph Bridge (`src/data/dem_graph.py`)**
  - Convert Stim DEM into bipartite graph tensor representations (fault variable nodes, detector check nodes, priors, observables).
  - Support batched vectorized message passing across sliding windows.
  - Verified node/edge counts match DEM; verified priors and PyG `HeteroData` export.
  - **Status:** Complete (Verified with automated tests in `tests/test_dem_graph.py`)

- [x] **Task 1.4: Classical Min-Sum Baselines A0 & A1 (`src/decoder/baselines.py`)**
  - A0: Floating-point unweighted min-sum BP.
  - A1: Normalized min-sum with iteration-dependent scaling $\alpha_t$ (tuned on validation set).
  - Implemented Min-1 / Min-2 fast CNU and optional memory damping $\gamma$.
  - Verified baseline accuracy and single-fault recovery on DEM bipartite graphs.
  - **Status:** Complete (Verified with automated tests in `tests/test_baselines.py`)

- [x] **Task 1.5: Orbit-Tied Quantized Neural BP Core (`src/decoder/qnbp.py` & `src/decoder/quantization.py`)**
  - Unfolded neural BP architecture with orbit-tied $\alpha_{o, t}$ and signed memory damping $\gamma_{o, t}$ (Relay-BP inspired).
  - Straight-through estimator (STE) power-of-two quantization $\Delta = 2^{-\text{round}(\tilde{b})}$.
  - Canonical signed-digit (CSD) multiplier-free weights (shift-and-add arithmetic).
  - Numerically stable log-domain observable loss $\mathcal{L}_{\text{obs}} = \sum_k \text{BCE}(q_k, y_k) + \lambda \sum_c \text{BCE}(\hat{s}_c, s_c)$.
  - Bit-exact integer-only reference model in pure Python for hardware co-simulation.
  - **Status:** Complete (Verified with automated tests in `tests/test_qnbp.py`)

- [x] **Task 1.6: Sliding Window Manager & Margin-Gated Fast Path (`src/decoder/sliding_window.py`)**
  - Sliding window state machine with width $W \in \{3, 5, 6\}$ and commit stride $F \in \{1, 2\}$.
  - Gates G1, G2, G3 implementation with margin threshold $\tau$.
  - Trace-driven queue stability simulator: verified expected service time $\mathbb{E}[S]$ and buffer capacity boundary.
  - **Status:** Complete (Verified with automated tests in `tests/test_sliding_window.py`)

---

## 🧪 Phase 2: Real Empirical Testing Protocol (RETP) — Anti-Hallucination & Q1 Rigor

All experiments must use genuine, non-synthetic quantum error correction pipelines to ensure results are 100% authentic, reproducible, and verifiable for top-tier peer review (IEEE TQE / QST).

- [ ] **Protocol 2.1: Stim Hardware-Circuit Monte Carlo Error Sweep**
  - Run genuine circuit-level depolarizing error models directly compiled with `stim.Circuit.compile_detector_sampler()`.
  - Physical error rate sweep: $p \in \{0.001, 0.002, 0.003, 0.004, 0.005\}$ on $[[72,12,6]]$.
  - Sample sufficient shots to record $\ge 100$ failure events per data point with exact 95% Wilson score confidence intervals.

- [ ] **Protocol 2.2: Gold-Standard BP+OSD Baseline Comparison**
  - Benchmark Orbit-Tied QNBP against the gold standard in QLDPC decoding: C++ `ldpc.bposd.bposd_decoder` (`ldpc 2.4.1`).
  - Compare Logical Error Rate (LER), decoding time per shot, and iteration counts against:
    1. Unweighted Min-Sum BP (A0)
    2. Normalized Min-Sum BP (A1)
    3. Official BP+OSD-0 / BP+OSD-CS (the offline optimal benchmark)
    4. Orbit-Tied QNBP (Proposed hardware fast-path)

- [ ] **Protocol 2.3: Bit-Exact Hardware Reference & Multiplier-Free Verification**
  - Run inference through the pure integer decoder (`src/decoder/integer_reference.py`).
  - Formally verify that inference uses zero floating-point operations and zero hardware multipliers (strictly bit shifts `>>` and integer adds `+`).
  - Validate bit-exact numerical parity against the PyTorch 4-bit STE quantizer.

- [ ] **Protocol 2.4: Continuous Streaming Sliding-Window & Queue Stability Test**
  - Stream continuous syndrome extractions ($R = 12$ to $R = 24$ rounds) through the sliding window engine ($W=3, F=1$).
  - Measure real acceptance rate for confidence margin gates G1, G2, and G3.
  - Run trace-driven queue simulation under realistic quantum cycle times ($t_{\text{cycle}} = 1000$ ns, fast path = 24 ns/iter, slow fallback = 100 ns/iter).
  - Verify buffer overflow fraction and P99 backlog across buffer capacities $B \in \{0, 1, 2, 5, 10, 15, 20\}$.

- [ ] **Protocol 2.5: Ablation Ladder (A0–A10) & Paired Statistical Significance**
  - Evaluate the full ladder (A0 through A10) on identical paired Stim shots.
  - Compute McNemar's paired test statistic and exact two-tailed $p$-value for Claim C1 ($P_L(\text{A4}) < P_L(\text{A5})$ with $p < 0.01$).
  - Quantization degradation test for Claim C2: verify 4-bit model is within 10% relative error of float32.
  - Export all raw outcomes and summary metrics into `results/ablations_results.json`.

- [ ] **Protocol 2.6: Publication-Grade IEEE Vector Figures**
  - Generate 300 DPI vector PDF figures in `results/figures/`:
    - **Fig F2**: Logical Frame Error Rate vs. Physical Error Rate ($p \in [10^{-3}, 5\times 10^{-3}]$) comparing QNBP, BP, and BP+OSD.
    - **Fig F3**: Torus Symmetry Orbit Tying vs. 5-Seed Random-Tying Control Distribution.
    - **Fig F4**: Quantization Bit-Width Sweep (3-bit, 4-bit, 5-bit, 6-bit, Float32, and 4-bit Integer Hardware Reference).
    - **Fig F5**: Margin-Gated Fast-Path Trade-Offs (Acceptance Rate vs. Error in Accepted Windows for G1, G2, G3).
    - **Fig F7**: Queue Backlog & Buffer Overflow Fraction vs. Buffer Capacity.

---

## 📊 Phase 3: Hardware Modeling & Q1 Manuscript Authoring
- [ ] SystemVerilog RTL for VNU, CNU, and G3 Gate.
- [ ] Bit-exact co-simulation (RTL vs. Python Reference).
- [ ] Vivado resource and Fmax synthesis reports (0 DSPs).
- [ ] Complete manuscript drafting according to IEEE TQE / QST guidelines.
