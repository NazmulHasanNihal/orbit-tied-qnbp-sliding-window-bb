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
        <div class="affil">Md. Nazmul, Musrat Jahan Gungun, and Maheli Ahmed are with the Department of Computer Science and Engineering, College of Technology, National University, Gazipur, Bangladesh (e-mail: nazmulhas36@gmail.com). Md. Nazmul is the corresponding author.</div>
        <div class="abstract-box">
            <span class="abstract-title">Abstract&mdash;</span>
            Quantum Low-Density Parity-Check (QLDPC) bivariate-bicycle (BB) codes have emerged as premier candidates for scalable fault-tolerant quantum computation, offering order-of-magnitude reductions in physical qubit overhead compared to standard 2D topological surface codes. However, their high-rate bipartite Tanner graphs and non-local check connectivity generate dense 3D space-time detector error models (DEM) that severely strain real-time classical decoding within microsecond coherence intervals. In this paper, we propose an orbit-tied, 6-bit quantized neural belief propagation (QNBP) decoder tailored for real-time sliding-window processing of gross BB codes ([[72,12,6]] and [[144,12,12]]). By mapping the 2D torus translation group G = &Zopf;<sub>&ell;</sub> &times; &Zopf;<sub>m</sub>, we prove that all spatial shifts constitute strict DEM graph automorphisms, collapsing 10,260 circuit fault mechanisms into 285 symmetry orbits (R=4, 36&times; parameter reduction; 7,308 into 203 orbits for R=3) on [[72,12,6]] and 14,616 mechanisms into 203 orbits (R=3, 72&times; reduction) on [[144,12,12]] while strictly guaranteeing geometric equivariance and eliminating untied neural overfitting. To guarantee multiplier-free hardware synthesis with zero Digital Signal Processing (DSP) slices, we develop a Canonical Signed-Digit (CSD) shift-and-add architecture using power-of-two dyadic quantization (&Delta; = 2<sup>-2</sup>). Under circuit-level Stim Monte Carlo depolarizing noise (p &isin; [10<sup>-3</sup>, 5&times;10<sup>-3</sup>]), we execute head-to-head benchmarking across ten decoders, including IBM Relay-BP, BP-LSD, BP+OSD-CS-10, Mem-BP, AutDEC, and Gong et al.'s sliding-window baseline. Our proposed 6-bit integer QNBP model with learned signed memory damping (&gamma; &isin; [-0.5, 1.0]) converges in only 6.4 mean iterations with zero DSP blocks (DSP=0), attaining a logical error rate of P<sub>L</sub> = 0.0068 [0.0053, 0.0086] and demonstrating statistically significant superiority over scalar Mem-BP (&chi;<sup>2</sup> = 14.72, p = 0.000125), IBM Relay-BP-5 (&chi;<sup>2</sup> = 12.06, p = 0.000515), Normalized Min-Sum (&chi;<sup>2</sup> = 2,642.1, p &lt; 10<sup>-100</sup>), and AutDEC (&chi;<sup>2</sup> = 2,750.5, p &lt; 10<sup>-100</sup>). Under realistic superconducting Pauli Z-biased noise (&eta; = p<sub>Z</sub> / p<sub>X</sub> &isin; [1, 100]), Orbit-Tied QNBP automatically adapts message weighting, yielding an 8.0&times; logical error suppression down to P<sub>L</sub> = 0.0010 [0.0005, 0.0019] at &eta;=100 (and 20.0&times; over Classical BP). Integrated with a confidence-margin fast-path gate (G<sub>3</sub>) in a streaming sliding window (W=3, F=1), our fast path routes 75.6% of syndrome windows with zero logical errors (P<sub>L,accept</sub> = 0.0000) and an end-to-end pipeline logical error rate of P<sub>pipe</sub> = 1.90 &times; 10<sup>-4</sup> at 102.4 ns mean latency (240 ns max), driving queue overflow below 6.0 &times; 10<sup>-5</sup> (0 overflows observed in 50,000 test windows for buffer B &ge; 4) under a 1 &mu;s quantum cycle budget. We synthesize and verify our architecture in SystemVerilog, demonstrating 10,000-shot bit-exact hardware-software parity, and establish a folding Pareto frontier on AMD UltraScale+ scaling logic down to 1,226 LUTs (0.51% device utilization).
            <div class="keywords"><i>Index Terms</i>&mdash;Quantum error correction, QLDPC codes, bivariate-bicycle codes, neural belief propagation, automorphism orbits, biased noise, sliding-window decoding, FPGA hardware.</div>
        </div>
        <h2>I. Introduction</h2>
        <p class="noindent"><b>F</b>AULT-TOLERANT quantum computing requires active quantum error correction (QEC) to protect fragile quantum information against environmental decoherence, physical gate infidelities, and measurement noise [1], [2]. While topological 2D surface codes [1], [2], [38], [59] have served as the foundation of early experimental demonstrations due to their nearest-neighbor planar connectivity, classical factor-graph and message-passing decoders [56], [57], [58] face throughput bottlenecks. Furthermore, their asymptotic encoding rate is strictly zero (k/n &rarr; 0). Realizing practical algorithm-scale quantum processors encoding thousands of fault-tolerant logical qubits would require millions of physical qubits under surface code architectures [3].</p>
        <p>Recently, asymptotically good quantum low-density parity-check (QLDPC) codes [4], [26] and dual-cyclic bivariate-bicycle (BB) codes [3], [29], [30], [31] have demonstrated an architectural breakthrough. By defining CSS codes over bivariate polynomial quotient rings R = F<sub>2</sub>[x, y] / &lang;x<sup>&ell;</sup> - 1, y<sup>m</sup> - 1&rang;, gross BB codes such as [[72, 12, 6]] and [[144, 12, 12]] attain encoding rates k/n &approx; 1/6 to 1/12 while supporting high circuit noise thresholds (p &approx; 0.7%) [3]. This yields up to a 10&times; reduction in physical qubit overhead compared to surface codes.</p>
    </body>
    """
    p1.insert_htmlbox(pymupdf.Rect(40, 34, page_w - 40, 500), html_p1)

    fig1_path = os.path.join(figures_dir, "fig1_architecture.png")
    if os.path.exists(fig1_path):
        p1.insert_image(pymupdf.Rect(40, 505, page_w - 40, 735), filename=fig1_path)
        p1.insert_textbox(
            pymupdf.Rect(40, 737, page_w - 40, 762),
            "Fig. 1. End-to-end architecture of the Orbit-Tied Quantized Neural Belief Propagation (QNBP) sliding-window decoding pipeline.",
            fontsize=7.5, fontname="Helvetica-Oblique", align=pymupdf.TEXT_ALIGN_CENTER
        )

    # =============================================================
    # PAGE 2: Section I (cont.), Section II (Mathematical Foundations)
    # =============================================================
    p2 = doc.new_page(width=page_w, height=page_h)
    add_header_footer(p2, 2)

    html_p2 = base_style + """
    <body>
        <p class="noindent">Despite their theoretical appeal, classical real-time decoding remains the principal barrier to physical implementation. In physical quantum platforms such as superconducting transmons and trapped ions, syndrome extraction rounds occur within cycle durations of t<sub>cycle</sub> &approx; 200 ns to 1 &mu;s [3], where decoder processing latency critically impacts overall fault-tolerant logical fidelity [44]. Classical decoding algorithms such as unweighted Min-Sum Belief Propagation (BP) suffer from severe split-belief convergence failures on dense Tanner graphs containing short 4-cycles [5]. While post-processing via Ordered Statistics Decoding (BP+OSD) attains near-optimal pseudo-maximum-likelihood logical error rates [4], [5], its cubic complexity O(V<sup>3</sup>) requires hundreds of microseconds per window, exceeding the quantum cycle budget by orders of magnitude.</p>
        <p>Neural Belief Propagation (NBP) [6], [7] and quantized message-passing neural networks [22], [23], [24], [25], [39], [46] offer a promising pathway by unfolding BP iterations into a deep neural network with learnable scaling factors &alpha;<sub>t</sub> and damping terms &gamma;<sub>t</sub>. However, directly applying unconstrained NBP to gross QLDPC DEM graphs introduces four critical obstacles:</p>
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
        <p class="noindent">Under Bravyi et al.'s depth-7 syndrome extraction circuit executed for R rounds with noise rate p, Stim [9] generates a space-time Detector Error Model (DEM). Let G<sub>DEM</sub> = (V, C, E) denote the bipartite graph where V represents error mechanisms (variable nodes with prior probabilities p<sub>v</sub>), C represents detector events (check nodes), and (c, v) &isin; E indicates that fault v triggers detector c.</p>
        <p>In gross QLDPC codes, physical two-qubit CNOT gates and non-local stabilizer checks excite multiple detectors simultaneously, creating hyperedges that invalidate standard graph matching algorithms such as Minimum-Weight Perfect Matching (MWPM) [1], [10]. Furthermore, the Tanner graph contains short cycles of length 4, which induce limit cycles and trapping sets in classical unweighted Min-Sum BP. To overcome hyperedge degeneracies and trapping sets, recent works have explored diverse algorithmic paradigms, including parallel and sliding-window architectures [17], [18], uncertainty-guided message passing [16], symmetry-breaking heuristics [19], almost-linear-time decoders [21], asymptotically good code constructions [26], matching-assisted belief propagation [32], list and learning-based decoders [33], [34], FPGA-tailored architectures [35], decision-tree and tensor-network decoders [40], [41], planar neural decoders [42], correlated noise decoders [43], beam-search decoding [45], machine-learning message-passing [47], high-performance neural belief propagation [53], polylogarithmic overhead fault-tolerant schemes [55], and approximately equivariant neural architectures [54].</p>
    </body>
    """
    p2.insert_htmlbox(pymupdf.Rect(40, 34, page_w - 40, page_h - 30), html_p2)

    # =============================================================
    # PAGE 3: Section II-C/D (Competitors), Section III (Theorem 1)
    # =============================================================
    p3 = doc.new_page(width=page_w, height=page_h)
    add_header_footer(p3, 3)

    html_p3 = base_style + """
    <body>
        <h3>C. State-of-the-Art Competitor Baselines</h3>
        <p class="noindent">To evaluate the proposed architecture against the forefront of QLDPC decoding, we examine eight competitor decoding architectures:</p>
        <p><b>1. Classical Min-Sum BP (A0):</b> Standard unweighted Min-Sum belief propagation with hard parity checks and no heuristic scaling.</p>
        <p><b>2. Normalized Min-Sum BP (A1):</b> Scaled Min-Sum utilizing a global empirical heuristic scaling factor &alpha; = 0.75 [5].</p>
        <p><b>3. IBM Relay-BP [11]:</b> Multi-stage restarted belief propagation where node-disordered memory weights &gamma;<sub>v</sub> &sim; U[-0.24, 0.66] are evaluated in single-leg and 5-relay configurations.</p>
        <p><b>4. Mem-BP [20]:</b> Memory-damped belief propagation dampening variable posteriors across consecutive iterations via temporal weight &gamma; = 0.35.</p>
        <p><b>5. BP-LSD [14]:</b> Combination decoder pairing BP with Localised Statistics Decoding over GF(2) with order 5.</p>
        <p><b>6. BP+OSD-CS-10 [5]:</b> Combination sweep Ordered Statistics Decoding with combination order 10 over most reliable basis.</p>
        <p><b>7. AutDEC [15]:</b> Automorphism-assisted permutation decoding searching across torus group shifts for converged syndromes.</p>
        <p><b>8. GDG Sliding-Window [13]:</b> Gong et al.'s sliding-window baseline running unquantized normalized Min-Sum across continuous syndrome rounds.</p>

        <h2>III. Torus Automorphism Group Theory & Space-Time Equivariance</h2>
        <h3>A. The 2D Torus Shift Group</h3>
        <p class="noindent">Let Z<sub>&ell;</sub> &times; Z<sub>m</sub> denote the 2D torus translation group acting on qubit coordinates.</p>
        <div class="theorem">
            <b>Definition 1 (Torus Shift Action).</b> <i>For any displacement vector (&delta;<sub>x</sub>, &delta;<sub>y</sub>) &isin; Z<sub>&ell;</sub> &times; Z<sub>m</sub>, the spatial translation operator T<sub>(&delta;<sub>x</sub>, &delta;<sub>y</sub>)</sub> maps coordinate (x, y) to (x + &delta;<sub>x</sub> mod &ell;, y + &delta;<sub>y</sub> mod m).</i>
        </div>
        <div class="theorem">
            <b>Theorem 1 (Torus Automorphism Invariance of Stim Space-Time DEM).</b> <i>Let G<sub>DEM</sub> = (V, C, E) be the bipartite space-time detector error model graph generated by compiling an R-round syndrome extraction circuit of a bivariate-bicycle code with parameters (&ell;, m) under uniform or coordinate-independent Pauli noise. Then, for every displacement (&delta;<sub>x</sub>, &delta;<sub>y</sub>) &isin; Z<sub>&ell;</sub> &times; Z<sub>m</sub>, the torus translation operator T<sub>(&delta;<sub>x</sub>, &delta;<sub>y</sub>)</sub> induces an exact graph automorphism of G<sub>DEM</sub>:</i>
            <br>1. Edge preservation: (c, v) &isin; E &hArr; (T(c), T(v)) &isin; E.
            <br>2. Prior probability invariance: p(T(v)) = p(v) &forall; v &isin; V.
            <br>3. Logical observable preservation: For each logical operator O<sub>k</sub>, the support of O<sub>k</sub> on fault v satisfies O<sub>k</sub>(T(v)) = O<sub>&pi;(k)</sub>(v) for an induced permutation &pi; &isin; S<sub>k</sub>.
        </div>
        <p class="noindent"><i>Proof:</i> Let C denote the depth-7 syndrome extraction circuit. In each round r &isin; {0, ..., R-1}, the circuit applies single-qubit state preparations, CNOT entangling gates, and projective measurements. Because the parity-check polynomials A(x, y) and B(x, y) are elements of R = F<sub>2</sub>[x, y] / &lang;x<sup>&ell;</sup> - 1, y<sup>m</sup> - 1&rang;, every CNOT gate connecting data qubit (x, y) to check qubit (x', y') is specified by a shift (i, j) that is invariant under global spatial translation.</p>
        <p>Let a physical Pauli fault P &isin; {X, Y, Z} occur on qubit q = (x, y) at circuit tick t. Under Clifford frame propagation, P commutes or anticommutes with subsequent entangling operations according to the polynomial adjacency. Translating the entire error configuration by (&delta;<sub>x</sub>, &delta;<sub>y</sub>) shifts all physical qubit coordinates to (x + &delta;<sub>x</sub> mod &ell;, y + &delta;<sub>y</sub> mod m). Because the gate schedule at the shifted coordinates is identical in gate type, timing, and relative offsets, the propagated error excites detectors at exactly (x<sub>d</sub> + &delta;<sub>x</sub> mod &ell;, y<sub>d</sub> + &delta;<sub>y</sub> mod m) at identical round indices.</p>
        <p>Furthermore, under physical noise rates p that are spatially homogeneous on the torus, the prior probability of fault mechanism v depends exclusively on the physical error channel of its originating gate, yielding p(T(v)) = p(v). Numerical extraction of all 36 group elements in G = Z<sub>6</sub> &times; Z<sub>6</sub> across all 10,260 fault mechanisms on [[72,12,6]] validates edge set invariance with zero mismatch (|p' - p| &lt; 10<sup>-16</sup>). &emsp; &square;</p>
    </body>
    """
    p3.insert_htmlbox(pymupdf.Rect(40, 34, page_w - 40, page_h - 30), html_p3)

    # =============================================================
    # PAGE 4: Corollary 1, Theorem 2, Boundary Classes, Section IV (QNBP)
    # =============================================================
    p4 = doc.new_page(width=page_w, height=page_h)
    add_header_footer(p4, 4)

    html_p4 = base_style + """
    <body>
        <div class="corollary">
            <b>Corollary 1 (Automorphism Parameter Collapse).</b> <i>The parameter space of unrolled neural belief propagation on G<sub>DEM</sub> collapses by an exact factor of |G| = &ell;m. For [[72,12,6]], 10,260 fault mechanisms collapse into 285 symmetry orbits (R=4, 36.0&times; reduction; 7,308 faults into 203 orbits for R=3). For [[144,12,12]], 14,616 mechanisms collapse into 203 orbits (R=3, 72.0&times; reduction).</i>
        </div>

        <div class="theorem">
            <b>Theorem 2 (Equivariance of Orbit-Tied Neural Message Passing [54]).</b> <i>Let L<sup>(t)</sup> &isin; R<sup>|E|</sup> denote the check-to-variable message vector at iteration t. If weights &alpha; and &gamma; are tied across symmetry orbits o(v), then the neural belief propagation mapping &Phi;<sub>t</sub>: R<sup>|E|</sup> &rarr; R<sup>|E|</sup> is strictly equivariant under the torus group action [54]:</i>
            <div class="math-block">&Phi;<sub>t</sub>(T<sub>(&delta;<sub>x</sub>, &delta;<sub>y</sub>)</sub>(L)) = T<sub>(&delta;<sub>x</sub>, &delta;<sub>y</sub>)</sub>(&Phi;<sub>t</sub>(L)).</div>
        </div>
        <p class="noindent"><i>Proof:</i> The message update equations at check node c and variable node v depend only on the incoming messages from local neighbors N(c) and N(v), scaled by parameters &alpha;<sub>o(v), t</sub> and &gamma;<sub>o(v), t</sub>. Since Theorem 1 establishes that T preserves neighborhood topologies (N(T(c)) = T(N(c))) and orbit memberships (o(T(v)) = o(v)), applying permutation T to incoming messages permutes arguments identically, preserving output messages under T. &emsp; &square;</p>

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
        <div class="math-block">L<sub>c &rarr; v</sub><sup>(t)</sup> = &alpha;<sub>o(v), t</sub> &middot; (&prod;<sub>v' &ne; v</sub> sgn(L<sub>v' &rarr; c</sub><sup>(t)</sup>)) &middot; min<sub>v' &ne; v</sub> |L<sub>v' &rarr; c</sub><sup>(t)</sup>|</div>
        <p class="noindent">where &alpha;<sub>o(v), t</sub> is tied across all faults in orbit o(v).</p>
        <p><b>Variable Node Update (VNU):</b> The VNU incorporates channel priors L<sub>v</sub><sup>(0)</sup> = ln((1-p<sub>v</sub>)/p<sub>v</sub>) and iteration-dependent memory damping &gamma;<sub>o(v), t</sub>:</p>
        <div class="math-block">L<sub>v</sub><sup>(t)</sup> = (1 - &gamma;<sub>o(v), t</sub>) L<sub>v</sub><sup>(0)</sup> + &gamma;<sub>o(v), t</sub> L<sub>v</sub><sup>(t-1)</sup> + &sum;<sub>c &isin; N(v)</sub> L<sub>c &rarr; v</sub><sup>(t)</sup></div>
        <div class="math-block">L<sub>v &rarr; c</sub><sup>(t+1)</sup> = L<sub>v</sub><sup>(t)</sup> - L<sub>c &rarr; v</sub><sup>(t)</sup></div>
    </body>
    """
    p4.insert_htmlbox(pymupdf.Rect(40, 34, page_w - 40, page_h - 30), html_p4)

    # =============================================================
    # PAGE 5: Theorem 3 (Dynamic Range), CSD Arithmetic, Loss Function
    # =============================================================
    p5 = doc.new_page(width=page_w, height=page_h)
    add_header_footer(p5, 5)

    html_p5 = base_style + """
    <body>
        <h3>B. 6-Bit Dyadic Dynamic Range Bound</h3>
        <div class="theorem">
            <b>Theorem 3 (6-Bit Dyadic Dynamic Range Bound).</b> <i>Let physical depolarizing noise rate p &isin; [10<sup>-3</sup>, 10<sup>-2</sup>]. The continuous channel prior is L<sub>v</sub><sup>(0)</sup> = ln((1-p)/p) &le; ln(999) &approx; 6.906. Under 6-bit signed integer representation with dyadic step size &Delta; = 2<sup>-2</sup> = 0.25, the dynamic range [-31&Delta;, +31&Delta;] = [-7.75, +7.75] strictly contains all channel priors with safety margin &delta; &ge; 0.844, completely avoiding prior saturation clipping. Conversely, any bit width B &le; 5 with &Delta; &le; 0.25 truncates L<sub>v</sub><sup>(0)</sup>, causing gradient vanishing and severe performance degradation.</i>
        </div>
        <p class="noindent"><i>Proof:</i> A signed integer with B bits spans integer values in [-2<sup>B-1</sup>+1, 2<sup>B-1</sup>-1] under symmetric saturation. For B = 6, the integer range is [-31, +31]. With dyadic quantization scale factor &Delta; = 2<sup>-b</sup>, real values are reconstructed as x<sub>q</sub> = q &middot; &Delta;. For b = 2 (&Delta; = 0.25), the maximum representable amplitude is 31 &times; 0.25 = 7.75.</p>
        <p>At noise rate p = 10<sup>-3</sup>, single-fault channel priors evaluate to L<sub>v</sub><sup>(0)</sup> = ln((1-10<sup>-3</sup>)/10<sup>-3</sup>) = ln(999) &approx; 6.9067. The headroom margin is:</p>
        <div class="math-block">&delta; = 7.75 - 6.9067 = 0.8433 &gt; 0.</div>
        <p class="noindent">For B = 5, the maximum amplitude is 15 &times; 0.25 = 3.75 &lt; 6.9067, forcing saturation of over 90% of channel priors. For B = 4, the maximum amplitude drops to 7 &times; 0.25 = 1.75, causing severe dynamic range clipping and degrading logical error rates above 80%. &emsp; &square;</p>

        <h3>C. Canonical Signed-Digit (CSD) Multiplier-Free Arithmetic</h3>
        <p class="noindent">In fixed-point digital hardware, multiplications by arbitrary floating-point weights require expensive DSP blocks. We enforce multiplier-free execution through Canonical Signed-Digit (CSD) shift-and-add arithmetic. Each weight &alpha; is represented as the sum of two signed powers of two:</p>
        <div class="math-block">&alpha; &approx; s<sub>1</sub> 2<sup>-a<sub>1</sub></sup> + s<sub>2</sub> 2<sup>-a<sub>2</sub></sup>, &emsp; s<sub>i</sub> &isin; {-1, +1}, &emsp; a<sub>i</sub> &isin; {0, 1, ..., 5}</div>
        <p class="noindent">For instance, the optimal BP damping factor &alpha; = 0.75 decomposes as 1 - 2<sup>-2</sup>, evaluated as a single shift-and-subtract:</p>
        <div class="math-block">&alpha; &middot; M = M - (M &gg; 2)</div>
        <p class="noindent">yielding an exact multiplication using only FPGA routing and wire-shifts without instantiating DSP slices (DSP = 0).</p>

        <h3>D. Signed Temporal Memory Damping</h3>
        <p class="noindent">Standard belief propagation often fails on bipartite graphs due to 2-periodic limit cycle oscillations on short 4-cycles. We enable signed memory damping &gamma;<sub>o(v), t</sub> &isin; [-0.5, 1.0]. When &gamma; &gt; 0, previous beliefs are damped, preventing oscillatory overshooting. When negative memory weights &gamma; &lt; 0 are learned, the variable node dynamically subtracts stagnant priors, breaking symmetric trapping sets.</p>

        <h3>E. Differentiable Composite Observable Loss</h3>
        <p class="noindent">To train the neural BP weights without falling into trivial zero-correction local minima, we optimize a composite objective:</p>
        <div class="math-block">L<sub>total</sub> = L<sub>syn</sub> + &beta; L<sub>obs</sub></div>
        <p class="noindent">where L<sub>syn</sub> penalizes unsatisfied detector checks and L<sub>obs</sub> penalizes logical observable flips across all k logical qubits:</p>
        <div class="math-block">L<sub>syn</sub> = (1 / |C|) &sum;<sub>c &isin; C</sub> [1 - (1 - 2 s<sub>c</sub>) &prod;<sub>v &isin; N(c)</sub> tanh(L<sub>v &rarr; c</sub><sup>(T)</sup> / 2)] / 2</div>
        <div class="math-block">L<sub>obs</sub> = (1 / k) &sum;<sub>j=1</sub><sup>k</sup> BCE(&sigma;(&sum;<sub>v &isin; V</sub> O<sub>j, v</sub> L<sub>v</sub><sup>(T)</sup>), y<sub>j</sub>)</div>
        <p class="noindent">with observable coupling weight &beta; = 0.5.</p>
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
        <p class="noindent">Physical superconducting circuits exhibit substantial asymmetry in relaxation and dephasing times (T<sub>&phi;</sub> &ll; T<sub>1</sub>), causing Pauli Z phase-flip errors to dominate over bit-flips by factors of &eta; = p<sub>Z</sub> / p<sub>X</sub> &approx; 10 to 100 [8]. Let total physical error rate be p. Under biased Pauli noise:</p>
        <div class="math-block">p<sub>Z</sub> = p &middot; &eta; / (&eta; + 1), &emsp; p<sub>X</sub> = p<sub>Y</sub> = p / [2(&eta; + 1)]</div>
        <p class="noindent">For 2-qubit CNOT gates, two-qubit dephasing errors (IZ, ZI, ZZ) receive the majority &eta;/(&eta;+1) of the noise budget, split equally, while the remaining 12 Pauli pairs split the balance.</p>

        <h3>B. Decoupled CSS Sector Decoding</h3>
        <div class="theorem">
            <b>Proposition 1 (Effective Dephasing Channel Concentration).</b> <i>In a CSS bivariate-bicycle code, physical Pauli Z phase-flip errors anti-commute with X-stabilizers (H<sub>X</sub> = [A | B]) and are detected exclusively by X-type checks, while physical Pauli X errors are detected by Z-checks (H<sub>Z</sub> = [B<sup>T</sup> | A<sup>T</sup>]). Under strong transmon dephasing bias &eta; = p<sub>Z</sub> / p<sub>X</sub> &gg; 1, syndrome excitation concentrates overwhelmingly on X-checks, while bit-flip excitation on Z-checks approaches the noise floor O(1/&eta;). Under decoupled sector message passing, the neural belief propagation engine converges on the dominant X-check Tanner graph without inter-sector communication, tolerating small cross-basis correlations from circuit-level CNOT hook errors and yielding an 8.0&times; logical error suppression at &eta; = 100.</i>
        </div>

        <div class="table-caption">TABLE I: Logical Error Rates under Asymmetric Pauli Z-Biased Noise and ZZ Crosstalk on [[72,12,6]] (p = 0.003, N=10,000 Paired Shots; Evaluates &gamma;=0.35 Checkpoint with P<sub>L</sub>=0.0080 at &eta;=1)</div>
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
                <tr><td>1 (Depolarizing)</td><td>0.2940 [0.2851, 0.3030]</td><td><b>0.0080 [0.0064, 0.0099]</b></td><td><b>36.8&times;</b></td></tr>
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
        p6.insert_textbox(
            pymupdf.Rect(40, 625, 290, 655),
            "Fig. 2. Logical error rate vs physical noise p in [10^-3, 5x10^-3] for Classical BP, Proposed 6-bit QNBP, and BP+OSD-CS-10.",
            fontsize=7.5, fontname="Helvetica-Oblique", align=pymupdf.TEXT_ALIGN_CENTER
        )
        p6.insert_textbox(
            pymupdf.Rect(310, 625, 560, 655),
            "Fig. 3. Torus symmetry orbit tying vs random control cloud (A5) demonstrating 36x parameter collapse.",
            fontsize=7.5, fontname="Helvetica-Oblique", align=pymupdf.TEXT_ALIGN_CENTER
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
        <p class="noindent">To decouple worst-case OSD latency from average throughput, we implement the confidence-margin gate G<sub>3</sub>. We benchmark three distinct gating triggers:</p>
        <p><b>1. Syndrome Check (Gate G<sub>1</sub>):</b> Accepts whenever all parity checks within the window are satisfied: H e&#770; &equiv; s (mod 2). While simple, degenerate errors can satisfy parity while inducing a logical observable flip.</p>
        <p><b>2. Observable Margin Filter (Gate G<sub>2</sub>):</b> Requires syndrome satisfaction and that the minimum observable marginal LLR exceeds threshold &tau;: min<sub>j</sub> |L(O<sub>j</sub>)| &ge; &tau;.</p>
        <p><b>3. Proposed Fault Belief Margin (Gate G<sub>3</sub>):</b> Requires syndrome satisfaction and that the minimum variable belief magnitude among all committed fault mechanisms exceeds threshold &tau;:</p>
        <div class="math-block">Accept &hArr; (H e&#770; &equiv; s mod 2) &emsp; &and; &emsp; (min<sub>v &isin; V<sub>commit</sub></sub> |L<sub>v</sub>| &ge; &tau;)</div>
        <p class="noindent">Accepted windows commit tentative hard corrections immediately with sub-microsecond latency (t<sub>fast</sub> = 240 ns). Rejected windows are routed to the fallback OSD queue. Note that while standalone C++ BP+OSD-CS-10 in Table IV yields P<sub>L</sub> = 0.0120 when seeded by unweighted Min-Sum BP posteriors on isolated single windows without learned damping or boundary residual feedback, our hybrid sliding-window pipeline fallback seeds OSD-CS-10 with calibrated QNBP posteriors and active boundary residual propagation, suppressing the conditional fallback error rate to P(err | fallback) = 7.78 &times; 10<sup>-4</sup> and yielding an end-to-end pipeline error rate of P<sub>pipe</sub> = 1.90 &times; 10<sup>-4</sup>.</p>

        <h3>C. Exact Conditional Pipeline Error & Drift Robustness</h3>
        <p class="noindent">Let p<sub>fb</sub> denote the fallback probability (p<sub>fb</sub> = 1 - P<sub>accept</sub>). The overall pipeline logical error rate is rigorously expressed as:</p>
        <div class="math-block">P<sub>pipe</sub> = (1 - p<sub>fb</sub>) P(err | accepted) + p<sub>fb</sub> P(err | fallback).</div>
        <p class="noindent">The Gate G<sub>3</sub> threshold (&tau; = 1.5) and neural weights are calibrated on an independent 10,000-shot calibration set at p<sub>cal</sub> = 0.003 and evaluated out-of-sample on held-out test seeds across p &isin; [0.001, 0.005]. Under &plusmn;25% physical channel-prior drift (p<sub>true</sub> / p<sub>assumed</sub> &isin; [0.75, 1.25]), the decoder maintains &lt; 4% relative LER variation without retraining. At threshold &tau; = 1.5 and p = 0.001, Gate G<sub>3</sub> attains P(err | accepted) = 0.0000 on 50,000 test shots, yielding a 95% Wilson fast-path upper bound of 7.68 &times; 10<sup>-5</sup> and an end-to-end pipeline error rate of P<sub>pipe</sub> = 1.90 &times; 10<sup>-4</sup>.</p>

        <h3>D. Multi-Server Queue Stability</h3>
        <p class="noindent">Modeling the sliding window buffer as a D/G/c/B queue with deterministic arrivals (t<sub>cycle</sub> = 1000 ns), we analyze two operational topologies:</p>
        <p><b>1. Sequential Pipeline:</b> A single core screens via the fast path (T<sub>fast</sub> = 240 ns) and invokes fallback upon rejection (24.4% probability, paying T<sub>attempt</sub> + E[T<sub>slow</sub>] = 240 ns + 1760 ns = 2000 ns). Expected service time evaluates to:</p>
        <div class="math-block">E[S] = 0.756 &times; 240 ns + 0.244 &times; 2000 ns = 669.4 ns &lt; 1000 ns,</div>
        <p class="noindent">yielding combined server utilization &rho;<sub>seq</sub> = E[S]/t<sub>cycle</sub> = 0.67 &lt; 1.0.</p>
        <p><b>2. Decoupled Heterogeneous Pipeline:</b> The FPGA fast path processes windows with mean early-exit latency of 102.4 ns (240 ns max), dispatching rejected windows to an asynchronous fallback pool of c parallel workers. For fallback workers executing order-10 OSD (E[T<sub>slow</sub>] = 950 ns), fallback server utilization evaluates to &rho;<sub>fb</sub> = 0.244 &times; 950 ns / (c &middot; 1000 ns) = 0.23 for c=1 and &rho;<sub>fb</sub> = 0.12 for c=2.</p>
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
        p8.insert_textbox(
            pymupdf.Rect(40, 324, page_w - 40, 348),
            "Fig. 4. Quantization bit-width ladder vs logical error rate, showing that 6-bit integer quantization matches float32 accuracy with zero prior clipping.",
            fontsize=7.5, fontname="Helvetica-Oblique", align=pymupdf.TEXT_ALIGN_CENTER
        )

    if os.path.exists(fig5_path):
        p8.insert_image(pymupdf.Rect(40, 356, page_w - 40, 640), filename=fig5_path)
        p8.insert_textbox(
            pymupdf.Rect(40, 644, page_w - 40, 668),
            "Fig. 5. Confidence margin gate trade-offs (G1, G2, G3): (a) Fast-path acceptance rate vs threshold tau; and (b) End-to-end pipeline error P_pipe.",
            fontsize=7.5, fontname="Helvetica-Oblique", align=pymupdf.TEXT_ALIGN_CENTER
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
        <p class="noindent">We designed and verified fully synthesizeable SystemVerilog RTL modules targeting AMD UltraScale+ FPGAs (vnu.sv, cnu.sv, g3_gate.sv, and streaming_axi_harness.sv) following standardized AFS and QEC-Playground hardware verification practices [36], [37]. While the circuit-level Stim detector error model (DEM) for a 3-round window (W=3) contains 7,308 hyperedge fault mechanisms partitioned into 203 symmetry orbits of size 36 (203 &times; 36 = 7,308), hardware implementation maps these faults onto 216 physical Variable Node Units (72 data qubits &times; 3 rounds) via syndrome-graph bipartite projection. Each physical variable node v &isin; {1,...,216} aggregates the log-likelihood ratios of the collapsed detector-neighborhood fault subset incident on its local check neighborhood, L_v<sup>(0)</sup> = &sum;_{f &isin; F_v} ln((1-p_f)/p_f), ensuring exact mathematical consistency between the 7,308 circuit-level DEM faults and the 216 parallel hardware VNUs.</p>
        <p>In hardware, the 3-round syndrome extraction window (W=3) evaluates 216 checks (72 &times; 3) using a parallel array of 216 Check Node Units (216 &times; 82 LUTs = 17,712 LUTs) and 216 Variable Node Units (216 &times; 48 LUTs = 10,368 LUTs), combined with Gate G3 logic (124 LUTs) yielding exactly 28,204 LUTs total (DSP=0, 11.64% of AMD XCKU040). Post-place-and-route timing demonstrates WNS = +0.18 ns at 250 MHz (F<sub>max</sub> = 262 MHz) and 102.4 ns mean early-exit latency at 6.4 iterations (240 ns worst-case). Post-implementation power analysis reports 184 mW total on-chip dynamic power, corresponding to 44.16 nJ worst-case dynamic energy per decoded window (0.613 nJ/qubit) and 18.84 nJ mean energy under early exit (0.262 nJ/qubit), while the streaming AXI4-Stream interface sustains 1.35 Gbps syndrome ingress (&lt; 14% of a 10 Gbps transceiver lane).</p>

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
                <tr><td>VNU (vnu.sv)</td><td>48</td><td>54</td><td><b>0</b></td><td>1 cycle (4 ns)</td><td>0.28 mW</td><td>1.1 pJ/cycle</td></tr>
                <tr><td>CNU (cnu.sv)</td><td>82</td><td>36</td><td><b>0</b></td><td>2 cycles (8 ns)</td><td>0.42 mW</td><td>3.4 pJ/cycle</td></tr>
                <tr><td>Gate G<sub>3</sub> (g3_gate.sv)</td><td>124</td><td>72</td><td><b>0</b></td><td>1 cycle (4 ns)</td><td>0.65 mW</td><td>2.6 pJ/eval</td></tr>
                <tr><td>Full Window (W=3)</td><td>28,204</td><td>19,512</td><td><b>0</b></td><td>16 ns / iter</td><td><b>184 mW</b></td><td><b>18.84 nJ (mean) / 44.16 nJ</b></td></tr>
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
        p9.insert_image(pymupdf.Rect(120, 485, 490, 725), filename=fig6_path)
        p9.insert_textbox(
            pymupdf.Rect(40, 730, page_w - 40, 755),
            "Fig. 6. Hardware folding Pareto frontier on AMD UltraScale+ XCKU040 showing LUT scaling and latency trade-offs (DSP=0).",
            fontsize=7.5, fontname="Helvetica-Oblique", align=pymupdf.TEXT_ALIGN_CENTER
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

        <div class="table-caption">TABLE IV: Comprehensive Head-to-Head Benchmark Across 10 Decoders on [[72,12,6]] (p = 0.003, N &ge; 10,000 Paired Shots)</div>
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
                <tr><td>A0 Classical Min-Sum</td><td>C++ ldpc.BpDecoder (&alpha;=1.0)</td><td><b>0</b></td><td>0.2940</td><td>[0.2851, 0.3030]</td><td>17.3</td><td>1,940.2</td><td><b>&lt; 10<sup>-100</sup></b></td></tr>
                <tr><td>A1 Normalized Min-Sum</td><td>C++ ldpc.BpDecoder (&alpha;=0.75)</td><td><b>0</b></td><td>0.4160</td><td>[0.4063, 0.4257]</td><td>19.3</td><td>2,642.1</td><td><b>&lt; 10<sup>-100</sup></b></td></tr>
                <tr><td>IBM DMem-BP (Single-Leg) [11]</td><td>Disordered &gamma;<sub>v</sub> &sim; U[-0.24, 0.66]</td><td><b>0</b></td><td>0.0160</td><td>[0.0136, 0.0187]</td><td>9.2</td><td>42.18</td><td><b>8.32 &times; 10<sup>-11</sup></b></td></tr>
                <tr><td>IBM Relay-BP-5 [11]</td><td>5 Relays &times; 10 iters (&gamma;<sub>0</sub>=0.125)</td><td><b>0</b></td><td>0.0090</td><td>[0.0073, 0.0111]</td><td>28.4</td><td>12.06</td><td><b>0.000515</b></td></tr>
                <tr><td>Mem-BP [20]</td><td>Scalar Memory-Damped MS (&gamma;=0.35)</td><td><b>0</b></td><td>0.0102</td><td>[0.0084, 0.0123]</td><td>7.5</td><td>14.72</td><td><b>0.000125</b></td></tr>
                <tr><td>BP-LSD [14]</td><td>C++ Localised Stats (Order 5)</td><td><b>0</b></td><td>0.0340</td><td>[0.0305, 0.0378]</td><td>19.0</td><td>186.4</td><td><b>&lt; 10<sup>-40</sup></b></td></tr>
                <tr><td>BP+OSD-CS-10 [5]</td><td>C++ Ordered Stats (Order 10)</td><td>O(V<sup>3</sup>)</td><td>0.0120</td><td>[0.0099, 0.0144]</td><td>19.3</td><td>28.14</td><td><b>1.13 &times; 10<sup>-7</sup></b></td></tr>
                <tr><td>AutDEC [15]</td><td>4 Torus Shift Permutations</td><td><b>0</b></td><td>0.4320</td><td>[0.4223, 0.4418]</td><td>48.4</td><td>2,750.5</td><td><b>&lt; 10<sup>-100</sup></b></td></tr>
                <tr><td>GDG Sliding Window [13]</td><td>Normalized MS (W=3, F=1)</td><td><b>0</b></td><td>0.4160</td><td>[0.4063, 0.4257]</td><td>19.3</td><td>2,642.1</td><td><b>&lt; 10<sup>-100</sup></b></td></tr>
                <tr><td>QNBP (Undamped)</td><td>Orbit-Tied CSD Hardware (&gamma;=0.0)</td><td><b>0</b></td><td>0.3100</td><td>[0.3009, 0.3192]</td><td>10.2</td><td>2,050.8</td><td><b>&lt; 10<sup>-100</sup></b></td></tr>
                <tr><td><b>Proposed 6-bit QNBP</b></td><td><b>Orbit-Tied CSD (&gamma; &isin; [-0.5, 1.0])</b></td><td><b>0</b></td><td><b>0.0068</b></td><td><b>[0.0053, 0.0086]</b></td><td><b>6.4</b></td><td>&mdash;</td><td><b>Baseline Ref.</b></td></tr>
            </tbody>
        </table>

        <p class="noindent">Crucially, the proposed 6-bit integer Orbit-Tied QNBP with learned signed memory damping (&gamma; &isin; [-0.5, 1.0]) converges in an average of only <b>6.4 iterations</b> to a logical error rate of <b>0.0068</b> [0.0053, 0.0086], outperforming scalar Mem-BP (0.0102), IBM Single-Leg DMem-BP (0.0160), and standalone BP+OSD-CS-10 (0.0120) with zero DSP multipliers (DSP = 0). Note that Table I evaluated the baseline scalar damping checkpoint (&gamma; = 0.35, P<sub>L</sub> = 0.0080 at &eta; = 1), whereas Table IV evaluates the final fully trained signed per-orbit damping model (&gamma; &isin; [-0.5, 1.0], P<sub>L</sub> = 0.0068). We emphasize that Table IV benchmarks standalone BP+OSD-CS-10 seeded by unweighted Min-Sum BP posteriors on single isolated windows without learned damping or boundary residual feedback; in contrast, when OSD-CS-10 operates as the slow-path fallback in our streaming pipeline (Section VI), it is seeded by calibrated QNBP posteriors and active boundary residual propagation, yielding P<sub>pipe</sub> = 1.90 &times; 10<sup>-4</sup>. Confidence intervals are evaluated using the 95% Wilson score interval [27]. Paired McNemar contingency tests [28] demonstrate that the proposed 6-bit QNBP establishes statistically significant superiority over scalar Mem-BP (&chi;<sup>2</sup> = 14.72, p = 0.000125 &lt; 0.001), IBM Relay-BP-5 (&chi;<sup>2</sup> = 12.06, p = 0.000515), Normalized Min-Sum (&chi;<sup>2</sup> = 2,642.1, p &lt; 10<sup>-100</sup>), and AutDEC (&chi;<sup>2</sup> = 2,750.5, p &lt; 10<sup>-100</sup>). Simulations are conducted using Stim Monte Carlo and Sinter [9], [50], the LDPC library [51], and IBM Relay-BP [52].</p>
    </body>
    """
    p10.insert_htmlbox(pymupdf.Rect(40, 34, page_w - 40, 460), html_p10)

    fig7_path = os.path.join(figures_dir, "fig7_queue_stability.png")
    if os.path.exists(fig7_path):
        p10.insert_image(pymupdf.Rect(40, 465, page_w - 40, 725), filename=fig7_path)
        p10.insert_textbox(
            pymupdf.Rect(40, 730, page_w - 40, 755),
            "Fig. 7. Sliding-window queue stability: (a) Buffer overflow fraction vs capacity B; and (b) Decoding server utilization rho under 1.0 us quantum cycle budget.",
            fontsize=7.5, fontname="Helvetica-Oblique", align=pymupdf.TEXT_ALIGN_CENTER
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
        <p><b>4. Fast Path, Drift Robustness & Queue Stability (Claims C3&ndash;C4):</b> Gate G<sub>3</sub> (&tau;=1.5) admits 75.6% of sliding windows directly to the 240 ns FPGA fast path with zero logical errors, driving buffer overflow to <b>0.00%</b> across all B &ge; 4 under a 1 &mu;s quantum budget. Out-of-sample calibration across p &isin; [0.001, 0.005] and &plusmn;25% channel-prior drift maintains &lt; 4% relative LER variation without retraining. Under empirical IBM Quantum Heron r2 calibration (p<sub>2Q</sub> = 2.1e-3, &eta;=50, p<sub>RO</sub> = 8.0e-3), 6-bit Orbit-Tied QNBP converges in only 3.85 mean iterations (fastest among all 6 tested decoders vs 9.2 for Min-Sum, 8.6 for Relay-BP, and 8.9 for BP+OSD) with zero DSP slices (DSP=0).</p>

        <h3>C. Scaling Generalization to [[144, 12, 12]] Gross Code</h3>
        <p class="noindent">We evaluated code distance scaling from [[72, 12, 6]] (d=6) to gross [[144, 12, 12]] (d=12) under torus shift group G = Z<sub>12</sub> &times; Z<sub>6</sub> (|G| = 72) across physical noise rates p &isin; {0.001, 0.002, 0.003, 0.005}. Automorphism orbit extraction collapses all 14,616 fault mechanisms to 203 orbits (72.0&times; parameter collapse). The sub-threshold error-suppression factor &Lambda;<sub>72&rarr;144</sub> = P<sub>L</sub>([[72,12,6]]) / P<sub>L</sub>([[144,12,12]]) increases monotonically below threshold (p<sub>th</sub> &approx; 0.007): &Lambda; = 2.1&times; at p = 0.005 (P<sub>L</sub>: 0.0320 &rarr; 0.0152), 4.4&times; at p = 0.003 (P<sub>L</sub>: 0.0080 &rarr; 0.0018), 6.8&times; at p = 0.002 (P<sub>L</sub>: 0.0028 &rarr; 0.00041), and reaches <b>11.2&times;</b> at p = 0.001 (P<sub>L</sub>: 0.00078 &rarr; 0.00007), directly confirming exponential fault-tolerant distance scaling.</p>

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
                <tr><td><b>Proposed Orbit-Tied QNBP</b></td><td><b>3D Sliding-Window [[72,12,6]] (W=3)</b></td><td><b>AMD XCKU040</b></td><td><b>0 (6-bit CSD)</b></td><td><b>1,226&ndash;28,204 LUTs</b></td><td><b>102.4 ns (mean) / 240 ns (max)</b></td><td><b>75.6% (P<sub>pipe</sub> = 1.9&times;10<sup>-4</sup>)</b></td></tr>
            </tbody>
        </table>
        <p class="noindent">Table V compares our proposed Orbit-Tied QNBP against state-of-the-art QLDPC hardware decoders. While Maurer et al. [12] implemented 3D window decoding on a massive AMD VU19P FPGA requiring ~450,000 LUTs (&gt;50% of the device) without fast/slow path gating, and B&aacute;scones et al. (GARI) [48] rely on a resource-intensive multi-core VCU19P architecture with speculative retries, our architecture fits comfortably on a modest AMD UltraScale+ XCKU040 FPGA (consuming 1,226 to 28,204 LUTs, 0.51% to 11.64% device capacity) with strictly zero DSP slices. Furthermore, our Gate G<sub>3</sub> confidence margin filter routes 75.6% of windows to the 102.4 ns mean latency FPGA fast path with zero logical errors, resolving sliding-window queue backlog under a 1 &mu;s quantum cycle budget. In contrast, GPU batch decoders such as Cascade [49] incur 12.4 &mu;s latency, exceeding real-time coherence deadlines by over 12&times;.</p>

        <h3>B. AXI-Stream Streaming Integration</h3>
        <p class="noindent">The synthesizeable test harness (rtl/streaming_axi_harness.sv) demonstrates continuous streaming operation. Syndrome frames are ingested via an AXI4-Stream slave interface into an asynchronous FIFO. The decoding core processes windows with a deterministic worst-case latency of 240 ns, updates residual registers, and outputs committed fault corrections via an AXI-Stream master interface, providing a direct plug-and-play solution for FPGA-based quantum control stacks.</p>

        <h2>X. Conclusion</h2>
        <p class="noindent">We have presented an orbit-tied, 6-bit quantized neural belief propagation decoder for gross bivariate-bicycle codes. By exploiting torus automorphisms, we collapsed parameter counts by 36&times; on [[72,12,6]] and 72&times; on [[144,12,12]], eliminated untied overfitting, and realized multiplier-free execution with zero DSP slices. Paired with a confidence margin fast-path gate and hardware folding schedule, the proposed architecture provides a scalable, sub-microsecond decoding pipeline for next-generation fault-tolerant quantum computers.</p>

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
