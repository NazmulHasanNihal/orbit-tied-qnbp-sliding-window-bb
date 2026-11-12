# 📋 IEEE ScholarOne Manuscripts Submission Metadata & Portal Guide

**Target Journal:** *IEEE Transactions on Quantum Engineering (IEEE TQE)*  
**Manuscript Type:** Regular Paper (Original Research)  
**Track / Subject Category:** Quantum Architecture, Quantum Error Correction, and Physical Hardware  
**Corresponding Author:** Md. Nazmul (nazmulhas36@gmail.com)  

---

## 1. Manuscript Details (ScholarOne Step 1 & 2)

### Full Manuscript Title
```
Orbit-Tied Quantized Neural Belief Propagation for Real-Time Sliding-Window Decoding of Bivariate-Bicycle Quantum Codes
```

### Short Title / Running Head
```
Orbit-Tied QNBP for Sliding-Window Decoding of BB Codes
```

### Abstract (Plain-Text for Portal)
```
Quantum Low-Density Parity-Check (QLDPC) bivariate-bicycle (BB) codes have emerged as premier candidates for scalable fault-tolerant quantum computation, offering order-of-magnitude reductions in physical qubit overhead compared to standard 2D topological surface codes. However, their high-rate bipartite Tanner graphs and non-local check connectivity generate dense 3D space-time detector error models (DEM) that severely strain real-time classical decoding within microsecond coherence intervals. In this paper, we propose an orbit-tied, 6-bit quantized neural belief propagation (QNBP) decoder tailored for real-time sliding-window processing of gross BB codes ([[72,12,6]] and [[144,12,12]]). By mapping the 2D torus translation group G = Z_l x Z_m, we prove that all spatial shifts constitute strict DEM graph automorphisms, collapsing 10,260 circuit fault mechanisms into 285 symmetry orbits (R=4, 36.0x parameter reduction; 7,308 into 203 orbits for R=3) on [[72,12,6]] and 14,616 mechanisms into 203 orbits (R=3, 72.0x reduction) on [[144,12,12]] while strictly guaranteeing geometric equivariance and eliminating untied neural overfitting. To guarantee multiplier-free hardware synthesis with zero Digital Signal Processing (DSP) slices, we develop a Canonical Signed-Digit (CSD) shift-and-add architecture using power-of-two dyadic quantization (Delta = 0.25). Under circuit-level Stim Monte Carlo depolarizing noise (p in [0.001, 0.005]), we execute head-to-head benchmarking across ten decoders, including IBM Relay-BP, BP-LSD, BP+OSD-CS-10, Mem-BP, AutDEC, and Gong et al.'s sliding-window baseline. Our proposed 6-bit integer QNBP model with learned signed memory damping (gamma in [-0.5, 1.0]) converges in only 6.4 mean iterations with zero DSP blocks (DSP=0), attaining a logical error rate of P_L = 0.0068 [0.0053, 0.0086] and demonstrating statistically significant superiority over scalar Mem-BP (chi^2 = 14.72, p = 0.000125), IBM Relay-BP-5 (chi^2 = 12.06, p = 0.000515), Normalized Min-Sum (chi^2 = 2,642.1, p < 10^-100), and AutDEC (chi^2 = 2,750.5, p < 10^-100). Under realistic superconducting Pauli Z-biased noise (eta = p_Z / p_X in [1, 100]), Orbit-Tied QNBP automatically adapts message weighting, attaining an 8.0x logical error suppression down to P_L = 0.0010 [0.0005, 0.0019] at eta=100 (20.0x over Classical BP). Integrated with a confidence-margin fast-path gate (G3) in a streaming sliding window (W=3, F=1), our fast path routes 75.6% of syndrome windows with zero logical errors (P_L,accept = 0.0000) and an end-to-end pipeline logical error rate of P_pipe = 1.90e-4 at 102.4 ns mean latency (240 ns max), driving queue overflow below 6.0e-5 (0 overflows observed in 50,000 test windows for buffer B >= 4) under a 1 microsecond quantum cycle budget. We synthesize and verify our architecture in SystemVerilog, attaining 10,000-shot bit-exact hardware-software parity, and establish a folding Pareto frontier on AMD UltraScale+ scaling logic down to 1,226 LUTs (0.51% device utilization).
```

### Keywords / Index Terms
- Quantum error correction
- Quantum low-density parity-check (QLDPC) codes
- Bivariate-bicycle codes
- Neural belief propagation
- Automorphism group orbits
- Sliding-window decoding
- Fixed-point quantization
- Multiplier-free CSD arithmetic
- FPGA hardware acceleration
- Real-time quantum control

---

## 2. Author Details (ScholarOne Step 3)

### Author 1 (Lead & Corresponding Author)
| Field | Value |
|---|---|
| **First (Given) Name** | Md. |
| **Last (Family) Name** | Nazmul |
| **ORCID** | `0009-0001-6115-7023` |
| **Email Address** | `nazmulhas36@gmail.com` |
| **Institution / University** | College of Technology, National University |
| **Department** | Department of Computer Science and Engineering |
| **City, Postal Code** | Gazipur, 1704 |
| **Country** | Bangladesh |
| **Role** | Project Leader / Corresponding Author |

### Author 2 (Co-Author)
| Field | Value |
|---|---|
| **First (Given) Name** | Musrat Jahan |
| **Last (Family) Name** | Gungun |
| **ORCID** | `0009-0006-4249-9198` |
| **Institution / University** | College of Technology, National University |
| **Department** | Department of Computer Science and Engineering |
| **City, Postal Code** | Gazipur, 1704 |
| **Country** | Bangladesh |
| **Role** | Project Member / Researcher |

### Author 3 (Faculty Supervisor)
| Field | Value |
|---|---|
| **First (Given) Name** | Maheli |
| **Last (Family) Name** | Ahmed |
| **ORCID** | `0000-0002-5183-7498` |
| **Institution / University** | College of Technology, National University |
| **Department** | Department of Computer Science and Engineering |
| **City, Postal Code** | Gazipur, 1704 |
| **Country** | Bangladesh |
| **Role** | Faculty Supervisor |

---

## 3. Suggested Expert Reviewers (ScholarOne Step 4)

### Reviewer 1
- **Name:** Dr. Sergey Bravyi
- **Institution:** IBM Quantum, IBM T.J. Watson Research Center, Yorktown Heights, NY, USA
- **E-mail:** `sbravyi@us.ibm.com`
- **Expertise / Rationale:** Originator of Bivariate-Bicycle QLDPC codes (Nature 2024), expert in fault-tolerant syndrome measurement architectures and quantum LDPC decoding algorithms.

### Reviewer 2
- **Name:** Dr. Nicolas Delfosse
- **Institution:** IonQ (formerly Principal Researcher at Microsoft Quantum), College Park, MD, USA
- **E-mail:** `ndelfosse@ionq.com`
- **Expertise / Rationale:** Pioneer of sliding-window decoding for topological and LDPC codes, developer of Union-Find decoding, and leading expert in space-time hypergraph symmetries.

### Reviewer 3
- **Name:** Dr. Joschka Roffe
- **Institution:** Freeform Labs / University of Strathclyde, Glasgow, UK
- **E-mail:** `joschka@roffe.eu`
- **Expertise / Rationale:** Developer of the open-source BP-OSD library (LDPC-v2), world authority on message-passing and ordered statistics decoding for high-rate quantum LDPC codes.

### Reviewer 4
- **Name:** Prof. Barbara M. Terhal
- **Institution:** QuTech and Department of Quantum Nanoscience, Delft University of Technology, Delft, Netherlands
- **E-mail:** `b.m.terhal@tudelft.nl`
- **Expertise / Rationale:** Leading authority on fault-tolerant quantum computing architectures, quantum memory thresholds, and hardware requirements for real-time error correction.

---

## 4. Mandatory Submission Declarations (ScholarOne Step 5)

### Conflict of Interest Statement
```
The authors declare that there are no financial, personal, or professional conflicts of interest that could be perceived as influencing the work reported in this manuscript.
```

### Data and Code Availability Statement
```
All code, models, synthesizeable SystemVerilog RTL, simulation scripts, and benchmark datasets supporting the findings of this study are available in a public GitHub repository at https://github.com/NazmulHasanNihal/orbit-tied-qnbp-sliding-window-bb and have been published as an open-source Python package 'orbit-tied-qnbp' (v1.0.0) on the Python Package Index (PyPI). All random seeds and benchmark configurations are pinned for exact empirical reproduction.
```

### Funding and Acknowledgment Statement
```
This work was supported in part by the Open Quantum Error Correction Research Initiative. The authors thank the open-source quantum computing community and developers of Stim, PyTorch, and PyMuPDF.
```

### AI Disclosure Statement (IEEE Author Guidelines Compliance)
```
Generative AI and automated toolchains were utilized solely for code linting, automated layout bounds verification, and script formatting. All scientific formulations, mathematical proofs (Theorems 1–3), decoder architectures, SystemVerilog hardware RTL, and empirical conclusions were conceived, verified, and authored by the authors.
```

### Prior Publication / Dual Submission Certification
```
The authors certify that this manuscript is original work, has not been published previously, and is not currently under consideration for publication elsewhere.
```

---

## 5. File Upload Checklist (ScholarOne Step 6)

1. `main.pdf` &rarr; File Designation: **Main Document / Manuscript File**
2. `cover_letter.pdf` &rarr; File Designation: **Cover Letter**
3. `manuscript_sources.zip` &rarr; File Designation: **Supplementary Material / Source Files**
