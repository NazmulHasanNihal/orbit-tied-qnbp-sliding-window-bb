# Documentation & Technical Whitepapers

This directory contains the complete technical documentation, mathematical proofs, empirical validation reports, and reproducibility procedures supporting the manuscript:

**"Orbit-Tied Quantized Neural Belief Propagation for Sliding-Window Decoding of Bivariate-Bicycle Codes"**  
*Under Review at IEEE Transactions on Quantum Engineering (TQE)*

---

## 📑 Index of Technical Reports

| Document | Description | Focus Areas |
| :--- | :--- | :--- |
| **[`REPRODUCIBILITY_GUIDE.md`](./REPRODUCIBILITY_GUIDE.md)** | Step-by-step reproduction instructions | Environment setup, automated test suites (46 tests), simulation seeds, figure generation, and table verification. |
| **[`MATHEMATICAL_VALIDATION.md`](./MATHEMATICAL_VALIDATION.md)** | Rigorous mathematical derivations & proofs | Group actions ($G = \mathbb{Z}_\ell \times \mathbb{Z}_m$), permutation equivariance (Proposition 2), dyadic quantization bounds (Lemma 1), CSS decoupling (Proposition 3). |
| **[`HARDWARE_VALIDATION.md`](./HARDWARE_VALIDATION.md)** | Hardware synthesis & microarchitecture | Multiplier-free CSD arithmetic ($DSP=0$), 6-bit integer datapath, energy scaling ($18.84\text{ nJ}$), AXI4-Stream ingress, 216-VNU core. |
| **[`EXPERIMENTAL_VALIDATION.md`](./EXPERIMENTAL_VALIDATION.md)** | Benchmark empirical analysis | Master benchmark comparison across 10 decoders, McNemar $\chi^2$ statistical significance tests, Gate $G_3$ calibration, and 100-round continuous streaming tests. |
| **[`../FINAL_VERIFICATION.md`](../FINAL_VERIFICATION.md)** | 12-phase technical audit & verification scorecard | Verification matrix of all 76 claims with 39 automated assertions passing (100.0%). |
| **[`../CLAIMS_LEDGER.md`](../CLAIMS_LEDGER.md)** | Quantitative claim traceability ledger | Every number in paper, README, and docs mapped to source JSON artifact. |
| **[`../REVIEWER_RISKS.md`](../REVIEWER_RISKS.md)** | Peer-review defense dossier | Detailed mathematical, architectural, and baseline answers to 15 hardest referee questions. |
| **[`../TODO_HUMAN.md`](../TODO_HUMAN.md)** | External hardware & cluster instructions | Exact CLI commands for Vivado implementation, Verilator co-sim, and $N \ge 10^6$ Monte Carlo scaling. |
| **[`../CHANGELOG.md`](../CHANGELOG.md)** | Technical development & audit changelog | Detailed audit history across all development and audit phases. |
| **[`AUDIT_REPORT.md`](./AUDIT_REPORT.md)** | Baseline peer-review audit | Comprehensive verification report against IEEE Transactions author standards. |
| **[`RESEARCH_PLAN.md`](./RESEARCH_PLAN.md)** | Initial unified research roadmap | Original monolithic research plan, milestone breakdown, and architectural targets for the project. |

---

## 🏛️ Author & Citation Information

1. **Md. Nazmul** (Lead & Corresponding Author)  
   * **Role:** Lead Researcher, Conceptualization, Methodology & Software Architecture  
   * **Email:** [`nazmulhas36@gmail.com`](mailto:nazmulhas36@gmail.com)  
   * **ORCID:** [0009-0001-6115-7023](https://orcid.org/0009-0001-6115-7023)

2. **Musrat Jahan Gungun** (Co-Author)  
   * **Role:** Data Curation, Baseline Benchmarking, Validation & Statistical Testing  
   * **Email:** [`gungunjahan84@gmail.com`](mailto:gungunjahan84@gmail.com)  
   * **ORCID:** [0009-0006-4249-9198](https://orcid.org/0009-0006-4249-9198)

3. **Maheli Ahmed** (Co-Author & Faculty Supervisor)  
   * **Role:** Faculty Supervision, Resources, Formal Analysis & Model Governance  
   * **Email:** [`maheli.ahmed.cse.cot@gmail.com`](mailto:maheli.ahmed.cse.cot@gmail.com)  
   * **ORCID:** [0000-0002-5183-7498](https://orcid.org/0000-0002-5183-7498)

*Department of Computer Science and Engineering, College of Technology, National University, Gazipur, Bangladesh*

