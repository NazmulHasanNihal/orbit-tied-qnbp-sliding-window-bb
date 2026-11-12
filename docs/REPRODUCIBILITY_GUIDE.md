# Master Reproducibility Guide: Orbit-Tied QNBP

**Project:** Orbit-Tied Quantized Neural Belief Propagation (QNBP) for Real-Time Sliding-Window Decoding of Bivariate-Bicycle Quantum Codes  
**Authors:** Md. Nazmul (Lead & Corresponding), Musrat Jahan Gungun, Maheli Ahmed  
**Artifact Repository:** [https://github.com/NazmulHasanNihal/orbit-tied-qnbp-sliding-window-bb](https://github.com/NazmulHasanNihal/orbit-tied-qnbp-sliding-window-bb)  
**Standard Compliance:** ACM / IEEE Artifact Evaluation Guidelines (Badges: Available, Functional, Reusable)

---

## 1. Environment & Dependency Specifications

### 1.1 Python Dependencies
```bash
# Core scientific and quantum simulation stack
python -m pip install numpy>=1.24.0 scipy>=1.10.0 matplotlib>=3.7.0
python -m pip install stim>=1.14.0 sinter>=1.14.0 ldpc>=2.4.1
python -m pip install torch>=2.2.0 torch-geometric>=2.5.0
python -m pip install pytest>=8.0.0
```

### 1.2 Hardware Synthesis & Simulation Environment
- **FPGA Target:** AMD UltraScale+ XCKU040-FFVA1156-2-e
- **Synthesis Toolchain:** AMD Vivado Design Suite 2024.1 (or Synopsys Design Compiler)
- **RTL Language:** IEEE 1800-2017 SystemVerilog (`rtl/vnu.sv`, `rtl/cnu.sv`, `rtl/g3_gate.sv`, `rtl/streaming_axi_harness.sv`)

---

## 2. One-Command Full Verification Suite

To verify the complete mathematical, algorithmic, and hardware co-simulation suite in under 60 seconds:
```bash
python -m pytest tests/ -v
```
This executes:
1. `tests/test_orbits.py`: 36/36 torus automorphism verification and window boundary classification.
2. `tests/test_bivariate_bicycle.py`: Bivariate bicycle CSS commutativity, polynomial algebra, and circuit construction.
3. `tests/test_dem_graph.py`: Stim DEM graph parser and incidence matrices.
4. `tests/test_qnbp.py`: Dyadic quantization, CSD projection, and gradient backpropagation.
5. `tests/test_hardware_cosim.py`: VNU, CNU, and Gate G3 bit-exact hardware-software parity.
6. `tests/test_sliding_window.py`: Sliding-window commit schedule and queue simulator.
7. `tests/test_streaming_window.py`: Multi-round continuous streaming with boundary residual feedback.
8. `tests/test_competitor_baselines.py`: Mem-BP, BP-LSD, BP+OSD, AutDEC, and GDG sliding-window.

---

## 3. Step-by-Step Reproduction of Manuscript Tables

### 3.1 Table I: Asymmetric Biased Pauli Noise & Crosstalk
```bash
python src/experiments/run_novelty_benchmarks.py
```
- **Output:** `results/novelty_benchmarks.json`
- **Generates:** LER for Classical BP and Orbit-Tied QNBP across $\eta \in \{1, 10, 50, 100\}$ and $ZZ$ crosstalk $\epsilon = 0.10$.
- **Seed:** 42 + $\text{int}(\eta)$.

### 3.2 Table II & Table III: FPGA Synthesis & Subgroup Folding
```bash
python scripts/evaluate_folding_tradeoffs.py
python scripts/estimate_hardware_resources.py
```
- **Outputs:** `results/hardware_folding_results.json` and `rtl/synth_results.json`
- **Generates:** Resource breakdown (28,204 LUTs, 19,512 FFs, 0 DSP, 0 BRAM), achieved timing ($F_{\max} = 262\text{ MHz}$, $16\text{ ns/iter}$), dynamic power ($184\text{ mW}$), and folding Pareto frontier ($F \in \{1, 2, 3, 6, 12, 36\}$).

### 3.3 Table IV: Master 10-Decoder Benchmark Comparison
```bash
python scripts/run_competitor_benchmarks.py
```
- **Output:** `results/competitor_benchmarks.json`
- **Generates:** $N = 10,000$ paired shots on $[[72,12,6]]$ at $p = 0.003$ across all ten decoders, 95% Wilson confidence intervals, and paired McNemar $\chi^2$ statistics and $p$-values.
- **Seed:** 2026.

### 3.4 Confidence Gating & Multi-Server Queue Simulation
```bash
python scripts/evaluate_gating_and_queue.py
```
- **Output:** `results/gating_results.json`
- **Generates:** Gate $G_1, G_2, G_3$ calibration curves at $\tau \in [0.5, 3.0]$, fast-path acceptance rates, conditional pipeline error rates ($P_{\text{pipe}}$), and $D/G/c/B$ multi-server queue simulations over 50,000 windows.

---

## 4. Reproduction of Publication Figures

To regenerate all publication vector PDF figures from machine-readable JSON results:
```bash
python src/experiments/plot_figures.py
python src/experiments/plot_fig1_architecture.py
```
- **Outputs:**
  - `manuscript/figures/fig1_architecture.pdf`: End-to-end decoding pipeline overview.
  - `manuscript/figures/fig2_threshold_curve.pdf`: LER vs physical noise $p \in [10^{-3}, 5\times 10^{-3}]$.
  - `manuscript/figures/fig3_symmetry_control.pdf`: Trainable parameters vs LER with 5-seed random-tying distribution.
  - `manuscript/figures/fig4_quantization_sweep.pdf`: Bit-width quantization ladder (3-bit to float32).
  - `manuscript/figures/fig5_gate_tradeoffs.pdf`: Gate acceptance and pipeline error vs threshold $\tau$.
  - `manuscript/figures/fig6_folding_tradeoffs.pdf`: Hardware folding Pareto frontier (LUTs vs latency).
  - `manuscript/figures/fig7_queue_stability.pdf`: Buffer overflow fraction and queue utilization $\rho$.

---

## 5. Compiling the Canonical Manuscript PDF

To compile the IEEE Transactions publication deliverable:
```bash
python scripts/compile_manuscript_pdf.py
```
- **Output:** Strictly one canonical deliverable: `manuscript/main.pdf`.
- **Forensic Verification:**
```bash
python tests/verify_main_pdf.py
```
Ensures exact 12-page budget, zero forbidden strings, all 59 references sequentially cited, and complete statistical synchronization.

