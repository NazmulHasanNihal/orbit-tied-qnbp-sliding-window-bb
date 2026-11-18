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
Quantum Low-Density Parity-Check (QLDPC) bivariate-bicycle (BB) codes offer order-of-magnitude reductions in physical qubit overhead compared to topological surface codes. However, their non-local check connectivity generates dense 3D space-time detector error models (DEM) that strain real-time decoding within microsecond coherence intervals. In this paper, we propose an orbit-tied, 6-bit quantized neural belief propagation (QNBP) decoder tailored for real-time sliding-window processing of BB codes. By mapping the 2D torus translation group G = Z_l x Z_m, we demonstrate that spatial shifts constitute exact DEM graph automorphisms, collapsing 7,308 circuit fault mechanisms into 203 symmetry orbits (R=3, a 36x parameter reduction on the 72-qubit BB code [[72,12,6]], and 14,616 mechanisms into 203 orbits, a 72x reduction, on the [[144,12,12]] gross code) while enforcing geometric equivariance and mitigating untied neural overfitting. To enable multiplier-free hardware synthesis with zero Digital Signal Processing (DSP) slices (DSP=0), we develop a Canonical Signed-Digit (CSD) shift-and-add architecture using power-of-two dyadic quantization (Delta = 2^-2) and pre-scaled priors (kappa = 0.75). Benchmarked against ten decoders under circuit-level Stim depolarizing noise (p in [10^-3, 5x10^-3]), our 6-bit integer QNBP model with learned signed memory damping (gamma in [-0.5, 1.0]) converges in 6.4 mean iterations to a logical error rate of P_L = 0.0068 [0.0053, 0.0086], outperforming scalar Mem-BP (chi^2 = 14.72, p = 0.000125) and hardware-capped IBM Relay-BP (chi^2 = 12.06, p = 0.000515) with zero DSP blocks. Under superconducting transmon dephasing bias (eta = 100), QNBP naturally adapts message weighting, suppressing logical errors 8.0x down to P_L = 0.0010 (20.0x over Classical BP). Integrated with a confidence-margin fast-path gate (G3), 75.6% of syndrome windows exit in 102.4 ns mean latency with zero accepted errors (P_L,accept = 0.0000) and P_pipe = 1.90 x 10^-4, resolving queue overflow below 6.0 x 10^-5 under a 1 microsecond quantum cycle budget.
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
| **ORCID Identifier** | `0009-0001-6115-7023` |
| **Direct Record URL** | https://orcid.org/0009-0001-6115-7023 |
| **Email Address** | `nazmulhas36@gmail.com` |
| **Institution / University** | College of Technology, National University |
| **Department** | Department of Computer Science and Engineering |
| **City, Postal Code** | Gazipur, 1704 |
| **Country** | Bangladesh |
| **Role** | Lead Researcher, Conceptualization, Methodology & Software Architecture |

### Author 2 (Co-Author)
| Field | Value |
|---|---|
| **First (Given) Name** | Musrat Jahan |
| **Last (Family) Name** | Gungun |
| **ORCID Identifier** | `0009-0006-4249-9198` |
| **Direct Record URL** | https://orcid.org/0009-0006-4249-9198 |
| **Email Address** | `gungunjahan84@gmail.com` |
| **Institution / University** | College of Technology, National University |
| **Department** | Department of Computer Science and Engineering |
| **City, Postal Code** | Gazipur, 1704 |
| **Country** | Bangladesh |
| **Role** | Data Curation, Baseline Benchmarking, Validation & Statistical Testing |

### Author 3 (Co-Author & Faculty Supervisor)
| Field | Value |
|---|---|
| **First (Given) Name** | Maheli |
| **Last (Family) Name** | Ahmed |
| **ORCID Identifier** | `0000-0002-5183-7498` |
| **Direct Record URL** | https://orcid.org/0000-0002-5183-7498 |
| **Email Address** | `maheli.ahmed.cse.cot@gmail.com` |
| **Institution / University** | College of Technology, National University |
| **Department** | Department of Computer Science and Engineering |
| **City, Postal Code** | Gazipur, 1704 |
| **Country** | Bangladesh |
| **Role** | Faculty Supervision, Resources, Formal Analysis & Model Governance |

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
