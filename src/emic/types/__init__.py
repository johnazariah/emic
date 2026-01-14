"""
Core types for epsilon-machine representation.

Public API:
    - Symbol (TypeVar)
    - Alphabet (Protocol)
    - ConcreteAlphabet
    - Distribution
    - Transition
    - CausalState
    - EpsilonMachine
    - EpsilonMachineBuilder
"""

from emic.types.alphabet import Alphabet, ConcreteAlphabet, Symbol
from emic.types.machine import EpsilonMachine, EpsilonMachineBuilder
from emic.types.probability import Distribution, ProbabilityValue
from emic.types.states import CausalState, StateId, Transition

__all__ = [
    "Alphabet",
    "CausalState",
    "ConcreteAlphabet",
    "Distribution",
    "EpsilonMachine",
    "EpsilonMachineBuilder",
    "ProbabilityValue",
    "StateId",
    "Symbol",
    "Transition",
]
