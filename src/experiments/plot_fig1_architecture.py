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
    fig, ax = plt.subplots(figsize=(12, 5.0), dpi=300)
    ax.set_xlim(0, 120)
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
                fontsize=10.5, fontweight="bold", color=border_color)
        line_y = y + h - 7.5
        for line in subtitle_lines:
            ax.text(x + w / 2, line_y, line, ha="center", va="center",
                    fontsize=8.5, color="#212121")
            line_y -= 3.6

    def draw_arrow(x1, y1, x2, y2, label=""):
        ax.annotate(
            "", xy=(x2, y2), xytext=(x1, y1),
            arrowprops=dict(arrowstyle="->", color="#37474f", lw=1.8, mutation_scale=15)
        )
        if label:
            ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 1.8, label,
                    ha="center", va="bottom", fontsize=8.0, fontweight="bold", color="#37474f")

    # Box 1: Quantum Circuit & DEM
    draw_box(
        2, 12, 22, 26, c_circuit, c_circuit_b,
        "1. Stim Space-Time DEM",
        [
            "Gross BB Code [[72,12,6]]",
            "Bravyi Depth-7 Circuit",
            "Noise p in [10^-3, 5x10^-3]",
            "10,260 Fault Mechanisms",
            "Bipartite Tanner Graph",
        ]
    )

    # Box 2: Torus Automorphism Orbits
    draw_box(
        28, 12, 22, 26, c_orbit, c_orbit_b,
        "2. Torus Automorphism",
        [
            "Group G = Z_l x Z_m (36 shifts)",
            "Exact Symmetries (Thm 1)",
            "10,260 -> 285 Orbits (36x)",
            "Equivariance Enforced",
            "Window Boundary Classes",
        ]
    )

    # Box 3: 6-Bit Unfolded QNBP
    draw_box(
        54, 12, 23, 26, c_qnbp, c_qnbp_b,
        "3. 6-Bit Integer QNBP",
        [
            "T=15 Unfolded Iterations",
            "Dyadic Step Delta = 0.25",
            "Dynamic Range [-7.75, +7.75]",
            "CSD Shift-and-Add (DSP=0)",
            "Soft Syndrome Parity Loss",
        ]
    )

    # Box 4: Confidence Margin Gate
    draw_box(
        81, 15, 17, 20, c_gate, c_gate_b,
        "4. Margin Gate G3",
        [
            "Syndrome Matched?",
            "M_min = min |L_v| >= tau",
            "Zero False Flips",
            "Log-Depth Evaluator",
        ]
    )

    # Fast Path & Fallback Boxes
    draw_box(
        102, 26, 17, 16, c_fast, c_fast_b,
        "Fast-Path FPGA",
        [
            "Admit Rate: 15.6%",
            "Latency: ~360 ns",
            "LER: 0.0000 (0 Err)",
            "Immediate Commit",
        ]
    )

    draw_box(
        102, 6, 17, 16, c_slow, c_slow_b,
        "Fallback Pool",
        [
            "Admit Rate: 84.4%",
            "C++ BP+OSD-0",
            "LER: 0.0680",
            "Buffered Queue",
        ]
    )

    # Connecting Arrows
    draw_arrow(24, 25, 28, 25, "Extract DEM")
    draw_arrow(50, 25, 54, 25, "Orbit Tying")
    draw_arrow(77, 25, 81, 25, "Posterior L_v")

    # Branching Arrows from Gate
    ax.annotate(
        "", xy=(102, 34), xytext=(98, 28),
        arrowprops=dict(arrowstyle="->", color=c_fast_b, lw=2.0, mutation_scale=14)
    )
    ax.text(97, 33, "Pass (>= tau)", ha="right", va="bottom", fontsize=8.5, fontweight="bold", color=c_fast_b)

    ax.annotate(
        "", xy=(102, 14), xytext=(98, 22),
        arrowprops=dict(arrowstyle="->", color=c_slow_b, lw=2.0, mutation_scale=14)
    )
    ax.text(97, 15, "Fail (< tau)", ha="right", va="top", fontsize=8.5, fontweight="bold", color=c_slow_b)

    # Bottom Sliding Window Banner
    banner = patches.FancyBboxPatch(
        (2, 2), 75, 6, boxstyle="round,pad=0.5,rounding_size=1.0",
        linewidth=1.2, edgecolor="#78909c", facecolor="#eceff1"
    )
    ax.add_patch(banner)
    ax.text(
        39.5, 5,
        "Continuous Streaming Sliding Window (Width W = 3 rounds, Commit Stride F = 1 round, Cycle = 1000 ns)",
        ha="center", va="center", fontsize=8.5, fontweight="bold", color="#37474f"
    )

    fig.tight_layout()
    fig.savefig(os.path.join(output_dir, "fig1_architecture.pdf"))
    fig.savefig(os.path.join(output_dir, "fig1_architecture.png"))
    plt.close(fig)
    print("✅ Figure F1 generated successfully in results/figures/!")


if __name__ == "__main__":
    generate_figure_1()

