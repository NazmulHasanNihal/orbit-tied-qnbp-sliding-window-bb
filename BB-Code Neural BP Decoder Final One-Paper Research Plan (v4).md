# BB-Code Neural BP Decoder: Final One-Paper Research Plan (v4)

Nov 5, 2026 · @Nazmul Hasan Nihal

## 1. Verdict and final form

This is the strongest defensible version of the project: one paper, three testable claims, and hardware results scoped to what you can actually produce. It is rated 8.0/10 as a plan, not 10/10, because that score can only be earned by results, and no one can certify "100% novelty" in a field where several groups publish monthly.

| Dimension | Score now | What lifts it |
| --- | --- | --- |
| Idea and venue fit | 8.5 | Clear gap: trained, symmetry-tied, multiplier-free BP for BB codes |
| Novelty (as a combination) | 8 | Re-run the prior-art search before submission; individual pieces are partly covered (section 2) |
| Feasibility with your resources | 7 | Cut the PyPI package, the board-level verification and the second paper |
| Evidence readiness | open | Checkpoints 1 to 3 in section 9 decide this |

**Final form.** One journal paper of about 12 to 14 pages, target IEEE Transactions on Quantum Engineering, with Quantum Science and Technology as backup. It ships with a public GitHub repository containing the Stim-to-graph bridge, training code, fixed-point reference model, RTL and synthesis reports.

**What the paper can honestly say if the experiments work:** a trained decoder with a few dozen to a few hundred parameters, run in 3 to 5 bit shift-and-add arithmetic, that matches or beats tuned min-sum BP on the \[\[72,12,6\]\] and \[\[144,12,12\]\] codes, with a measured fast-path and fallback split.

**What it must not say:** zero logical degradation on the fast path, 100% novelty, sub-500 ns latency, or hardware-in-the-loop validation, unless measurements back each one.

## 2. Prior-art map (searched 5 Nov 2026)

The combination in this plan is still open, but three of its ingredients already exist separately, so the novelty claim must be about the combination, not the parts. I worked from search results and did not read each paper in full, so verify details before citing.

| Work | What it does | Overlap with this plan | What stays open |
| --- | --- | --- | --- |
| [Relay-BP, Müller et al.](https://arxiv.org/abs/2506.01779) | Disordered memory strengths; beats BP+OSD+CS-10 on BB codes; argued real-time on FPGA | Main accuracy baseline; memory-strength idea | Strengths are sampled, not learned or orbit-tied |
| [FPGA Relay-BP, Maurer et al.](https://arxiv.org/abs/2510.21600) | Gross-code FPGA decoder, 24 ns per BP iteration, 4 to 6 bit integers match float | Low-bit integer BP on FPGA already exists | Learned scales, shift-add only, orbit-tied parameters |
| [FPGA-tailored algorithms](https://arxiv.org/pdf/2511.21660) | Latency-tail analysis of Relay on gross and two-gross codes | Real-time tail model | Fast-path gate plus trace-driven queue with fallback pool |
| [Scalable neural decoders](https://arxiv.org/html/2604.08358v1) | Translation-equivariant convolutions; notes BB codes have torus symmetry | Equivariance on BB codes as a concept | It is a GPU network, not NBP, not quantized, no FPGA |
| [ML decoding for BB codes, Blue et al.](https://arxiv.org/pdf/2504.13043) | Recurrent transformer, circuit-level, \[\[72,12,6\]\] | Neural decoding of BB circuit noise | Heavy model, GPU only |
| [Neural BP, Liu and Poulin](https://www.researchgate.net/publication/333307424_Neural_Belief-Propagation_Decoders_for_Quantum_Error-Correcting_Codes) and a [Harvard thesis](https://dash.harvard.edu/items/78dcef0b-782d-43e9-bf9b-a630fc7c8057) | NBP concept; thesis reports difficulty reaching a threshold on BB codes | Plain NBP baseline | Tying, quantization, windowed circuit-level BB |
| [Gong et al., GDG sliding window](https://arxiv.org/abs/2403.18901) and [QUITS](https://arxiv.org/pdf/2504.02673) | Window framework and Stim circuit builders for BB codes | Infrastructure and baselines | None needed; reuse them |
| [Graph neural post-selection](https://arxiv.org/pdf/2610.00504) and [BP convergence prediction](https://arxiv.org/html/2604.07995) | Predict decoder failure or BP convergence on BB codes | Confidence-gating idea | Our gate is on-chip, from LLR margin, with no extra network |
| [Approximately equivariant networks, Wang et al.](https://proceedings.mlr.press/v162/wang22aa/wang22aa.pdf) | Relaxed weight tying beats strict tying when symmetry is imperfect | Justifies boundary classes | None |

**Corrections to plan v3**

1. "FPGA prior art uses no quantization" is wrong. Maurer et al. report 4 to 6 bit integer BP that matches floating point. Your claim becomes: learned, power-of-two scales with shift-add arithmetic and tied parameters.
2. "Signed memory strengths" may not be new. Relay-BP already uses disordered memory strengths, and I believe its range includes negative values; check the paper before claiming. Reframe as learned, orbit-tied strengths.
3. I could not find Cascade (ICML 2026), GraphQEC, QuBA, AutDEC or SymBreak in my searches. Confirm each exists and what it does before they appear in your prior-art memo.
4. The "proof of queue stability" is a standard utilization condition. Present it as a measured, trace-driven model, not a theorem.
5. The code labels "\[\[14, 23, 24\]\]" and "\[\[24, 25\]\]" are garbled. Use \[\[72,12,6\]\] and \[\[144,12,12\]\].

**The defensible novelty** is the combination of three things: orbit-tied unfolded BP trained end-to-end on windowed circuit-level DEMs of BB codes; power-of-two quantization trained in the loop so inference needs no multipliers; and a margin-gated fast path with measured fallback and queueing. Re-run this search the week you submit.

## 3. Research question and contributions

**Research question.** Can a belief-propagation decoder whose parameters are tied across the translation orbits of a bivariate-bicycle code, and quantized to power-of-two scales, match or beat tuned min-sum BP and approach Relay-BP on circuit-level noise, using far fewer parameters and no multipliers?

Each contribution below has a pass test written before any experiment, so the results cannot be argued into a win afterwards. The thresholds are proposed starting values; adjust them once, at the Checkpoint 0 review, then freeze them.

| Claim | Pass test (proposed) | If it fails |
| --- | --- | --- |
| C1. Orbit-tied unfolded BP with window boundary classes | Beats the best tuned normalized min-sum by at least 20% in logical error rate per round, or matches untied NBP with at least 10x fewer parameters, on \[\[72,12,6\]\] at p between 0.002 and 0.003; and beats the random-tying control A5 | Report it as a negative result on symmetry; keep C2 and C3 as an efficiency paper |
| C2. Power-of-two quantization, no multipliers | 4-bit model within 10% relative logical error of the float tied model; the inference graph contains only shifts, adds, compares | Raise to 5 or 6 bits (Maurer et al. show 4 to 6 bits work for plain BP) and report the cost |
| C3. Margin-gated fast path with measured fallback | Fast path accepts at least 80% of windows at p = 0.001; error rate among accepted windows reported with a 95% interval and not worse than the fallback decoder alone by more than the interval; queue stays stable at measured service times | Report the achieved acceptance rate and the trade-off curve; drop the numeric target, keep the analysis |

**Fallback framing.** If C1 does not beat Relay-BP, the paper becomes an efficiency paper: comparable logical error rate at a fraction of the parameters and logic resources. That is still publishable at TQE or QST, provided the comparison is fair and the numbers are measured.

**Non-goals.** No new code family, no second paper, no claim of board-level hardware validation, no general-purpose Python package beyond the repository.

## 4. Experimental setup

Everything runs on Stim circuit-level simulations of two codes, with a fixed protocol so every decoder sees identical shots.

| Item | Choice |
| --- | --- |
| Codes | \[\[72,12,6\]\] (l=6, m=6, torus group of 36 shifts) as the main code; \[\[144,12,12\]\] gross code (l=12, m=6, 72 shifts) for the scaling result |
| Circuit | Bravyi et al. syndrome-extraction circuit built in Stim; start from the circuit builders in [Gong et al.](https://github.com/gongaa/SlidingWindowDecoder) or [QUITS](https://arxiv.org/pdf/2504.02673) and check detector counts against your own DEM |
| Noise | Uniform circuit-level depolarizing at p = 0.001, 0.002, 0.003, 0.005; a second noise model only if time allows |
| Windows | Sweep width W in {3, 5, 6} and commit stride F in {1, 2}; pick one setting for hardware after the sweep |
| Decoding split | X and Z decoded separately first, as Maurer et al. do; joint XYZ only as an extension |
| Iterations | T in {10, 20, 30, 50}, with every decoder compared at equal T and equal window |
| Data | Stim-sampled shots at a mix of p; separate seeds for train, validation and test; the syndrome loss needs no labels, the observable loss uses Stim's logical flips |
| Statistics | Run each test point until 100 logical failures or a shot cap; report 95% intervals; never plot a point below 20 failures |

**Baselines.**

- B0: floating-point unweighted min-sum BP.
- B1: normalized min-sum with the scale tuned per iteration on the validation set. This is the baseline a reviewer will push hardest, so tune it properly.
- Relay-BP using IBM's reference implementation, and BP+OSD with combination sweep 10 using the `ldpc` package.
- GDG sliding-window decoding from Gong et al.
- Neural decoders such as Blue et al. only where noise model and metric match exactly; otherwise cite, do not plot.

**Metrics.** Logical error rate per round after window commits; parameter count and bits per parameter; fast-path acceptance rate; error rate among accepted windows; iterations-to-converge histogram; LUT, FF, BRAM and DSP counts; Fmax and cycles per iteration.

**Size check before anything else.** One third-party repository reports a 12-round gross-code memory with 1728 detectors and 67,752 error mechanisms. Confirm this from your own DEM, then compute the node and edge counts of one window. That decides whether the hardware design is fully parallel or folded across orbits (section 7).

**Compute assumption.** A Ryzen-class desktop for Stim sampling and small-model training, plus free cloud GPU hours when needed. Orbit-tied models have so few parameters that training on CPU is workable, but sampling millions of shots is the real cost, so budget it in week 2.

## 5. Method

The decoder has four parts: a tied unfolded BP core, a trainable loss, quantization trained in the loop, and a gated fast path with fallback.

### 5.1 Orbit-tied unfolded BP

Run T unfolded iterations of normalized min-sum with memory on the window's detector error model (DEM) graph. Variable nodes are faults, check nodes are detectors, and a positive log-likelihood ratio means no error.

```latex
\Lambda_v^{(t)} = (1-\gamma_{o(v),t})\,\lambda_v + \gamma_{o(v),t}\,\Lambda_v^{(t-1)} + \sum_{c \in N(v)} m_{c\to v}^{(t)}
```

```latex
m_{c\to v}^{(t)} = \alpha_{o(c,v),t} \Big(\prod_{v' \in N(c)\setminus v} \operatorname{sign} L_{v'\to c}\Big) \min_{v' \in N(c)\setminus v} \big|L_{v'\to c}\big|, \qquad L_{v\to c} = \Lambda_v^{(t-1)} - m_{c\to v}^{(t-1)}
```

The map o(.) sends each node or edge to its orbit under the shift group G = Z\_l x Z\_m acting on the DEM, refined by the window class (open-left, interior, open-right). Parameters alpha and gamma exist per orbit, class and iteration, so an untied model's parameter count shrinks by up to |G| (36 or 72 here). The memory form above is the usual memory-BP update; match it to the exact definition in Müller et al. when you implement.

1. **Compute the orbits, never assume them.** Apply each shift to the DEM's detectors and faults, and check that priors and observable membership are preserved. Where merged faults or the schedule break a shift, split the orbit and report how many nodes that touched.
2. **Interior rounds share parameters across time.** Open-left and open-right rounds get their own parameters, because the window cut breaks the symmetry there. If strict tying costs accuracy, allow small learned offsets per class, as in [approximately equivariant networks](https://proceedings.mlr.press/v162/wang22aa/wang22aa.pdf).
3. **Keep X and Z decoders separate at first.** Tie across X and Z only as a later experiment.

### 5.2 Loss

Train on the logical outcome, not on matching the sampled error, because degenerate codes accept many valid corrections. The probability that logical observable k is flipped follows from the posteriors:

```latex
q_k = \tfrac{1}{2}\Big(1 - \prod_{v \in O_k} \tanh\tfrac{\Lambda_v}{2}\Big)
```

The product runs over hundreds of faults, so compute its magnitude in the log domain with the stable identity below, and take the sign from the hard decisions with a straight-through gradient.

```latex
\ln\tanh\tfrac{x}{2} = \ln\big(-\operatorname{expm1}(-x)\big) - \operatorname{log1p}\big(e^{-x}\big), \qquad x > 0
```

```latex
\mathcal{L} = \sum_{t} \omega_t \Big[ \sum_{k} \mathrm{BCE}\big(q_k^{(t)}, y_k\big) + \lambda \sum_{c} \mathrm{BCE}\big(\hat{s}_c^{(t)}, s_c\big) \Big]
```

Here y\_k is the true logical flip from Stim, s\_c the observed syndrome bit, and s-hat\_c the soft parity of check c computed the same way as q\_k. Weights omega\_t grow with t, so every iteration is supervised and gradients do not vanish. Ablation A6 compares this against the softplus parity loss of Liu and Poulin.

### 5.3 Quantization with power-of-two scales

```latex
x_q = \operatorname{clip}\big(\operatorname{round}(x/\Delta),\, -(2^{k-1}-1),\, 2^{k-1}-1\big), \qquad \Delta = 2^{-\operatorname{round}(\tilde{b})}
```

- The exponent b-tilde is a continuous trainable value per tensor type and iteration. The forward pass rounds it, the backward pass uses a straight-through gradient.
- Alpha and gamma are projected onto a small table. Start with single terms such as 1 - 2^-a and signed 2^-a, then test two-term canonical signed-digit values (plus or minus 2^-a plus or minus 2^-b) as ablation A7b. Either way a multiply becomes one shift and one add or subtract.
- Train in floating point first, then fine-tune with the bit width stepped down 8, 6, 5, 4, 3.
- Accumulators are wider than messages (start at k + 3 bits, with saturation). Report both widths.
- Write an integer-only Python reference model and make it bit-exact with the fake-quantized PyTorch forward pass before writing any RTL.

### 5.4 Fast-path gate and fallback

A window is accepted on the fast path when BP converges within T iterations and a confidence test passes. Three gates are compared, so the choice is evidence, not assertion.

| Gate | Accept when | Why test it |
| --- | --- | --- |
| G1 | Syndrome is matched | Baseline: cheapest, but can accept a valid-syndrome logical flip |
| G2 | G1, and the smallest absolute LLR among faults hard-decided as flipped is at least tau | Cheap filter on weakly supported corrections |
| G3 | G1, and for every logical observable the smallest absolute LLR among committed faults touching it is at least tau | Targets exactly the logical-flip failure; reuses the comparator tree already used by check nodes |

Plan v3 used the minimum over all faults. That will probably reject many correct windows, since weakly informed faults are normal, so keep it only as a control. Tau is calibrated on the validation set to meet an error budget among accepted windows. Rejected windows go to Relay-BP or BP+OSD.

One structural fact shapes the hardware model: window k+1's input depends on the corrections committed by window k. A slow window therefore delays its successors, which section 7 models explicitly.

## 6. Experiment ladder and ablations

Eleven experiments, each isolating one design choice, so every gain in the paper can be traced to a single cause. Nine are core, two are extensions to drop first if time runs short.

| ID | Model or comparison | Question it answers | Priority |
| --- | --- | --- | --- |
| A0 | Floating-point unweighted min-sum | Where does plain BP stand | Core |
| A1 | Normalized min-sum, scale tuned per iteration on validation data | How far does careful classical tuning go; the hardest baseline | Core |
| A2 | Unfolded BP with an independent weight per edge, no tying | What does tying buy; run on \[\[72,12,6\]\], and with per-node weights on the gross code if edge-level is too large | Core |
| A3 | A2 with orbit tying, no boundary classes | Does torus symmetry help | Core |
| A4 | A3 plus window boundary classes | Do the boundary classes help | Core |
| A5 | Random-tying control: same number of groups as A4, assigned at random, at least 5 seeds | Do gains come from symmetry or just from fewer parameters | Core |
| A6 | Loss comparison: log-domain observable plus syndrome loss, softplus parity loss, error-matching BCE | Does the loss matter on high-degree checks | Extension |
| A7 | Quantization: float vs 6, 5, 4, 3 bits; power-of-two vs free LSQ scale; one-term vs two-term CSD weights | What does the multiplier-free constraint cost | Core |
| A8 | Memory strengths: none, sampled as in Relay-BP, learned positive, learned signed | Do learned or signed strengths beat sampled ones | Extension |
| A9 | Gates G1, G2, G3 and the v3 minimum-over-all-faults control | Which gate gives the best acceptance for a given error among accepted | Core |
| A10 | Full pipeline vs Relay-BP, BP+OSD, GDG at equal window and iterations | Is the system competitive end to end | Core |

**Protocol for every row.**

- At least 3 training seeds; report mean and standard deviation across seeds.
- The same held-out Stim shots for every decoder, so comparisons are paired.
- Equal parameter budget when comparing against untied models; equal tuning effort for baselines.
- Publish negative results. If A5 matches A4, the symmetry claim is dead and the paper says so.
- Robustness check: train at p = 0.003, test at 0.001 and 0.005, and report the loss in accuracy.

**Decision table for the headline result.**

| Outcome | What the paper claims |
| --- | --- |
| A4 beats A1 and A5, A7 holds at 4 bits | Full claim C1 + C2 |
| A4 matches A1 with far fewer parameters than A2 | Efficiency claim only |
| A4 does not beat A5 | No symmetry claim; the quantization and gate results carry the paper |
| A10 shows no advantage over Relay-BP in accuracy | Claim resource savings and latency only, if section 7 supports them |

## 7. Hardware and real-time analysis

The hardware results in this paper are simulation and synthesis results, not measurements on a board. Maurer et al. ran on an AMD VU19P with a real-time controller; without a board you cannot claim that, and a reviewer will accept a clearly labeled synthesis study.

### 7.1 What you can produce

1. An integer-only Python reference model, bit-exact with the quantized PyTorch model.
2. SystemVerilog for the variable-node unit, check-node unit and gate, wired into one BP iteration over one window.
3. RTL simulation (Verilator or cocotb) that matches the reference model bit for bit on at least 10,000 shots. Label it RTL simulation, never hardware-in-the-loop.
4. Vivado synthesis and implementation reports: LUT, FF, BRAM, DSP (target 0), Fmax and cycles per iteration.

In week 1, check which FPGA devices your Vivado edition supports. Plan v3 named the XCKU15P, which may need a license you do not have. Pick the largest supported part that fits one window, and compare cost per edge rather than absolute totals, so results stay comparable with larger devices.

### 7.2 Fully parallel or folded

Maurer et al. give every variable and check node its own compute unit and finish one BP iteration in two clock cycles. For a window with thousands of fault nodes that needs a very large device. Because the graph is shift-invariant and parameters are shared per orbit, a folded design can process the |G| shifts in time slots on shared units with address-shifted memory. That trades cycles for logic.

Report a latency-versus-resource curve with fold factors that divide |G|. The folding benefit is a hypothesis until measured, so do not state it in the abstract before the numbers exist.

### 7.3 Latency, measured not promised

Per-window latency is iterations times cycles per iteration divided by Fmax, with the iteration count taken from the simulated histogram. As an illustration only: at Maurer et al.'s 24 ns per iteration and a 1 microsecond syndrome cycle, a stride of F = 2 gives 2000 ns per window, so a single sequential unit has room for about 83 iterations; F = 1 leaves about 41. Your own numbers replace these.

### 7.4 Queueing model

Windows arrive every F x T\_cycle. Window k+1 needs the corrections committed by window k, so a single decoding chain is a sequential queue, not a pool. A fallback window pays for its failed fast attempt as well as the slow decode, which plan v3 left out:

```latex
\mathbb{E}[S] = p_{\text{fast}}\,S_{\text{fast}} + (1-p_{\text{fast}})\big(S_{\text{attempt}} + \mathbb{E}[S_{\text{slow}}]\big) < F \cdot T_{\text{cycle}}
```

This mean condition is necessary, not sufficient: the tail decides whether the buffer overflows, as the [latency-tail analysis of Relay](https://arxiv.org/pdf/2511.21660) shows. Model two cases:

- **Sequential chain.** One decoder per basis; a slow window stalls its successors. Measure backlog and the probability that waiting time exceeds a buffer of B windows.
- **Parallel windows.** A two-layer scheme where non-overlapping windows decode at once, with c fallback servers. Only here does a D/G/c pool apply.

Drive both with a trace-driven simulation: iteration counts from your reference model, converted to time with the stated clock, and Relay-BP iteration counts from its reference implementation under the same assumption. Present the result as a stability region over p\_fast and E\[S\_slow\], and call it a model, not a proof.

## 8. Software artifact, scoped down

Ship one public GitHub repository that regenerates every figure in the paper. A polished PyPI package with a C++ zero-copy bridge costs weeks and adds nothing a reviewer scores, so it moves to after acceptance.

**The repository contains:**

1. A converter from a Stim detector error model to a PyTorch Geometric bipartite graph: detectors, faults, priors, and observable membership per fault.
2. Orbit extraction with a built-in check that fails loudly if a shift is not an automorphism of the DEM. This is the reusable part and the part reviewers can verify.
3. Training and evaluation scripts, the integer-only reference model, the RTL and the Vivado scripts, plus a config file per figure.
4. Pinned package versions, fixed seeds, and a tagged release archived with a DOI (for example on Zenodo).

**Tests that must pass before release:**

- Node and edge counts of the converted graph equal the DEM's detector and fault counts.
- Every claimed orbit survives the shift check, or is split and reported.
- The quantized PyTorch forward pass and the integer reference model agree bit for bit.
- The RTL simulation matches the reference model on 10,000 shots.

Pick a repository name that is free on GitHub and PyPI, and a permissive license after checking the licenses of what you depend on. Do not reuse the name `stim-pyg` until you have confirmed it is available and not misleading about its relation to Stim.

## 9. Timeline with checkpoints

&#91;embedded content: 20-week plan - 5 phases, 5 checkpoints\]

Checkpoint 1, at the end of week 8, decides whether the symmetry claim stands; every later phase adapts to that answer.

| Checkpoint | Pass criterion | If not passed |
| --- | --- | --- |
| 0 (week 3) | Orbit check done on the \[\[72,12,6\]\] DEM; A0, A1, Relay-BP and BP+OSD behave as published within statistical error; Vivado device chosen; section 3 thresholds frozen | Fix the pipeline first. If most nodes fall outside full orbits, switch to approximate tying and say so |
| 1 (week 8) | Pass test for C1 in section 3, including the random-tying control A5 | Reframe as the efficiency paper; skip optional experiments |
| 2 (week 12) | 4-bit model within 10% relative error of float; gate acceptance and error among accepted measured on both codes | Raise to 5 or 6 bits, report the cost, drop the numeric acceptance target |
| 3 (week 17) | RTL matches the reference model on 10,000 shots; DSP count 0; synthesis report complete | Submit with synthesis estimates labeled as estimates; make no timing claims beyond them |
| 4 (week 20) | Every claim in the claim table (section 11) has a figure; prior-art search re-run; baselines re-checked | Slip the date; never submit an unsupported claim |

**Assumptions.** About 15 hours a week; at 8 hours a week plan on 30 or more weeks. Start the introduction, related work and method sections in week 9, in parallel with experiments, so weeks 18 to 20 are for results and polish.

## 10. Risk register

The two risks most likely to hurt are a strong classical baseline and the cost of sampling rare failures. Both are visible in the first eight weeks.

| Risk | Early signal | Response |
| --- | --- | --- |
| The DEM breaks the torus symmetry more than expected | Many nodes fall outside full orbits at Checkpoint 0 | Split orbits, switch to approximate tying with learned per-class offsets, report the fraction of nodes affected |
| Tuned normalized min-sum (A1) is nearly as good as tied NBP | A4 gain under 5% at Checkpoint 1; an existing thesis already reports trouble getting a threshold from simple NBP on BB codes | Add learned memory strengths and per-iteration supervision; if still flat, switch to the efficiency framing |
| Relay-BP wins on accuracy at equal iterations | A10 gap persists after fair tuning | Claim resources and latency, not accuracy; say so in the abstract |
| Quantization costs too much at 3 or 4 bits | A7 gap above 10% at 4 bits | Move to 5 or 6 bits; Maurer et al. show those widths work for plain BP |
| Rare-failure sampling is too expensive | Fewer than 20 failures per point at p = 0.001 after a day of sampling | Base the main curves on p = 0.002 and above; run p = 0.001 only on the fast-path acceptance study, where failures matter less |
| The gate accepts logical flips or rejects too many windows | Error among accepted windows exceeds the budget, or acceptance below 50% | Use G3, recalibrate tau, publish the full trade-off curve instead of one operating point |
| No board, or a license limit, blocks the hardware study | Vivado cannot target the chosen device at Checkpoint 0 | Pick a supported device; label everything as synthesis and simulation |
| A competing paper appears mid-project | Monthly search finds an overlapping preprint; several relevant ones appeared in recent months | Search monthly; post a preprint after Checkpoint 2 to fix priority; reposition on the unique parts |
| Time runs out | Two checkpoints slip by more than 2 weeks | Drop A6 and A8 first, then the gross-code runs, then the folding study |
| Overclaiming in the abstract | A claim with no figure in section 11's claim table | Delete the claim or add the experiment before submission |

## 11. Paper, claims, first week and references

**Working title.** Orbit-Tied, Power-of-Two Quantized Belief Propagation for Sliding-Window Decoding of Bivariate-Bicycle Codes. Change it if the results favor the efficiency framing.

**Venue.** Primary: IEEE Transactions on Quantum Engineering. Backup: Quantum Science and Technology. A hardware-heavy follow-up, if you later have a board, could go to IEEE TCAD. Post a preprint after Checkpoint 2.

**Outline.** Introduction; background on BB codes, the DEM and sliding windows; method (section 5); setup; results with the ablation ladder; hardware and real-time analysis; limitations; conclusion. About 12 to 14 pages plus an appendix.

**Claim table.** Every sentence in the abstract must map to a row here. A row with no figure is deleted.

| Claim in the paper | Evidence required | Figure |
| --- | --- | --- |
| Orbit tying improves accuracy or efficiency | A1 to A4 | F2, F3 |
| The gain comes from symmetry, not from fewer parameters | A5, at least 5 random seeds | F3 |
| A 4-bit power-of-two model nearly matches float | A7 | F4 |
| The fast path accepts a stated share of windows at a stated error | A9, with 95% intervals | F5 |
| Inference needs no multipliers, at a stated logic cost | RTL, Vivado report, DSP count 0 | Table, F6 |
| Decoding keeps up under stated assumptions | Trace-driven queue simulation | F7 |
| The system is competitive with Relay-BP and BP+OSD | A10 at equal window and iterations | F2 |

Figures: F1 pipeline diagram; F2 logical error rate versus p for the main decoders; F3 parameters versus error, with the random-tying distribution; F4 bits versus error; F5 acceptance versus error among accepted; F6 latency versus resources across fold factors; F7 queue stability region.

**First week.**

- [ ] Read Müller et al., Maurer et al., the FPGA-tailored paper, the scalable neural decoder paper and Blue et al. in full. Confirm whether Relay-BP's memory strengths include negative values.
- [ ] Install Stim, sinter, ldpc, PyTorch and PyTorch Geometric. Build the \[\[72,12,6\]\] circuit and record detector and fault counts.
- [ ] Write the orbit check: apply each shift to the DEM and test that priors and observable membership are preserved.
- [ ] Run baselines A0 and A1 at p = 0.003 with a small shot count to test the pipeline.
- [ ] Check which FPGA devices your Vivado edition supports.
- [ ] Draft the claim table and freeze the section 3 thresholds.

I can write the week-1 scripts (circuit build, DEM counts, orbit check) next.

**References.** Taken from search results; open and read each before citing.

- Bravyi et al., high-threshold and low-overhead fault-tolerant quantum memory, Nature 627, 778 (2024).
- Liu and Poulin, [neural belief-propagation decoders for quantum error-correcting codes](https://www.researchgate.net/publication/333307424_Neural_Belief-Propagation_Decoders_for_Quantum_Error-Correcting_Codes) (2019).
- Müller et al., [Improved belief propagation is sufficient for real-time decoding of quantum memory](https://arxiv.org/abs/2506.01779).
- Maurer et al., [Real-time decoding of the gross code memory with FPGAs](https://arxiv.org/abs/2510.21600).
- [FPGA-tailored algorithms for real-time decoding of quantum LDPC codes](https://arxiv.org/pdf/2511.21660).
- Gong, Cammerer and Renes, [Toward low-latency iterative decoding of QLDPC codes under circuit-level noise](https://arxiv.org/abs/2403.18901).
- [QUITS: a modular QLDPC code circuit simulator](https://arxiv.org/pdf/2504.02673).
- Blue et al., [Machine learning decoding of circuit-level noise for bivariate bicycle codes](https://arxiv.org/pdf/2504.13043).
- [Scalable neural decoders for practical fault-tolerant quantum computation](https://arxiv.org/html/2604.08358v1).
- [Graph neural post-selection for quantum error correction](https://arxiv.org/pdf/2610.00504).
- [Belief propagation convergence prediction for bivariate bicycle codes](https://arxiv.org/html/2604.07995).
- [GPU-based parallel BP decoding for quantum LDPC memory](https://arxiv.org/pdf/2610.13879).
- [Improved noisy syndrome decoding of quantum LDPC codes with sliding window](https://arxiv.org/pdf/2311.03307).
- [The END: an equivariant neural decoder for quantum error correction](https://arxiv.org/pdf/2304.07362).
- Wang et al., [Approximately equivariant networks for imperfectly symmetric dynamics](https://proceedings.mlr.press/v162/wang22aa/wang22aa.pdf), ICML 2022.
