"""
Source protocol and implementations for sequence generation.

Public API:
    - SequenceSource (Protocol)
    - SeededSource (Protocol)
    - StochasticSource (Base class)
    - GoldenMeanSource
    - EvenProcessSource
    - BiasedCoinSource
    - PeriodicSource
    - SequenceData
    - TakeN
    - SkipN
    - BitFlipNoise
"""

from emic.sources.base import StochasticSource
from emic.sources.empirical import SequenceData
from emic.sources.protocol import SeededSource, SequenceSource
from emic.sources.synthetic import (
    BiasedCoinSource,
    EvenProcessSource,
    GoldenMeanSource,
    PeriodicSource,
)
from emic.sources.transforms import BitFlipNoise, SkipN, TakeN

__all__ = [
    "BiasedCoinSource",
    "BitFlipNoise",
    "EvenProcessSource",
    "GoldenMeanSource",
    "PeriodicSource",
    "SeededSource",
    "SequenceData",
    "SequenceSource",
    "SkipN",
    "StochasticSource",
    "TakeN",
]
