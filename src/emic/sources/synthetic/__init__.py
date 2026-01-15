"""Synthetic stochastic sources."""

from emic.sources.synthetic.biased_coin import BiasedCoinSource
from emic.sources.synthetic.even_process import EvenProcessSource
from emic.sources.synthetic.golden_mean import GoldenMeanSource
from emic.sources.synthetic.periodic import PeriodicSource

__all__ = [
    "BiasedCoinSource",
    "EvenProcessSource",
    "GoldenMeanSource",
    "PeriodicSource",
]
