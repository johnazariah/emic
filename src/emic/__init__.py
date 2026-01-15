"""
emic - Epsilon Machine Inference & Characterization

A Python framework for constructing and analyzing epsilon-machines
based on computational mechanics.
"""

from emic.pipeline import Pipeline, identity, tap
from emic.types import (
    Alphabet,
    CausalState,
    ConcreteAlphabet,
    Distribution,
    EpsilonMachine,
    EpsilonMachineBuilder,
    ProbabilityValue,
    StateId,
    Symbol,
    Transition,
)

__version__ = "0.0.1"
__all__ = [
    "Alphabet",
    "CausalState",
    "ConcreteAlphabet",
    "Distribution",
    "EpsilonMachine",
    "EpsilonMachineBuilder",
    "Pipeline",
    "ProbabilityValue",
    "StateId",
    "Symbol",
    "Transition",
    "identity",
    "tap",
]
