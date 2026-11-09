# Findings & Architectural Decisions

## 1. Mathematical Definitions of Primary Codes

From Bravyi et al. (Nature 2024, Table 3):
- **Polynomial definitions:**
  $$A(x, y) = x^3 + y + y^2$$
  $$B(x, y) = y^3 + x + x^2$$
- **Primary Main Evaluation Code:** $[[72, 12, 6]]$
  - Parameters: $\ell = 6, m = 6$, $n = 2\ell m = 72$, $k = 12, d = 6$.
  - Torus translation group $G = \mathbb{Z}_6 \times \mathbb{Z}_6$, order $|G| = 36$.
  - Check matrices:
    $$H_X = [A, B], \quad H_Z = [B^T, A^T]$$
  - Each check node has degree 6 (3 ones in $A$, 3 ones in $B$).
  - Each data qubit participates in 6 checks (3 $X$ checks from $A, B$, 3 $Z$ checks from $B^T, A^T$).
- **Scaling Gross Code:** $[[144, 12, 12]]$
  - Parameters: $\ell = 12, m = 6$, $n = 2\ell m = 144$, $k = 12, d = 12$.
  - Torus translation group $G = \mathbb{Z}_{12} \times \mathbb{Z}_6$, order $|G| = 72$.
  - Identical polynomials $A, B$.

---

## 2. Literature Discoveries & Prior-Art Grounding

### Müller et al. (Relay-BP, arXiv:2506.01779)
- Confirmed: Memory damping update is $\Lambda_j(t) = (1 - \gamma_j)\Lambda_j(0) + \gamma_j M_j(t-1)$.
- Crucial confirmation: Negative memory strengths ($\gamma_j < 0$) are indispensable to escape symmetric trapping sets and dampen oscillatory limit cycles.
- Limitation of Relay-BP: Relies on random sampling over hundreds of relay legs ($R \le 600$). Our QNBP learns compact orbit-tied parameters $\gamma_{o, t}$ directly via end-to-end backpropagation, avoiding random searches.

### Maurer et al. (FPGA Gross Code Decoder, arXiv:2510.21600)
- Confirmed: Integer quantization at **int4 (4-bit)** achieves identical logical error rates to 32-bit floating-point for split X/Z decoding on the $[[144, 12, 12]]$ gross code.
- Fully parallel execution completes 1 BP iteration in 2 clock cycles (24 ns at 83 MHz on AMD VU19P).
- Our advantage: We achieve multiplier-free hardware using power-of-two learned scaling and orbit-tying, reducing parameter storage by $36\times$ or $72\times$.

### Keyi Yin et al. (SymBreak, arXiv:2412.02885)
- Explores degeneracy-induced symmetric traps in QLDPC codes and demonstrates that symmetry perturbation or noise injection helps escape traps. Our boundary class weights and signed memory achieve symmetry handling systematically.

---

## 3. Sliding-Window Architecture & Gating Rules

- Sliding window parameters: width $W \in \{3, 5, 6\}$ syndrome rounds, commit stride $F \in \{1, 2\}$ rounds.
- Fast-Path Margin Gating:
  - **G1**: Soft syndrome parity matches observed syndrome ($\hat{s}_c = s_c$ for all checks).
  - **G2**: G1, and the minimum absolute LLR among all flipped candidate faults $\min_{v: \hat{e}_v=1} |\Lambda_v| \ge \tau$.
  - **G3**: G1, and for each logical observable $k$, the minimum absolute LLR among committed faults supporting observable $k$ exceeds threshold $\tau$:
    $$\min_{v \in O_k, \hat{e}_v=1} |\Lambda_v| \ge \tau$$
  - Threshold $\tau$ is calibrated on validation shots to ensure zero statistically significant degradation vs. fallback alone.

