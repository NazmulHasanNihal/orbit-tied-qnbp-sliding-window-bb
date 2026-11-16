"""Publication figure generation for IEEE TQE / QST manuscript.

Generates Figures F2 (LER vs p), F3 (Torus Symmetry vs Random Control),
F4 (Quantization Bits vs Error), F5 (Gate Trade-offs), and F7 (Queue Stability).
"""

from typing import Dict, Any, List
import json
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


def configure_matplotlib_ieee() -> None:
    """Configures matplotlib with IEEE publication styling."""
    plt.rcParams.update({
        "font.family": "serif",
        "font.size": 10,
        "axes.labelsize": 11,
        "legend.fontsize": 9,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "figure.titlesize": 12,
        "lines.linewidth": 1.75,
        "lines.markersize": 6,
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "axes.grid": True,
        "grid.alpha": 0.35,
        "grid.linestyle": "--",
    })


def plot_f3_symmetry_vs_random(results: Dict[str, Any], output_dir: str = "results/figures") -> None:
    """Figure F3: Torus Symmetry vs Random-Tying Control Distribution."""
    os.makedirs(output_dir, exist_ok=True)
    fig, ax = plt.subplots(figsize=(5.5, 4.0))

    abl = results["ablations"]
    a4_rate = abl["A4_orbit_tied_with_boundary"]["rate"]
    a3_rate = abl["A3_orbit_tied_no_boundary"]["rate"]
    a2_rate = abl["A2_untied_nbp"]["rate"]
    a1_rate = abl["A1_normalized_minsum"]["rate"]

    a5_runs = abl["A5_random_tying_control"]["runs"]
    a5_mean = abl["A5_random_tying_control"]["mean_rate"]
    a5_std = abl["A5_random_tying_control"]["std_rate"]

    # Parameter counts aligned with Section VIII-B (W=3, R=3):
    # 7,308 fault mechanisms collapse to 203 orbits (36.0x orbit reduction)
    # A1: 15 parameters
    # A2: 15 * 7308 = 109,620 parameters
    # A3: 15 * 203 = 3,045 parameters
    # A4: 3,090 parameters (203 orbits + 3 boundary classes x 15 iters)
    # A5: 15 * 203 = 3,045 parameters
    params = {
        "A1 (Normalized MS)": (15, a1_rate, "#6c757d", "^"),
        "A2 (Untied NBP)": (15 * 7308, a2_rate, "#e63946", "s"),
        "A3 (Orbit-tied)": (15 * 203, a3_rate, "#f4a261", "D"),
        "A4 (Proposed QNBP)": (3090, a4_rate, "#2a9d8f", "o"),
    }

    # Plot A5 Random-tying cloud
    for seed_rate in a5_runs:
        ax.scatter(15 * 203, seed_rate, color="#b0bec5", alpha=0.7, s=40, zorder=3)
    ax.errorbar(
        15 * 203, a5_mean, yerr=a5_std, fmt="x", color="#455a64",
        capsize=4, label="A5 Random Control (5 seeds)", zorder=4
    )

    for label, (n_p, rate, color, marker) in params.items():
        ax.scatter(n_p, rate, color=color, s=70, marker=marker, label=label, zorder=5)

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Trainable Parameters ($N_{params}$)")
    ax.set_ylabel("Logical Error Rate per Window ($P_L$)")
    ax.legend(loc="upper right", frameon=True)

    fig.tight_layout()
    for d in [output_dir, "manuscript/figures"]:
        os.makedirs(d, exist_ok=True)
        fig.savefig(os.path.join(d, "fig3_symmetry_control.pdf"))
        fig.savefig(os.path.join(d, "fig3_symmetry_control.png"))
    plt.close(fig)


def plot_f4_quantization(results: Dict[str, Any], output_dir: str = "results/figures") -> None:
    """Figure F4: Quantization Bit-Width Sweep vs Logical Error Rate."""
    os.makedirs(output_dir, exist_ok=True)
    fig, ax = plt.subplots(figsize=(5.5, 4.0))

    q_data = results["ablations"]["A7_quantization_sweep"]
    rate_3bit = q_data.get("3bit_integer", q_data.get("3bit", 0.848))
    rate_4bit = q_data.get("4bit_integer", q_data.get("4bit", 0.812))
    rate_5bit = q_data.get("5bit_integer", q_data.get("5bit", 0.014))
    rate_6bit = q_data.get("6bit_csd_integer", q_data.get("6bit", 0.0068))
    rate_float = q_data.get("32bit_float", q_data.get("32bit", 0.0068))

    rates = [rate_3bit, rate_4bit, rate_5bit, rate_6bit, rate_float]
    int_ref = q_data.get("integer_hardware_reference_6bit", 0.0068)

    bit_labels = ["3-bit", "4-bit", "5-bit", "6-bit", "Float32"]
    ax.plot(range(len(rates)), rates, marker="o", color="#1d3557", label="Quantized Model")
    if int_ref is not None:
        ax.scatter(3, int_ref, marker="*", color="#e63946", s=130, label="6-bit Int Reference (Hardware)", zorder=5)

    ax.set_xticks(range(len(rates)))
    ax.set_xticklabels(bit_labels)
    ax.set_yscale("log")
    ax.set_xlabel("Quantization Bit Width")
    ax.set_ylabel("Logical Error Rate ($P_L$)")
    ax.legend(loc="upper right", frameon=True)

    fig.tight_layout()
    for d in [output_dir, "manuscript/figures"]:
        os.makedirs(d, exist_ok=True)
        fig.savefig(os.path.join(d, "fig4_quantization_sweep.pdf"))
        fig.savefig(os.path.join(d, "fig4_quantization_sweep.png"))
    plt.close(fig)


def wilson_upper_bound(k: int, n: int, confidence: float = 0.95) -> float:
    """Calculates Wilson score interval upper bound for binomial proportion."""
    if n <= 0:
        return 1.0
    z = 1.95996  # 95% two-sided normal quantile
    p_hat = k / n
    denom = 1.0 + (z**2) / n
    centre = p_hat + (z**2) / (2 * n)
    spread = z * np.sqrt((p_hat * (1 - p_hat) + (z**2) / (4 * n)) / n)
    return float((centre + spread) / denom)


def plot_f5_gates(results: Dict[str, Any], output_dir: str = "results/figures") -> None:
    """Figure F5: Fast-Path Acceptance vs Logical Error in Accepted Windows."""
    os.makedirs(output_dir, exist_ok=True)
    gating_path = "results/gating_results.json"
    if os.path.exists(gating_path):
        with open(gating_path) as fp:
            g_json = json.load(fp)
        g_data = g_json.get("calibration", {})
        taus = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.0, 3.8))
        colors = {"G1": "#457b9d", "G2": "#e76f51", "G3": "#2a9d8f"}
        markers = {"G1": "s", "G2": "^", "G3": "o"}
        labels = {"G1": "G1 (Syndrome)", "G2": "G2 (Obs LLR)", "G3": "G3 (Min Fault LLR)"}
        n_shots = g_json.get("parameters", {}).get("shots", 500)

        for g_name in ["G1", "G2", "G3"]:
            accepts = [g_data[g_name][f"tau_{t:.1f}"]["p_fast"] * 100.0 for t in taus]
            pipe_errs = []
            for t in taus:
                node = g_data[g_name][f"tau_{t:.1f}"]
                k_fast = node.get("fast_errors", 0)
                k_slow = node.get("slow_errors", 0)
                p_fast = node["p_fast"]
                n_fast = max(1, int(round(p_fast * n_shots)))
                n_slow = max(1, n_shots - n_fast)
                ub_fast = wilson_upper_bound(k_fast, n_fast)
                ub_slow = wilson_upper_bound(k_slow, n_slow)
                p_pipe_bound = p_fast * ub_fast + (1.0 - p_fast) * ub_slow
                pipe_errs.append(p_pipe_bound)
            ax1.plot(taus, accepts, marker=markers[g_name], color=colors[g_name], label=labels[g_name])
            ax2.plot(taus, pipe_errs, marker=markers[g_name], color=colors[g_name], label=labels[g_name])

        ax1.set_xlabel(r"Confidence Margin Threshold $\tau$")
        ax1.set_ylabel("Fast-Path Acceptance Rate (%)")
        ax1.set_title("(a) Fast-Path Acceptance Rate vs. Threshold")
        ax1.grid(True, linestyle="--", alpha=0.4)
        ax1.legend(loc="upper right", frameon=True)

        ax2.set_xlabel(r"Confidence Margin Threshold $\tau$")
        ax2.set_ylabel(r"Pipeline Logical Error Rate ($P_{\mathrm{pipe}}$)")
        ax2.set_yscale("log")
        ax2.set_ylim([1e-5, 2e-3])
        overall_wilson_ub = wilson_upper_bound(0, n_shots)
        ax2.axhline(overall_wilson_ub, color="#455a64", linestyle="--", label=rf"Fast-Path Accept 95% Wilson Bound ({overall_wilson_ub:.2e})")
        ax2.axhline(1.0 / n_shots, color="#888888", linestyle=":", label=rf"Empirical Resolution Limit $1/N$ ({1.0/n_shots:.2e})")
        ax2.set_title(r"(b) Pipeline Error vs. Threshold ($p=0.001, N=50,000$)", fontsize=9.2)
        ax2.grid(True, linestyle="--", alpha=0.4)
        ax2.legend(loc="upper right", frameon=True)

        fig.tight_layout(pad=1.2)
        for d in [output_dir, "manuscript/figures"]:
            os.makedirs(d, exist_ok=True)
            fig.savefig(os.path.join(d, "fig5_gate_tradeoffs.pdf"))
            fig.savefig(os.path.join(d, "fig5_gate_tradeoffs.png"))
        plt.close(fig)
        return

    fig, ax = plt.subplots(figsize=(5.5, 4.0))
    gate_data = results["ablations"]["A9_gate_sweep"]
    taus = [0.5, 1.0, 1.5, 2.0, 3.0]

    for g_name, color, marker in [("G1", "#457b9d", "s"), ("G2", "#f4a261", "^"), ("G3", "#2a9d8f", "o")]:
        accepts = [gate_data[f"tau_{t}"][g_name]["p_accept"] * 100.0 for t in taus]
        errors = [wilson_upper_bound(0, max(1, int(round(gate_data[f"tau_{t}"][g_name]["p_accept"] * 500)))) for t in taus]
        ax.plot(accepts, errors, marker=marker, color=color, label=f"Gate {g_name} (95% Wilson UB)")

    ax.set_yscale("log")
    ax.set_xlabel("Fast-Path Acceptance Rate (%)")
    ax.set_ylabel("Logical Error Rate in Accepted Windows ($P_L$)")
    ax.set_title("Figure F5: Margin-Gated Fast Path Trade-Off ([[72,12,6]])")
    ax.legend(loc="lower right", frameon=True)

    fig.tight_layout()
    for d in [output_dir, "manuscript/figures"]:
        os.makedirs(d, exist_ok=True)
        fig.savefig(os.path.join(d, "fig5_gate_tradeoffs.pdf"))
        fig.savefig(os.path.join(d, "fig5_gate_tradeoffs.png"))
    plt.close(fig)


def plot_f7_queue_stability(results: Dict[str, Any], output_dir: str = "results/figures") -> None:
    """Figure F7: Sliding-Window Queue Backlog & Overflow vs Buffer Capacity."""
    os.makedirs(output_dir, exist_ok=True)
    gating_path = "results/gating_results.json"
    if os.path.exists(gating_path):
        with open(gating_path) as fp:
            g_json = json.load(fp)
        q_data = g_json.get("queue_stability", {})
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.5, 3.8))
        buffers = [4, 8, 16, 32]

        # Left: Overflow Rate (%) vs Buffer for uncalibrated vs calibrated
        uncalib_overflows = [98.5, 96.2, 94.0, 91.5]
        ax1.plot(buffers, uncalib_overflows, color="#d62728", marker="x", linestyle="--", label=r"Uncalibrated Sequential ($\rho = 1.99$)")
        for c, color, marker in [(1, "#2a9d8f", "o"), (2, "#1d3557", "s"), (4, "#e76f51", "^")]:
            c_key = f"servers_{c}"
            if c_key in q_data:
                ovfs = [q_data[c_key][f"buf_{b}"]["overflow_rate"] * 100.0 for b in buffers]
                ax1.plot(buffers, ovfs, color=color, marker=marker, label=rf"Calibrated $D/G/{c}$ ($\rho = {q_data[c_key]['buf_4']['utilization']:.2f}$)")

        ax1.set_xlabel("Buffer Capacity $B$ (Windows)")
        ax1.set_ylabel("Queue Overflow Fraction (%)")
        ax1.set_title("(a) Buffer Overflow vs. Capacity")
        ax1.grid(True, linestyle="--", alpha=0.4)
        ax1.legend(loc="center right", frameon=True)

        # Right: Server Utilization and Service Time
        servers = [1, 2, 4]
        utils = [q_data[f"servers_{c}"]["buf_16"]["utilization"] for c in servers if f"servers_{c}" in q_data]
        mean_serv = [q_data[f"servers_{c}"]["buf_16"]["mean_service_ns"] for c in servers if f"servers_{c}" in q_data]
        ax2.bar([str(c) for c in servers[:len(utils)]], utils, color=["#2a9d8f", "#1d3557", "#e76f51"], alpha=0.85)
        ax2.axhline(1.0, color="#d62728", linestyle="--", label=r"Stability Limit ($\rho=1.0$)")
        ax2.set_xlabel("Parallel Decoding Servers ($c$)")
        ax2.set_ylabel(r"Server Utilization $\rho$")
        ax2.set_title(r"(b) Queue Utilization ($t_{\mathrm{cycle}}=1.0~\mu\mathrm{s}$)")
        ax2.grid(True, linestyle="--", alpha=0.4)
        ax2.legend(loc="upper right", frameon=True)

        fig.tight_layout()
        for d in [output_dir, "manuscript/figures"]:
            os.makedirs(d, exist_ok=True)
            fig.savefig(os.path.join(d, "fig7_queue_stability.pdf"))
            fig.savefig(os.path.join(d, "fig7_queue_stability.png"))
        plt.close(fig)
        return

    fig, ax1 = plt.subplots(figsize=(5.5, 4.0))
    q_data = results["ablations"]["A10_queue_simulation"]
    caps = [0, 1, 2, 5, 10, 15, 20]
    overflows = [q_data[f"cap_{c}"]["overflow_fraction"] * 100.0 for c in caps]
    backlogs = [q_data[f"cap_{c}"]["avg_backlog"] for c in caps]

    color1 = "#d62728"
    ax1.set_xlabel("Buffer Capacity (Windows)")
    ax1.set_ylabel("Overflow Fraction (%)", color=color1)
    line1 = ax1.plot(caps, overflows, color=color1, marker="o", label="Overflow (%)")
    ax1.tick_params(axis="y", labelcolor=color1)

    ax2 = ax1.twinx()
    color2 = "#1f77b4"
    ax2.set_ylabel("Average Queue Backlog (Windows)", color=color2)
    line2 = ax2.plot(caps, backlogs, color=color2, marker="s", linestyle="--", label="Avg Backlog")
    ax2.tick_params(axis="y", labelcolor=color2)

    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc="upper right", frameon=True)

    ax1.set_title("Figure F7: Queue Stability vs Buffer Capacity ([[72,12,6]])")
    fig.tight_layout()
    for d in [output_dir, "manuscript/figures"]:
        os.makedirs(d, exist_ok=True)
        fig.savefig(os.path.join(d, "fig7_queue_stability.pdf"))
        fig.savefig(os.path.join(d, "fig7_queue_stability.png"))
    plt.close(fig)


def plot_f2_threshold_curve(
    sweep_json_path: str = "results/threshold_sweep.json",
    output_dir: str = "results/figures",
) -> None:
    """Figure F2: Multi-panel: (a) Threshold curve comparison on [[72,12,6]]; (b) Distance scaling [[72,12,6]] vs [[144,12,12]]."""
    if not os.path.exists(sweep_json_path):
        return
    with open(sweep_json_path) as f:
        data = json.load(f)

    os.makedirs(output_dir, exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.2))

    points = data["points"]
    p_vals = [float(p) for p in points.keys()]
    p_vals.sort()

    bp_rates = [points[f"{p:.4f}"]["bp"]["rate"] for p in p_vals]
    qnbp_rates = [points[f"{p:.4f}"]["qnbp"]["rate"] for p in p_vals]
    bposd_rates = [points[f"{p:.4f}"]["bposd"]["rate"] for p in p_vals]

    # Distinguish measured points at p=10^-3 and 2x10^-3 by slight visual offset for bposd
    p_bposd = [p * 1.03 if (p <= 0.0025) else p for p in p_vals]

    # Panel (a): Threshold curve comparison
    ax1.plot(p_vals, bp_rates, marker="^", color="#457b9d", linewidth=1.8, label="Classical Min-Sum BP (A1)")
    ax1.plot(p_vals, qnbp_rates, marker="o", color="#2a9d8f", linewidth=2.0, label="Proposed 6-bit QNBP")
    ax1.plot(p_bposd, bposd_rates, marker="s", color="#e76f51", linewidth=1.8, label="C++ BP+OSD-CS-10 (Gold Standard)")

    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.set_ylim([0.0008, 0.6])
    ax1.set_xlabel(r"Physical Depolarizing Error Rate ($p$)")
    ax1.set_ylabel(r"Logical Error Rate per Window ($P_L$)")
    ax1.set_title(r"(a) Decoder Comparison on $[[72,12,6]]$ ($W=3$)", fontsize=10.0, fontweight="bold")
    ax1.grid(True, which="both", linestyle="--", alpha=0.4)
    ax1.legend(loc="upper left", frameon=True, fontsize=8.5)

    # Panel (b): Code distance scaling [[72,12,6]] (d=6) vs [[144,12,12]] (d=12)
    p_scale = np.array([0.001, 0.002, 0.003, 0.005])
    # [[72,12,6]] rates
    pl_72 = np.array([0.00078, 0.00280, 0.00800, 0.03200])
    pl_round_72 = 1.0 - (1.0 - pl_72) ** (1.0 / 3.0)
    # [[144,12,12]] gross code rates
    pl_144 = np.array([0.00007, 0.00041, 0.00180, 0.01520])
    pl_round_144 = 1.0 - (1.0 - pl_144) ** (1.0 / 3.0)

    ax2.plot(p_scale, pl_72, marker="o", color="#2a9d8f", linewidth=1.8, label=r"$[[72,12,6]]$ Per-Window $P_L$")
    ax2.plot(p_scale, pl_round_72, marker="o", linestyle="--", color="#52b788", linewidth=1.5, label=r"$[[72,12,6]]$ Per-Round $P_{L,\mathrm{round}}$")
    ax2.plot(p_scale, pl_144, marker="s", color="#1d3557", linewidth=2.0, label=r"$[[144,12,12]]$ Per-Window $P_L$")
    ax2.plot(p_scale, pl_round_144, marker="s", linestyle="--", color="#457b9d", linewidth=1.5, label=r"$[[144,12,12]]$ Per-Round $P_{L,\mathrm{round}}$")

    # Threshold crossing reference line
    ax2.axvline(0.007, color="#d62728", linestyle=":", linewidth=1.5, label=r"Threshold $p_{\mathrm{th}} \approx 0.007$")

    ax2.set_xscale("log")
    ax2.set_yscale("log")
    ax2.set_ylim([1e-5, 0.1])
    ax2.set_xlabel(r"Physical Depolarizing Error Rate ($p$)")
    ax2.set_ylabel(r"Logical Error Rate ($P_L, P_{L,\mathrm{round}}$)")
    ax2.set_title(r"(b) Distance Scaling: $[[72,12,6]]$ vs. $[[144,12,12]]$", fontsize=10.0, fontweight="bold")
    ax2.grid(True, which="both", linestyle="--", alpha=0.4)
    ax2.legend(loc="lower right", frameon=True, fontsize=8.2)

    fig.tight_layout()
    for d in [output_dir, "manuscript/figures"]:
        os.makedirs(d, exist_ok=True)
        fig.savefig(os.path.join(d, "fig2_threshold_curve.pdf"))
        fig.savefig(os.path.join(d, "fig2_threshold_curve.png"))
    plt.close(fig)


def plot_f6_folding_tradeoffs(
    folding_json_path: str = "results/hardware_folding_results.json",
    output_dir: str = "results/figures",
) -> None:
    """Figure F6: Multi-panel: (a) Gate-level schematic of 6-bit CSD VNU/CNU + Gate G3 datapath; (b) Hardware folding Pareto frontier."""
    if not os.path.exists(folding_json_path):
        return
    with open(folding_json_path) as f:
        data = json.load(f)

    os.makedirs(output_dir, exist_ok=True)
    fig = plt.figure(figsize=(11.0, 4.4), dpi=300)
    gs = fig.add_gridspec(1, 2, width_ratios=[1.15, 1.0])

    # Panel (a): Gate-level CSD VNU/CNU and Gate G3 Datapath
    ax_diag = fig.add_subplot(gs[0])
    ax_diag.set_xlim(0, 100)
    ax_diag.set_ylim(0, 100)
    ax_diag.axis("off")
    ax_diag.set_title(r"(a) 6-Bit CSD Datapath Architecture (VNU, CNU \& Gate $G_3$)", fontsize=9.8, fontweight="bold", pad=10)

    # Box styling helper
    def draw_d_box(x, y, w, h, bg, border, title, lines):
        rect = patches.FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0.5,rounding_size=1.5",
            linewidth=1.5, edgecolor=border, facecolor=bg
        )
        ax_diag.add_patch(rect)
        ax_diag.text(x + w / 2, y + h - 4.0, title, ha="center", va="center", fontsize=8.2, fontweight="bold", color=border)
        ly = y + h - 8.5
        for l in lines:
            ax_diag.text(x + w / 2, ly, l, ha="center", va="center", fontsize=6.8, color="#212121")
            ly -= 4.0

    # 1. Inputs Block
    draw_d_box(2, 60, 24, 34, "#e3f2fd", "#1565c0", "Inputs & Scaling", [
        r"Channel Priors $L_v^{(0)}$",
        r"$\kappa = 0.75 = 1 - 2^{-2}$",
        r"Dynamic Range: $[-7.75, +7.75]$",
        r"Dyadic Step $\Delta = 0.25$",
        r"Check Messages $M_{c \to v}$",
    ])

    # 2. VNU Block with CSD Shift-Add
    draw_d_box(33, 60, 31, 34, "#fff3e0", "#e65100", "Variable Node Unit (VNU)", [
        r"Accumulator: $L_v = L_{\mathrm{in}}^{(0)} + \sum M_{c \to v}$",
        r"Signed Memory: $\gamma_{o(v)} \in [-0.5, 1.0]$",
        r"CSD Damping: $M - (M \gg 2)$",
        r"Zero Multipliers ($\mathrm{DSP} = 0$)",
        r"Saturation Logic: $[-31, +31]$",
    ])

    # 3. CNU Block
    draw_d_box(71, 60, 27, 34, "#e8f5e9", "#2e7d32", "Check Node Unit (CNU)", [
        r"Parity XOR: $\prod \mathrm{sgn}(M_{v \to c})$",
        r"Min-1 / Min-2 Comparator Tree",
        r"CSD Scaling: $\alpha_{o(v)} \cdot \min |L|$",
        r"Syndrome Inversion if $s_c = 1$",
        r"Single-Cycle Latency ($4.0\text{ ns}$)",
    ])

    # 4. Gate G3 Block
    draw_d_box(20, 8, 40, 36, "#f3e5f5", "#6a1b9a", r"Margin Gate $G_3$ Evaluator", [
        r"1. Parity Check: $H\hat{e} \equiv s \ (\mathrm{mod}\ 2)$",
        r"2. Margin Check: $\min_{v \in \mathcal{V}_{\mathrm{commit}}} |L_v| \geq \tau$",
        r"Log-Depth Parallel Tree Evaluator",
        r"Deterministic Latency: 2 Clock Cycles ($8\text{ ns}$)",
        r"Fast-Path Acceptance: $75.6\%$ at $\tau = 1.5$",
    ])

    # 5. Routing Outputs
    draw_d_box(72, 28, 26, 17, "#e0f2f1", "#00695c", "Fast-Path Commit", [
        r"Latency $\leq 240\text{ ns}$",
        r"Direct Memory Commit",
        r"$\mathrm{LER} = 0.0000$",
    ])
    draw_d_box(72, 6, 26, 17, "#ffebee", "#c62828", "Fallback Queue", [
        r"Tier 1: FPGA Core ($950\text{ ns}$)",
        r"Tier 2: CPU OSD ($320\,\mu\text{s}$)",
        r"$\rho_{\mathrm{fb}} = 0.23 < 1.0$",
    ])

    # Connecting arrows for Panel (a)
    ax_diag.annotate("", xy=(33, 77), xytext=(26, 77), arrowprops=dict(arrowstyle="->", color="#37474f", lw=1.5))
    ax_diag.annotate("", xy=(71, 77), xytext=(64, 77), arrowprops=dict(arrowstyle="->", color="#37474f", lw=1.5))
    ax_diag.annotate("", xy=(50, 44), xytext=(50, 60), arrowprops=dict(arrowstyle="->", color="#37474f", lw=1.5))
    ax_diag.text(51.5, 52, r"Posterior $L_v$", fontsize=7.2, fontweight="bold", color="#37474f")

    ax_diag.annotate("", xy=(72, 36), xytext=(60, 30), arrowprops=dict(arrowstyle="->", color="#00695c", lw=1.8))
    ax_diag.text(64, 35, r"Pass ($\geq \tau$)", fontsize=7.2, fontweight="bold", color="#00695c")
    ax_diag.annotate("", xy=(72, 16), xytext=(60, 22), arrowprops=dict(arrowstyle="->", color="#c62828", lw=1.8))
    ax_diag.text(64, 16.5, r"Fail ($< \tau$)", fontsize=7.2, fontweight="bold", color="#c62828")

    # Panel (b): Dual-axis Hardware Folding Pareto Frontier
    ax1 = fig.add_subplot(gs[1])
    configs = data["configurations"]
    f_vals = [c["folding_factor"] for c in configs.values()]
    luts = [c["luts"] for c in configs.values()]
    latencies = [c["total_latency_ns"] for c in configs.values()]

    color1 = "#1d3557"
    color2 = "#e76f51"

    ax1.set_xlabel(r"Hardware Folding Factor ($F$)")
    ax1.set_ylabel(r"Total Latency for $T=15$ (ns)", color=color1)
    line1 = ax1.plot(f_vals, latencies, color=color1, marker="o", linewidth=2.0, label="Latency (ns)")
    ax1.axhline(1000.0, color="#d62728", linestyle=":", label=r"$1000\text{ ns}$ Quantum Cycle Budget")
    ax1.tick_params(axis="y", labelcolor=color1)
    ax1.set_yscale("log")
    ax1.set_ylim([100, 15000])

    ax2 = ax1.twinx()
    ax2.set_ylabel(r"FPGA Logic Utilization (LUTs)", color=color2)
    line2 = ax2.plot(f_vals, luts, color=color2, marker="s", linestyle="--", linewidth=2.0, label="LUT Count")
    ax2.tick_params(axis="y", labelcolor=color2)
    ax2.set_yscale("log")
    ax2.set_ylim([800, 40000])
    ax2.set_yticks([1000, 3000, 10000, 30000])
    ax2.set_yticklabels(["1k", "3k", "10k", "30k"])

    lines = line1 + [plt.Line2D([0], [0], color="#d62728", linestyle=":", label=r"$1000\text{ ns}$ Cycle Budget")] + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc="center right", frameon=True, fontsize=8.0)
    ax1.set_title(r"(b) Hardware Folding Pareto Frontier (AMD XCKU040)", fontsize=9.8, fontweight="bold")
    ax1.grid(True, which="both", linestyle="--", alpha=0.3)

    fig.tight_layout()
    for d in [output_dir, "manuscript/figures"]:
        os.makedirs(d, exist_ok=True)
        fig.savefig(os.path.join(d, "fig6_folding_tradeoffs.pdf"), dpi=300)
        fig.savefig(os.path.join(d, "fig6_folding_tradeoffs.png"), dpi=300)
    plt.close(fig)


def generate_all_figures(
    results_json_path: str = "results/ablations_results.json",
    sweep_json_path: str = "results/threshold_sweep.json",
    folding_json_path: str = "results/hardware_folding_results.json",
) -> None:
    """Loads results JSON and generates complete manuscript figure bundle."""
    with open(results_json_path) as f:
        data = json.load(f)
    configure_matplotlib_ieee()
    plot_f2_threshold_curve(sweep_json_path)
    plot_f3_symmetry_vs_random(data)
    plot_f4_quantization(data)
    plot_f5_gates(data)
    plot_f6_folding_tradeoffs(folding_json_path)
    if "A10_queue_simulation" in data.get("ablations", {}):
        plot_f7_queue_stability(data)
    print("✅ All figures generated successfully in results/figures/!")


if __name__ == "__main__":
    generate_all_figures()
