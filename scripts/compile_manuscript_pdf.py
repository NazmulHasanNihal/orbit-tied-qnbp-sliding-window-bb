"""Compiles the 12-Page Extended IEEE Journal Manuscript into a Publication-Grade PDF.

Generates manuscript/main.pdf formatted in IEEE Transactions journal style
complete with title, abstract, mathematical formulations, Theorems 1, 2, 3,
Proposition 1, Corollary 1, Tables I, II, III, IV, V, all 7 embedded vector
figures (Figures 1-7), and comprehensive 59-reference bibliography with verified DOIs.
"""

from typing import List, Dict, Any
import os
import re
import pymupdf


def build_ieee_manuscript_pdf(
    output_pdf_path: str = "manuscript/main.pdf",
    figures_dir: str = "results/figures",
) -> None:
    """Builds an exhaustive 12-page publication PDF of the complete research paper."""
    doc = pymupdf.open()
    page_w, page_h = 612.0, 792.0  # US Letter (points)

    def add_header_footer(page: pymupdf.Page, page_num: int) -> None:
        header_rect = pymupdf.Rect(40, 18, page_w - 40, 32)
        footer_rect = pymupdf.Rect(40, page_h - 26, page_w - 40, page_h - 12)
        page.insert_textbox(
            header_rect,
            "IEEE TRANSACTIONS ON QUANTUM ENGINEERING, VOL. XX, NO. X, 2026",
            fontsize=7.5, fontname="Helvetica-Bold", color=(0.4, 0.4, 0.4)
        )
        page.insert_textbox(
            footer_rect,
            f"Page {page_num} of 12",
            fontsize=7.5, fontname="Helvetica", align=pymupdf.TEXT_ALIGN_RIGHT, color=(0.4, 0.4, 0.4)
        )

    base_style = """
    <style>
        body { font-family: times; font-size: 8.6pt; line-height: 1.30; color: #111; }
        h1 { font-family: times; font-size: 14.5pt; font-weight: bold; text-align: center; margin-bottom: 4px; line-height: 1.15; }
        .authors { font-family: times; font-size: 9.5pt; text-align: center; margin-bottom: 3px; }
        .affil { font-family: times; font-size: 8.0pt; font-style: italic; text-align: center; color: #444; margin-bottom: 8px; }
        .abstract-box { border-top: 1px solid #222; border-bottom: 1px solid #222; padding: 5px 0; margin-bottom: 8px; }
        .abstract-title { font-weight: bold; font-size: 8.6pt; }
        .keywords { font-size: 8.0pt; margin-top: 4px; }
        h2 { font-family: helvetica; font-size: 9.8pt; font-weight: bold; margin-top: 5px; margin-bottom: 3px; border-bottom: 0.5px solid #888; text-transform: uppercase; }
        h3 { font-family: helvetica; font-size: 8.8pt; font-weight: bold; margin-top: 4px; margin-bottom: 2px; }
        p { text-align: justify; margin-bottom: 4px; text-indent: 10pt; }
        .noindent { text-indent: 0pt; }
        .math-block { text-align: center; font-family: times; font-style: italic; margin: 3.5px 0; font-size: 9.0pt; }
        .theorem { background: #f8f9fa; border-left: 3px solid #1565c0; padding: 4px 7px; margin: 5px 0; font-size: 8.3pt; }
        .corollary { background: #f4fbf7; border-left: 3px solid #2e7d32; padding: 4px 7px; margin: 5px 0; font-size: 8.3pt; }
        table { width: 100%; border-collapse: collapse; margin: 4px 0; font-size: 7.2pt; }
        th { border-top: 1.5px solid #222; border-bottom: 1px solid #222; padding: 2.2px; text-align: center; font-weight: bold; }
        td { border-bottom: 0.5px solid #ddd; padding: 2.0px; text-align: center; }
        .table-caption { font-size: 7.8pt; font-weight: bold; margin-bottom: 2px; text-align: center; }
        .ref-item { font-size: 5.4pt; line-height: 1.10; margin-bottom: 2.5px; text-align: justify; text-indent: -10pt; padding-left: 10pt; }
    </style>
    """

    # =============================================================
    # PAGE 1: Title, Abstract, Introduction, Figure 1
    # =============================================================
    p1 = doc.new_page(width=page_w, height=page_h)
    add_header_footer(p1, 1)

    html_p1 = base_style + """
    <body>
        <h1>Orbit-Tied Quantized Neural Belief Propagation for Real-Time Sliding-Window Decoding of Bivariate-Bicycle Quantum Codes</h1>
        <div class="authors">Md. Nazmul, Musrat Jahan Gungun, and Maheli Ahmed</div>
        <div class="affil">Department of Computer Science and Engineering, College of Technology, National University, Gazipur-1704, Bangladesh<br>(e-mail: nazmulhas36@gmail.com, gungunjahan84@gmail.com, maheli.ahmed.cse.cot@gmail.com). Md. Nazmul is the corresponding author.</div>
        <div class="abstract-box">
            <span class="abstract-title">Abstract&mdash;</span>
            Bivariate-bicycle (BB) quantum codes offer high encoding rates but generate dense 3D space-time detector error models (DEM) challenging real-time decoding within microsecond coherence intervals. We propose an orbit-tied, 6-bit quantized neural belief propagation (QNBP) decoder for real-time sliding-window processing of BB codes. Spatial shifts under the 2D torus translation group induce exact DEM graph automorphisms, collapsing 7,308 fault mechanisms into 203 spatial symmetry orbits per layer (3,090 total parameters across T=15 unrolled decoding layers, representing a 35.5&times; parameter collapse from 109,620 untied edge weights on [[72,12,6]] and 72.0&times; on [[144,12,12]]), enforcing equivariance and eliminating untied overfitting. We develop a multiplier-free Canonical Signed-Digit (CSD) architecture using dyadic step size (&Delta; = 2<sup>-2</sup>) and pre-scaling (&kappa; = 0.75) with zero DSP slices (DSP=0). Benchmarked against twelve decoders under Stim depolarizing noise (p = 0.003), 6-bit QNBP converges in 6.4 mean iterations to logical error rate P<sub>L</sub> = 0.0068 [0.0053, 0.0086], outperforming scalar Mem-BP and hardware-capped IBM Relay-BP. Under transmon dephasing bias (&eta; = 100), QNBP suppresses logical errors 8.0&times; to P<sub>L</sub> = 0.0010. Integrated with a confidence-margin gate (G<sub>3</sub>), 75.6% of windows exit in 102.4 ns mean latency with zero accepted errors (95% bound 7.92 &times; 10<sup>-5</sup>) and pipeline error P<sub>pipe</sub> = 1.90 &times; 10<sup>-3</sup> at p = 0.003 (7.00 &times; 10<sup>-6</sup> at p = 0.001), resolving queue overflow under a 1 &mu;s quantum cycle deadline.
            <div class="keywords"><i>Index Terms</i>&mdash;Quantum error correction, QLDPC codes, bivariate-bicycle codes, neural belief propagation, automorphism orbits, biased noise, sliding-window decoding, FPGA hardware.</div>
        </div>
        <h2>I. Introduction</h2>
        <p class="noindent"><b>F</b>AULT-TOLERANT quantum computing requires active quantum error correction (QEC) to protect fragile quantum information against environmental decoherence, physical gate infidelities, and measurement noise [1], [2]. While topological 2D surface codes [1], [2], [38], [59] have served as the foundation of early experimental demonstrations due to their nearest-neighbor planar connectivity, classical factor-graph and message-passing decoders [56], [57], [58] face throughput bottlenecks. Furthermore, their asymptotic encoding rate is strictly zero (k/n &rarr; 0). Realizing practical algorithm-scale quantum processors encoding thousands of fault-tolerant logical qubits would require millions of physical qubits under surface code architectures [3].</p>
        <p>Recently, asymptotically good quantum low-density parity-check (QLDPC) codes [4], [26] and dual-cyclic bivariate-bicycle (BB) codes [3], [29], [30], [31] have demonstrated an architectural breakthrough. By defining CSS codes over bivariate polynomial quotient rings R = F<sub>2</sub>[x, y] / &lang;x<sup>&ell;</sup> - 1, y<sup>m</sup> - 1&rang;, BB codes such as the 72-qubit code [[72, 12, 6]] and the [[144, 12, 12]] gross code attain encoding rates k/n &approx; 1/6 to 1/12 while supporting high circuit noise thresholds (p &approx; 0.7%) [3]. This yields up to a 10&times; reduction in physical qubit overhead compared to surface codes.</p>
    </body>
    """
    p1.insert_htmlbox(pymupdf.Rect(40, 34, page_w - 40, 500), html_p1)

    fig1_path = os.path.join(figures_dir, "fig1_architecture.png")
    if os.path.exists(fig1_path):
        p1.insert_image(pymupdf.Rect(40, 505, page_w - 40, 735), filename=fig1_path)
        p1.insert_htmlbox(
            pymupdf.Rect(40, 737, page_w - 40, 762),
            '<div style="font-family: helvetica; font-size: 7.5pt; font-style: italic; text-align: center; line-height: 1.15;">'
            'Fig. 1. End-to-end architecture of the Orbit-Tied Quantized Neural Belief Propagation (QNBP) sliding-window decoding pipeline.'
            '</div>'
        )

    # =============================================================
    # PAGE 2: Section I (cont.), Section II (Mathematical Foundations)
    # =============================================================
    p2 = doc.new_page(width=page_w, height=page_h)
    add_header_footer(p2, 2)

    html_p2 = base_style + """
    <body>
        <p class="noindent">Despite their theoretical appeal, classical real-time decoding remains the principal barrier to physical implementation. In physical quantum platforms such as superconducting transmons and trapped ions, syndrome extraction rounds occur within cycle durations of t<sub>cycle</sub> &approx; 200 ns to 1 &mu;s [3], where decoder processing latency critically impacts overall fault-tolerant logical fidelity [44]. Classical decoding algorithms such as unweighted Min-Sum Belief Propagation (BP) suffer from severe split-belief convergence failures on dense Tanner graphs containing short 4-cycles [5], [24]. While post-processing via Ordered Statistics Decoding (BP+OSD) attains near-optimal pseudo-maximum-likelihood logical error rates [4], [5], [25], its cubic complexity O(V<sup>3</sup>) requires hundreds of microseconds per window, exceeding the quantum cycle budget by orders of magnitude.</p>
        <p>Neural Belief Propagation (NBP) [6], [7] and quantized message-passing neural networks [22], [23], [39], [46] offer a promising pathway by unfolding BP iterations into a deep neural network with learnable scaling factors &alpha;<sub>t</sub> and damping terms &gamma;<sub>t</sub>. However, directly applying unconstrained NBP to QLDPC DEM graphs introduces four critical obstacles:</p>
        <p><b>1. Curse of Dimensionality & Overfitting:</b> Unrolled DEM graphs contain over 10<sup>4</sup> fault mechanisms. Assigning independent trainable parameters to each edge creates over 10<sup>5</sup> parameters, causing catastrophic overfitting on finite training syndromes.</p>
        <p><b>2. High Hardware Multiplier Cost:</b> Standard floating-point or fixed-point neural weights require hardware DSP multiplier slices, which exhaust available FPGA fabric at high check degrees.</p>
        <p><b>3. Continuous Streaming Queue Backlog:</b> Real-time QEC requires decoding continuous streams of syndrome rounds R &rarr; &infin;. A sliding window decoder must commit decoded rounds with deterministic worst-case latency to prevent exponential buffer overflow.</p>
        <p><b>4. Physical Noise Asymmetry:</b> In real-world superconducting hardware, dephasing noise dominates bit-flip noise by orders of magnitude (p<sub>Z</sub> &gg; p<sub>X</sub>) [8], demanding decoders capable of exploiting biased channels without parameter bloat.</p>

        <h2>II. Mathematical Foundations & Related Work</h2>
        <h3>A. Quantum CSS Codes & Polynomial Rings</h3>
        <p class="noindent">Bivariate-Bicycle CSS codes are defined by two commuting polynomials A(x, y) and B(x, y) over the bivariate polynomial quotient ring R = F<sub>2</sub>[x, y] / &lang;x<sup>&ell;</sup> - 1, y<sup>m</sup> - 1&rang; [3]. The physical data qubits reside on two disjoint blocks corresponding to the polynomials, yielding block length n = 2&ell;m. Parity-check matrices are defined as:</p>
        <div class="math-block">H<sub>X</sub> = [A | B], &emsp; H<sub>Z</sub> = [B<sup>T</sup> | A<sup>T</sup>]</div>
        <p class="noindent">where A and B denote the &ell;m &times; &ell;m binary circulant matrix representations of A(x, y) and B(x, y), respectively. CSS commutativity requires:</p>
        <div class="math-block">H<sub>X</sub> H<sub>Z</sub><sup>T</sup> = AB + BA &equiv; 0 (mod 2)</div>
        <p class="noindent">which is identically satisfied because R is commutative. For the [[72, 12, 6]] code, parameters are &ell; = 6, m = 6, with polynomials:</p>
        <div class="math-block">A(x, y) = x<sup>3</sup> + y + y<sup>2</sup>, &emsp; B(x, y) = y<sup>3</sup> + x + x<sup>2</sup></div>
        <p class="noindent">yielding n = 72 data qubits, k = 12 logical qubits, and code distance d = 6. For the [[144, 12, 12]] gross code, parameters are &ell; = 12, m = 6 with identical monomial exponents, yielding n = 144, k = 12, d = 12.</p>

        <h3>B. Space-Time Detector Error Model Hypergraphs</h3>
        <p class="noindent">Under Bravyi et al.'s depth-7 syndrome extraction circuit executed for R rounds with noise rate p, Stim [9] generates a space-time Detector Error Model (DEM). Let G<sub>DEM</sub> = (V, C, E) denote the bipartite graph where V represents error mechanisms (variable nodes with prior probabilities p<sub>v</sub>), C represents detector events (check nodes), and (c, v) &isin; E indicates that fault v triggers detector c. Throughout this work, the primary performance metric P<sub>L</sub> denotes the any-observable logical frame error rate per decoded window, P<sub>L</sub> = P(y&#770; &ne; y), where a trial is deemed in error if any of the k = 12 logical observables is misidentified. We also report the standardized per-round logical error rate defined by P<sub>L,round</sub> = 1 - (1 - P<sub>L</sub>)<sup>1/W</sup>.</p>
        <p>In gross QLDPC codes, physical two-qubit CNOT gates and non-local stabilizer checks excite multiple detectors simultaneously, creating hyperedges that invalidate standard graph matching algorithms such as Minimum-Weight Perfect Matching (MWPM) [1], [10]. Furthermore, the Tanner graph contains short cycles of length 4, which induce limit cycles and trapping sets in classical unweighted Min-Sum BP. To overcome hyperedge degeneracies and trapping sets, recent works have explored diverse algorithmic paradigms, including parallel and sliding-window architectures [17], [18], uncertainty-guided message passing [16], symmetry-breaking heuristics [19], almost-linear-time decoders [21], asymptotically good code constructions [26], matching-assisted belief propagation [32], list and learning-based decoders [33], [34], FPGA-tailored architectures [35], decision-tree and tensor-network decoders [40], [41], planar neural decoders [42], correlated noise decoders [43], beam-search decoding [45], machine-learning message-passing [47], polylogarithmic overhead fault-tolerant schemes [55], and approximately equivariant neural architectures [54].</p>
    </body>
    """
    p2.insert_htmlbox(pymupdf.Rect(40, 34, page_w - 40, page_h - 30), html_p2)

    # =============================================================
    # PAGE 3: Section II-C/D (Competitors), Section III (Proposition 1)
    # =============================================================
    p3 = doc.new_page(width=page_w, height=page_h)
    add_header_footer(p3, 3)

    html_p3 = base_style + """
    <body>
        <h3>C. State-of-the-Art Competitor Baselines & Architectural Positioning</h3>
        <p class="noindent">To evaluate against the forefront of QLDPC decoding, we examine eight competitor baselines and position against related paradigms:</p>
        <p><b>1. Classical & Normalized Min-Sum (A0, A1):</b> Standard unweighted Min-Sum and heuristic attenuation (&alpha; = 0.75 [5]). Without learned per-orbit damping, uniform fixed-point check attenuation under-corrects low-degree checks and stalls on short 4-cycles.</p>
        <p><b>2. IBM Relay-BP [11]:</b> Multi-stage restarted BP with disordered memory weights &gamma;<sub>v</sub> &sim; U[-0.24, 0.66]. While unconstrained 300-leg Relay-BP attains P<sub>L</sub> = 0.0060, its 148.5 mean iterations and 2.38 &mu;s CPU latency drastically exceed real-time limits; when capped to 5 legs (50 iters), P<sub>L</sub> degrades to 0.0090. In contrast, Orbit-Tied QNBP converges in 6.4 mean iterations (102.4 ns) without random restarts.</p>
        <p><b>3. Planar Neural Decoders (Liang et al. [42]):</b> Tailored specifically for 2D planar codes (surface/color) with nearest-neighbor grid connectivity; cannot handle non-local bivariate-bicycle DEM hypergraphs.</p>
        <p><b>4. Equivariant Architectures (Wang et al. [54]):</b> Explores approximate equivariance on continuous geometric domains, whereas Orbit-Tied QNBP enforces <i>exact</i> discrete group equivariance (Proposition 2) on the 2D torus quotient ring.</p>
        <p><b>5. Mem-BP [20], BP-LSD [14], BP+OSD-CS-10 [5], AutDEC [15], GDG Sliding-Window [13]:</b> We also benchmark Mem-BP (&gamma; = 0.35), BP-LSD (order 5), BP+OSD-CS-10 (order 10 over MRB, 320 &mu;s latency), AutDEC (torus search), and GDG sliding window (which degenerates to A1 without inter-window residual propagation).</p>
        <p><b>6. Collaborative Decoders (CoDecoder, Guang et al. [60]):</b> Employs a GPU logical-operator-aware neural frontend routing uncertain shots to a strong CPU/GPU fallback (Cascade [49] or Relay-BP [11]); in contrast, Orbit-Tied QNBP operates as a deterministic, zero-DSP single-FPGA message-passing core with an on-chip CSD fallback.</p>

        <h2>III. Torus Automorphism Group Theory & Space-Time Equivariance</h2>
        <h3>A. The 2D Torus Shift Group</h3>
        <p class="noindent">Let Z<sub>&ell;</sub> &times; Z<sub>m</sub> denote the 2D torus translation group acting on qubit coordinates.</p>
        <div class="theorem">
            <b>Definition 1 (Torus Shift Action).</b> <i>For any displacement vector (&delta;<sub>x</sub>, &delta;<sub>y</sub>) &isin; Z<sub>&ell;</sub> &times; Z<sub>m</sub>, the spatial translation operator T<sub>(&delta;<sub>x</sub>, &delta;<sub>y</sub>)</sub> maps coordinate (x, y) to (x + &delta;<sub>x</sub> mod &ell;, y + &delta;<sub>y</sub> mod m).</i>
        </div>
        <div class="theorem">
            <b>Proposition 1 (Torus Translation Invariance of Space-Time DEM).</b> <i>Let G<sub>DEM</sub> = (V, C, E) be the bipartite space-time detector error model graph generated by compiling an R-round syndrome extraction circuit of a bivariate-bicycle code with parameters (&ell;, m) under uniform or coordinate-independent Pauli noise. Then, for every displacement (&delta;<sub>x</sub>, &delta;<sub>y</sub>) &isin; Z<sub>&ell;</sub> &times; Z<sub>m</sub>, the torus translation operator T<sub>(&delta;<sub>x</sub>, &delta;<sub>y</sub>)</sub> induces an exact graph automorphism of G<sub>DEM</sub>:</i>
            <br>1. Edge preservation: (c, v) &isin; E &hArr; (T(c), T(v)) &isin; E.
            <br>2. Prior probability invariance: <i>p</i>(<i>T</i>(<i>v</i>)) = <i>p</i>(<i>v</i>) for all <i>v</i> &isin; <i>V</i>.
            <br>3. Logical homology preservation: For each logical operator O<sub>k</sub>, the translated operator satisfies T(O<sub>k</sub>) &equiv; O<sub>&pi;(k)</sub> mod stabilizers on the torus for an induced permutation &pi; &isin; S<sub>k</sub>.
        </div>

        <h3>C. Automorphism Subgroup & Symmetry Breaking</h3>
        <p class="noindent">While static code parity checks commute with the full torus symmetry Z<sub>&ell;</sub> &times; Z<sub>m</sub> &rtimes; D<sub>4</sub>, circuit-level DEM compilation reveals that directed CNOT scheduling across ticks 1..6 breaks spatial inversion (x, y) &rarr; (-x, -y) with 6,876 violations. Sliding-window boundaries break temporal translation into three classes, and transmon dephasing breaks CSS duality. Thus, Z<sub>&ell;</sub> &times; Z<sub>m</sub> is the maximal exact automorphism group of the space-time DEM.</p>
        <p class="noindent"><i>Proof:</i> Let C denote the depth-7 syndrome extraction circuit. In each round r &isin; {0, ..., R-1}, the circuit applies single-qubit state preparations, CNOT entangling gates, and projective measurements. Because the parity-check polynomials A(x, y) and B(x, y) are elements of R = F<sub>2</sub>[x, y] / &lang;x<sup>&ell;</sup> - 1, y<sup>m</sup> - 1&rang;, every CNOT gate connecting data qubit (x, y) to check qubit (x', y') is specified by a shift (i, j) that is invariant under global spatial translation.</p>
        <p>Let a physical Pauli fault P &isin; {X, Y, Z} occur on qubit q = (x, y) at circuit tick t. Under Clifford frame propagation, P commutes or anticommutes with subsequent entangling operations according to the polynomial adjacency. Translating the entire error configuration by (&delta;<sub>x</sub>, &delta;<sub>y</sub>) shifts all physical qubit coordinates to (x + &delta;<sub>x</sub> mod &ell;, y + &delta;<sub>y</sub> mod m). Because the gate schedule at the shifted coordinates is identical in gate type, timing, and relative offsets, the propagated error excites detectors at exactly (x<sub>d</sub> + &delta;<sub>x</sub> mod &ell;, y<sub>d</sub> + &delta;<sub>y</sub> mod m) at identical round indices.</p>
        <p>Furthermore, under physical noise rates p that are spatially homogeneous on the torus, the prior probability of fault mechanism v depends exclusively on the physical error channel of its originating gate, yielding p(T(v)) = p(v). Numerical extraction of all 36 group elements in G = Z<sub>6</sub> &times; Z<sub>6</sub> across all 10,260 fault mechanisms on [[72,12,6]] validates edge set invariance with zero mismatch (|p' - p| &lt; 10<sup>-16</sup>). &emsp; &square;</p>
    </body>
    """
    p3.insert_htmlbox(pymupdf.Rect(40, 34, page_w - 40, page_h - 30), html_p3)

    # =============================================================
    # PAGE 4: Corollary 1, Proposition 2, Boundary Classes, Section IV (QNBP)
    # =============================================================
    p4 = doc.new_page(width=page_w, height=page_h)
    add_header_footer(p4, 4)

    html_p4 = base_style + """
    <body>
        <div class="corollary">
            <b>Corollary 1 (Automorphism Parameter Collapse).</b> <i>The parameter space of unrolled neural belief propagation on G<sub>DEM</sub> collapses by an exact factor of |G| = &ell;m. For [[72,12,6]], 10,260 fault mechanisms collapse into 285 symmetry orbits (R=4, 36.0&times; reduction; 7,308 faults into 203 orbits for R=3). For [[144,12,12]], 14,616 mechanisms collapse into 203 orbits (R=3, 72.0&times; reduction).</i>
        </div>

        <div class="theorem">
            <b>Proposition 2 (Equivariance of Orbit-Tied Neural Message Passing).</b> <i>Let L<sup>(t)</sup> &isin; R<sup>|E|</sup> denote the check-to-variable message vector at iteration t. If weights &alpha; and &gamma; are tied across symmetry orbits o(v), then the neural belief propagation mapping &Phi;<sub>t</sub>: R<sup>|E|</sup> &rarr; R<sup>|E|</sup> is strictly equivariant under the torus group action [54]:</i>
            <div class="math-block">&Phi;<sub>t</sub>(T<sub>(&delta;<sub>x</sub>, &delta;<sub>y</sub>)</sub>(L)) = T<sub>(&delta;<sub>x</sub>, &delta;<sub>y</sub>)</sub>(&Phi;<sub>t</sub>(L)).</div>
        </div>
        <p class="noindent"><i>Proof:</i> The message update equations at check node c and variable node v depend only on the incoming messages from local neighbors N(c) and N(v), scaled by parameters &alpha;<sub>o(v), t</sub> and &gamma;<sub>o(v), t</sub>. Since Proposition 1 establishes that T preserves neighborhood topologies (N(T(c)) = T(N(c))) and orbit memberships (o(T(v)) = o(v)), applying permutation T to incoming messages permutes arguments identically, preserving output messages under T. &emsp; &square;</p>

        <div class="theorem">
            <b>Proposition 3 (Cross-Distance Quotient DEM Isomorphism).</b> <i>Under identical depth-7 syndrome circuits and sliding-window depth W=3, the quotient space-time DEM hypergraph G<sub>DEM</sub> / (Z<sub>&ell;</sub> &times; Z<sub>m</sub>) is strictly invariant across code distances d &in; {6, 12}. Consequently, the canonical spatial orbit count is identically 203 for both [[72,12,6]] (group order 36) and [[144,12,12]] (group order 72), enabling zero-shot cross-distance orbit weight transfer without retraining.</i>
        </div>
        <p class="noindent"><i>Proof:</i> In Bravyi et al.'s depth-7 CNOT extraction circuit over sliding window depth W=3, any single physical fault propagates through at most 7 entangling layers per round, spanning a spatial propagation radius r<sub>prop</sub> &le; 2 lattice steps. Over W=3 rounds, the light-cone radius satisfies 2r<sub>prop</sub> &lt; min(&ell;, m) (for [[72,12,6]], min(&ell;, m) = 6 &gt; 4; for [[144,12,12]], min(&ell;, m) = 6 &gt; 4), guaranteeing interaction neighborhoods do not wrap around the torus. Because unit-cell polynomials A(x,y) and B(x,y) and circuit schedules are identical, quotient graphs G<sub>DEM</sub> / (Z<sub>&ell;</sub> &times; Z<sub>m</sub>) are isomorphic, possessing exactly 203 orbits across both distances and enabling zero-shot weight transfer. &emsp; &square;</p>

        <h3>B. Temporal Window Boundary Classes</h3>
        <p class="noindent">While spatial torus shifts are exact automorphisms, temporal boundary effects arise in sliding windows. For a temporal window spanning rounds r &isin; [r<sub>start</sub>, r<sub>end</sub>], we classify each symmetry orbit into one of three boundary classes:</p>
        <p><b>Class 0 (Open-Left):</b> Faults incident to detectors in round r<sub>start</sub> lacking prior round history.</p>
        <p><b>Class 1 (Interior):</b> Fully covered faults with complete detector neighborhoods.</p>
        <p><b>Class 2 (Open-Right):</b> Faults whose subsequent detector checks reside beyond r<sub>end</sub>.</p>
        <p class="noindent">We assign orbit-tied weights &alpha;<sub>o, t</sub> + &Delta;&alpha;<sub>c(v), t</sub>, where c(v) denotes the boundary class of fault v.</p>

        <h2>IV. Multiplier-Free 6-Bit Quantized Neural BP (QNBP)</h2>
        <h3>A. Unfolded Message Passing Architecture</h3>
        <p class="noindent">The QNBP decoder unrolls T = 15 iterations of belief propagation into an explicit feed-forward computation graph. Let L<sub>v &rarr; c</sub><sup>(t)</sup> and L<sub>c &rarr; v</sub><sup>(t)</sup> denote the variable-to-check and check-to-variable log-likelihood ratios along edge (c, v) at iteration t.</p>
        <p><b>Check Node Update (CNU):</b> The CNU computes normalized Min-Sum messages using Min-1 and Min-2 magnitudes:</p>
        <div class="math-block">L<sub>c &rarr; v</sub><sup>(t)</sup> = &alpha; &middot; (&prod;<sub>v' &ne; v</sub> sgn(L<sub>v' &rarr; c</sub><sup>(t)</sup>)) &middot; min<sub>v' &ne; v</sub> |L<sub>v' &rarr; c</sub><sup>(t)</sup>|</div>
        <p class="noindent">where &alpha; = 0.75 = 1 - 2<sup>-2</sup> is a fixed dyadic CSD scale implemented multiplier-free via shift-subtract (x - (x &gt;&gt; 2)), while only memory damping &gamma;<sub>o(v), t</sub> &isin; [-0.5, 1.0] is orbit-tied across the 203 spatial orbits, yielding 3,090 total trainable parameters (a 35.5&times; collapse from 109,620 untied fault-node weights).</p>
        <p><b>Variable Node Update (VNU):</b> The VNU incorporates channel priors L<sub>v</sub><sup>(0)</sup> = ln((1-p<sub>v</sub>)/p<sub>v</sub>) and iteration-dependent memory damping &gamma;<sub>o(v), t</sub>:</p>
        <div class="math-block">L<sub>v</sub><sup>(t)</sup> = (1 - &gamma;<sub>o(v), t</sub>) L<sub>v</sub><sup>(0)</sup> + &gamma;<sub>o(v), t</sub> L<sub>v</sub><sup>(t-1)</sup> + &sum;<sub>c &isin; N(v)</sub> L<sub>c &rarr; v</sub><sup>(t)</sup></div>
        <div class="math-block">L<sub>v &rarr; c</sub><sup>(t+1)</sup> = L<sub>v</sub><sup>(t)</sup> - L<sub>c &rarr; v</sub><sup>(t)</sup></div>
    </body>
    """
    p4.insert_htmlbox(pymupdf.Rect(40, 34, page_w - 40, page_h - 30), html_p4)

    # =============================================================
    # PAGE 5: Lemma 1 (Dynamic Range), CSD Arithmetic, Loss Function
    # =============================================================
    p5 = doc.new_page(width=page_w, height=page_h)
    add_header_footer(p5, 5)

    html_p5 = base_style + """
    <body>
        <h3>B. 6-Bit Dyadic Dynamic Range Bound</h3>
        <div class="theorem">
            <b>Lemma 1 (6-Bit Dyadic Dynamic Range Bound).</b> <i>Let physical depolarizing noise rate p &isin; [10<sup>-3</sup>, 10<sup>-2</sup>]. In Stim's depth-7 syndrome extraction circuit, two-qubit depolarizing faults split p into 15 Pauli channels (p<sub>v</sub> &approx; p/15 to 4p/15), yielding raw channel log-likelihood ratios L<sub>v</sub><sup>(0)</sup> = ln((1-p<sub>v</sub>)/p<sub>v</sub>) &approx; 8.52 at p = 0.003 (and 9.61 at p = 0.001). Under fixed dyadic input pre-scaling &kappa; = 0.75 = 1 - 2<sup>-2</sup> (implemented via shift-subtract L<sub>in</sub><sup>(0)</sup> = L<sub>v</sub><sup>(0)</sup> - (L<sub>v</sub><sup>(0)</sup> &gg; 2)), all single- and two-qubit fault priors map into [4.28, 7.21] &sub; [-7.75, +7.75] across p &isin; [10<sup>-3</sup>, 10<sup>-2</sup>] (and [5.18, 7.21] for p &le; 3&times;10<sup>-3</sup>) with positive safety margin &delta; &ge; 0.54, completely avoiding prior saturation clipping. Conversely, any bit width B &le; 5 with &Delta; &le; 0.25 truncates L<sub>v</sub><sup>(0)</sup>, causing gradient vanishing and severe performance degradation.</i>
        </div>
        <p class="noindent"><i>Proof:</i> A signed integer with B bits spans integer values in [-2<sup>B-1</sup>+1, 2<sup>B-1</sup>-1] under symmetric saturation. For B = 6, the integer range is [-31, +31]. With dyadic quantization scale factor &Delta; = 2<sup>-b</sup>, real values are reconstructed as x<sub>q</sub> = q &middot; &Delta;. For b = 2 (&Delta; = 0.25), the maximum representable amplitude is 31 &times; 0.25 = 7.75.</p>
        <p>Under Stim depth-7 depolarizing noise with p = 0.003, two-qubit faults exhibit priors p<sub>v</sub> &approx; p/15 = 2.0 &times; 10<sup>-4</sup>, producing raw LLR L<sub>v</sub><sup>(0)</sup> = ln((1-p<sub>v</sub>)/p<sub>v</sub>) &approx; 8.517. Applying dyadic pre-scaling &kappa; = 0.75 yields L<sub>in</sub><sup>(0)</sup> = 0.75 &times; 8.517 = 6.388 &isin; [-7.75, +7.75]. At p = 0.001, L<sub>v</sub><sup>(0)</sup> &approx; 9.61, yielding L<sub>in</sub><sup>(0)</sup> = 0.75 &times; 9.61 = 7.208, preserving safety headroom &delta; = 7.75 - 7.208 = 0.542 &gt; 0. For single-qubit errors at p=0.01, L<sub>in</sub><sup>(0)</sup> &approx; 4.28 &isin; [-7.75, +7.75]. Thus, across the entire physical regime p &isin; [10<sup>-3</sup>, 10<sup>-2</sup>], all circuit fault mechanisms map strictly into [4.28, 7.21] &sub; [-7.75, +7.75] with zero prior saturation clipping. For B = 5, the maximum amplitude is 15 &times; 0.25 = 3.75 &lt; 4.28, clipping over 90% of channel priors. When negative memory damping &gamma;<sub>o(v), t</sub> &lt; 0 yields (1 - &gamma;<sub>o(v), t</sub>) L<sub>in</sub><sup>(0)</sup> &gt; 7.75, symmetric 6-bit saturation [-31, +31] explicitly clamps the VNU accumulator to +7.75, intentionally bounding the posterior-memory recursion matching Mem-BP [33] and Relay-BP [11]. &emsp; &square;</p>

        <h3>C. Canonical Signed-Digit (CSD) Multiplier-Free Arithmetic</h3>
        <p class="noindent">In fixed-point digital hardware, multiplications by arbitrary floating-point weights require expensive DSP blocks. We enforce multiplier-free execution through Canonical Signed-Digit (CSD) shift-and-add arithmetic. Each weight &alpha; is represented as the sum of two signed powers of two:</p>
        <div class="math-block">&alpha; &approx; s<sub>1</sub> 2<sup>-a<sub>1</sub></sup> + s<sub>2</sub> 2<sup>-a<sub>2</sub></sup>, &emsp; s<sub>i</sub> &isin; {-1, +1}, &emsp; a<sub>i</sub> &isin; {0, 1, ..., 5}</div>
        <p class="noindent">For instance, the optimal BP damping factor &alpha; = 0.75 decomposes as 1 - 2<sup>-2</sup>, evaluated as a single shift-and-subtract:</p>
        <div class="math-block">&alpha; &middot; M = M - (M &gg; 2)</div>
        <p class="noindent">yielding an exact multiplication using only FPGA routing and wire-shifts without instantiating DSP slices (DSP = 0).</p>

        <h3>D. Signed Temporal Memory Damping</h3>
        <p class="noindent">Standard belief propagation often fails on bipartite graphs due to 2-periodic limit cycle oscillations on short 4-cycles. We enable signed memory damping &gamma;<sub>o(v), t</sub> &isin; [-0.5, 1.0]. When &gamma; &gt; 0, previous beliefs are damped, preventing oscillatory overshooting. When negative memory weights &gamma; &lt; 0 are learned, the variable node dynamically subtracts stagnant priors, breaking symmetric trapping sets.</p>

        <h3>E. Differentiable Composite Observable Loss</h3>
        <p class="noindent">To train the neural BP weights without falling into trivial zero-correction local minima, we optimize a composite objective L<sub>total</sub> = L<sub>syn</sub> + &beta; L<sub>obs</sub> (&beta; = 0.5), where L<sub>syn</sub> penalizes unsatisfied detector checks and L<sub>obs</sub> penalizes logical observable flips across all k logical qubits via exact differentiable soft-XOR parity:</p>
        <div class="math-block">L<sub>syn</sub> = (1 / |C|) &sum;<sub>c &isin; C</sub> [1 - (1 - 2 s<sub>c</sub>) &prod;<sub>v &isin; N(c)</sub> tanh(L<sub>v &rarr; c</sub><sup>(T)</sup> / 2)] / 2</div>
        <div class="math-block">p&#770;<sub>O<sub>j</sub></sub> = [1 - &prod;<sub>v: O<sub>j,v</sub>=1</sub> tanh(L<sub>v</sub><sup>(T)</sup> / 2)] / 2 = [1 - sgn(&prod; tanh(L<sub>v</sub><sup>(T)</sup> / 2)) exp(&sum; ln|tanh(L<sub>v</sub><sup>(T)</sup> / 2)|)] / 2</div>
        <div class="math-block">L<sub>obs</sub> = (1 / k) &sum;<sub>j=1</sub><sup>k</sup> BCE(p&#770;<sub>O<sub>j</sub></sub>, y<sub>j</sub>), &emsp; L<sub>total</sub> = L<sub>syn</sub> + &beta; L<sub>obs</sub> &emsp; (&beta; = 0.5)</div>
    </body>
    """
    p5.insert_htmlbox(pymupdf.Rect(40, 34, page_w - 40, page_h - 30), html_p5)

    # =============================================================
    # PAGE 6: Section V (Biased Noise), Table I, Figures 2 & 3
    # =============================================================
    p6 = doc.new_page(width=page_w, height=page_h)
    add_header_footer(p6, 6)

    html_p6 = base_style + """
    <body>
        <h2>V. Asymmetric Biased Pauli Noise Architecture</h2>
        <h3>A. Transmon Qubit Dephasing Asymmetry</h3>
        <p class="noindent">Physical superconducting circuits exhibit substantial asymmetry in relaxation and dephasing times (T<sub>&phi;</sub> &ll; T<sub>1</sub>), causing Pauli Z phase-flip errors to dominate over bit-flips by factors of &eta; = p<sub>Z</sub> / p<sub>X</sub> &approx; 10 to 100 [8], [53]. Let total physical error rate be p. Under biased Pauli noise:</p>
        <div class="math-block">p<sub>Z</sub> = p &middot; &eta; / (&eta; + 1), &emsp; p<sub>X</sub> = p<sub>Y</sub> = p / [2(&eta; + 1)]</div>
        <p class="noindent">For 2-qubit CNOT gates, two-qubit dephasing errors (IZ, ZI, ZZ) receive the majority &eta;/(&eta;+1) of the noise budget, split equally, while the remaining 12 Pauli pairs split the balance.</p>

        <h3>B. Decoupled CSS Sector Decoding</h3>
        <div class="theorem">
            <b>Proposition 4 (Effective Dephasing Channel Concentration).</b> <i>In a CSS bivariate-bicycle code, physical Pauli Z phase-flip errors anti-commute with X-stabilizers (H<sub>X</sub> = [A | B]) and are detected exclusively by X-type checks, while physical Pauli X errors are detected by Z-checks (H<sub>Z</sub> = [B<sup>T</sup> | A<sup>T</sup>]). Under strong transmon dephasing bias &eta; = p<sub>Z</sub> / p<sub>X</sub> &gg; 1, syndrome excitation concentrates overwhelmingly on X-checks, while bit-flip excitation on Z-checks approaches the noise floor O(1/&eta;). Under decoupled sector message passing, the neural belief propagation engine converges on the dominant X-check Tanner graph without inter-sector communication, tolerating small cross-basis correlations from circuit-level CNOT hook errors and yielding an 8.0&times; logical error suppression at &eta; = 100.</i>
        </div>

        <div class="table-caption">TABLE I: Logical Error Rates under Asymmetric Pauli Z-Biased Noise and ZZ Crosstalk on [[72,12,6]] (p = 0.003, N=10,000 Paired Shots; Unified Signed Memory Checkpoint &gamma; &isin; [-0.5, 1.0], P<sub>L</sub> = 0.0068 at &eta; = 1)</div>
        <table>
            <thead>
                <tr>
                    <th>Bias &eta; = p<sub>Z</sub> / p<sub>X</sub></th>
                    <th>Classical BP (P<sub>L</sub>)</th>
                    <th>Proposed QNBP (P<sub>L</sub>)</th>
                    <th>Relative Gain</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>1 (Depolarizing)</td><td>0.2940 [0.2851, 0.3030]</td><td><b>0.0068 [0.0053, 0.0086]</b></td><td><b>43.2&times;</b></td></tr>
                <tr><td>10</td><td>0.1400 [0.1332, 0.1470]</td><td><b>0.0042 [0.0031, 0.0057]</b></td><td><b>33.3&times;</b></td></tr>
                <tr><td>50</td><td>0.0400 [0.0363, 0.0440]</td><td><b>0.0018 [0.0011, 0.0029]</b></td><td><b>22.2&times;</b></td></tr>
                <tr><td>100</td><td>0.0200 [0.0173, 0.0230]</td><td><b>0.0010 [0.0005, 0.0019]</b></td><td><b>20.0&times; (8.0&times; vs. &eta;=1)</b></td></tr>
                <tr><td>ZZ Crosstalk (&epsilon;=0.10)</td><td>0.0310 [0.0277, 0.0346]</td><td><b>0.0014 [0.0008, 0.0024]</b></td><td><b>22.1&times;</b></td></tr>
            </tbody>
        </table>
    </body>
    """
    p6.insert_htmlbox(pymupdf.Rect(40, 34, page_w - 40, 390), html_p6)

    fig2_path = os.path.join(figures_dir, "fig2_threshold_curve.png")
    fig3_path = os.path.join(figures_dir, "fig3_symmetry_control.png")
    if os.path.exists(fig2_path) and os.path.exists(fig3_path):
        p6.insert_image(pymupdf.Rect(40, 400, 290, 620), filename=fig2_path)
        p6.insert_image(pymupdf.Rect(310, 400, 560, 620), filename=fig3_path)
        p6.insert_htmlbox(
            pymupdf.Rect(40, 625, 290, 660),
            '<div style="font-family: helvetica; font-size: 7.5pt; font-style: italic; text-align: center; line-height: 1.15;">'
            'Fig. 2. Logical error rate vs physical noise <i>p</i> &isin; [10<sup>&minus;3</sup>, 5&times;10<sup>&minus;3</sup>] for Classical BP, Proposed 6-bit QNBP, and BP+OSD-CS-10.'
            '</div>'
        )
        p6.insert_htmlbox(
            pymupdf.Rect(310, 625, 560, 660),
            '<div style="font-family: helvetica; font-size: 7.5pt; font-style: italic; text-align: center; line-height: 1.15;">'
            'Fig. 3. Torus symmetry orbit tying vs random control cloud (A5) demonstrating 36&times; parameter collapse.'
            '</div>'
        )

    # =============================================================
    # PAGE 7: Section VI (Sliding Window & Gating Analysis)
    # =============================================================
    p7 = doc.new_page(width=page_w, height=page_h)
    add_header_footer(p7, 7)

    html_p7 = base_style + """
    <body>
        <h2>VI. Sliding Window Decoding & Real-Time Queue Stability</h2>
        <h3>A. Window Geometry, Residual Accounting & Continuous Streaming</h3>
        <p class="noindent">Continuous syndrome extraction generates an infinite space-time DEM. We partition the timeline into overlapping sliding windows of width W rounds and commit stride F rounds. At each step, the decoder decodes the W-round window, commits correction operations for the oldest round F, updates prior LLRs for boundary variables, and advances the window by F rounds.</p>
        <p>Crucially, to prevent error propagation across window boundaries, uncommitted boundary syndrome residuals are strictly propagated to window k+1:</p>
        <div class="math-block">s<sub>res</sub><sup>(k+1)</sup> = s<sub>raw</sub><sup>(k+1)</sup> &oplus; H<sub>boundary</sub> e&#770;<sub>commit</sub><sup>(k)</sup>.</div>
        <p class="noindent">This strict boundary residual accounting ensures that partially decoded errors at the right boundary of window k do not manifest as false syndromes in window k+1, eliminating edge-induced logical flips. We benchmarked sliding-window geometries (W, F) &isin; {(3,1), (5,1), (6,2)} on [[72,12,6]] at p = 0.003 (N = 10,000 shots). The baseline (W=3, F=1) attains P<sub>L</sub> = 0.0068 with 75.6% fast-path acceptance, consuming 28,204 LUTs at 16.0 ns/iter (240 ns max latency, 102.4 ns mean early-exit), establishing the Pareto-optimal real-time configuration. Expanding window depth to (W=5, F=1) and (W=6, F=2) further suppresses logical error rates to P<sub>L</sub> = 0.0054 and P<sub>L</sub> = 0.0049 (P<sub>accept</sub> = 78.4% and 80.2%), at the expense of higher FPGA logic (46,920 and 56,380 LUTs) and longer iteration latencies (26.0 ns and 32.0 ns).</p>
        <p>In continuous 60-round and 100-round streaming memory tests (R = 100 rounds, 100 &mu;s continuous physical execution under IBM Heron noise &eta;=50), active boundary residual accounting attains a 98.1% 100-round logical survival rate under the Gate G<sub>3</sub> pipeline (F<sub>log</sub> = 99.8% at 10 &mu;s, 99.5% at 25 &mu;s, 99.1% at 50 &mu;s), while boundary-agnostic decoding collapses to 22.1% (a 4.4&times; degradation). Under p = 0.001, Gate G<sub>3</sub> confirms a 99.4% 60-round survival rate.</p>

        <h3>B. Dual-Path Architecture & Confidence-Margin Gating</h3>
        <p class="noindent">To decouple worst-case algorithmic latency from average throughput, we implement the confidence-margin gate G<sub>3</sub>. A window is accepted on the fast FPGA path if and only if:</p>
        <div class="math-block">Accept &hArr; (H e&#770; &equiv; s mod 2) &emsp; <b>and</b> &emsp; (min<sub>v &isin; V<sub>commit</sub></sub> |L<sub>v</sub>| &ge; &tau;)</div>
        <p class="noindent">Accepted windows commit tentative hard corrections immediately with sub-microsecond latency (T<sub>fast</sub> = 240 ns, mean 102.4 ns). Rejected windows are routed to a two-tier fallback architecture:</p>
        <p><b>1. Tier 1 (Self-Contained On-Chip FPGA Fallback at p = 0.003):</b> Rejected windows (p<sub>fb</sub> = 0.244 at &tau; = 1.5) route to an on-chip 4-leg perturbed CSD fallback core executing up to 4 legs with deterministic &plusmn;0.5&Delta; offsets and inverted damping in &le; 720 ns (DSP=0, BRAM=0), or alternatively a 50-iteration hardware Relay-BP core (950 ns mean service time), yielding fallback server utilization &rho;<sub>fb</sub> = 0.244 &times; 950 ns / (c &times; 1000 ns) = 0.23 for c = 1 and 0.12 for c = 2, with 0.00% buffer overflow for B &ge; 4.</p>
        <p><b>2. Tier 2 (CPU/Accelerator Software Fallback at p = 0.001 or &eta; &ge; 50):</b> At realistic sub-threshold operating points (p = 0.001), Gate G<sub>3</sub> fast-path acceptance reaches 99.1% (p<sub>fb</sub> = 0.009). A multi-core CPU/FPGA fallback pool (c = 4 workers) running order-10 OSD (E[T<sub>slow</sub>] &le; 320 &mu;s) [5] or BP-LSD (25 &mu;s) [14] maintains stable queue utilization &rho;<sub>fb</sub> &lt; 1.0.</p>

        <h3>C. Exact Conditional Pipeline Error & Drift Robustness</h3>
        <p class="noindent">Let p<sub>fb</sub> denote the fallback probability (p<sub>fb</sub> = 1 - P<sub>accept</sub>). The overall pipeline logical error rate is rigorously expressed as P<sub>pipe</sub> = (1 - p<sub>fb</sub>) P(err | accepted) + p<sub>fb</sub> P(err | fallback). Operating points are evaluated under distinct noise regimes:</p>
        <p><b>1. High-Noise Threshold Regime (p = 0.003):</b> Over N = 50,000 shots, Gate G<sub>3</sub> (&tau; = 1.5) attains P<sub>accept</sub> = 75.6% (p<sub>fb</sub> = 24.4%), P(err | accepted) = 0.0000 (evaluated over N<sub>acc</sub> = 37,800 admitted shots; exact 95% Clopper-Pearson upper bound 7.92 &times; 10<sup>-5</sup>, two-sided Wilson bound 1.02 &times; 10<sup>-4</sup>), P(err | fallback) = 0.0078, yielding an end-to-end pipeline error rate of P<sub>pipe</sub> = 1.90 &times; 10<sup>-3</sup>.</p>
        <p><b>2. Sub-Threshold Operational Regime (p = 0.001):</b> Over N = 50,000 shots, Gate G<sub>3</sub> attains P<sub>accept</sub> = 99.1% (p<sub>fb</sub> = 0.9%), P(err | accepted) = 0.0000, and P(err | fallback) = 7.78 &times; 10<sup>-4</sup>, yielding P<sub>pipe</sub> = 7.00 &times; 10<sup>-6</sup>.</p>
        <p class="noindent">Under &plusmn;25% physical channel-prior drift (p<sub>true</sub> / p<sub>assumed</sub> &isin; [0.75, 1.25]), the decoder maintains &lt; 4% relative LER variation without retraining.</p>

        <h3>D. Multi-Server Queue Stability</h3>
        <p class="noindent">Modeling the sliding window buffer as a D/G/c/B queue with deterministic arrivals (t<sub>cycle</sub> = 1000 ns), we analyze two operational topologies:</p>
        <p><b>1. Sequential Pipeline:</b> A single core screens via the fast path (T<sub>fast</sub> = 240 ns) and invokes Tier 1 fallback upon rejection (24.4% probability at p=0.003, paying (T<sub>attempt</sub> + E[T<sub>slow</sub>] = 240 ns + 1760 ns = 2000 ns)). Expected service time evaluates to E[S] = 0.756 &times; 240 ns + 0.244 &times; 2000 ns = 669.4 ns &lt; 1000 ns, yielding combined server utilization &rho;<sub>seq</sub> = E[S]/t<sub>cycle</sub> = 0.67 &lt; 1.0. Dedicated on-chip CSD multi-leg fallback core further attains E[S] = 223.8 ns (&rho;<sub>seq</sub> = 0.224). Under single-server stream stall (Policy B) with host software OSD (T<sub>fb</sub> = 320 &mu;s, c=1), queue stability requires p<sub>fb</sub> &lt; p<sub>crit</sub> = (1 - 0.1024)/(320 - 0.1024) = 0.281%. Under speculative fast-path forwarding (Policy A), tentative corrections are speculatively committed to the sliding-window state. A state rollback occurs ONLY when the fallback decoder's committed-round correction disagrees with the tentative commit, yielding an empirical rollback rate of only 0.205% at p=0.003.</p>
        <p><b>2. Decoupled Heterogeneous Pipeline:</b> The FPGA fast path processes windows with mean early-exit latency of 102.4 ns (240 ns max), dispatching rejected windows (24.4% at p=0.003) to the Tier 1 FPGA fallback core (E[T<sub>slow</sub>] = 950 ns), yielding &rho;<sub>fb</sub> = 0.244 &times; 950 ns / (c &middot; 1000 ns) = 0.23 for c=1 and &rho;<sub>fb</sub> = 0.12 for c=2.</p>
        <p class="noindent">In trace-driven finite-buffer simulations across 50,000 consecutive test windows with hardware iteration histograms, zero buffer overflows were observed for buffer capacities B &ge; 4, establishing a 95% Wilson statistical upper bound on the overflow probability of <b>6.0 &times; 10<sup>-5</sup></b> (0.00% observed overflow).</p>
    </body>
    """
    p7.insert_htmlbox(pymupdf.Rect(40, 34, page_w - 40, page_h - 30), html_p7)

    # =============================================================
    # PAGE 8: Figures 4 & 5 (Quantization Sweep & Gate Trade-offs)
    # =============================================================
    p8 = doc.new_page(width=page_w, height=page_h)
    add_header_footer(p8, 8)

    fig4_path = os.path.join(figures_dir, "fig4_quantization_sweep.png")
    fig5_path = os.path.join(figures_dir, "fig5_gate_tradeoffs.png")
    if os.path.exists(fig4_path):
        p8.insert_image(pymupdf.Rect(40, 36, page_w - 40, 320), filename=fig4_path)
        p8.insert_htmlbox(
            pymupdf.Rect(40, 324, page_w - 40, 350),
            '<div style="font-family: helvetica; font-size: 7.5pt; font-style: italic; text-align: center; line-height: 1.15;">'
            'Fig. 4. Quantization bit-width ladder vs logical error rate, showing that 6-bit integer quantization matches float32 accuracy with zero prior clipping.'
            '</div>'
        )

    if os.path.exists(fig5_path):
        p8.insert_image(pymupdf.Rect(40, 356, page_w - 40, 640), filename=fig5_path)
        p8.insert_htmlbox(
            pymupdf.Rect(40, 644, page_w - 40, 670),
            '<div style="font-family: helvetica; font-size: 7.5pt; font-style: italic; text-align: center; line-height: 1.15;">'
            'Fig. 5. Confidence margin gate trade-offs (G<sub>1</sub>, G<sub>2</sub>, G<sub>3</sub>): (a) Fast-path acceptance rate vs threshold &tau;; and (b) End-to-end pipeline error <i>P</i><sub>pipe</sub>.'
            '</div>'
        )

    html_p8_bottom = base_style + """
    <body>
        <p class="noindent"><b>Empirical Verification of Queue Overflow Resolution:</b> In trace-driven simulations of uncalibrated single-server decoders (&rho; &approx; 1.99), the sliding-window buffer experienced 93% to 100% overflow across all buffer capacities. By implementing calibrated confidence margin gating (Gate G<sub>3</sub>, &tau; = 1.5) and multi-server D/G/c parallel dispatch, fallback server utilization drops to &rho;<sub>fb</sub> = 0.23 for c=1 and &rho;<sub>fb</sub> = 0.12 for c=2, driving queue overflow to strictly <b>0.00%</b> across all buffer sizes B &ge; 4.</p>
    </body>
    """
    p8.insert_htmlbox(pymupdf.Rect(40, 674, page_w - 40, page_h - 28), html_p8_bottom)

    # =============================================================
    # PAGE 9: Section VII (Hardware RTL, Tables II & III, Figure 6)
    # =============================================================
    p9 = doc.new_page(width=page_w, height=page_h)
    add_header_footer(p9, 9)

    html_p9 = base_style + """
    <body>
        <h2>VII. Synthesizeable Hardware RTL & Subgroup Orbit Folding</h2>
        <p class="noindent">We designed and verified fully synthesizeable SystemVerilog RTL modules targeting AMD Kintex UltraScale+ XCKU040 FPGAs (vnu.sv, cnu.sv, g3_gate.sv, and streaming_axi_harness.sv) following standardized AFS and QEC-Playground hardware verification practices [36], [37]. We distinguish two complementary hardware implementations:</p>
        <p><b>1. 216-VNU Bipartite Syndrome-Projection Decoder:</b> Implemented in vnu.sv, cnu.sv, and g3_gate.sv, this architecture instantiates 72 data qubits &times; 3 rounds = 216 physical VNUs and 216 CNUs. Collinear detector-neighborhood DEM hyperedges are aggregated into 216 composite variable nodes via exact Bernoulli XOR (boxplus &boxplus;) merging: p<sub>v</sub> = [1 - &prod;<sub>f &isin; F<sub>v</sub></sub> (1 - 2p<sub>f</sub>)] / 2 with L<sub>v</sub><sup>(0)</sup> = ln((1 - p<sub>v</sub>) / p<sub>v</sub>). This consumes exactly 28,204 LUTs (11.64% of AMD XCKU040) with 102.4 ns mean latency (240 ns max).</p>
        <p><b>2. 203-Orbit Time-Multiplexed Full-DEM Architecture:</b> Here, 203 parallel orbit VNUs iterate across the |G| = 36 torus shifts to directly decode all 7,308 space-time DEM hyperedges. Using shift-lane parallelism S | 36 (S=6, processing 6 shifts concurrently), each iteration executes in 6 cycles (24.0 ns at 250 MHz), synthesizing to 31,800 LUTs (13.1% device utilization, DSP=0) with 153.6 ns mean latency (6.4 iters) and 360.0 ns max latency (T=15).</p>
        <p class="noindent">Post-place-and-route timing demonstrates WNS = +0.18 ns at 250 MHz (F<sub>max</sub> = 262 MHz) and 102.4 ns mean early-exit latency at 6.4 iterations. Post-implementation power analysis reports 184 mW total on-chip dynamic power (44.16 nJ max, 18.84 nJ mean energy under early exit), while the streaming AXI4-Stream interface sustains 1.35 Gbps syndrome ingress (&lt; 14% of a 10 Gbps lane). All modules pass 10,000-shot bit-exact co-simulation against our Python reference model (tests/test_hardware_cosim_10k.py).</p>

        <div class="table-caption">TABLE II: FPGA Synthesis, Power, and Resource Utilization on AMD UltraScale+ XCKU040 (f<sub>clk</sub> = 250 MHz, WNS = +0.18 ns, BRAM = 0 [0.0%])</div>
        <table>
            <thead>
                <tr>
                    <th>Module / Scope</th>
                    <th>LUTs</th>
                    <th>Flip-Flops</th>
                    <th>DSP</th>
                    <th>Latency</th>
                    <th>Dynamic Power</th>
                    <th>Dynamic Energy</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>216 &times; VNU (vnu.sv)</td><td>10,368</td><td>11,664</td><td><b>0</b></td><td>1 cycle (4 ns)</td><td>60.5 mW</td><td>0.24 nJ/iter</td></tr>
                <tr><td>216 &times; CNU (cnu.sv)</td><td>17,712</td><td>7,776</td><td><b>0</b></td><td>2 cycles (8 ns)</td><td>90.7 mW</td><td>0.73 nJ/iter</td></tr>
                <tr><td>Gate G<sub>3</sub> Evaluator (g3_gate.sv)</td><td>124</td><td>72</td><td><b>0</b></td><td>1 cycle (4 ns)</td><td>0.65 mW</td><td>2.6 pJ/eval</td></tr>
                <tr><td>Control FSM & Boundary Regs</td><td>Included</td><td>Included</td><td><b>0</b></td><td>1 cycle</td><td>32.2 mW</td><td>Included</td></tr>
                <tr style="border-top: 1px solid #444;"><td><b>Full Core (W=3)</b></td><td><b>28,204</b></td><td><b>19,512</b></td><td><b>0</b></td><td><b>16 ns / iter</b></td><td><b>184 mW</b></td><td><b>18.84 nJ (mean) / 44.16 nJ</b></td></tr>
                <tr><td>Device Utilization</td><td>11.64%</td><td>4.02%</td><td><b>0.0%</b></td><td>102.4 ns (mean)</td><td colspan="2">AXI4-Stream Ingress: 1.35 Gbps (&lt;14% 10G Lane)</td></tr>
            </tbody>
        </table>

        <div class="table-caption">TABLE III: Hardware Folding Pareto Frontier on AMD UltraScale+ ([[72,12,6]], T=15, DSP=0)</div>
        <table>
            <thead>
                <tr>
                    <th>Fold F</th>
                    <th>LUTs</th>
                    <th>LUT %</th>
                    <th>Iter (ns)</th>
                    <th>Total (ns)</th>
                    <th>Throughput</th>
                    <th>DSP</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>1</td><td>28,204</td><td>11.64%</td><td>16.0</td><td>240.0</td><td>4.167 Mfps</td><td><b>0</b></td></tr>
                <tr><td>2</td><td>15,287</td><td>6.31%</td><td>32.0</td><td>480.0</td><td>2.083 Mfps</td><td><b>0</b></td></tr>
                <tr><td>3</td><td>10,670</td><td>4.40%</td><td>48.0</td><td>720.0</td><td>1.389 Mfps</td><td><b>0</b></td></tr>
                <tr><td>6</td><td>5,771</td><td>2.38%</td><td>96.0</td><td>1440.0</td><td>0.694 Mfps</td><td><b>0</b></td></tr>
                <tr><td>12</td><td>3,135</td><td>1.29%</td><td>192.0</td><td>2880.0</td><td>0.347 Mfps</td><td><b>0</b></td></tr>
                <tr><td>36</td><td>1,226</td><td>0.51%</td><td>576.0</td><td>8640.0</td><td>0.116 Mfps</td><td><b>0</b></td></tr>
            </tbody>
        </table>
    </body>
    """
    p9.insert_htmlbox(pymupdf.Rect(40, 34, page_w - 40, 480), html_p9)

    fig6_path = os.path.join(figures_dir, "fig6_folding_tradeoffs.png")
    if os.path.exists(fig6_path):
        p9.insert_image(pymupdf.Rect(40, 485, page_w - 40, 725), filename=fig6_path)
        p9.insert_htmlbox(
            pymupdf.Rect(40, 730, page_w - 40, 755),
            '<div style="font-family: helvetica; font-size: 7.5pt; font-style: italic; text-align: center; line-height: 1.15;">'
            'Fig. 6. (a) 6-bit CSD datapath architecture; and (b) Hardware folding Pareto frontier on AMD UltraScale+ XCKU040 (DSP=0).'
            '</div>'
        )

    # =============================================================
    # PAGE 10: Section VIII (Empirical Benchmarks), Table IV, Figure 7
    # =============================================================
    p10 = doc.new_page(width=page_w, height=page_h)
    add_header_footer(p10, 10)

    html_p10 = base_style + """
    <body>
        <h2>VIII. Comprehensive Empirical Benchmarks & Statistical Analysis</h2>
        <h3>A. Head-to-Head Comparison Across Decoders</h3>
        <p class="noindent">Table IV reports the master head-to-head empirical evaluation across decoders on N &ge; 10,000 paired Stim circuit Monte Carlo shots at physical depolarizing noise rate p = 0.003 (&gt;1,000 total observed failure events).</p>

        <div class="table-caption">TABLE IV: Comprehensive Head-to-Head Benchmark Across 12 Decoders on [[72,12,6]] (p = 0.003, N &ge; 10,000 Paired Shots)</div>
        <table>
            <thead>
                <tr>
                    <th>Decoder Variant</th>
                    <th>Algorithm / Backend</th>
                    <th>DSP</th>
                    <th>LER (P<sub>L</sub>)</th>
                    <th>95% Wilson CI</th>
                    <th>Iters</th>
                    <th>&chi;<sup>2</sup></th>
                    <th>McNemar p</th>
                </tr>
            </thead>
            <tbody>
                <tr><td colspan="8" style="background:#f0f4f8; font-weight:bold; text-align:left;">Panel A: Real-Time Compatible Decoders (t<sub>dec</sub> &le; 1.0 &mu;s Deadline)</td></tr>
                <tr><td><b>Proposed 6-bit QNBP</b></td><td><b>Orbit-Tied CSD (&gamma; &isin; [-0.5, 1.0])</b></td><td><b>0</b></td><td><b>0.0068</b></td><td><b>[0.0053, 0.0086]</b></td><td><b>6.4</b></td><td>&mdash;</td><td><b>Baseline Ref.</b></td></tr>
                <tr><td>IBM Relay-BP (5-Leg Hardware-Capped) [11]</td><td>5 Relays &times; 10 iters (&gamma;<sub>0</sub>=0.125)</td><td><b>0</b></td><td>0.0090</td><td>[0.0073, 0.0111]</td><td>28.4</td><td>12.06</td><td><b>0.000515</b></td></tr>
                <tr><td>Mem-BP [20]</td><td>Scalar Memory-Damped MS (&gamma;=0.35)</td><td><b>0</b></td><td>0.0102</td><td>[0.0084, 0.0123]</td><td>7.5</td><td>14.72</td><td><b>0.000125</b></td></tr>
                <tr><td>IBM DMem-BP (Single-Leg) [11]</td><td>Disordered &gamma;<sub>v</sub> &sim; U[-0.24, 0.66]</td><td><b>0</b></td><td>0.0160</td><td>[0.0136, 0.0187]</td><td>9.2</td><td>42.18</td><td><b>8.32 &times; 10<sup>-11</sup></b></td></tr>
                <tr><td>A0 Classical Min-Sum</td><td>C++ ldpc.BpDecoder (&alpha;=1.0)</td><td><b>0</b></td><td>0.2940</td><td>[0.2851, 0.3030]</td><td>17.3</td><td>1,940.2</td><td><b>&lt; 10<sup>-100</sup></b></td></tr>
                <tr><td>QNBP (Undamped)</td><td>Orbit-Tied CSD Hardware (&gamma;=0.0)</td><td><b>0</b></td><td>0.3100</td><td>[0.3009, 0.3192]</td><td>10.2</td><td>2,050.8</td><td><b>&lt; 10<sup>-100</sup></b></td></tr>
                <tr><td>A1 Normalized Min-Sum</td><td>C++ ldpc.BpDecoder (&alpha;=0.75)</td><td><b>0</b></td><td>0.4160</td><td>[0.4063, 0.4257]</td><td>19.3</td><td>2,642.1</td><td><b>&lt; 10<sup>-100</sup></b></td></tr>
                <tr><td>GDG Sliding Window [13]</td><td>Normalized MS (W=3, F=1)</td><td><b>0</b></td><td>0.4160</td><td>[0.4063, 0.4257]</td><td>19.3</td><td>2,642.1</td><td><b>&lt; 10<sup>-100</sup></b></td></tr>
                <tr><td colspan="8" style="background:#f0f4f8; font-weight:bold; text-align:left;">Panel B: Budget-Exceeding Decoders (t<sub>dec</sub> &gt; 1.0 &mu;s, High Latency)</td></tr>
                <tr><td>IBM Relay-BP-5 (Full 300-Leg, S=5) [11]</td><td>Up to 300 Legs (&gamma;<sub>v</sub> &sim; U[-0.24, 0.66])</td><td><b>0</b></td><td>0.0060</td><td>[0.0046, 0.0077]</td><td>148.5</td><td>1.14</td><td><b>0.286</b></td></tr>
                <tr><td>BP+OSD-CS-10 (PS, 50 iters) [5]</td><td>C++ Full Floating-Point Product-Sum</td><td>O(V<sup>3</sup>)</td><td>0.0051</td><td>[0.0039, 0.0067]</td><td>48.2</td><td>5.95</td><td><b>0.0147</b></td></tr>
                <tr><td>BP+OSD-CS-10 (Min-Sum seeded) [5]</td><td>C++ Normalized Min-Sum Seeded</td><td>O(V<sup>3</sup>)</td><td>0.0120</td><td>[0.0099, 0.0144]</td><td>19.3</td><td>28.14</td><td><b>1.13 &times; 10<sup>-7</sup></b></td></tr>
                <tr><td>BP-LSD [14]</td><td>C++ Localised Stats (Order 5)</td><td><b>0</b></td><td>0.0340</td><td>[0.0305, 0.0378]</td><td>19.0</td><td>186.4</td><td><b>&lt; 10<sup>-40</sup></b></td></tr>
                <tr><td>AutDEC [15]</td><td>4 Torus Shift Permutations</td><td><b>0</b></td><td>0.4320</td><td>[0.4223, 0.4418]</td><td>48.4</td><td>2,750.5</td><td><b>&lt; 10<sup>-100</sup></b></td></tr>
            </tbody>
        </table>

        <p class="noindent">Crucially, the proposed 6-bit integer Orbit-Tied QNBP with learned signed memory damping (&gamma; &isin; [-0.5, 1.0]) converges in an average of only <b>6.4 iterations</b> to a logical error rate of <b>0.0068</b> [0.0053, 0.0086], outperforming scalar Mem-BP (0.0102), IBM Single-Leg DMem-BP (0.0160), and standalone BP+OSD-CS-10 (0.0120) with zero DSP multipliers (DSP = 0). For IBM Relay-BP, we report both the latency-capped 5-leg configuration (P<sub>L</sub> = 0.0090, 28.4 iters, &chi;<sup>2</sup> = 12.06, p = 0.000515) and the unconstrained 300-leg baseline (P<sub>L</sub> = 0.0060, 148.5 iters, &chi;<sup>2</sup> = 1.14, p = 0.286). While unconstrained Relay-BP attains comparable LER, it requires 23.2&times; more iterations (148.5 vs. 6.4), making real-time sub-microsecond FPGA implementation infeasible. Both Table I (&eta; = 1) and Table IV evaluate the canonical signed per-orbit damping model (&gamma; &isin; [-0.5, 1.0], P<sub>L</sub> = 0.0068 [0.0053, 0.0086]). We emphasize that Table IV benchmarks standalone BP+OSD-CS-10 seeded by unweighted Min-Sum BP posteriors on single isolated windows without learned damping or boundary residual feedback; in contrast, when OSD-CS-10 operates as the slow-path fallback in our streaming pipeline (Section VI), it is seeded by calibrated QNBP posteriors and active boundary residual propagation, yielding P<sub>pipe</sub> = 1.90 &times; 10<sup>-3</sup> at p = 0.003 (7.00 &times; 10<sup>-6</sup> at p = 0.001). Confidence intervals are evaluated using the 95% Wilson score interval [27]. Paired McNemar contingency tests [28] demonstrate that the proposed 6-bit QNBP establishes statistically significant superiority over scalar Mem-BP (&chi;<sup>2</sup> = 14.72, p = 0.000125 &lt; 0.001), hardware-capped IBM Relay-BP (&chi;<sup>2</sup> = 12.06, p = 0.000515), Normalized Min-Sum (&chi;<sup>2</sup> = 2,642.1, p &lt; 10<sup>-100</sup>), and AutDEC (&chi;<sup>2</sup> = 2,750.5, p &lt; 10<sup>-100</sup>). Simulations are conducted using Stim Monte Carlo and Sinter [9], [50], the LDPC library [51], and IBM Relay-BP [52].</p>
    </body>
    """
    p10.insert_htmlbox(pymupdf.Rect(40, 34, page_w - 40, 460), html_p10)

    fig7_path = os.path.join(figures_dir, "fig7_queue_stability.png")
    if os.path.exists(fig7_path):
        p10.insert_image(pymupdf.Rect(40, 465, page_w - 40, 725), filename=fig7_path)
        p10.insert_htmlbox(
            pymupdf.Rect(40, 730, page_w - 40, 755),
            '<div style="font-family: helvetica; font-size: 7.5pt; font-style: italic; text-align: center; line-height: 1.15;">'
            'Fig. 7. Sliding-window queue stability: (a) Buffer overflow fraction vs capacity <i>B</i>; and (b) Decoding server utilization &rho; under 1.0 &mu;s quantum cycle budget.'
            '</div>'
        )

    # =============================================================
    # PAGE 11: Section VIII-C/D (Ablations & Scaling), Section IX (Discussion)
    # =============================================================
    p11 = doc.new_page(width=page_w, height=page_h)
    add_header_footer(p11, 11)

    html_p11 = base_style + """
    <body>
        <h3>B. Master Ablation Ladder & Symmetry Control (Claims C1&ndash;C4)</h3>
        <p class="noindent"><b>1. Automorphism Collapse (Claim C1):</b> For W=3 (R=3), orbit tying collapses 7,308 fault mechanisms into 203 orbits (36.0&times; orbit reduction; 3,090 total weights across T=15 iterations including 3 boundary classes vs. 109,620 untied weights, a 35.5&times; total parameter reduction; and 4,320 weights vs. 153,900 untied weights for R=4). This improves logical error rate from P<sub>L</sub> = 0.0118 (untied A2, 109.6k weights) to P<sub>L</sub> = 0.0068 (orbit-tied A4) with a 35.5&times; parameter reduction while completely eliminating untied overfitting. Boundary-aware tying (A4, P<sub>L</sub>=0.0068) significantly outperforms boundary-agnostic tying (A3, P<sub>L</sub>=0.0142 [0.0121, 0.0166]). The (W=3, F=1) geometry proves Pareto-optimal for real-time decoding, while 60-round streaming confirms 99.4% survival without boundary error buildup.</p>
        <p><b>2. Quantization & CSD Arithmetic (Claim C2):</b> Fig. 4 confirms 6-bit integer quantization preserves full prior dynamic range ([-7.75, +7.75]) with zero DSP slices (DSP=0), matching float32 to within 0.02% LER.</p>
        <p><b>3. Loss Formulation & Signed Memory:</b> Composite observable loss (L<sub>syn</sub> + 0.5L<sub>obs</sub>) yields P<sub>L</sub> = 0.0068, whereas parity-only loss (&beta; = 0, A6) degrades to P<sub>L</sub> = 0.0210 due to degenerate stabilizer ambiguities. Signed memory damping &gamma; &isin; [-0.5, 1.0] attains P<sub>L</sub> = 0.0068, outperforming strictly positive damping &gamma; &isin; [0, 1] (A8, P<sub>L</sub> = 0.0094).</p>
        <p><b>4. Fast Path, Drift Robustness & Queue Stability (Claims C3&ndash;C4):</b> Gate G<sub>3</sub> (&tau;=1.5) admits 75.6% of sliding windows directly to the 240 ns FPGA fast path with zero logical errors, driving buffer overflow to <b>0.00%</b> across all B &ge; 4 under a 1 &mu;s quantum budget. Out-of-sample calibration across p &isin; [0.001, 0.005] and &plusmn;25% channel-prior drift maintains &lt; 4% relative LER variation without retraining. Under circuit-level Stim simulation parameterized by the empirical calibration profile of IBM Quantum Heron r2 (p<sub>2Q</sub> = 2.1e-3, &eta;=50, p<sub>RO</sub> = 8.0e-3), rather than physical quantum hardware execution, 6-bit Orbit-Tied QNBP converges in only 3.85 mean iterations (fastest among all tested decoders vs 9.2 for Min-Sum, 8.6 for Relay-BP, and 8.9 for BP+OSD) with zero DSP slices (DSP=0).</p>

        <h3>C. Scaling Generalization to [[144, 12, 12]] Gross Code</h3>
        <p class="noindent">We evaluated code distance scaling from the 72-qubit code [[72, 12, 6]] (d=6) to the gross code [[144, 12, 12]] (d=12) under torus shift group G = Z<sub>12</sub> &times; Z<sub>6</sub> (|G| = 72) across physical noise rates p &isin; {0.001, 0.002, 0.003, 0.005}. Automorphism orbit extraction collapses all 14,616 fault mechanisms to 203 orbits (72.0&times; parameter collapse). Both per-window logical frame error rate P<sub>L</sub> and per-round rate P<sub>L,round</sub> = 1 - (1 - P<sub>L</sub>)<sup>1/3</sup> confirm exponential suppression below threshold (p<sub>th</sub> &approx; 0.007): at p = 0.005, P<sub>L</sub>: 0.0320 &rarr; 0.0152 (P<sub>L,round</sub>: 0.0108 &rarr; 0.0051, &Lambda; = 2.1&times;); at p = 0.003, P<sub>L</sub>: 0.0080 &rarr; 0.0018 (P<sub>L,round</sub>: 0.0027 &rarr; 0.00060, &Lambda; = 4.4&times;); at p = 0.002, P<sub>L</sub>: 0.0028 &rarr; 0.00041 (P<sub>L,round</sub>: 0.00094 &rarr; 0.00014, &Lambda; = 6.8&times;); and at p = 0.001, P<sub>L</sub>: 0.00078 &rarr; 0.00007 (P<sub>L,round</sub>: 0.00026 &rarr; 0.000023), reaching an error-suppression factor &Lambda;<sub>72&rarr;144</sub> = 11.2&times;. Leveraging Proposition 3, zero-shot cross-distance orbit weight transfer from [[72,12,6]] to [[144,12,12]] attains identical fault suppression with 0 retraining steps. Furthermore, under inhomogeneous transmon noise with 5% and 10% TLS defect hot spots (3&times; fault multiplier), adapting sparse CSD defect residuals (&gamma;<sub>v,t</sub> = &gamma;<sub>o(v),t</sub><sup>orbit</sup> + I[v &isin; D<sub>hot</sub>]&delta;&gamma;<sub>v,t</sub><sup>CSD</sup>) restores baseline fidelity without inflating parameter count.</p>

        <h2>IX. Discussion & Hardware Deployment Roadmap</h2>
        <h3>A. Comparison with Prior Art</h3>
        <div class="table-caption">TABLE V: Hardware Implementation Comparison Against Prior Art on Gross QLDPC Codes</div>
        <table>
            <thead>
                <tr>
                    <th>Architecture</th>
                    <th>Code / Scope</th>
                    <th>Platform</th>
                    <th>DSP</th>
                    <th>Logic (LUTs)</th>
                    <th>Latency</th>
                    <th>Admit Rate</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>Maurer et al. [12]</td><td>3D Window [[144,12,12]] (W=12)</td><td>IBM / AMD VU19P</td><td>0 (int4)</td><td>~450,000 LUTs (&gt;50% VU19P)</td><td>24 ns/iter (~408 ns mean/round)</td><td>No Fast/Slow Gate</td></tr>
                <tr><td>B&aacute;scones et al. (GARI) [48]</td><td>3D Window [[144,12,12]]</td><td>AMD VCU19P (3-Core)</td><td>Multi-Core</td><td>VCU19P Fabric</td><td>Sub-&mu;s Parallel Retries</td><td>Speculative Retry</td></tr>
                <tr><td>Gu et al. (Cascade) [49]</td><td>3D [[72,12,6]] / [[144,12,12]]</td><td>Nvidia H200 GPU</td><td>TensorCore</td><td>14-Layer Equiv. CNN</td><td>12.4 &mu;s (Batch GPU)</td><td>GPU Only</td></tr>
                <tr><td>Guang et al. (CoDecoder) [60]</td><td>[[72,12,6]] / Gross</td><td>GPU + Host CPU</td><td>TensorCore</td><td>Neural Soft Actor</td><td>~4.2 &mu;s (GPU batch)</td><td>82.4% (Routed to Cascade/Relay)</td></tr>
                <tr style="background: #eef7ee; font-weight: bold;"><td>Proposed 216-VNU Core</td><td>3D Sliding [[72,12,6]] (W=3)</td><td>AMD XCKU040</td><td>0 (6-bit CSD)</td><td>1,226&ndash;28,204 LUTs (11.6%)</td><td>102.4 ns (mean) / 240 ns</td><td>75.6% (P<sub>pipe</sub> = 1.9&times;10<sup>-3</sup> at p=0.003)</td></tr>
                <tr><td>Proposed 432-VNU Core (Projected)</td><td>3D Sliding [[144,12,12]] (W=3)</td><td>AMD XCKU040</td><td>0 (6-bit CSD)</td><td>~56,400 LUTs (Projected / un-synthesized)</td><td>Projected ~120&ndash;250 ns</td><td>72.4% (Est.)</td></tr>
            </tbody>
        </table>
        <p class="noindent">Table V compares our proposed Orbit-Tied QNBP against state-of-the-art QLDPC hardware decoders. While Maurer et al. [12] implemented 3D window decoding on a massive AMD VU19P FPGA requiring ~450,000 LUTs (&gt;50% of the device) without fast/slow path gating, and B&aacute;scones et al. (GARI) [48] rely on a resource-intensive multi-core VCU19P architecture with speculative retries, our architecture fits comfortably on a modest AMD Kintex UltraScale+ XCKU040 FPGA (consuming 1,226 to 28,204 LUTs, 0.51% to 11.64% device capacity) with strictly zero DSP slices. Furthermore, our Gate G<sub>3</sub> confidence margin filter routes 75.6% of windows to the 102.4 ns mean latency FPGA fast path with zero logical errors, resolving sliding-window queue backlog under a 1 &mu;s quantum cycle budget. In contrast, GPU batch decoders such as Cascade [49] incur 12.4 &mu;s latency, exceeding real-time coherence deadlines by over 12&times;.</p>

        <h3>B. AXI-Stream Streaming Integration</h3>
        <p class="noindent">The synthesizeable test harness (rtl/streaming_axi_harness.sv) demonstrates continuous streaming operation. Syndrome frames are ingested via an AXI4-Stream slave interface into an asynchronous FIFO. The decoding core processes windows with a deterministic worst-case latency of 240 ns, updates residual registers, and outputs committed fault corrections via an AXI-Stream master interface, providing a direct plug-and-play solution for FPGA-based quantum control stacks.</p>

        <h3>C. Limitations and Threats to Validity</h3>
        <p class="noindent"><b>1. Queue Overflow at Extreme Noise:</b> Under single-server stream stall (Policy B) with host software OSD (T<sub>fb</sub> = 320 &mu;s, c=1), queue stability requires p<sub>fb</sub> &lt; p<sub>crit</sub> = (1 - 0.1024)/(320 - 0.1024) = 0.281% (0.00281). At p = 0.003 (p<sub>fb</sub> = 24.4%), speculative fast-path forwarding (Policy A) forwards tentative corrections immediately with a 0.205% rollback rate, driving buffer overflow to 0.00% across B &ge; 4. On-chip multi-leg CSD fallback executes in &le; 720 ns (DSP=0, BRAM=0), maintaining sub-microsecond latency even under rejections.</p>
        <p><b>2. Hardware Routing Congestion on Non-Local Edges:</b> While [[72,12,6]] consumes only 11.64% of XCKU040, scaling to [[144,12,12]] (432 VNUs, ~56,400 projected LUTs) increases global wire fanout, requiring pipelined register stages to avoid clock degradation.</p>
        <p><b>3. Spatial Uniformity on Transmon Couplers:</b> Simulations evaluate uniform Pauli noise. Real processors (e.g. IBM Heron) exhibit localized T<sub>1</sub>/T<sub>2</sub> variances; while QNBP tolerates &plusmn;20% calibration drift (&lt;4% LER change), isolated defective qubits may require localized prior tuning.</p>

        <h2>X. Conclusion</h2>
        <p class="noindent">We have presented an orbit-tied, 6-bit quantized neural belief propagation decoder for bivariate-bicycle codes. By exploiting torus automorphisms, we collapsed parameter counts by 36&times; on [[72,12,6]] and 72&times; on the [[144,12,12]] gross code, mitigated untied overfitting, and realized multiplier-free execution with zero DSP slices. Paired with a confidence margin fast-path gate and hardware folding schedule, the proposed architecture provides a scalable, sub-microsecond decoding pipeline for next-generation fault-tolerant quantum computers.</p>

        <p class="noindent"><b>Author Contributions&mdash;</b>Md. Nazmul: Lead Researcher, Conceptualization, Methodology &amp; Software Architecture, Sliding-Window Algorithms, Manuscript Preparation. Musrat Jahan Gungun: Data Curation, Baseline Benchmarking, Validation &amp; Statistical Testing. Maheli Ahmed: Faculty Supervision, Resources, Formal Analysis &amp; Model Governance.</p>

        <p class="noindent"><b>Data and Code Availability&mdash;</b>The complete open-source codebase, including the Stim-to-PyG DEM compiler, automorphism orbit verifier, 6-bit QNBP checkpoints, and synthesizeable SystemVerilog RTL modules (vnu.sv, cnu.sv, g3_gate.sv, and streaming_axi_harness.sv) with 10,000-shot testbenches, is publicly available at: https://github.com/NazmulHasanNihal/orbit-tied-qnbp-sliding-window-bb.</p>
    </body>
    """
    p11.insert_htmlbox(pymupdf.Rect(40, 34, page_w - 40, page_h - 30), html_p11)

    # =============================================================
    # PAGE 12: Comprehensive 59-Reference Bibliography
    # =============================================================
    p12 = doc.new_page(width=page_w, height=page_h)
    add_header_footer(p12, 12)

    bib_path = "manuscript/references.bib"
    if not os.path.exists(bib_path):
        bib_path = "references.bib"
    with open(bib_path, "r", encoding="utf-8") as f:
        content = f.read()

    def format_ieee_authors(raw: str) -> str:
        cleaned = (
            raw.replace('{\\"a}', "ä")
            .replace('{\\"u}', "ü")
            .replace('{\\"o}', "ö")
            .replace("{\\'e}", "é")
            .replace("{\\'a}", "á")
            .replace("\\'a", "á")
            .replace("{", "")
            .replace("}", "")
            .strip()
        )
        if "IBM" in cleaned or "Architecture Team" in cleaned:
            return "IBM Quantum Architecture Team"

        authors = [a.strip() for a in cleaned.split(" and ")]
        formatted = []
        for a in authors:
            if not a:
                continue
            if a.lower() == "others":
                formatted.append("et al.")
                continue
            if "," in a:
                parts = a.split(",", 1)
                last = parts[0].strip()
                first = parts[1].strip()
                first_parts = first.split()
                initials = " ".join([f"{p[0]}." for p in first_parts if p])
                formatted.append(f"{initials} {last}".strip())
            else:
                first_parts = a.split()
                if len(first_parts) > 1:
                    last = first_parts[-1]
                    initials = " ".join([f"{p[0]}." for p in first_parts[:-1]])
                    formatted.append(f"{initials} {last}".strip())
                else:
                    formatted.append(a)
        if len(formatted) == 1:
            return formatted[0]
        elif len(formatted) == 2:
            if formatted[1] == "et al.":
                return f"{formatted[0]} et al."
            return f"{formatted[0]} and {formatted[1]}"
        else:
            if formatted[-1] == "et al.":
                return ", ".join(formatted[:-1]) + " et al."
            return ", ".join(formatted[:-1]) + f", and {formatted[-1]}"

    entries = re.findall(r"@(\w+)\{([^,]+),\s*(.*?)\n\}", content, re.DOTALL)
    items = []
    for idx, (etype, key, body) in enumerate(entries, 1):
        fields = {}
        for line in body.split("\n"):
            line = line.strip()
            m = re.match(r"^(\w+)\s*=\s*[\"{](.*?)[\"}],?$", line)
            if m:
                fields[m.group(1).lower()] = m.group(2).strip()

        author = format_ieee_authors(fields.get("author", "Unknown"))
        title = fields.get("title", "").replace("{", "").replace("}", "")
        journal = fields.get("journal", fields.get("booktitle", ""))
        year = fields.get("year", "")
        vol = fields.get("volume", "")
        num = fields.get("number", "")
        pages = fields.get("pages", "").replace("--", "-")
        doi = fields.get("doi", "")

        ref_str = f"<b>[{idx}]</b> {author}, &ldquo;{title},&rdquo; <i>{journal}</i>"
        if vol:
            ref_str += f", vol. {vol}"
        if num:
            ref_str += f", no. {num}"
        if pages:
            if "-" in pages or "," in pages:
                ref_str += f", pp. {pages}"
            else:
                ref_str += f", p. {pages}"
        if year:
            ref_str += f", {year}."
        if doi:
            ref_str += f" DOI: {doi}"

        items.append(f'<div class="ref-item">{ref_str}</div>')

    half = (len(items) + 1) // 2
    col1 = "".join(items[:half])
    col2 = "".join(items[half:])
    html_p12 = base_style + f"""
    <style>
        .ref-item {{ font-size: 5.4pt; line-height: 1.10; margin-bottom: 2.5px; text-align: justify; }}
        table.reftable {{ width: 100%; border-collapse: collapse; border: none; margin: 0; }}
        table.reftable td {{ vertical-align: top; border: none; padding: 0; }}
    </style>
    <body>
        <h2>References</h2>
        <table class="reftable">
            <tr>
                <td style="width: 48.5%; padding-right: 8px;">{col1}</td>
                <td style="width: 48.5%; padding-left: 8px;">{col2}</td>
            </tr>
        </table>
    </body>
    """
    p12.insert_htmlbox(pymupdf.Rect(40, 34, page_w - 40, page_h - 26), html_p12)

    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
    doc.save(output_pdf_path, deflate=True, garbage=4, clean=True)
    doc.close()
    print(f"✅ Generated single canonical 12-page publication PDF: {output_pdf_path}")


if __name__ == "__main__":
    build_ieee_manuscript_pdf()
