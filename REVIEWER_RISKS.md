# REVIEWER_RISKS.md — Defense & Answers to the 15 Hardest Reviewer Questions

**Target Venue:** *IEEE Transactions on Quantum Engineering (IEEE TQE)*  
**Document Purpose:** Pre-emptively provides exhaustive, mathematically rigorous, and empirically validated answers to the 15 most challenging, critical, and skeptical peer-review questions.

---

### Q1: *How does your decoder compare to IBM's full Relay-BP ($P_L=0.0060$)? Why didn't you declare IBM Relay-BP the winner if its error rate is lower?*
**Response:**  
We evaluate IBM Relay-BP under two distinct operational paradigms in Table IV:
1. **Hardware-Capped Real-Time Regime ($t_{\text{dec}} \le 1.0\,\mu\text{s}$ Deadline):** When constrained to 5 relay legs ($\le 50$ iterations, $454.4\text{ ns}$ execution latency), IBM Relay-BP attains $P_L = 0.0090$ [0.0073, 0.0111]. Proposed Orbit-Tied QNBP achieves $P_L = 0.0068$ [0.0053, 0.0086] in an average of only $6.4$ iterations ($102.4\text{ ns}$ mean latency), attaining a statistically significant superiority over capped Relay-BP ($\chi^2 = 12.06, p = 0.000515 < 0.001$, McNemar test).
2. **Unconstrained Offline/Software Regime ($t_{\text{dec}} > 1.0\,\mu\text{s}$):** While full 300-leg Relay-BP achieves $P_L = 0.0060$, it requires an average of **148.5 iterations** (with up to 24,000 max iterations across 300 legs), consuming $2.38\,\mu\text{s}$ in optimized C++ and $>27\,\text{ms}$ in Python. This exceeds the $1.0\,\mu\text{s}$ coherence deadline of superconducting transmons by $2.4\times$ to $27,000\times$. For real-time fault-tolerant decoding, latency-matched comparison is paramount; our architecture delivers $23.2\times$ faster convergence ($6.4$ vs. $148.5$ iters) and fits directly onto an AMD FPGA with strictly zero DSP slices.

---

### Q2: *Your Normalized Min-Sum baseline ($\alpha=0.75$) performed drastically worse ($P_L=0.4160$) than unweighted Min-Sum ($P_L=0.2940$). Isn't Normalized Min-Sum supposed to improve over unweighted BP?*
**Response:**  
Heuristic uniform attenuation $\alpha = 0.75$ was derived by Chen & Fossorier (2002) for *classical* LDPC codes, where parity-check matrices are ultra-sparse, lack short cycles of length 4, and check degrees vary widely. Under classical sparse graphs, $\alpha < 1.0$ mitigates LLR over-confidence.  
However, on *quantum* bivariate-bicycle codes:
1. Bipartite Tanner graphs possess short girth-6 cycles and dense check degree ($d_c = 6$).
2. A comprehensive grid sweep across $\alpha \in \{0.5, 0.625, 0.75, 0.875, 1.0\}$ and iteration budgets $I \in \{15, 30, 50\}$ on 500 held-out Stim shots (`results/min_sum_tuning.json`) revealed that unweighted Min-Sum ($\alpha^* = 1.0, I^* = 50$) achieves the optimum among uniform scalings ($P_L = 0.2220$), whereas uniform attenuation $\alpha = 0.75$ degrades decoding ($P_L = 0.4180$).
3. Uniform attenuation prematurely suppresses marginal syndrome messages and traps belief propagation in symmetric limit cycles. In contrast, our learned Orbit-Tied QNBP assigns distinct *per-orbit* scaling factors $\alpha_{o,t}$ and signed memory damping $\gamma_{o,t}$, breaking symmetric trapping sets without premature integer attenuation.

---

### Q3: *Why does GDG Sliding Window [13] yield the exact same error rate ($0.4160$) as Normalized Min-Sum? Was it just an identical duplicate?*
**Response:**  
GDG Sliding Window (Gong et al., 2024) executes normalized Min-Sum BP across continuous syndrome frames, relying on inter-window boundary residual propagation ($s_{\text{res}}^{(k+1)} = s_{\text{raw}}^{(k+1)} \oplus H_{\text{boundary}} \hat{e}^{(k)}$) to resolve temporal boundary faults.  
When benchmarked on an *isolated, single-window frame* without inter-window residual feedback, the sliding-window engine mathematically reduces to single-window Normalized Min-Sum with $\alpha = 0.75$. We have explicitly documented this equivalence in Section VIII-A, Table IV, and `results/competitor_benchmarks.json` to ensure transparent architectural reporting.

---

### Q4: *In earlier drafts, $P_{\text{pipe}}$ was reported as $1.90\times 10^{-4}$ at $p=0.003$. Now it is $1.90\times 10^{-3}$. What explains this $10\times$ difference?*
**Response:**  
The preliminary draft inadvertently cited $P_{\text{pipe}} = 1.90\times 10^{-4}$ from preliminary sub-threshold evaluations at $p = 0.001$.  
At physical noise rate $p = 0.003$, Gate $G_3$ ($\tau = 1.5$) rejects $p_{\text{fb}} = 0.244$ ($24.4\%$) of windows. Given that $P(\text{err} \mid \text{accepted}) = 0.0$ and fallback error rate is $P(\text{err} \mid \text{fallback}) = 0.0078$, the exact law of total probability gives:
$$P_{\text{pipe}} = (1 - p_{\text{fb}}) \cdot 0 + p_{\text{fb}} \cdot P(\text{err} \mid \text{fallback}) = 0.244 \times 0.0078 = \mathbf{1.9032 \times 10^{-3}}.$$
At sub-threshold noise $p = 0.001$, fallback rejection drops to $p_{\text{fb}} = 0.009$ ($0.9\%$) with fallback error $7.78\times 10^{-4}$, yielding:
$$P_{\text{pipe}} = (1 - 0.009) \cdot 0 + 0.009 \times 7.78\times 10^{-4} = \mathbf{7.00 \times 10^{-6}}.$$
Both operational points are now completely unmixed, explicitly defined, and synchronized across the manuscript, tables, and code.

---

### Q5: *You claim zero accepted errors on the fast path ($P_{L,\text{accept}} = 0.0000$). How can you claim zero errors on a finite Monte Carlo sample?*
**Response:**  
We do not claim zero errors as an infinite-sample certainty; we report zero observed errors over $N_{\text{acc}} = 37,800$ accepted Monte Carlo shots ($0 / 37,800$), which establishes an exact one-sided **95% Clopper-Pearson statistical upper bound** of:
$$P_{L, \text{accept}} \le 1 - (1 - 0.95)^{1/37800} = \mathbf{7.92 \times 10^{-5}},$$
and a 95% Wilson score upper bound of $1.02\times 10^{-4}$. All occurrences in the Abstract, Section VI-B, and Table IV state this exact statistical bound.

---

### Q6: *In sliding-window decoding, window $k+1$ depends on committed boundary corrections of window $k$. If window $k$ routes to fallback and takes hundreds of microseconds, how can the stream avoid stalling and overflowing the queue?*
**Response:**  
We evaluated this exact inter-window dependency in our discrete-event simulation (`scripts/evaluate_gating_and_queue.py`, `results/gating_results.json`):
1. **Policy B (Stream Stall):** If the FPGA fast path stalls waiting for software fallback, queue divergence is guaranteed at $p=0.003$ because $p_{\text{fb}} = 24.4\% \gg p_{\text{crit}} \approx 0.28\%$, leading to $100\%$ buffer overflow.
2. **Policy A (Speculative Fast Path):** When window $k$ routes to fallback, the FPGA does not stall; it speculatively decodes window $k+1$ using tentative correction $\hat{e}_{\text{fast}}^{(k)}$. Because tentative fast-path decisions agree with fallback on $>99.2\%$ of rejected windows, mis-speculation occurs in only $0.205\%$ of windows (41 rollbacks / 20,000 windows). In the rare event of a rollback, window $k+1$ is flushed and re-decoded, driving buffer overflow to **0.00%** across all buffer depths $B \ge 4$ under a $1.0\,\mu\text{s}$ quantum cycle budget.

---

### Q7: *Stim depth-7 depolarizing noise produces raw prior LLRs up to $8.52$. Your 6-bit grid only covers $[-7.75, +7.75]$. Don't raw priors clip?*
**Response:**  
Unscaled raw priors under Stim depth-7 depolarizing noise indeed range from $4.6435$ to $8.5156$, which would clip $67.49\%$ of fault priors on a $[-7.75, +7.75]$ grid.  
However, as proven in Lemma 1 and verified in `scripts/verify_quant_clipping.py`:
- We apply dyadic pre-scaling $\kappa = 0.75 = 1 - 2^{-2}$, implemented in hardware using a single shift-and-subtract operation with zero multipliers.
- Dyadic scaling strictly contracts all fault mechanism priors into $[3.4827, 6.3867]$.
- Evaluated across 10,000 shots ($73,080,000$ prior evaluations), scaled priors achieve **100.0000% coverage**, **0.0000% clipping**, and maintain a positive saturation safety headroom margin of $\delta = 1.3633$ ($+17.59\%$).

---

### Q8: *Are the 203 orbits guaranteed to be exact automorphisms under Stim circuit fault propagation, or is this an approximation?*
**Response:**  
They are **exact mathematical graph automorphisms**.  
In Proposition 1, we prove that because bivariate-bicycle codes are defined over quotient polynomial rings $\mathcal{R} = \mathbb{F}_2[x, y] / \langle x^\ell - 1, y^m - 1 \rangle$, 2D torus translations $T_{(\delta_x, \delta_y)} \in \mathbb{Z}_\ell \times \mathbb{Z}_m$ preserve polynomial monomial adjacency, CNOT gate connectivity, detector schedules, and prior probabilities.  
To empirically verify this, `scripts/verify_automorphism_orbits.py` evaluated **263,088 group action operations** across all 36 group elements on $[[72,12,6]]$, demonstrating **0 closure violations, 0 probability violations, and 0 topological mismatches**, confirming all 203 orbits have an exact uniform size of 36.

---

### Q9: *Why does dephasing noise bias ($\eta=100$) improve logical error rate by $8.0\times$? Doesn't Classical BP also improve under biased noise?*
**Response:**  
Yes, Classical BP error rate also drops as noise becomes biased because the channel entropy decreases.  
However, as demonstrated in Table I:
- Proposed Orbit-Tied QNBP maintains a **$20.0\times$ advantage** over Classical BP at $\eta = 100$ ($P_L = 0.0010$ vs. $0.0200$) and a **$6.0\times$ advantage** over Tuned Min-Sum ($P_L = 0.0010$ vs. $0.0060$).
- In Proposition 3, we prove that in CSS codes, physical $Z$-errors are detected exclusively by $X$-checks. As $\eta \to \infty$, $Z$-check syndrome excitation vanishes as $\mathcal{O}(p/\eta)$, allowing the QNBP message-passing engine to decouple onto the $X$-check Tanner graph without inter-sector crosstalk.

---

### Q10: *Does your RTL in `rtl/` synthesize the entire 7,308-fault DEM, or is it a bipartite syndrome projection?*
**Response:**  
The synthesizeable SystemVerilog RTL in `rtl/` implements the **216-VNU Bipartite Syndrome-Projection Architecture** (`vnu.sv`, `cnu.sv`, `g3_gate.sv`, and `streaming_axi_harness.sv`):
- It instantiates $72 \text{ data qubits} \times 3 \text{ rounds} = 216$ physical VNUs and 216 CNUs.
- Detector-neighborhood collinear DEM hyperedges are aggregated into 216 composite variable nodes with composite priors $L_v^{(0)} = \sum_{f \in \mathcal{F}_v} \ln((1 - p_f)/p_f)$.
- The 203-orbit full-DEM architecture (31,800 LUTs) is an analytical design alternative. We have explicitly distinguished these two scopes in Section VII-A and Table V.

---

### Q11: *Where are the Vivado place-and-route timing and power reports supporting $\text{WNS} = +0.18\text{ ns}$ and $184\text{ mW}$?*
**Response:**  
We have audited and updated all hardware claims:
- The resource count of 28,204 LUTs is derived from bottom-up module sizing of synthesized processing units ($216 \times 48\text{ VNU} + 216 \times 82\text{ CNU} + 124\text{ gate} = 28,204\text{ LUTs}$, $19,512\text{ FFs}$, $0\text{ DSP}$, $0\text{ BRAM}$).
- Unverified claims of "post-place-and-route Worst Negative Slack WNS = +0.18 ns" have been removed from the manuscript and README, and softened to: *"Estimated synthesis timing indicates operation up to $250\text{ MHz}$ ($4.0\text{ ns}$ clock period), with analytical dynamic power estimated at $\sim 184\text{ mW}$ based on switching activity models."*
- The complete batch Vivado implementation script (`rtl/synth_xcku040.tcl`) is committed and documented in `TODO_HUMAN.md` for external replication.

---

### Q12: *How does your hardware scale to the gross code $[[144, 12, 12]]$? Did you synthesize the 432-VNU core?*
**Response:**  
In Table V and Section IX, the $[[144, 12, 12]]$ hardware numbers are explicitly labeled as **"Proposed 432-VNU Core (Projected)"** with **"$\sim 56,400$ LUTs (Projected / un-synthesized)"**.  
The logic count is projected from individual processing units ($432 \times 48\text{ VNU} + 432 \times 82\text{ CNU} + 124\text{ gate} \approx 56,400\text{ LUTs}$), which occupies $23.3\%$ of AMD XCKU040 logic. We do not claim an implemented top-level bitstream for the 144-qubit gross code.

---

### Q13: *Why did your IBM Heron r2 calibration benchmark have such wide confidence intervals?*
**Response:**  
The preliminary benchmark in `results/realworld_benchmarks.json` evaluated 250 shots under the empirical calibration profile of IBM Quantum Heron r2 ($p_{\text{2Q}} = 2.1\times 10^{-3}, \eta=50, p_{\text{RO}} = 8.0\times 10^{-3}$), observing 1 error ($P_L = 0.0040$ [0.0007, 0.0223]).  
We explicitly report this sample size in Section VIII-B and highlight in `TODO_HUMAN.md` that high-statistics verification with $N \ge 10^5$ shots is required to narrow the confidence intervals. Furthermore, we clarify in Section VIII-B that this represents a circuit-level Stim simulation parameterized by Heron calibration data, not physical execution on IBM cloud QPUs.

---

### Q14: *How does your work differ from Wang et al.'s approximately equivariant networks and Liang et al.'s planar neural decoders?*
**Response:**  
In Section II-D, we provide an explicit comparative positioning:
1. **Wang et al. (2022):** Formulated approximate equivariance for continuous or imperfect geometric symmetries. Our approach exploits *exact*, discrete group automorphisms $G = \mathbb{Z}_\ell \times \mathbb{Z}_m$ over dual-cyclic quotient rings on the 2D torus, guaranteeing 100% mathematical closure and equivariance (Proposition 2) without approximation error.
2. **Liang et al. (2025):** Designed planar neural decoders for 2D topological surface and color codes with nearest-neighbor grid boundaries. Planar architectures cannot accommodate the non-local bipartite check connectivity, high node degrees ($d_v=6, d_c=6$), and 3D space-time detector error models characteristic of gross bivariate-bicycle QLDPC codes.

---

### Q15: *Can this decoder run on physical transmon quantum processors with spatially non-uniform, drifting noise and crosstalk?*
**Response:**  
Yes. In Section VI-C and Section IX-C, we evaluated drift robustness:
- Out-of-sample channel drift tests across $\pm 20\%$ channel-prior variation maintain $<4\%$ relative deviation in logical error rate without retraining.
- Under $ZZ$ crosstalk ($\epsilon = 0.10$), QNBP suppresses logical errors by $22.1\times$ over Classical BP ($0.0014$ vs. $0.0310$).
- As noted in our "Limitations and Threats to Validity" section, extreme localized "hot qubit" defects on physical QPUs can be addressed by localized prior re-tuning using our modular CSD prior registers.
