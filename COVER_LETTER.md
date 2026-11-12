# Official Editorial Cover Letter — IEEE Transactions on Quantum Engineering

**To:**  
Prof. Rodney Van Meter, Editor-in-Chief  
*IEEE Transactions on Quantum Engineering (IEEE TQE)*  
IEEE Quantum Initiative  

**From:**  
Md. Nazmul (Lead & Corresponding Author)  
*On behalf of co-authors Musrat Jahan Gungun and Maheli Ahmed*  
Department of Computer Science and Engineering  
College of Technology, National University, Gazipur, Bangladesh  
E-mail: `nazmulhas36@gmail.com` • ORCID: `0009-0001-6115-7023`  

**Date:** November 12, 2026  

**Subject:** Submission of Original Research Manuscript: *"Orbit-Tied Quantized Neural Belief Propagation for Real-Time Sliding-Window Decoding of Bivariate-Bicycle Quantum Codes"*  

---

Dear Prof. Van Meter and Members of the Editorial Board,

On behalf of my co-authors, I am pleased to submit our original research manuscript, titled **"Orbit-Tied Quantized Neural Belief Propagation for Real-Time Sliding-Window Decoding of Bivariate-Bicycle Quantum Codes,"** for consideration as a Regular Paper in the *IEEE Transactions on Quantum Engineering*.

The manuscript contains 12 pages in standard IEEE Transactions two-column format, comprising 7 multi-panel figures, 5 benchmark tables, rigorous mathematical theorems, cycle-accurate SystemVerilog hardware co-simulation, and 59 sequential references.

### Authorship Sequence
- **Md. Nazmul** (Lead & Corresponding Author; ORCID: `0009-0001-6115-7023`) — Project leader / Contact person
- **Musrat Jahan Gungun** (Co-Author; ORCID: `0009-0006-4249-9198`) — Project member / Researcher
- **Maheli Ahmed** (Faculty Supervisor; ORCID: `0000-0002-5183-7498`) — Supervisor  
*All authors are affiliated with the Department of Computer Science and Engineering, College of Technology, National University, Gazipur, Bangladesh.*

### Motivation and Core Engineering Problem
Quantum Low-Density Parity-Check (QLDPC) bivariate-bicycle (BB) codes (Bravyi et al., *Nature* 2024) offer an order-of-magnitude reduction in physical qubit overhead compared to topological surface codes. However, deploying them in real-time quantum control systems has remained blocked by a fundamental decoding dilemma: their dense, non-local check connectivity creates 3D space-time Detector Error Models (DEM) with thousands of correlated fault mechanisms. Conventional software decoders (e.g., BP+OSD) take hundreds of microseconds on CPUs, causing catastrophic backlog and buffer overflow under the strict ~1 μs coherence budget of superconducting quantum processors.

### Key Technical Contributions
1. **Torus Automorphism Equivariance (Theorem 2):** We prove that 2D torus translations $G = \mathbb{Z}_\ell 	imes \mathbb{Z}_m$ constitute strict DEM graph automorphisms. Weight tying across automorphism orbits collapses 7,308 fault mechanisms to 203 orbits ($36.0	imes$ parameter reduction) on $[[72,12,6]]$ and 14,616 mechanisms to 203 orbits ($72.0	imes$ reduction) on $[[144,12,12]]$, strictly guaranteeing geometric equivariance and eliminating untied neural overfitting.
2. **Multiplier-Free 6-Bit Dyadic CSD Architecture (Theorem 3):** We prove dyadic clipping bounds ($[-7.75, +7.75]$, $\Delta=0.25$) and implement all variable- and check-node operations with zero DSP multipliers ($	ext{DSP}=0$) using two-term Canonical Signed-Digit (CSD) shift-and-add arithmetic.
3. **Multi-Stage Margin Gating & Streaming Sliding Window:** In a streaming sliding window ($W=3, F=1$), our margin gate $G_3$ routes 75.6% of syndrome windows with zero logical errors ($P_{L, 	ext{accept}} = 0.0000$), delivering an end-to-end pipeline error rate of $P_{	ext{pipe}} = 1.90 	imes 10^{-4}$ at 102.4 ns mean latency (240 ns max), keeping queue buffer overflow below $6.0 	imes 10^{-5}$ under $1\,\mu	ext{s}$ quantum cycles.
4. **100-Round Continuous Streaming Memory Survival:** We validate continuous multi-round streaming over $R=100$ measurement rounds ($100\,\mu	ext{s}$). Active temporal boundary residual propagation preserves $98.1\%$ logical survival at 100 rounds ($F_{	ext{log}} = 0.9981$ at 10 μs, $0.9812$ at 100 μs), whereas boundary-agnostic decoding collapses to $22.1\%$ ($4.4	imes$ degradation).
5. **Real-World IBM Quantum Heron Calibration Benchmark:** Benchmarked against the empirical calibration snapshot of IBM's flagship 133-qubit Heron r2 processor ($p_{	ext{2Q}} = 2.1 	imes 10^{-3}, \eta = 50.0$), Orbit-Tied QNBP converges in only 3.85 mean iterations—the fastest among all 6 models tested (vs. 9.16 for Classical Min-Sum, 11.86 for Normalized Min-Sum, and 8.86 for BP+OSD-CS-10) with $	ext{DSP}=0$.
6. **Synthesizeable Hardware & Co-Simulation Parity:** We synthesize our design in SystemVerilog for AMD UltraScale+ XCKU040 ($f_{	ext{clk}} = 250	ext{ MHz}$, 28,204 LUTs, 0 DSPs) and verify 10,000-shot bit-exact hardware-software co-simulation parity.

### Editorial Certifications
- **Originality:** This manuscript is original, has not been published previously, and is not currently under review elsewhere.
- **Reproducibility:** The complete software library (`orbit-tied-qnbp` v1.0.0) is published on PyPI and GitHub (`github.com/NazmulHasanNihal/orbit-tied-qnbp-sliding-window-bb`) with pinned seeds, automated test suites, and SystemVerilog RTL.
- **Conflict of Interest:** The authors declare no competing financial or personal interests.

Thank you very much for your time and editorial guidance.

Sincerely,  
**Md. Nazmul** (Lead & Corresponding Author)  
*On behalf of co-authors Musrat Jahan Gungun and Maheli Ahmed*  
Department of Computer Science and Engineering  
College of Technology, National University, Gazipur, Bangladesh  
E-mail: `nazmulhas36@gmail.com` • ORCID: `0009-0001-6115-7023`
