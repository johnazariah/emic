# Specification 023: Quantum Analysis Module

## Status
📝 Planning

## Overview

This specification defines the analysis functions for quantum epsilon-machines: computing quantum complexity measures, comparing classical and quantum models, and performing bidirectional (forward/reverse) analysis for causal asymmetry studies.

## Dependencies

- Spec 002: Core Types
- Spec 005: Analysis Protocol (classical measures)
- Spec 021: Quantum Core Types
- Spec 022: q-Machine Construction

---

## 1. Quantum Complexity Measures

### 1.1 Quantum Statistical Complexity

```python
def quantum_statistical_complexity(qm: QMachine[A]) -> float:
    """
    Cq = S(ρ) = -Tr(ρ log₂ ρ)
    
    Computed via Gram matrix eigenvalues for efficiency:
        Cq = -Σᵢ λᵢ log₂(λᵢ)
    
    This is the minimum quantum memory (in qubits) required
    for optimal prediction of the stochastic process.
    
    Properties:
        E ≤ Cq ≤ Cμ
        Cq = Cμ iff all quantum causal states are orthogonal
        Cq = E  iff full crypticity elimination achieved
    """
    return qm.gram_matrix.quantum_statistical_complexity()
```

### 1.2 Complexity Gap

```python
def complexity_gap(qm: QMachine[A]) -> float:
    """
    ΔC = Cμ - Cq
    
    The quantum memory advantage — information saved by using
    quantum rather than classical encoding.
    
    Properties:
        0 ≤ ΔC ≤ χ  (bounded by crypticity)
        ΔC = 0 iff no quantum advantage
        ΔC = χ iff full crypticity elimination
    """
```

### 1.3 Quantum Crypticity

```python
def quantum_crypticity(qm: QMachine[A]) -> float:
    """
    χ_q = Cq - E
    
    Quantum analogue of crypticity: information stored in the
    q-machine that is not accessible as past-future correlation.
    
    Properties:
        0 ≤ χ_q ≤ χ  (quantum crypticity ≤ classical)
        χ_q = 0 iff Cq = E (maximum quantum advantage)
    """
```

### 1.4 Advantage Ratio

```python
def advantage_ratio(qm: QMachine[A]) -> float:
    """
    Cq / Cμ — ratio of quantum to classical complexity.
    
    Properties:
        0 ≤ ratio ≤ 1
        ratio = 1 means no advantage
        ratio → 0 means large advantage
    
    Returns 1.0 if Cμ = 0 (trivial process).
    """
```

---

## 2. Quantum Analysis Summary

Extends the classical `AnalysisSummary`:

```python
@dataclass(frozen=True)
class QuantumAnalysisSummary:
    """Complete classical + quantum analysis of a stochastic process."""
    
    # Classical measures (from AnalysisSummary)
    statistical_complexity: float       # Cμ
    entropy_rate: float                 # hμ
    excess_entropy: float               # E
    crypticity: float                   # χ = Cμ - E
    
    # Quantum measures
    quantum_statistical_complexity: float  # Cq
    complexity_gap: float                  # Cμ - Cq
    quantum_crypticity: float              # Cq - E
    advantage_ratio: float                 # Cq / Cμ
    
    # Structural
    num_states: int
    alphabet_size: int
    gram_matrix_rank: int                  # Effective rank of Gram matrix
    truncation_depth: int                  # L used in construction
    
    # Validation
    cq_leq_cmu: bool                       # Cq ≤ Cμ satisfied?
    cq_geq_E: bool                         # Cq ≥ E satisfied?
    
    def to_dict(self) -> dict[str, float | int | bool]: ...
    
    def __str__(self) -> str:
        """
        Example output:
        
        ═══ Quantum Analysis: Golden Mean (p=0.5) ═══
        Classical:
          Cμ = 0.918 bits    hμ = 0.650 bits/sym
          E  = 0.811 bits    χ  = 0.107 bits
        Quantum:
          Cq = 0.834 bits    ΔC = 0.084 bits
          χq = 0.023 bits    Cq/Cμ = 0.909
        Bounds:
          E ≤ Cq ≤ Cμ : ✓
        """


def quantum_analyze(qm: QMachine[A]) -> QuantumAnalysisSummary:
    """
    Compute all classical and quantum measures for a q-machine.
    
    This is the main entry point for quantum analysis.
    """
```

---

## 3. Comparison Functions

### 3.1 Side-by-Side Comparison

```python
def compare_classical_quantum(
    machine: EpsilonMachine[A],
    qmachine: QMachine[A],
) -> dict[str, tuple[float, float]]:
    """
    Side-by-side comparison of classical and quantum measures.
    
    Returns:
        Dict mapping measure name to (classical_value, quantum_value)
        
    Example:
        {
            "statistical_complexity": (0.918, 0.834),
            "crypticity": (0.107, 0.023),
            "excess_entropy": (0.811, 0.811),  # Same for both
        }
    """
```

### 3.2 Process Family Sweep

```python
@dataclass(frozen=True)
class SweepResult:
    """Result of sweeping a parameter across a process family."""
    parameter_name: str
    parameter_values: tuple[float, ...]
    cmu_values: tuple[float, ...]
    cq_values: tuple[float, ...]
    E_values: tuple[float, ...]
    chi_values: tuple[float, ...]
    gap_values: tuple[float, ...]

def sweep_parameter(
    process_factory: Callable[[float], EpsilonMachine[A]],
    parameter_name: str,
    parameter_values: Sequence[float],
    qmachine_config: QMachineConfig = QMachineConfig(),
) -> SweepResult:
    """
    Sweep a parameter and compute classical + quantum measures at each point.
    
    Args:
        process_factory: Function that takes parameter value and returns ε-machine
        parameter_name: Name of the parameter (for labeling)
        parameter_values: Values to sweep over
        qmachine_config: Configuration for q-machine construction
    
    Example:
        results = sweep_parameter(
            process_factory=lambda p: GoldenMeanSource(p=p).true_machine,
            parameter_name="p",
            parameter_values=np.linspace(0.01, 0.99, 50),
        )
        # Plot results.cmu_values vs results.cq_values
    """
```

---

## 4. Bidirectional Analysis (Causal Asymmetry)

Causal asymmetry requires constructing both forward and reverse ε-machines.

### 4.1 Reverse Machine Construction

```python
def reverse_machine(machine: EpsilonMachine[A]) -> EpsilonMachine[A]:
    """
    Construct the reverse ε-machine (ε⁻-machine).
    
    The reverse machine predicts the past from the future.
    For a process with transition matrices T^(x), the reverse
    process has transitions:
    
        T̃^(x)_ij = πⱼ T^(x)_ji / πᵢ
    
    where π is the stationary distribution.
    
    Note: The reverse machine may have a different number of
    causal states than the forward machine.
    """
```

### 4.2 Bidirectional Analysis

```python
@dataclass(frozen=True)
class BidirectionalAnalysis:
    """Forward + reverse analysis for causal asymmetry study."""
    
    # Forward
    forward_cmu: float       # Cμ⁺
    forward_cq: float        # Cq⁺
    forward_chi: float       # χ⁺
    forward_num_states: int
    
    # Reverse
    reverse_cmu: float       # Cμ⁻
    reverse_cq: float        # Cq⁻
    reverse_chi: float       # χ⁻
    reverse_num_states: int
    
    # Shared
    excess_entropy: float    # E (same for forward and reverse)
    entropy_rate: float      # hμ (same for forward and reverse)
    
    # Asymmetry measures
    @property
    def classical_asymmetry(self) -> float:
        """ΔCμ = |Cμ⁺ - Cμ⁻|"""
        return abs(self.forward_cmu - self.reverse_cmu)
    
    @property
    def quantum_asymmetry(self) -> float:
        """ΔCq = |Cq⁺ - Cq⁻|"""
        return abs(self.forward_cq - self.reverse_cq)
    
    @property
    def asymmetry_restored(self) -> bool:
        """True if quantum model restores temporal symmetry."""
        return self.quantum_asymmetry < 1e-6 and self.classical_asymmetry > 1e-6
    
    def __str__(self) -> str:
        """
        Example:
        
        ═══ Bidirectional Analysis ═══
        Direction    Cμ      Cq      χ       States
        Forward      1.234   0.987   0.247   3
        Reverse      0.876   0.987   0.111   2
        
        Classical asymmetry:  ΔCμ = 0.358
        Quantum asymmetry:    ΔCq = 0.000
        Symmetry restored:    ✓
        """


def bidirectional_analyze(machine: EpsilonMachine[A]) -> BidirectionalAnalysis:
    """
    Full bidirectional analysis: forward + reverse, classical + quantum.
    
    1. Compute forward classical and quantum measures
    2. Construct reverse ε-machine
    3. Compute reverse classical and quantum measures
    4. Compute asymmetry measures
    """
```

---

## 5. Pipeline Integration

```python
# Full analysis pipeline
summary = (
    GoldenMeanSource(p=0.5)
    >> TakeN(100_000)
    >> SpectralInference(SpectralConfig())
    >> construct_qmachine
    >> quantum_analyze
)

# Bidirectional
bidir = (
    machine
    >> bidirectional_analyze
)

# Parameter sweep
sweep = sweep_parameter(
    process_factory=lambda p: GoldenMeanSource(p=p).true_machine,
    parameter_name="p",
    parameter_values=np.linspace(0.01, 0.99, 50),
)
```

---

## 6. Output Formats

Extend the existing output module:

### 6.1 LaTeX Table

```python
def quantum_summary_to_latex(summary: QuantumAnalysisSummary) -> str:
    """
    LaTeX table fragment:
    
    \begin{tabular}{lrr}
    \toprule
    Measure & Classical & Quantum \\
    \midrule
    Statistical complexity & 0.918 & 0.834 \\
    Crypticity & 0.107 & 0.023 \\
    \bottomrule
    \end{tabular}
    """
```

### 6.2 Sweep Plot Data

```python
def sweep_to_csv(result: SweepResult, path: Path) -> None:
    """Export sweep results as CSV for plotting."""

def sweep_to_latex_pgfplot(result: SweepResult) -> str:
    """Export sweep data as pgfplots-compatible LaTeX."""
```

---

## 7. Validation Requirements

| Test | Description |
|------|-------------|
| `test_advantage_ratio_bounds` | 0 ≤ Cq/Cμ ≤ 1 |
| `test_gap_bounded_by_crypticity` | ΔC ≤ χ |
| `test_quantum_crypticity_nonneg` | χ_q ≥ 0 |
| `test_summary_consistency` | All measures internally consistent |
| `test_reverse_machine_ergodic` | Reverse machine is valid ε-machine |
| `test_reverse_same_E` | Forward and reverse have same E |
| `test_reverse_same_hmu` | Forward and reverse have same hμ |
| `test_symmetric_process_no_asymmetry` | Symmetric processes have ΔCμ = 0 |
| `test_sweep_monotonicity` | Results change smoothly with parameter |
| `test_bidir_golden_mean` | Golden Mean bidirectional analysis |
| `test_bidir_even_process` | Even Process bidirectional analysis |
| `test_latex_output_valid` | LaTeX table compiles |
| `test_csv_roundtrip` | CSV export/import preserves values |

---

## 8. File Layout

```
src/emic/quantum/analysis/
├── __init__.py
├── measures.py            # quantum_statistical_complexity, gap, quantum_crypticity
├── summary.py             # QuantumAnalysisSummary, quantum_analyze
├── comparison.py          # compare_classical_quantum
├── sweep.py               # SweepResult, sweep_parameter
├── bidirectional.py       # reverse_machine, BidirectionalAnalysis, bidirectional_analyze
└── output.py              # LaTeX/CSV export for quantum results
```

---

*Depends on: Spec 002, Spec 005, Spec 021, Spec 022*
*Required by: Spec 024 (Decoherence Trajectories)*
