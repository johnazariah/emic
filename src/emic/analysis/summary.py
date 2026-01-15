"""Analysis summary for epsilon-machines."""

from __future__ import annotations

from collections.abc import Hashable
from dataclasses import dataclass
from typing import TYPE_CHECKING, TypeVar

from emic.analysis.measures import (
    entropy_rate,
    excess_entropy,
    state_count,
    statistical_complexity,
    topological_complexity,
    transition_count,
)

if TYPE_CHECKING:
    from emic.types import EpsilonMachine

A = TypeVar("A", bound=Hashable)


@dataclass(frozen=True)
class AnalysisSummary:
    """
    Complete analysis of an epsilon-machine.

    Contains all computed measures for easy access and display.
    """

    # Core measures
    statistical_complexity: float
    entropy_rate: float
    excess_entropy: float
    crypticity: float

    # Structural measures
    num_states: int
    num_transitions: int
    alphabet_size: int
    topological_complexity: float

    def to_dict(self) -> dict[str, float | int]:
        """Convert to dictionary for serialization."""
        return {
            "C_mu": self.statistical_complexity,
            "h_mu": self.entropy_rate,
            "E": self.excess_entropy,
            "chi": self.crypticity,
            "num_states": self.num_states,
            "num_transitions": self.num_transitions,
            "alphabet_size": self.alphabet_size,
            "C_top": self.topological_complexity,
        }

    def __str__(self) -> str:
        """Return human-readable summary."""
        return (
            f"ε-Machine Analysis:\n"
            f"  States: {self.num_states}\n"
            f"  Transitions: {self.num_transitions}\n"
            f"  Alphabet: {self.alphabet_size} symbols\n"
            f"  Statistical Complexity Cμ: {self.statistical_complexity:.4f} bits\n"
            f"  Entropy Rate hμ: {self.entropy_rate:.4f} bits/symbol\n"
            f"  Excess Entropy E: {self.excess_entropy:.4f} bits\n"
            f"  Crypticity χ: {self.crypticity:.4f} bits\n"
        )


def analyze(machine: EpsilonMachine[A]) -> AnalysisSummary:
    """
    Compute all standard measures for an epsilon-machine.

    Args:
        machine: The epsilon-machine to analyze

    Returns:
        AnalysisSummary with all computed measures

    Examples:
        >>> from emic.sources.synthetic.golden_mean import GoldenMeanSource
        >>> machine = GoldenMeanSource(p=0.5).true_machine
        >>> summary = analyze(machine)
        >>> summary.num_states
        2
    """
    c_mu = statistical_complexity(machine)
    h_mu = entropy_rate(machine)
    e = excess_entropy(machine)

    return AnalysisSummary(
        statistical_complexity=c_mu,
        entropy_rate=h_mu,
        excess_entropy=e,
        crypticity=c_mu - e,
        num_states=state_count(machine),
        num_transitions=transition_count(machine),
        alphabet_size=len(machine.alphabet),
        topological_complexity=topological_complexity(machine),
    )
