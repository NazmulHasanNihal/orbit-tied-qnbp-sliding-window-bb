---
name: ai-for-science
description: >-
  Accelerate scientific research pipelines, computational experiments, HPC refactoring,
  and data exploration using Google Antigravity. Use when the user wants to profile,
  parallelize, or optimize scientific code (NumPy, PyTorch, C++, CUDA), build automated
  scientific ML pipelines, conduct exploratory data analysis on research datasets, or
  adhere to GDG AI for Science best practices for reproducible computational research.
---

# Antigravity for Science: Research Pipeline & HPC Optimization Guide

This skill implements the principles and practices established by the **Google Developer Groups (GDG) AI for Science** initiative for Google Antigravity. It guides the agent and researcher in structuring computational experiments, refactoring research scripts for high-performance computing (HPC), and enforcing reproducibility across publication workflows.

---

## 1. Core Principles of AI-Driven Scientific Research

1. **Reproducibility First**:
   - Pinned dependencies via `requirements.txt` or `environment.yml` / lockfiles.
   - Pinned random seeds across NumPy, PyTorch, Python random, and hardware backends (e.g. `torch.backends.cudnn.deterministic = True`).
   - Deterministic artifact naming and experiment run logs (JSON / Parquet / CSV).

2. **Performance Scaling & Vectorization**:
   - Eliminate Python `for`-loops over array elements; vectorize using NumPy or tensor backends.
   - Profile memory and computation before and after optimization (`cProfile`, `torch.profiler`, `line_profiler`).
   - Decouple computation kernels from I/O and visualization.

3. **Data Integrity & Exploration**:
   - Inspect data shapes, distribution outliers, missing values, and NaN/inf anomalies before training or decoding.
   - Generate automated exploratory data summaries and publication-quality plots (PDF/SVG).

---

## 2. High-Performance Scientific Computing (HPC) Optimization

When refactoring scientific code for local multi-core or cluster environments:

### A. Parallelization Strategies
* **Multi-Processing / ProcessPoolExecutor**: For embarrassingly parallel simulations (e.g., Monte Carlo syndrome decoding across error rates or batches).
* **Numba / JIT Compilation**: Use `@numba.njit(parallel=True, fastmath=True)` for custom non-vectorized numerical loops.
* **Vectorized Tensor Kernels**: For neural belief propagation (BP) or matrix operations, leverage PyTorch batch tensors and batched sparse-dense operations.
* **Fixed-Point / Quantized Kernels**: Integer arithmetic (e.g., 6-bit quantization) to accelerate inference and reduce memory footprint.

### B. Memory Footprint Management
* Use generator streams and chunked reads for massive datasets or simulation traces.
* Avoid intermediate array allocations by performing in-place operations where safe (`out=` parameter in NumPy / `tensor.add_()`).
* Clear CUDA cache or memory buffers between simulation iterations: `gc.collect()`, `torch.cuda.empty_cache()`.

---

## 3. Workflow Steps for Scientific Tasks

1. **Understand Problem & Constraints**:
   - Determine physical/mathematical model (e.g., Bivariate Bicycle code checks, Tanner graph structure, sliding-window block lengths).
   - Identify metrics: Word Error Rate (WER), Frame Error Rate (FER), Block Error Rate (BLER), Bit Error Rate (BER), syndrome decoding latency, convergence steps.

2. **Exploratory Data Analysis & Baseline**:
   - Implement baseline solver or decoder (e.g., standard Min-Sum or belief propagation without neural weights).
   - Verify ground-truth correctness on small toy codes before scaling.

3. **Algorithm Enhancement & Quantization**:
   - Apply automorphism weight tying across Tanner graph orbits.
   - Quantize message exchange and parity check computations (e.g., 6-bit integer).
   - Benchmark throughput vs. baseline.

4. **Manuscript Artifacts**:
   - Generate vector plots (`matplotlib`, `seaborn` with `usetex=True` or serif fonts).
   - Save raw simulation data with metadata for open-science reproducibility.

