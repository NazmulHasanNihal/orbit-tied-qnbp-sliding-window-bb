"""Architectural Pipeline Diagram Generator for Figure F1.

Renders high-quality vector schematic (PDF + PNG) depicting the complete
Orbit-Tied QNBP sliding-window decoding pipeline for BB codes.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def generate_figure_1(output_dir: str = "results/figures") -> None:
    """Generates Figure 1: End-to-end decoding and hardware architecture."""
    os.makedirs(output_dir, exist_ok=True)
    fig, ax = plt.subplots(figsize=(14.0, 5.0), dpi=300)
    ax.set_xlim(0, 142)
    ax.set_ylim(0, 50)
    ax.axis("off")

    # Color Palette (IEEE Computer Society style)
    c_circuit = "#e3f2fd"
    c_circuit_b = "#1565c0"
    c_orbit = "#e8f5e9"
    c_orbit_b = "#2e7d32"
    c_qnbp = "#fff3e0"
    c_qnbp_b = "#e65100"
    c_gate = "#f3e5f5"
    c_gate_b = "#6a1b9a"
    c_fast = "#e0f2f1"
    c_fast_b = "#00695c"
    c_slow = "#ffebee"
    c_slow_b = "#c62828"

    def draw_box(x, y, w, h, bg_color, border_color, title, subtitle_lines):
        rect = patches.FancyBboxPatch(
            (x, y), w, h, boxstyle="round,pad=0.8,rounding_size=1.5",
            linewidth=1.8, edgecolor=border_color, facecolor=bg_color
        )
        ax.add_patch(rect)
        ax.text(x + w / 2, y + h - 3.2, title, ha="center", va="center",
                fontsize=10.0, fontweight="bold", color=border_color)
        line_y = y + h - 7.5
        for line in subtitle_lines:
            ax.text(x + w / 2, line_y, line, ha="center", va="center",
                    fontsize=8.2, color="#212121")
            line_y -= 3.6

    def draw_arrow(x1, y1, x2, y2, label=""):
        ax.annotate(
            "", xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(arrowstyle="->", color="#37474f", lw=1.8, mutation_scale=15)
        )
        if label:
            ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 1.8, label,
                    ha="center", va="bottom", fontsize=8.0, fontweight="bold", color="#37474f")

    # Box 1: Quantum Circuit & DEM (width 18, x=2..20, padded 1.2..20.8)
    draw_box(
        2, 12, 18, 26, c_circuit, c_circuit_b,
        "1. Stim Space-Time DEM",
        [
            "Gross BB Code [[72,12,6]]",
            "Bravyi Depth-7 Circuit",
            r"Noise $p \in [10^{-3}, 5\times 10^{-3}]$",
            "10,260 Fault Mechanisms",
            "Bipartite Tanner Graph",
        ]
    )

    # Box 2: Torus Automorphism Orbits (width 20, x=31..51, padded 30.2..51.8)
    draw_box(
        31, 12, 20, 26, c_orbit, c_orbit_b,
        "2. Torus Automorphism",
        [
            r"$G = \mathbb{Z}_\ell \times \mathbb{Z}_m$ (36 Shifts)",
            "Exact Symmetries (Thm 1)",
            "10,260 -> 285 Orbits (36x)",
            "Equivariance Enforced",
            "Window Boundary Classes",
        ]
    )

    # Box 3: 6-Bit Unfolded QNBP (width 20, x=62..82, padded 61.2..82.8)
    draw_box(
        62, 12, 20, 26, c_qnbp, c_qnbp_b,
        "3. 6-Bit Integer QNBP",
        [
            "T=15 Unfolded Iterations",
            r"Dyadic Step $\Delta = 0.25$",
            "Dynamic Range [-7.75, +7.75]",
            "CSD Shift-and-Add (DSP=0)",
            "Composite Observable Loss",
        ]
    )

    # Box 4: Confidence Margin Gate G3 (width 17, x=93..110, padded 92.2..110.8)
    draw_box(
        93, 13, 17, 24, c_gate, c_gate_b,
        "4. Margin Gate G3",
        [
            "Syndrome Matched?",
            r"$M_{\min} = \min |L_v| \geq \tau$",
            "Zero False Flips",
            "Log-Depth Evaluator",
        ]
    )

    # Fast Path & Fallback Boxes (width 17, x=122..139, padded 121.2..139.8)
    draw_box(
        122, 26, 17, 16, c_fast, c_fast_b,
        "Fast-Path FPGA",
        [
            "Accept Rate: 75.6%",
            "Latency: 240 ns (T=15)",
            "LER: 0.0000 (0 Err)",
            "Immediate Commit",
        ]
    )

    draw_box(
        122, 6, 17, 16, c_slow, c_slow_b,
        "Fallback Pool",
        [
            "Fallback: 24.4%",
            "C++ BP+OSD-CS-10",
            r"$P_{\mathrm{pipe}} = 1.9\times 10^{-4}$",
            r"Buffered $D/G/c$ Queue",
        ]
    )

    # Connecting Arrows with generous 11-unit horizontal spacing
    draw_arrow(21.5, 25, 30.5, 25, "Extract DEM")
    draw_arrow(52.5, 25, 61.5, 25, "Orbit Tying")
    draw_arrow(83.5, 25, 92.5, 25, r"Posterior $L_v$")

    # Branching Arrows from Gate: start outside Box 4 padding (110.8), cleanly onto arrow shafts
    ax.annotate(
        "", xy=(121.5, 34), xytext=(111.5, 27),
        arrowprops=dict(arrowstyle="->", color=c_fast_b, lw=2.0, mutation_scale=14)
    )
    ax.text(116.5, 32.5, r"Pass ($\geq \tau$)", ha="center", va="bottom", fontsize=8.0, fontweight="bold", color=c_fast_b)

    ax.annotate(
        "", xy=(121.5, 14), xytext=(111.5, 23),
        arrowprops=dict(arrowstyle="->", color=c_slow_b, lw=2.0, mutation_scale=14)
    )
    ax.text(116.5, 16.5, r"Fail ($< \tau$)", ha="center", va="top", fontsize=8.0, fontweight="bold", color=c_slow_b)

    # Bottom Sliding Window Banner
    banner = patches.FancyBboxPatch(
        (2, 2), 108, 6, boxstyle="round,pad=0.5,rounding_size=1.0",
        linewidth=1.2, edgecolor="#78909c", facecolor="#eceff1"
    )
    ax.add_patch(banner)
    ax.text(
        56.0, 5,
        r"Continuous Streaming Sliding Window (Width $W = 3$ rounds, Commit Stride $F = 1$ round, Cycle = $1000\text{ ns}$)",
        ha="center", va="center", fontsize=8.5, fontweight="bold", color="#37474f"
    )

    fig.tight_layout()
    for d in [output_dir, "manuscript/figures"]:
        os.makedirs(d, exist_ok=True)
        fig.savefig(os.path.join(d, "fig1_architecture.pdf"), dpi=300)
        fig.savefig(os.path.join(d, "fig1_architecture.png"), dpi=300)
    plt.close(fig)
    print("✅ Figure F1 generated successfully in results/figures/ and manuscript/figures/!")


if __name__ == "__main__":
    generate_figure_1()
