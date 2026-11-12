# Comprehensive Project Audit Report: Orbit-Tied QNBP for Bivariate-Bicycle Codes

**Date:** November 11, 2026  
**Audit Team:** Multidisciplinary Senior Research Review Team (QEC Theory, LDPC Decoding, Neural/ML, Quantum Noise Modeling, FPGA/ASIC Hardware, Statistical Benchmarking, Journal Editorial)  
**Target Venue:** Top-Tier Q1 Quantum Engineering & Information Theory (IEEE TQE / PRX Quantum / Nature QI)  
**Subject Deliverable:** Manuscript (`manuscript/main.tex`, `manuscript/main.pdf`), SystemVerilog RTL (`rtl/`), Experimental Source (`src/`, `scripts/`), Raw Data (`results/`), Test Suite (`tests/`)

---

## Executive Summary

This forensic audit evaluates the theoretical, algorithmic, hardware, and empirical foundations of the project *"Orbit-Tied Quantized Neural Belief Propagation for Real-Time Sliding-Window Decoding of Bivariate-Bicycle Quantum Codes"*. The objective is to identify and resolve every discrepancy, unit error, mathematical ambiguity, or unverified claim prior to journal submission.

The core algorithmic concept (exploiting 2D torus translation automorphisms to tie neural BP weights, combining power-of-two quantization, and deploying a confidence margin fast-path gate) is fundamentally sound and empirically strong. However, this audit has uncovered **several critical numerical, architectural, and mathematical inconsistencies** that must be rigorously resolved to prevent peer-review rejection or post-publication corrections.

---

## 1. Complete Project Inventory & Dependency Map

### 1.1 File & Directory Inventory
| Category | Directory / Files | Purpose & Status |
| :--- | :--- | :--- |
| **Manuscript** | `manuscript/main.tex`, `main.pdf`, `references.bib` | Canonical 12-page IEEE Transactions journal submission source. |
| **Backup** | `manuscript/main_backup_preaudit.tex` | Immutable snapshot of the pre-audit manuscript. |
| **Archived Drafts**| `archive_old_drafts/main_{2,3,4,5}.pdf` | Superseded legacy draft iterations. |
| **Circuits & Codes**| `src/circuits/bivariate_bicycle.py` | Stim depth-7 circuit generation for $[[72,12,6]]$ and $[[144,12,12]]$. |
| **Graph Modeling** | `src/data/dem_graph.py` | Bipartite DEM graph extraction, incidence matrices, priors, observables. |
| **Automorphism Core**| `src/decoder/orbits.py` | Torus translation shift table, fault orbit partition, window classes. |
| **Decoders** | `src/decoder/{qnbp, quantization, integer_reference, baselines, competitor_baselines, sliding_window, streaming_window_decoder, sector_decoder}.py` | Python/PyTorch implementations of floating/integer decoders and competitor baselines. |
| **Hardware RTL** | `rtl/{vnu.sv, cnu.sv, g3_gate.sv, streaming_axi_harness.sv, synth_results.json}` | IEEE 1800-2017 SystemVerilog RTL modules and synthesis metadata. |
| **Evaluation** | `scripts/{run_competitor_benchmarks, evaluate_gating_and_queue, evaluate_folding_tradeoffs, estimate_hardware_resources, compile_manuscript_pdf}.py` | Execution scripts generating tabular benchmarks and hardware models. |
| **Raw Results** | `results/*.json` (`competitor_benchmarks`, `novelty_benchmarks`, `gating_results`, `ablations_results`, `hardware_folding_results`, `scaling_results`, `threshold_sweep`) | Machine-readable outputs from Monte Carlo runs. |
| **Figures** | `src/experiments/plot_figures.py`, `results/figures/`, `manuscript/figures/` | Matplotlib scripts generating publication vector PDFs (Figs. 1–7). |
| **Test Suite** | `tests/test_*.py` (12 test modules) | Automated pytest suite covering GF(2), DEM, orbits, QNBP, sliding window, and RTL parity. |

### 1.2 Pipeline Dependency Map
```
[Stim Circuit (bivariate_bicycle.py)]
         │
         ▼
[DEM Generation (Stim dem)] ───► [Graph Construction (dem_graph.py)]
         │                                      │
         ▼                                      ▼
[Orbit Extraction (orbits.py)] ───────► [QNBP Engine (qnbp.py / integer_reference.py)]
         │                                      │
         ▼                                      ▼
[Boundary Classes (orbits.py)] ───────► [Sliding Window (sliding_window.py)]
                                                │
         ┌──────────────────────────────────────┴──────────────────────────────────────┐
         ▼                                                                             ▼
[Competitor Benchmarks]                                                       [Confidence Gating & Queue]
(run_competitor_benchmarks.py)                                                (evaluate_gating_and_queue.py)
         │                                                                             │
         ▼                                                                             ▼
`results/competitor_benchmarks.json`                                          `results/gating_results.json`
         │                                                                             │
         ├──────────────────────────────────────┬──────────────────────────────────────┘
         ▼                                      ▼
[Figure Plotting (plot_figures.py)]   [RTL Co-Sim (test_hardware_cosim.py)]
         │                                      │
         ▼                                      ▼
`manuscript/figures/fig{1-7}.pdf`      `rtl/synth_results.json`
         │                                      │
         └──────────────────┬───────────────────┘
                            ▼
              [manuscript/main.tex (LaTeX)]
                            │
                            ▼
              `manuscript/main.pdf`
```

---

## 2. Critical Confirmed Issues

### Issue 1: 1000× Energy Calculation Error (Phase 2)
* **Severity:** 🔴 **CRITICAL (Definite Error)**
* **Location:** Abstract (line 36), Table II (line 347), and Section VII-A (line 386).
* **Finding:** The manuscript reports dynamic power as $P = 184\text{ mW}$, mean latency as $t_{\text{mean}} = 102.4\text{ ns}$, and worst-case latency as $t_{\text{worst}} = 240\text{ ns}$. It then reports energy as:
  $$\text{Reported Energy:} \quad 18.8\text{ pJ (mean)} \quad \text{and} \quad 44.2\text{ pJ (worst-case)}$$
* **Mathematical Truth:**
  $$E_{\text{mean}} = P \times t_{\text{mean}} = 184\text{ mW} \times 102.4\text{ ns} = 0.184\text{ W} \times 102.4 \times 10^{-9}\text{ s} = 18.8416 \times 10^{-9}\text{ J} = \mathbf{18.84\text{ nJ}}$$
  $$E_{\text{worst}} = P \times t_{\text{worst}} = 184\text{ mW} \times 240.0\text{ ns} = 0.184\text{ W} \times 240.0 \times 10^{-9}\text{ s} = 44.1600 \times 10^{-9}\text{ J} = \mathbf{44.16\text{ nJ}}$$
* **Impact:** The manuscript understated energy consumption by an exact factor of $1,000$ (reporting picojoules instead of nanojoules). While $18.84\text{ nJ}$ per decoded window ($0.26\text{ nJ}$ per data qubit) remains exceptionally low for an FPGA decoder, mislabeling nanojoules as picojoules is a severe unit error that any hardware referee would flag immediately.

### Issue 2: Queueing Latency & Fallback Utilization Discrepancy (Phase 3)
* **Severity:** 🔴 **CRITICAL (Mathematical Inconsistency)**
* **Location:** Section VI-D (lines 313–319).
* **Finding:** 
  1. In line 315, the text states $\mathbb{E}[T_{\text{slow}}] = 1760\text{ ns}$ and total fallback duration $= 2000\text{ ns}$, calculating:
     $$\mathbb{E}[S] = 0.756 \times 240\text{ ns} + 0.244 \times 2000\text{ ns} = 669.44\text{ ns} < 1000\text{ ns}$$
  2. Four lines later (line 319), the text computes fallback queue utilization using $950\text{ ns}$:
     $$\rho_{\text{fb}} = \frac{0.244 \times 950\text{ ns}}{1000\text{ ns}} = 0.2318 \approx 0.23$$
  3. In `results/gating_results.json`, lines 197–206, the queue simulation was executed with $p_{\text{fast}} = 0.88$ (the raw G3 calibration at $\tau=0.5$ or early setting) and $\mathbb{E}[S] = 230.23\text{ ns}$, yielding $\rho = 0.2302$.
* **Impact:** The text spliced three conflicting service times ($1760\text{ ns}$, $2000\text{ ns}$, and $950\text{ ns}$) and two acceptance rates ($0.756$ and $0.88$) to explain the single utilization number $\rho = 0.23$. Furthermore, asserting that $\mathbb{E}[S] < T_{\text{cycle}}$ mathematically guarantees zero buffer overflow is invalid: in finite-buffer queuing ($D/G/c/B$), burstiness and service-time variance dictate tail overflow.

### Issue 3: FPGA Macro-VNU Logic Count Contradiction (Phase 10)
* **Severity:** 🔴 **CRITICAL (Arithmetic Contradiction)**
* **Location:** Section VII-A (line 333).
* **Finding:** The text states:
  > *"parallel fault mechanisms ... are column-deduplicated into 498 physical macro-VNUs. Each macro-VNU evaluates LLR accumulation for its fault orbit ($498 \times 48\text{ LUTs} \approx 23,904\text{ LUTs}$), while 216 CNUs consume $216 \times 82\text{ LUTs} = 17,712\text{ LUTs}$, combined with shared comparator and control logic yielding a post-synthesis total of 28,204 LUTs."*
* **Mathematical Truth:**
  $$23,904\text{ LUTs} + 17,712\text{ LUTs} = 41,616\text{ LUTs} \ne 28,204\text{ LUTs}$$
* **Root Cause in Synthesis Reports:**
  In `rtl/synth_results.json` (lines 26–35), the synthesized full window for $[[72,12,6]]$ actually instantiates:
  - $\text{num\_vnus} = 216$ ($216 \times 48\text{ LUTs} = 10,368\text{ LUTs}$)
  - $\text{num\_cnus} = 216$ ($216 \times 82\text{ LUTs} = 17,712\text{ LUTs}$)
  - Gate $G_3$ & interconnect logic $= 124\text{ LUTs}$
  - Total: $10,368 + 17,712 + 124 = \mathbf{28,204\text{ LUTs}}$!
* **Impact:** The synthesized total of 28,204 LUTs is correct, but the prose erroneously inserted "498 macro-VNUs" (a theoretical count of fault classes in a window) instead of explaining the actual architecture where 216 check-centric/variable units process the syndrome lattice.

### Issue 4: Ambiguous CSS Sector Separation Formulation (Phase 4)
* **Severity:** 🟠 **HIGH (Theoretical Precision)**
* **Location:** Section V-B, Theorem 4 (lines 236–238).
* **Finding:** Theorem 4 states: *"Under high dephasing bias $\eta \to \infty$, the effective error rate on the Z-sector approaches 0, allowing the decoder to allocate 100% of its iteration budget to the dominant dephasing sector."*
* **Theoretical Flaw:** 
  1. In CSS codes, physical Pauli $Z$ errors are detected by $X$-type checks ($H_X = [A \mid B]$). Physical Pauli $X$ errors are detected by $Z$-type checks ($H_Z = [B^T \mid A^T]$).
  2. Under dephasing bias ($p_Z \gg p_X$), physical $Z$ errors dominate; therefore, the $X$-syndrome check sector receives the dominant syndrome excitation, while the $Z$-syndrome check sector has near-zero excitation. Saying "the error rate on the Z-sector approaches 0" is ambiguous because readers confuse physical $Z$ errors with $Z$-checks.
  3. Under circuit-level noise, two-qubit CNOT gates in the syndrome extraction circuit propagate $Z$ errors into $ZZ$ and $X$ errors into $XX$, while measurement faults and physical $Y$ errors ($Y = iXZ$) trigger checks in *both* sectors simultaneously. Thus, independent $X/Z$ decoding is an *effective approximation* under circuit-level noise, not an exact graph decoupling.

### Issue 5: Undocumented Window Round Counts in Orbit Collapse (Phase 6)
* **Severity:** 🟠 **HIGH (Clarity & Reproducibility)**
* **Location:** Abstract (line 36), Corollary 1 (line 137).
* **Finding:** The text states:
  > *"collapsing 10,260 circuit fault mechanisms into 285 symmetry orbits ($36\times$ reduction) on $[[72,12,6]]$ and 14,616 mechanisms into 203 orbits ($72\times$ reduction) on $[[144,12,12]]$."*
* **Computational Audit:**
  - For $[[72,12,6]]$ ($|G|=36$):
    * $R=2$ rounds: 4,284 faults $\to$ 119 orbits ($36.0\times$ collapse)
    * $R=3$ rounds: 7,308 faults $\to$ 203 orbits ($36.0\times$ collapse)
    * $R=4$ rounds: 10,260 faults $\to$ 285 orbits ($36.0\times$ collapse)
  - For $[[144,12,12]]$ ($|G|=72$):
    * $R=2$ rounds: 8,568 faults $\to$ 119 orbits ($72.0\times$ collapse)
    * $R=3$ rounds: 14,616 faults $\to$ 203 orbits ($72.0\times$ collapse)
* **Impact:** 10,260 corresponds to an $R=4$ circuit on BB72, whereas 14,616 corresponds to an $R=3$ circuit on BB144, and the standard $W=3$ sliding window on BB72 has 7,308 faults. The manuscript must explicitly state the round depth $R$ for each count to avoid confusion.

### Issue 6: Table I vs. Table IV LER Discrepancy (Phase 11)
* **Severity:** 🟡 **MEDIUM (Contextual Clarification)**
* **Location:** Table I ($P_L = 0.0080$ at $\eta=1.0$) vs. Table IV ($P_L = 0.0068$).
* **Finding:** At $p=0.003$ on $[[72,12,6]]$, Table I reports $P_L = 0.0080$, while Table IV reports $P_L = 0.0068$.
* **Audit Trail:** Table I evaluated an earlier baseline checkpoint with fixed scalar damping $\gamma = 0.35$ (mean iterations: 6.8), whereas Table IV evaluates the final model with fully trained signed per-orbit damping $\gamma \in [-0.5, 1.0]$ (mean iterations: 6.4). This distinction is documented in Table I's caption, but must be reinforced in the main text.

---

## 3. Hardware & RTL Audit

### 3.1 Verilog Implementation vs. Trainable Weights
* In `rtl/vnu.sv` (lines 32, 71–75), memory damping is implemented as a fixed CSD shift:
  $$\text{damped\_term} = \text{val} - (\text{val} \ggg 2) \quad (\gamma = 0.75)$$
  controlled by a 1-bit `enable_damping` flag.
* In `rtl/cnu.sv` (line 25), normalized Min-Sum scaling is implemented as:
  $$\text{scaled\_mag} = \text{raw\_mag} - (\text{raw\_mag} \gg 2) \quad (\alpha = 0.75)$$
  controlled by a 1-bit `enable_alpha_scaling` flag.
* **Audit Assessment:** The synthesizeable RTL modules `vnu.sv` and `cnu.sv` demonstrate the hardware execution of the CSD shift-and-add architecture with zero DSP multipliers ($DSP=0$). However, they implement fixed canonical weights ($\alpha=0.75, \gamma=0.75$) rather than dynamic run-time coefficient reloading from LUT RAM. The manuscript must clarify that the synthesized RTL represents the canonical CSD kernel, while the neural software model proves that per-orbit learned variations within this CSD envelope further improve convergence.

### 3.2 Co-Simulation Scope
* `tests/test_hardware_cosim_10k.py` is a Python-based bit-exact arithmetic testbench matching the SystemVerilog bitwise operations across 10,000 vectors. It is not an external Verilator/QuestaSim binary invocation.
* **Audit Rule:** The manuscript must describe this as *bit-exact software-RTL algorithmic co-simulation*, avoiding any phrasing that implies physical cryogenic FPGA board-level measurements.

---

## 4. Summary of Required Modifications

| Target Area | Action Item | Priority |
| :--- | :--- | :---: |
| **Energy Units** | Update all energy occurrences from pJ to nJ ($18.84\text{ nJ}$ mean, $44.16\text{ nJ}$ worst-case). | 🔴 CRITICAL |
| **Queue Analysis** | Reconcile service times ($T_{\text{fast}}=240\text{ ns}, \mathbb{E}[T_{\text{slow}}]=1760\text{ ns}$), report sequential vs. parallel server models clearly, and reframe queue stability with finite-buffer simulation bounds ($N=50,000$ test shots, 0 overflows). | 🔴 CRITICAL |
| **Macro-VNU Logic** | Reconcile Section VII-A text with `synth_results.json` ($216 \times 48 = 10,368$ VNU LUTs + $216 \times 82 = 17,712$ CNU LUTs + 124 gate LUTs = 28,204 LUTs). | 🔴 CRITICAL |
| **CSS Theorem** | Re-derive Theorem 4 to clarify that physical $Z$ errors are detected by $X$-checks, and frame decoupling under circuit-level noise as an effective dephasing concentration. | 🔴 CRITICAL |
| **Orbit Counts** | Specify round depth $R$ for all reported counts ($R=4 \implies 10,260$ faults / 285 orbits on BB72; $R=3 \implies 7,308$ faults / 203 orbits on BB72; $R=3 \implies 14,616$ faults / 203 orbits on BB144). | 🟠 HIGH |
| **Hardware Framing** | Accurately describe RTL kernel synthesis and distinguish software learned weights from fixed CSD hardware kernel. | 🟠 HIGH |
| **Table Consistency** | Clarify the relationship between Table I ($\gamma=0.35$ checkpoint) and Table IV ($\gamma \in [-0.5, 1.0]$ trained checkpoint). | 🟡 MEDIUM |

---

## 5. Audit Conclusion

The scientific substance of the paper is exceptionally strong: the mathematical automorphism collapse, 6-bit dyadic dynamic range bound, and empirical gains over classical BP and Relay-BP are genuine and reproducible. Resolving the confirmed numerical, queuing, and architectural issues outlined above will elevate this manuscript to the highest standards of technical rigor and publication readiness.

