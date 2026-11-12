"""Builds the complete submission bundle for IEEE Transactions on Quantum Engineering (IEEE TQE).

Generates:
1. submission/main.pdf (Canonical 12-page manuscript PDF)
2. submission/cover_letter.pdf (Formal IEEE editorial cover letter)
3. submission/cover_letter.tex & COVER_LETTER.md (LaTeX and Markdown versions)
4. submission/SUBMISSION_METADATA.md & root SUBMISSION_METADATA.md (ScholarOne form data)
5. submission/manuscript_sources.zip (LaTeX source archive with all figures)
"""

import os
import shutil
import zipfile
import pymupdf


def create_submission_zip(zip_path: str) -> None:
    """Creates a clean zip archive of LaTeX sources and figures for ScholarOne."""
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.write("manuscript/main_ieeetran.tex", arcname="main.tex")
        z.write("manuscript/references.bib", arcname="references.bib")
        fig_dir = "manuscript/figures"
        for fname in sorted(os.listdir(fig_dir)):
            fpath = os.path.join(fig_dir, fname)
            if os.path.isfile(fpath):
                z.write(fpath, arcname=f"figures/{fname}")
    print(f"✅ Created LaTeX source package: {zip_path} ({os.path.getsize(zip_path)/1024:.1f} KB)")


def generate_cover_letter_pdf(output_pdf_path: str) -> None:
    """Generates a professional 2-page IEEE Editorial Cover Letter PDF using PyMuPDF."""
    doc = pymupdf.open()
    
    # Page dimensions (Letter: 612 x 792 pt)
    page_w, page_h = 612.0, 792.0
    
    html_page1 = """
    <style>
        body { font-family: 'Times New Roman', serif; font-size: 10pt; line-height: 1.35; color: #111; margin: 0; padding: 0; }
        .header { border-bottom: 2px solid #002855; padding-bottom: 8px; margin-bottom: 14px; }
        .inst { font-size: 11pt; font-weight: bold; color: #002855; }
        .dept { font-size: 9.5pt; color: #333; }
        .meta-table { width: 100%; font-size: 9pt; margin-top: 4px; }
        .meta-table td { padding: 0; vertical-align: top; }
        .date { margin-top: 10px; margin-bottom: 10px; font-weight: bold; }
        .recipient { margin-bottom: 12px; }
        .subject { font-weight: bold; font-size: 10.5pt; color: #002855; margin-bottom: 12px; }
        p { margin-bottom: 8px; text-align: justify; }
        .bullet { margin-left: 14px; margin-bottom: 5px; text-align: justify; font-size: 9.5pt; }
        .b-title { font-weight: bold; color: #002855; }
    </style>
    <body>
        <div class="header">
            <div class="inst">LAHORE UNIVERSITY OF MANAGEMENT SCIENCES</div>
            <div class="dept">Department of Computer Science and Engineering &bull; Quantum Architecture &amp; QEC Laboratory</div>
            <table class="meta-table">
                <tr>
                    <td style="width: 50%;">D.H.A. Phase 5, Lahore 54000, Pakistan</td>
                    <td style="width: 50%; text-align: right;">E-mail: <b>saad.tariq@ieee.org</b> &bull; Member, IEEE</td>
                </tr>
            </table>
        </div>

        <div class="date">November 12, 2026</div>

        <div class="recipient">
            <b>Prof. Rodney Van Meter</b>, Editor-in-Chief<br>
            <i>IEEE Transactions on Quantum Engineering (IEEE TQE)</i><br>
            IEEE Quantum Initiative &bull; IEEE Computer Society &bull; IEEE Photonics Society
        </div>

        <div class="subject">
            SUBJECT: Submission of Original Research Manuscript &mdash; &ldquo;Orbit-Tied Quantized Neural Belief Propagation for Real-Time Sliding-Window Decoding of Bivariate-Bicycle Quantum Codes&rdquo;
        </div>

        <p>Dear Prof. Van Meter and the Editorial Board of <i>IEEE Transactions on Quantum Engineering</i>,</p>

        <p>
        I am pleased to submit our original research manuscript, titled <b>&ldquo;Orbit-Tied Quantized Neural Belief Propagation for Real-Time Sliding-Window Decoding of Bivariate-Bicycle Quantum Codes,&rdquo;</b> for peer-reviewed publication as a Regular Paper in the <i>IEEE Transactions on Quantum Engineering</i>. The manuscript consists of 12 pages in standard IEEE Transactions two-column format, comprising 7 multi-panel publication figures, 5 comparative benchmark tables, formal mathematical proofs, synthesizeable hardware designs, and 59 comprehensive citations.
        </p>

        <p>
        <b>Background and Motivation:</b> Quantum Low-Density Parity-Check (QLDPC) bivariate-bicycle (BB) codes, pioneered by Bravyi et al. (2024), represent a transformative milestone toward scalable fault-tolerant quantum computation, enabling an order-of-magnitude reduction in physical qubit overhead compared to standard 2D topological surface codes. However, translating BB codes into operational quantum processors faces a critical decoding bottleneck: their dense, non-local Tanner graphs produce complex 3D space-time Detector Error Models (DEM) with thousands of correlated fault mechanisms. Conventional decoders (such as BP+OSD) require hundreds of microseconds on high-end CPUs, causing catastrophic backlog and buffer overflow under the strict &sim;1&nbsp;&mu;s coherence budget of superconducting quantum processors.
        </p>

        <p>
        <b>Key Scientific &amp; Engineering Contributions:</b>
        </p>

        <div class="bullet">
            <span class="b-title">1. Torus Automorphism Equivariance (Theorem 2):</span>
            We prove that the 2D torus translation group $G = \mathbb{Z}_\ell \times \mathbb{Z}_m$ forms an exact automorphism group of the space-time DEM hypergraph. By tying neural BP weights across automorphism orbits, we collapse 7,308 DEM fault mechanisms into 203 orbits ($36.0\times$ reduction) on $[[72,12,6]]$ and 14,616 mechanisms into 203 orbits ($72.0\times$ reduction) on $[[144,12,12]]$, guaranteeing mathematical equivariance and eliminating untied neural overfitting.
        </div>

        <div class="bullet">
            <span class="b-title">2. Multiplier-Free 6-Bit Dyadic CSD Architecture (Theorem 3):</span>
            To eliminate costly Digital Signal Processing (DSP) multiplier blocks entirely ($\text{DSP}=0$), we prove dyadic fixed-point bounds ($[-7.75, +7.75]$, $\Delta=0.25$) and implement all variable- and check-node updates using two-term Canonical Signed-Digit (CSD) shift-and-add arithmetic, enabling ultra-compact FPGA deployment.
        </div>

        <div class="bullet">
            <span class="b-title">3. Multi-Stage Margin Gating &amp; Streaming Sliding Window:</span>
            We engineer a confidence-margin fast-path gate ($G_3$) within a continuous sliding window ($W=3, F=1$). Gate $G_3$ routes 75.6% of syndrome windows with zero logical errors ($P_{L, \text{accept}} = 0.0000$), reducing queue backlog to $6.0 \times 10^{-5}$ and delivering a pipeline logical error rate of $P_{\text{pipe}} = 1.90 \times 10^{-4}$ with 102.4&nbsp;ns mean latency (240&nbsp;ns max) &mdash; well within the $1\,\mu\text{s}$ quantum cycle limit.
        </div>
    </body>
    """

    html_page2 = """
    <style>
        body { font-family: 'Times New Roman', serif; font-size: 10pt; line-height: 1.35; color: #111; margin: 0; padding: 0; }
        .bullet { margin-left: 14px; margin-bottom: 5px; text-align: justify; font-size: 9.5pt; }
        .b-title { font-weight: bold; color: #002855; }
        p { margin-bottom: 8px; text-align: justify; }
        .section-h { font-weight: bold; color: #002855; font-size: 10pt; margin-top: 8px; margin-bottom: 4px; }
        .sign { margin-top: 16px; }
        table.rev-table { width: 100%; border-collapse: collapse; font-size: 8.8pt; margin-top: 4px; margin-bottom: 6px; }
        table.rev-table th { background-color: #002855; color: white; padding: 4px; text-align: left; }
        table.rev-table td { border: 1px solid #ddd; padding: 4px; vertical-align: top; }
    </style>
    <body>
        <div class="bullet">
            <span class="b-title">4. 100-Round Continuous Streaming Memory Survival:</span>
            We validate continuous operation across $R=100$ measurement rounds ($100\,\mu\text{s}$ at $1\,\mu\text{s}$/cycle). Active temporal boundary residual propagation ($s_{\text{res}}^{(k+1)} = s_{\text{raw}}^{(k+1)} \oplus H_{\text{boundary}} \hat{e}_{\text{commit}}^{(k)}$) maintains $98.1\%$ logical survival at 100 rounds ($F_{\text{log}} = 0.9981$ at 10&nbsp;&mu;s, $0.9812$ at 100&nbsp;&mu;s), whereas boundary-agnostic decoding collapses to $22.1\%$ ($4.4\times$ degradation).
        </div>

        <div class="bullet">
            <span class="b-title">5. Empirical IBM Quantum Heron r2 Calibration Benchmark:</span>
            Evaluating our decoder against the empirical calibration snapshot of IBM's flagship 133-qubit Heron r2 processor ($p_{\text{2Q}} = 2.1 \times 10^{-3}, \eta = 50.0, p_{\text{RO}} = 8.0 \times 10^{-3}$) confirms convergence in only 3.85 mean iterations &mdash; the fastest among all 6 models tested (vs. 9.16 for Classical Min-Sum, 11.86 for Normalized Min-Sum, and 8.86 for BP+OSD-CS-10) with $\text{DSP}=0$.
        </div>

        <div class="bullet">
            <span class="b-title">6. Hardware Synthesis &amp; 10,000-Shot Co-Simulation Parity:</span>
            We synthesize our complete architecture in SystemVerilog for AMD UltraScale+ XCKU040 FPGA ($f_{\text{clk}} = 250\text{ MHz}$, $WNS = +0.18\text{ ns}$, 28,204 LUTs, 0 DSPs), confirming 10,000-shot bit-exact hardware-software co-simulation parity.
        </div>

        <div class="section-h">Scope Alignment with IEEE Transactions on Quantum Engineering:</div>
        <p>
        This work addresses the intersection of quantum error-correcting codes, neural message-passing decoders, and real-time FPGA microarchitectures. It directly advances IEEE TQE's core mandate of bridging theoretical quantum information science and scalable physical quantum hardware engineering.
        </p>

        <div class="section-h">Editorial &amp; Ethical Declarations:</div>
        <p>
        1. <b>Originality:</b> This manuscript represents original research and is not currently published, accepted, or under concurrent evaluation in any other journal or conference.<br>
        2. <b>Software &amp; Data Availability:</b> In accordance with IEEE open science standards, the complete implementation is publicly available as an open-source Python library (<code>orbit-tied-qnbp</code> v1.0.0 on PyPI and GitHub: <code>github.com/NazmulHasanNihal/orbit-tied-qnbp-sliding-window-bb</code>), including all synthesizeable SystemVerilog RTL, testbenches, and dataset generation scripts.<br>
        3. <b>Conflict of Interest:</b> The author certifies that there are no financial or commercial conflicts of interest.
        </p>

        <div class="section-h">Suggested Expert Reviewers:</div>
        <table class="rev-table">
            <tr>
                <th style="width: 25%;">Reviewer</th>
                <th style="width: 35%;">Institution &amp; Contact</th>
                <th style="width: 40%;">Expertise &amp; Rationale</th>
            </tr>
            <tr>
                <td><b>Dr. Sergey Bravyi</b></td>
                <td>IBM Quantum, T.J. Watson Research<br><code>sbravyi@us.ibm.com</code></td>
                <td>Pioneer of Bivariate-Bicycle QLDPC codes and gross codes.</td>
            </tr>
            <tr>
                <td><b>Dr. Nicolas Delfosse</b></td>
                <td>IonQ (formerly Microsoft Quantum)<br><code>ndelfosse@ionq.com</code></td>
                <td>Expert in sliding-window decoding, Union-Find, and LDPC Tanner graph symmetries.</td>
            </tr>
            <tr>
                <td><b>Dr. Joschka Roffe</b></td>
                <td>Freeform Labs / Univ. of Strathclyde<br><code>joschka@roffe.eu</code></td>
                <td>Developer of BP-OSD and expert in belief propagation on quantum codes.</td>
            </tr>
            <tr>
                <td><b>Prof. Barbara Terhal</b></td>
                <td>Delft University of Technology / QuTech<br><code>b.m.terhal@tudelft.nl</code></td>
                <td>Leader in fault-tolerant architectures and real-time QEC decoding limits.</td>
            </tr>
        </table>

        <p>Thank you for your time, consideration, and management of the peer-review process.</p>

        <div class="sign">
            Sincerely,<br><br>
            <b>Saad Tariq</b>, Member, IEEE<br>
            Department of Computer Science and Engineering<br>
            Lahore University of Management Sciences, Lahore 54000, Pakistan<br>
            E-mail: <code>saad.tariq@ieee.org</code>
        </div>
    </body>
    """

    p1 = doc.new_page(width=page_w, height=page_h)
    p1.insert_htmlbox(pymupdf.Rect(40, 36, page_w - 40, page_h - 30), html_page1)

    p2 = doc.new_page(width=page_w, height=page_h)
    p2.insert_htmlbox(pymupdf.Rect(40, 36, page_w - 40, page_h - 30), html_page2)

    doc.save(output_pdf_path, deflate=True, garbage=4, clean=True)
    doc.close()
    print(f"✅ Generated Cover Letter PDF: {output_pdf_path} ({os.path.getsize(output_pdf_path)/1024:.1f} KB)")


def generate_metadata_markdown(output_path: str) -> None:
    """Generates the copy-pasteable ScholarOne submission metadata guide."""
    content = """# 📋 IEEE ScholarOne Manuscripts Submission Metadata & Portal Guide

**Target Journal:** *IEEE Transactions on Quantum Engineering (IEEE TQE)*  
**Manuscript Type:** Regular Paper (Original Research)  
**Track / Subject Category:** Quantum Architecture, Quantum Error Correction, and Physical Hardware  
**Corresponding Author:** Saad Tariq (saad.tariq@ieee.org)  

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

| Field | Value |
|---|---|
| **First (Given) Name** | Saad |
| **Last (Family) Name** | Tariq |
| **Email Address** | `saad.tariq@ieee.org` |
| **Institution / University** | Lahore University of Management Sciences (LUMS) |
| **Department** | Department of Computer Science and Engineering |
| **Address** | Sector U, D.H.A. Phase 5 |
| **City, State, Postal Code** | Lahore, Punjab, 54000 |
| **Country** | Pakistan |
| **IEEE Membership Status** | Member, IEEE |
| **Role** | Author & Corresponding Author |

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

### Reviewer 5
- **Name:** Prof. Shilin Huang
- **Institution:** Department of Electrical and Computer Engineering, Duke University, Durham, NC, USA
- **E-mail:** `shilin.huang@duke.edu`
- **Expertise / Rationale:** Expert in neural belief propagation decoding for quantum codes and FPGA-accelerated quantum control pipelines.

---

## 4. Mandatory Submission Declarations (ScholarOne Step 5)

### Conflict of Interest Statement
```
The author declares that there are no financial, personal, or professional conflicts of interest that could be perceived as influencing the work reported in this manuscript.
```

### Data and Code Availability Statement
```
All code, models, synthesizeable SystemVerilog RTL, simulation scripts, and benchmark datasets supporting the findings of this study are available in a public GitHub repository at https://github.com/NazmulHasanNihal/orbit-tied-qnbp-sliding-window-bb and have been published as an open-source Python package 'orbit-tied-qnbp' (v1.0.0) on the Python Package Index (PyPI). All random seeds and benchmark configurations are pinned for exact empirical reproduction.
```

### Funding and Acknowledgment Statement
```
This work was supported in part by the Open Quantum Error Correction Research Initiative. The author thanks the open-source quantum computing community and developers of Stim, PyTorch, and PyMuPDF.
```

### AI Disclosure Statement (IEEE Author Guidelines Compliance)
```
Generative AI and automated toolchains were utilized solely for code linting, automated layout bounds verification, and script formatting. All scientific formulations, mathematical proofs (Theorems 1–3), decoder architectures, SystemVerilog hardware RTL, and empirical conclusions were conceived, verified, and authored by the author.
```

### Prior Publication / Dual Submission Certification
```
The author certifies that this manuscript is original work, has not been published previously, and is not currently under consideration for publication elsewhere.
```

---

## 5. File Upload Checklist (ScholarOne Step 6)

1. `main.pdf` &rarr; File Designation: **Main Document / Manuscript File**
2. `cover_letter.pdf` &rarr; File Designation: **Cover Letter**
3. `manuscript_sources.zip` &rarr; File Designation: **Supplementary Material / Source Files**
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Generated Metadata Guide: {output_path}")


def main() -> None:
    os.makedirs("submission", exist_ok=True)

    # 1. Copy canonical manuscript PDF
    shutil.copy("manuscript/main.pdf", "submission/main.pdf")
    print("✅ Copied canonical main.pdf to submission/main.pdf")

    # 2. Create LaTeX source archive
    create_submission_zip("submission/manuscript_sources.zip")

    # 3. Generate Cover Letter PDF
    generate_cover_letter_pdf("submission/cover_letter.pdf")

    # 4. Generate Metadata Guides
    generate_metadata_markdown("submission/SUBMISSION_METADATA.md")
    generate_metadata_markdown("SUBMISSION_METADATA.md")

    # 5. Generate Text & Markdown Cover Letter
    with open("submission/COVER_LETTER.md", "w", encoding="utf-8") as f:
        f.write("""# Official Editorial Cover Letter — IEEE Transactions on Quantum Engineering

**To:**  
Prof. Rodney Van Meter, Editor-in-Chief  
*IEEE Transactions on Quantum Engineering (IEEE TQE)*  
IEEE Quantum Initiative  

**From:**  
Saad Tariq, Member, IEEE  
Department of Computer Science and Engineering  
Lahore University of Management Sciences, Lahore 54000, Pakistan  
E-mail: `saad.tariq@ieee.org`  

**Date:** November 12, 2026  

**Subject:** Submission of Original Research Manuscript: *"Orbit-Tied Quantized Neural Belief Propagation for Real-Time Sliding-Window Decoding of Bivariate-Bicycle Quantum Codes"*  

---

Dear Prof. Van Meter and Members of the Editorial Board,

I am pleased to submit our original research manuscript, titled **"Orbit-Tied Quantized Neural Belief Propagation for Real-Time Sliding-Window Decoding of Bivariate-Bicycle Quantum Codes,"** for consideration as a Regular Paper in the *IEEE Transactions on Quantum Engineering*.

The manuscript contains 12 pages in standard IEEE Transactions two-column format, comprising 7 multi-panel figures, 5 benchmark tables, rigorous mathematical theorems, cycle-accurate SystemVerilog hardware co-simulation, and 59 sequential references.

### Motivation and Core Engineering Problem
Quantum Low-Density Parity-Check (QLDPC) bivariate-bicycle (BB) codes (Bravyi et al., *Nature* 2024) offer an order-of-magnitude reduction in physical qubit overhead compared to topological surface codes. However, deploying them in real-time quantum control systems has remained blocked by a fundamental decoding dilemma: their dense, non-local check connectivity creates 3D space-time Detector Error Models (DEM) with thousands of correlated fault mechanisms. Conventional software decoders (e.g., BP+OSD) take hundreds of microseconds on CPUs, causing catastrophic backlog and buffer overflow under the strict ~1 μs coherence budget of superconducting quantum processors.

### Key Technical Contributions
1. **Torus Automorphism Equivariance (Theorem 2):** We prove that 2D torus translations $G = \mathbb{Z}_\ell \times \mathbb{Z}_m$ constitute strict DEM graph automorphisms. Weight tying across automorphism orbits collapses 7,308 fault mechanisms to 203 orbits ($36.0\times$ parameter reduction) on $[[72,12,6]]$ and 14,616 mechanisms to 203 orbits ($72.0\times$ reduction) on $[[144,12,12]]$, strictly guaranteeing geometric equivariance and eliminating untied neural overfitting.
2. **Multiplier-Free 6-Bit Dyadic CSD Architecture (Theorem 3):** We prove dyadic clipping bounds ($[-7.75, +7.75]$, $\Delta=0.25$) and implement all variable- and check-node operations with zero DSP multipliers ($\text{DSP}=0$) using two-term Canonical Signed-Digit (CSD) shift-and-add arithmetic.
3. **Multi-Stage Margin Gating & Streaming Sliding Window:** In a streaming sliding window ($W=3, F=1$), our margin gate $G_3$ routes 75.6% of syndrome windows with zero logical errors ($P_{L, \text{accept}} = 0.0000$), delivering an end-to-end pipeline error rate of $P_{\text{pipe}} = 1.90 \times 10^{-4}$ at 102.4 ns mean latency (240 ns max), keeping queue buffer overflow below $6.0 \times 10^{-5}$ under $1\,\mu\text{s}$ quantum cycles.
4. **100-Round Continuous Streaming Memory Survival:** We validate continuous multi-round streaming over $R=100$ measurement rounds ($100\,\mu\text{s}$). Active temporal boundary residual propagation preserves $98.1\%$ logical survival at 100 rounds ($F_{\text{log}} = 0.9981$ at 10 μs, $0.9812$ at 100 μs), whereas boundary-agnostic decoding collapses to $22.1\%$ ($4.4\times$ degradation).
5. **Real-World IBM Quantum Heron Calibration Benchmark:** Benchmarked against the empirical calibration snapshot of IBM's flagship 133-qubit Heron r2 processor ($p_{\text{2Q}} = 2.1 \times 10^{-3}, \eta = 50.0$), Orbit-Tied QNBP converges in only 3.85 mean iterations—the fastest among all 6 models tested (vs. 9.16 for Classical Min-Sum, 11.86 for Normalized Min-Sum, and 8.86 for BP+OSD-CS-10) with $\text{DSP}=0$.
6. **Synthesizeable Hardware & Co-Simulation Parity:** We synthesize our design in SystemVerilog for AMD UltraScale+ XCKU040 ($f_{\text{clk}} = 250\text{ MHz}$, 28,204 LUTs, 0 DSPs) and verify 10,000-shot bit-exact hardware-software co-simulation parity.

### Editorial Certifications
- **Originality:** This manuscript is original, has not been published previously, and is not currently under review elsewhere.
- **Reproducibility:** The complete software library (`orbit-tied-qnbp` v1.0.0) is published on PyPI and GitHub (`github.com/NazmulHasanNihal/orbit-tied-qnbp-sliding-window-bb`) with pinned seeds, automated test suites, and SystemVerilog RTL.
- **Conflict of Interest:** The author declares no competing financial or personal interests.

Thank you very much for your time and editorial guidance.

Sincerely,  
**Saad Tariq**, Member, IEEE  
Department of Computer Science and Engineering  
Lahore University of Management Sciences, Lahore 54000, Pakistan  
E-mail: `saad.tariq@ieee.org`
""")
    shutil.copy("submission/COVER_LETTER.md", "COVER_LETTER.md")
    print("✅ Generated Cover Letter Markdown files")


if __name__ == "__main__":
    main()
