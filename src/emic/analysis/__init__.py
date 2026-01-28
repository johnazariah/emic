"""Analysis module for epsilon-machine measures."""

from emic.analysis.measures import (
    block_entropy,
    crypticity,
    entropy_rate,
    excess_entropy,
    state_count,
    statistical_complexity,
    topological_complexity,
    transition_count,
)
from emic.analysis.quantum import (
    decoherence_trajectory,
    dephasing_channel,
    quantum_advantage,
    quantum_complexity,
    quantum_density_matrix,
    quantum_signal_states,
    signal_state_overlap,
)
from emic.analysis.summary import AnalysisSummary, analyze

__all__ = [
    # Summary
    "AnalysisSummary",
    "analyze",
    # Core measures
    "statistical_complexity",
    "entropy_rate",
    "excess_entropy",
    "crypticity",
    # Block measures
    "block_entropy",
    # Structural measures
    "state_count",
    "topological_complexity",
    "transition_count",
    # Quantum measures
    "quantum_complexity",
    "quantum_advantage",
    "quantum_density_matrix",
    "quantum_signal_states",
    "signal_state_overlap",
    "dephasing_channel",
    "decoherence_trajectory",
]
