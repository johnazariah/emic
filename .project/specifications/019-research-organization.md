# Specification 019: Research Organization System

## Overview

This specification defines a clear separation between **infrastructure specifications** (how to build the software) and **research work** (what to investigate and discover). This addresses the growing complexity in specs 009-018 which mixed design documents with research planning.

---

## Problem Statement

Current issues:
1. Specs mix "how to build" with "what to investigate"
2. No structured way to track experiment status and results
3. No data storage strategy for reproducibility
4. Difficult to trace: hypothesis → experiment → result → paper claim
5. Specs 009-018 overlap significantly in scope

---

## New Directory Structure

```
.project/
├── specifications/     # Technical design only (infrastructure)
│   ├── 000-index.md
│   ├── 001-devcontainer.md
│   ├── 002-core-types.md
│   └── ...
│
├── research/           # Research planning and synthesis
│   ├── README.md       # Overview of research program
│   ├── questions/      # Open research questions
│   ├── hypotheses/     # Testable claims with predictions
│   ├── papers/         # Paper drafts and outlines
│   └── synthesis/      # Cross-cutting analysis
│
├── references/         # Source papers (already exists)
│   ├── Calculus_Of_Emergence_Crutchfield/
│   └── 9907176v2/
│
└── record/             # Already exists: JOURNAL.md, etc.

experiments/            # Top-level experiments directory
├── registry.yaml       # Master catalog of all experiments
├── README.md           # How to run experiments
│
├── convergence/        # Each experiment is self-contained
│   ├── config.yaml     # Parameters and metadata
│   ├── run.py          # Execution script
│   ├── results/        # Output data (parquet, figures)
│   │   ├── data.parquet
│   │   └── figures/
│   └── report.md       # Summary and interpretation
│
├── noise_robustness/
├── paper_verification/
└── algorithm_comparison/
```

---

## Research Organization

### 1. Research Questions (`research/questions/`)

Open-ended questions we're trying to answer.

**Format**:
```markdown
# Q001: How does noise affect epsilon-machine inference?

## Status: Active

## Context
Real-world data always contains noise. Understanding robustness is critical.

## Sub-questions
- Q001a: At what noise level does CSSR fail?
- Q001b: Which algorithm is most robust?
- Q001c: Can we detect and correct for noise?

## Related
- Experiments: noise_robustness
- Hypotheses: H003, H004
```

---

### 2. Hypotheses (`research/hypotheses/`)

Specific, testable claims with predictions.

**Format**:
```markdown
# H003: CSSR state count increases with bit-flip noise

## Status: Untested | Supported | Refuted | Inconclusive

## Statement
At low noise levels (ε < 0.1), CSSR will infer MORE states than
the true process due to spurious pattern detection in the noise.

## Prediction
For Golden Mean process with ε = 0.05:
- True states: 2
- Predicted inferred states: 3-5 (over-splitting)

## Test
Experiment: noise_robustness/bitflip
Config: epsilon = [0, 0.01, 0.02, 0.05, 0.1]
Metric: mean(inferred_states) vs true_states

## Result
[To be filled after experiment]

## Implications
If supported: Need noise-aware parameter selection
If refuted: CSSR more robust than expected
```

---

### 3. Papers (`research/papers/`)

Paper drafts with clear provenance.

```
research/papers/
├── emic-framework/
│   ├── outline.md      # Structure and claims
│   ├── claims.yaml     # Map claims to supporting experiments
│   ├── figures/        # Generated figures (linked from experiments)
│   └── draft.tex       # LaTeX source
│
└── noise-robustness/
    └── ...
```

**Claims Registry** (`claims.yaml`):
```yaml
claims:
  - id: C1
    text: "CSSR correctly infers Golden Mean structure with n > 5000"
    evidence:
      - experiment: convergence/golden_mean
        result_file: results/state_count.parquet
        condition: "mean_states == 2 when n >= 5000"
    status: supported

  - id: C2
    text: "Statistical complexity matches theoretical values"
    evidence:
      - experiment: paper_verification/known_processes
        result_file: results/complexity.parquet
        condition: "abs(C_mu - C_mu_true) < 0.01"
```

---

## Experiment System

### Registry (`experiments/registry.yaml`)

```yaml
experiments:
  convergence:
    id: EXP-001
    title: "Convergence Analysis"
    description: "State count and complexity vs sample size"
    status: planned | running | complete | failed
    created: 2024-01-20
    last_run: null
    questions: [Q002]
    hypotheses: [H001, H002]

  noise_robustness:
    id: EXP-002
    title: "Noise Robustness Analysis"
    status: planned
    questions: [Q001]
    hypotheses: [H003, H004, H005]

  paper_verification:
    id: EXP-003
    title: "Paper Result Verification"
    description: "Reproduce Crutchfield/Shalizi theoretical results"
    status: planned
    questions: [Q003]
```

---

### Experiment Structure

Each experiment directory:

```
experiments/convergence/
├── config.yaml         # Full configuration
├── run.py              # Main execution script
├── analysis.py         # Post-processing
├── results/
│   ├── raw/            # Raw output files
│   ├── processed/      # Aggregated data
│   │   └── summary.parquet
│   └── figures/
│       ├── states_vs_n.png
│       └── cmu_convergence.png
└── report.md           # Human-readable summary
```

**Config Format** (`config.yaml`):
```yaml
experiment:
  id: EXP-001
  name: convergence
  version: 1.0.0

parameters:
  processes:
    - name: GoldenMean
      params: {p: 0.5}
    - name: EvenProcess
      params: {p: 0.5}
  sample_sizes: [100, 500, 1000, 5000, 10000, 50000]
  repetitions: 50
  algorithms:
    - name: CSSR
      config: {max_history: 5, significance: 0.001}

outputs:
  - name: state_count
    type: parquet
    schema:
      process: string
      n: int
      rep: int
      states: int

execution:
  parallel: true
  n_workers: 4
  seed_base: 42
```

---

### Results Storage

**Parquet for tabular data**:
- Fast, columnar storage
- Query-able with pandas/polars
- Typed schema
- Compresses well

**Example query**:
```python
import polars as pl

df = pl.read_parquet("experiments/convergence/results/summary.parquet")

# Find sample size needed for 95% correct state count
df.filter(
    (pl.col("process") == "GoldenMean") &
    (pl.col("correct_rate") >= 0.95)
).sort("n").head(1)
```

---

## Migration Plan

### Phase 1: Create Structure

Create directories:
```
.project/research/
.project/research/questions/
.project/research/hypotheses/
.project/research/papers/
experiments/
```

### Phase 2: Migrate Content

| Old Location | New Location |
|--------------|--------------|
| spec 009 (Research Paper) | research/papers/emic-framework/outline.md |
| spec 010 (Alt Inference) | specifications/010 (keep - it's design) |
| spec 011 (Experiments) | experiments/README.md + registry.yaml |
| spec 012 (Derivation) | research/papers/derivation/outline.md |
| spec 013 (Experiment Ideas) | research/questions/ + experiments/ |
| spec 014 (Quantum) | research/questions/Q-quantum.md |
| spec 015 (Multivariate) | research/questions/Q-multivariate.md |
| spec 016 (Performance) | specifications/016 (keep - it's design) |
| spec 017 (Paper Results) | experiments/paper_verification/ |
| spec 018 (Noise) | experiments/noise_robustness/ |

### Phase 3: Update Index

Update `specifications/000-index.md` to reflect infrastructure-only focus.

---

## Workflow

### Starting New Research

1. **Ask a question** → `research/questions/Q-xxx.md`
2. **Form hypotheses** → `research/hypotheses/H-xxx.md`
3. **Design experiment** → `experiments/xxx/config.yaml`
4. **Run experiment** → `python experiments/xxx/run.py`
5. **Analyze results** → `experiments/xxx/report.md`
6. **Update hypothesis** → Status: supported/refuted
7. **Synthesize paper** → `research/papers/xxx/`

### Traceability

Every paper claim links back to:
- Experiment that produced the evidence
- Specific result file and query
- Hypothesis it supports/refutes
- Original research question

---

## Implementation

### Runner Script

```python
# experiments/runner.py
"""Experiment runner with registry management."""

@dataclass
class ExperimentRunner:
    base_dir: Path = Path("experiments")

    def run(self, name: str, dry_run: bool = False) -> None:
        """Run an experiment by name."""
        config = self.load_config(name)
        self.update_registry(name, status="running")

        try:
            results = self.execute(config)
            self.save_results(name, results)
            self.update_registry(name, status="complete")
        except Exception as e:
            self.update_registry(name, status="failed", error=str(e))
            raise

    def status(self) -> pd.DataFrame:
        """Show status of all experiments."""
        registry = yaml.safe_load(open(self.base_dir / "registry.yaml"))
        return pd.DataFrame(registry["experiments"]).T
```

---

## Success Criteria

| Metric | Target |
|--------|--------|
| Specs are infrastructure-only | No research content in 001-008 |
| Research questions catalogued | All open questions in research/ |
| Experiments have configs | All experiments in registry |
| Results are queryable | Parquet files with schema |
| Paper claims traced | Every claim links to evidence |

---

## Dependencies

- `polars` or `pandas` — DataFrame operations
- `pyyaml` — Config parsing
- `pyarrow` — Parquet support
- Already installed or easy to add

---

## References

1. Wilson, G. et al. (2017). Good Enough Practices in Scientific Computing.
2. Sandve, G.K. et al. (2013). Ten Simple Rules for Reproducible Computational Research.
