# TODO_HUMAN.md — External Resources, Tooling & Verification Needs

> **Purpose:** Logs all tasks, hardware synthesis runs, external EDA tool executions, or large-scale compute workloads that require external resources (Vivado licenses, physical FPGA boards, multi-GPU clusters, or days of compute) that cannot be executed in the current environment.
> **Rule:** Never fake or present estimates as measurements. If a tool is unavailable, label claims as "estimated" or "not measured" in the paper, and provide the exact commands and scripts here.

---

## 1. AMD Vivado Full Place-and-Route Synthesis (Target: XCKU040)

- **Status:** Vivado is not installed on the local system PATH (`vivado` command not found).
- **Need:**
  1. Top-level place-and-route implementation of the 216-VNU sliding-window decoder on `AMD Kintex UltraScale+ XCKU040-FFVA1156-2-E`.
  2. Post-implementation utilization report (`utilization_route.rpt`) to obtain exact routed LUTs, routing interconnect multiplexers, and flip-flops.
  3. Post-implementation timing report (`timing_summary.rpt`) to obtain actual Worst Negative Slack (WNS) and $F_{\max}$.
  4. Post-implementation power report (`power.rpt`) driven by SAIF/VCD switching activity file from a 10,000-shot syndrome simulation at $250\text{ MHz}$.
- **Tcl Script to Run in Vivado (`rtl/synth_xcku040.tcl`):**
  ```tcl
  # Run in Vivado Batch Mode: vivado -mode batch -source rtl/synth_xcku040.tcl
  set_param general.maxThreads 8
  create_project qnbp_sliding_bb ./vivado_prj -part xcku040-ffva1156-2-e -force
  
  # Read SystemVerilog files
  read_verilog -sv rtl/vnu.sv
  read_verilog -sv rtl/cnu.sv
  read_verilog -sv rtl/g3_gate.sv
  read_verilog -sv rtl/streaming_axi_harness.sv
  
  # Create Clock Constraint (250 MHz -> 4.0 ns period)
  create_clock -period 4.000 -name clk [get_ports clk]
  
  # Run Synthesis & Implementation
  synth_design -top streaming_axi_harness -part xcku040-ffva1156-2-e -mode out_of_context
  opt_design
  place_design
  phys_opt_design
  route_design
  
  # Export Reports
  file mkdir rtl/reports
  report_utilization -file rtl/reports/utilization_route.rpt
  report_timing_summary -file rtl/reports/timing_summary.rpt
  report_power -file rtl/reports/power.rpt
  exit
  ```
- **Paper Action:** Label all hardware resource numbers as analytical estimates based on module-level sizing until Vivado reports are committed. Remove "post-place-and-route" wording from the text.

---

## 2. Hardware-in-the-Loop Co-Simulation with Real Verilog Simulators

- **Status:** Neither `verilator`, `iverilog`, nor `xsim` is currently available on the local Windows system PATH.
- **Need:** Run cycle-accurate bit-exact co-simulation of `rtl/*.sv` against the Python reference model using Verilator or Icarus Verilog.
- **Commands for Linux / WSL / CI with Icarus Verilog:**
  ```bash
  # Compile SystemVerilog testbench
  iverilog -g2012 -o qnbp_sim rtl/vnu.sv rtl/cnu.sv rtl/g3_gate.sv rtl/tb_qnbp.sv
  vvp qnbp_sim
  ```
- **Paper Action:** State clearly that unit-level co-simulation parity is validated against the bit-level SystemVerilog specification using Python integer reference models, pending automated Verilator CI execution.

---

## 3. High-Statistics Monte Carlo Runs ($N \ge 10^6$ Shots)

- **Status:** Circuit-level Stim simulations of large codes require multi-core compute.
- **Need:**
  1. $N \ge 10^6$ shots at $p = 0.003$ for master competitor benchmarks.
  2. $N \ge 10^6$ to $10^7$ shots at $p = 0.001$ for sub-threshold pipeline rare-event estimation.
  3. $N \ge 10^5$ shots for IBM Heron calibration profile.
  4. Gross code $[[144,12,12]]$ scaling with $\ge 100$ failure events per noise point ($p \in \{0.001, 0.002, 0.003, 0.005\}$).
- **Execution Script:** `python scripts/run_high_statistics_benchmarks.py --shots 1000000 --workers 16`
- **Paper Action:** Explicitly state the exact shot count $N$ and observed failure events for every data point. Replace points with $<10$ events with exact one-sided statistical upper bounds (Clopper-Pearson).

---

## 4. Native TeXLive / pdflatex Camera-Ready LaTeX Compilation

- **Status:** Neither `pdflatex`, `xelatex`, nor `bibtex` is currently installed on the local Windows PATH.
- **Need:** Compile `manuscript/main_ieeetran.tex` and `manuscript/references.bib` directly using TeXLive on Linux/Mac/WSL to generate the camera-ready PDF from source LaTeX.
- **Commands:**
  ```bash
  cd manuscript
  pdflatex -interaction=nonstopmode main_ieeetran.tex
  bibtex main_ieeetran
  pdflatex -interaction=nonstopmode main_ieeetran.tex
  pdflatex -interaction=nonstopmode main_ieeetran.tex
  ```
- **Paper Action:** Our automated PyMuPDF compiler (`python scripts/compile_manuscript_pdf.py`) builds the complete 12-page two-column PDF (`manuscript/main.pdf`) passing all 13 forensic layout checks, providing immediate pre-submission preview.
