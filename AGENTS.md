# AGENTS.md — Q1 Scientific Research & Engineering Configuration

> This root configuration file is loaded by the Antigravity Agent for every request.
> It defines the 5-Gate OpenSpec lifecycle, the Q1 Research standards, and registered skills.

---

## 🎯 Purpose & Scope

This workspace houses the official implementation of:
**"Orbit-Tied Quantized Neural Belief Propagation for Sliding-Window Decoding of Bivariate-Bicycle Codes"**  
(3D sliding-window neural BP decoder with automorphism orbit weight-tying and 6-bit integer quantization).

All work in this repository targets **top-tier peer-reviewed Q1 venues** (IEEE Transactions on Information Theory, Physical Review Applied, Nature Quantum Information, PRX Quantum, Quantum Science and Technology).

---

## 🧰 Installed Research & Engineering Skills

### 1. Scientific Manuscript & Journal Intelligence
| Skill | Path | Triggers & Use Cases |
|---|---|---|
| `scientific-paper-writer` | `./.agent/skills/scientific-paper-writer/SKILL.md` | "write paper", "manuscript", "draft section", "abstract", "latex", "nature", "ieee", "statistical reporting", "de-aigc" |
| `journal-intelligence` | `./.agent/skills/journal-intelligence/SKILL.md` | "author guidelines", "journal constraints", "ai disclosure", "template download", "desk rejection" |

### 2. Empirical Research & Analysis (1,151 Skills)
| Skill | Path | Triggers & Use Cases |
|---|---|---|
| `auto-empirical-research-skills` | `./.agent/skills/auto-empirical-research-skills/SKILL.md` | "empirical analysis", "causal inference", "econometrics", "benchmark suite", "replication package", "academic rewriting" |

### 3. AI for Science & HPC Optimization
| Skill | Path | Triggers & Use Cases |
|---|---|---|
| `ai-for-science` | `./.agent/skills/ai-for-science/SKILL.md` | "hpc", "parallelization", "vectorization", "reproducible pipeline", "profiling", "monte carlo scaling", "gpu cuda" |

### 4. Code Retrieval & AST Token Engine
| Tool / Skill | Path | Triggers & Use Cases |
|---|---|---|
| `jcodemunch` | `./.agent/skills/jcodemunch/SKILL.md` | "find symbol", "outline", "call graph", "blast radius", "search code", "o(1) retrieval" |

### 5. Core Machine Learning & Python Engineering
| Skill | Path | Triggers & Use Cases |
|---|---|---|
| `ml-engineer` | `./.agent/skills/ml-engineer/SKILL.md` | "pytorch", "neural bp", "cuda tensors", "model architecture", "loss function", "training loop" |
| `ml-pipeline-workflow` | `./.agent/skills/ml-pipeline-workflow/SKILL.md` | "dataset generator", "syndrome generation", "evaluation loop", "checkpointing" |
| `python-pro` | `./.agent/skills/python-pro/SKILL.md` | "python best practices", "type hints", "modular architecture", "clean code" |
| `python-performance-optimization` | `./.agent/skills/python-performance-optimization/SKILL.md` | "speed up", "bottleneck", "memory leak", "quantization", "6-bit int" |
| `python-testing-patterns` | `./.agent/skills/python-testing-patterns/SKILL.md` | "pytest", "unit tests", "decoder verification", "numerical parity" |
| `debugger` | `./.agent/skills/debugger/SKILL.md` | "debug", "investigate error", "trace bug", "fix failure" |
| `test-automator` | `./.agent/skills/test-automator/SKILL.md` | "automated tests", "regression suite", "continuous testing" |
| `git-advanced-workflows` | `./.agent/skills/git-advanced-workflows/SKILL.md` | "git branching", "worktrees", "clean commit history", "pr" |

### 6. Extended Antigravity Skill Vault (307 Skills)
| Skill | Path | Triggers & Use Cases |
|---|---|---|
| `antigravity-skill-vault` | `./.agent/skills/antigravity-skill-vault/SKILL.md` | Query `.agent/skills/antigravity-skill-vault/catalog.json` on-demand for any domain skill. |

---

## 🔄 5-Gate OpenSpec & Q1 Research Workflow

Every research engineering milestone adheres to the 5-Gate process:

```
GATE 1: UNDERSTAND
├── Read .agent/CONTINUITY.md for current research task and milestones
├── Query codebase via jCodeMunch (search_symbols, get_symbol_source) to preserve tokens
└── Select matching skills (ai-for-science, ml-engineer, scientific-paper-writer)

GATE 2: ANALYZE & MODEL
├── Mathematical correctness check (Bivariate Bicycle code syndrome relations, Tanner graph orbits)
├── Quantization & numerical stability review (6-bit int bounds, overflow prevention)
└── Assess dependencies and computational complexity

GATE 3: PLAN (Spec-Driven via OpenSpec)
├── Propose implementation plan with atomic testable steps
├── Document physical/mathematical formulation and error thresholds
└── User alignment before generating code

GATE 4: IMPLEMENT (RARV Loop)
├── Write modular, type-annotated, vectorized Python / PyTorch code
├── Quantize neural weights and check orbit-tying constraints
├── Verify execution, compile step, and numerical assertions
└── Update .agent/CONTINUITY.md

GATE 5: VERIFY & BENCHMARK
├── Run automated unit tests and parity benchmarks
├── Track physical error rate vs. logical error rate (WER / FER / BER curves)
├── Generate vector publication figures and format statistics to Q1 standards
└── Commit with clean Git message and update action log
```

---

## 🚫 Universal Research & Code Constraints

- **Zero Hallucinated Citations**: Every paper reference must be verified via WebSearch / DOI lookup (`scientific-paper-writer`).
- **No Inefficient Full-File Reads**: Prefer `jcodemunch` symbol lookups over reading entire multi-hundred line files.
- **Deterministic Experiments**: Pinned random seeds across NumPy, PyTorch, and Python random libraries.
- **Statistical Rigor**: Always report test statistic, exact p-values, sample sizes ($n$), and 95% confidence intervals on Monte Carlo runs.
