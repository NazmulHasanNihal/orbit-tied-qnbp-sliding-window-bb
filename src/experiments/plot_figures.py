"""Publication figure generation for IEEE TQE / QST manuscript.

Generates Figures F2 (LER vs p), F3 (Torus Symmetry vs Random Control),
F4 (Quantization Bits vs Error), F5 (Gate Trade-offs), and F7 (Queue Stability).
"""

from typing import Dict, Any, List
import json
import os
import matplotlib.pyplot as plt
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

    # Parameter counts
    params = {
        "A1 (Normalized MS)": (15, a1_rate, "#6c757d", "^"),
        "A2 (Untied NBP)": (15 * 7308, a2_rate, "#e63946", "s"),
        "A3 (Orbit-tied)": (15 * 285, a3_rate, "#f4a261", "D"),
        "A4 (Proposed QNBP)": (15 * 285 + 45, a4_rate, "#2a9d8f", "o"),
    }

    # Plot A5 Random-tying cloud
    for seed_rate in a5_runs:
        ax.scatter(15 * 285, seed_rate, color="#b0bec5", alpha=0.7, s=40, zorder=3)
    ax.errorbar(
        15 * 285, a5_mean, yerr=a5_std, fmt="x", color="#455a64",
        capsize=4, label="A5 Random Control (5 seeds)", zorder=4
    )

    for label, (n_p, rate, color, marker) in params.items():
        ax.scatter(n_p, rate, color=color, s=70, marker=marker, label=label, zorder=5)

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Trainable Parameters ($N_{params}$)")
    ax.set_ylabel("Logical Error Rate per Window ($P_L$)")
    ax.set_title("Figure F3: Symmetry Tying vs Random Control ([[72,12,6]], p=0.003)")
    ax.legend(loc="upper right", frameon=True)

    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "fig3_symmetry_control.pdf"))
    fig.savefig(os.path.join(output_dir, "fig3_symmetry_control.png"))
    plt.close(fig)


def plot_f4_quantization(results: Dict[str, Any], output_dir: str = "results/figures") -> None:
    """Figure F4: Quantization Bit-Width Sweep vs Logical Error Rate."""
    os.makedirs(output_dir, exist_ok=True)
    fig, ax = plt.subplots(figsize=(5.5, 4.0))

    q_data = results["ablations"]["A7_quantization_sweep"]
    bits = [3, 4, 5, 6, 32]
    rates = [q_data[f"{b}bit"] for b in bits]
    int_ref = q_data.get("integer_hardware_reference_6bit", q_data.get("integer_hardware_reference_4bit"))

    bit_labels = ["3-bit", "4-bit", "5-bit", "6-bit", "Float32"]
    ax.plot(range(len(bits)), rates, marker="o", color="#1d3557", label="Quantized Model")
    if int_ref is not None:
        idx_star = bits.index(6) if "integer_hardware_reference_6bit" in q_data else bits.index(4)
        lbl = "6-bit Int Reference (Hardware)" if "integer_hardware_reference_6bit" in q_data else "4-bit Int Reference"
        ax.scatter(idx_star, int_ref, marker="*", color="#e63946", s=130, label=lbl, zorder=5)

    ax.set_xticks(range(len(bits)))
    ax.set_xticklabels(bit_labels)
    ax.set_yscale("log")
    ax.set_xlabel("Quantization Bit Width")
    ax.set_ylabel("Logical Error Rate ($P_L$)")
    ax.set_title("Figure F4: Quantization vs Accuracy ([[72,12,6]], p=0.003)")
    ax.legend(loc="upper right", frameon=True)

    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "fig4_quantization_sweep.pdf"))
    fig.savefig(os.path.join(output_dir, "fig4_quantization_sweep.png"))
    plt.close(fig)


def plot_f5_gates(results: Dict[str, Any], output_dir: str = "results/figures") -> None:
    """Figure F5: Fast-Path Acceptance vs Logical Error in Accepted Windows."""
    os.makedirs(output_dir, exist_ok=True)
    fig, ax = plt.subplots(figsize=(5.5, 4.0))

    gate_data = results["ablations"]["A9_gate_sweep"]
    taus = [0.5, 1.0, 1.5, 2.0, 3.0]

    for g_name, color, marker in [("G1", "#457b9d", "s"), ("G2", "#f4a261", "^"), ("G3", "#2a9d8f", "o")]:
        accepts = [gate_data[f"tau_{t}"][g_name]["p_accept"] * 100.0 for t in taus]
        errors = [gate_data[f"tau_{t}"][g_name]["error_in_accept"] for t in taus]
        ax.plot(accepts, errors, marker=marker, color=color, label=f"Gate {g_name}")

    ax.set_yscale("log")
    ax.set_xlabel("Fast-Path Acceptance Rate (%)")
    ax.set_ylabel("Logical Error Rate in Accepted Windows ($P_L$)")
    ax.set_title("Figure F5: Margin-Gated Fast Path Trade-Off ([[72,12,6]])")
    ax.legend(loc="lower right", frameon=True)

    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "fig5_gate_tradeoffs.pdf"))
    fig.savefig(os.path.join(output_dir, "fig5_gate_tradeoffs.png"))
    plt.close(fig)


def plot_f7_queue_stability(results: Dict[str, Any], output_dir: str = "results/figures") -> None:
    """Figure F7: Sliding-Window Queue Backlog & Overflow vs Buffer Capacity."""
    os.makedirs(output_dir, exist_ok=True)
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
    fig.savefig(os.path.join(output_dir, "fig7_queue_stability.pdf"))
    fig.savefig(os.path.join(output_dir, "fig7_queue_stability.png"))
    plt.close(fig)


def plot_f2_threshold_curve(
    sweep_json_path: str = "results/threshold_sweep.json",
    output_dir: str = "results/figures",
) -> None:
    """Figure F2: Logical Error Rate vs Physical Error Rate (p in [10^-3, 5*10^-3])."""
    if not os.path.exists(sweep_json_path):
        return
    with open(sweep_json_path) as f:
        data = json.load(f)

    os.makedirs(output_dir, exist_ok=True)
    fig, ax = plt.subplots(figsize=(5.5, 4.0))

    points = data["points"]
    p_vals = [float(p) for p in points.keys()]
    p_vals.sort()

    bp_rates = [points[f"{p:.4f}"]["bp"]["rate"] for p in p_vals]
    qnbp_rates = [points[f"{p:.4f}"]["qnbp"]["rate"] for p in p_vals]
    bposd_rates = [points[f"{p:.4f}"]["bposd"]["rate"] for p in p_vals]

    ax.plot(p_vals, bp_rates, marker="^", color="#457b9d", label="Classical Min-Sum BP (A1)")
    ax.plot(p_vals, qnbp_rates, marker="o", color="#2a9d8f", label="Orbit-Tied QNBP (Proposed 6-bit)")
    ax.plot(p_vals, bposd_rates, marker="s", color="#e76f51", label="C++ BP+OSD-0 (Gold Standard)")

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Physical Depolarizing Error Rate ($p$)")
    ax.set_ylabel("Logical Error Rate per Window ($P_L$)")
    ax.set_title("Figure F2: Logical Error Rate vs Physical Noise ([[72,12,6]])")
    ax.legend(loc="lower right", frameon=True)

    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "fig2_threshold_curve.pdf"))
    fig.savefig(os.path.join(output_dir, "fig2_threshold_curve.png"))
    plt.close(fig)


def plot_f6_folding_tradeoffs(
    folding_json_path: str = "results/hardware_folding_results.json",
    output_dir: str = "results/figures",
) -> None:
    """Figure F6: Hardware Folding Area-Latency Pareto Frontier on AMD UltraScale+."""
    if not os.path.exists(folding_json_path):
        return
    with open(folding_json_path) as f:
        data = json.load(f)

    os.makedirs(output_dir, exist_ok=True)
    fig, ax1 = plt.subplots(figsize=(5.5, 4.0))

    configs = data["configurations"]
    f_vals = [c["folding_factor"] for c in configs.values()]
    luts = [c["luts"] for c in configs.values()]
    latencies = [c["total_latency_ns"] for c in configs.values()]
    throughputs = [c["throughput_mfps"] for c in configs.values()]

    color1 = "#1d3557"
    color2 = "#e76f51"

    ax1.set_xlabel("Hardware Folding Factor ($F$)")
    ax1.set_ylabel("Total Latency for $T=15$ (ns)", color=color1)
    line1 = ax1.plot(f_vals, latencies, color=color1, marker="o", linewidth=2.0, label="Latency (ns)")
    ax1.axhline(1000.0, color="#d62728", linestyle=":", label=r"1 $\mu$s Quantum Budget")
    ax1.tick_params(axis="y", labelcolor=color1)
    ax1.set_yscale("log")

    ax2 = ax1.twinx()
    ax2.set_ylabel("FPGA Logic Utilization (LUTs)", color=color2)
    line2 = ax2.plot(f_vals, luts, color=color2, marker="s", linestyle="--", linewidth=2.0, label="LUT Count")
    ax2.tick_params(axis="y", labelcolor=color2)
    ax2.set_yscale("log")

    lines = line1 + [plt.Line2D([0], [0], color="#d62728", linestyle=":")] + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc="center right", frameon=True)

    ax1.set_title("Figure F6: Hardware Folding Pareto Frontier ([[72,12,6]], DSP=0)")
    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "fig6_folding_tradeoffs.pdf"))
    fig.savefig(os.path.join(output_dir, "fig6_folding_tradeoffs.png"))
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
