"""
Process and algorithm registries.

Provides declarative registration of benchmark processes (data sources)
and inference algorithms with their configurations and ground truth.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable

    from emic.inference import InferenceAlgorithm
    from emic.sources import SequenceSource


T = TypeVar("T")


@dataclass(frozen=True)
class ProcessInfo:
    """
    Information about a benchmark process.

    Attributes:
        name: Unique identifier (e.g., "even_process")
        display_name: Human-readable name (e.g., "Even Process")
        factory: Callable that creates the source (takes seed as kwarg)
        ground_truth: Dictionary of expected metric values
        description: Optional description
        parameters: Parameters passed to the factory
    """

    name: str
    display_name: str
    factory: Callable[..., SequenceSource]
    ground_truth: dict[str, float] = field(default_factory=dict)
    description: str = ""
    parameters: dict[str, Any] = field(default_factory=dict)

    def create_source(self, seed: int = 42) -> SequenceSource:
        """Create a new source instance with the given seed."""
        return self.factory(_seed=seed, **self.parameters)


@dataclass(frozen=True)
class AlgorithmInfo:
    """
    Information about a benchmark algorithm.

    Attributes:
        name: Unique identifier (e.g., "cssr")
        display_name: Human-readable name (e.g., "CSSR")
        factory: Callable that creates the algorithm (takes config kwargs)
        config_class: Configuration class for the algorithm
        default_config: Default configuration parameters
        slow: Whether this algorithm is slow (skipped in --quick mode)
        description: Optional description
    """

    name: str
    display_name: str
    factory: Callable[..., InferenceAlgorithm]
    config_class: type | None = None
    default_config: dict[str, Any] = field(default_factory=dict)
    slow: bool = False
    description: str = ""

    def create_algorithm(self, **config_overrides: Any) -> InferenceAlgorithm:
        """Create a new algorithm instance with merged config."""
        config = {**self.default_config, **config_overrides}
        if self.config_class is not None:
            cfg = self.config_class(**config)
            return self.factory(cfg)
        return self.factory(**config)


class ProcessRegistry:
    """
    Registry of benchmark processes.

    Processes are data sources with known ground truth for validation.

    Example:
        registry = ProcessRegistry()
        registry.register(
            name="even_process",
            display_name="Even Process",
            factory=EvenProcessSource,
            parameters={"p": 0.5},
            ground_truth={"state_count": 2, "cmu": 1.0},
        )
        process = registry.get("even_process")
        source = process.create_source(seed=42)
    """

    def __init__(self) -> None:
        self._processes: dict[str, ProcessInfo] = {}

    def register(
        self,
        name: str,
        display_name: str,
        factory: Callable[..., SequenceSource],
        ground_truth: dict[str, float] | None = None,
        description: str = "",
        parameters: dict[str, Any] | None = None,
    ) -> None:
        """Register a process."""
        self._processes[name] = ProcessInfo(
            name=name,
            display_name=display_name,
            factory=factory,
            ground_truth=ground_truth or {},
            description=description,
            parameters=parameters or {},
        )

    def get(self, name: str) -> ProcessInfo:
        """Get a registered process by name."""
        if name not in self._processes:
            raise KeyError(f"Unknown process: {name}. Available: {list(self._processes)}")
        return self._processes[name]

    def list(self) -> list[str]:
        """List all registered process names."""
        return list(self._processes.keys())

    def all(self) -> list[ProcessInfo]:
        """Get all registered processes."""
        return list(self._processes.values())


class AlgorithmRegistry:
    """
    Registry of benchmark algorithms.

    Algorithms are inference methods that reconstruct epsilon-machines.

    Example:
        registry = AlgorithmRegistry()
        registry.register(
            name="cssr",
            display_name="CSSR",
            factory=CSSR,
            config_class=CSSRConfig,
            default_config={"max_history": 5, "significance": 0.05},
        )
        algo_info = registry.get("cssr")
        algo = algo_info.create_algorithm(max_history=8)
    """

    def __init__(self) -> None:
        self._algorithms: dict[str, AlgorithmInfo] = {}

    def register(
        self,
        name: str,
        display_name: str,
        factory: Callable[..., InferenceAlgorithm],
        config_class: type | None = None,
        default_config: dict[str, Any] | None = None,
        slow: bool = False,
        description: str = "",
    ) -> None:
        """Register an algorithm."""
        self._algorithms[name] = AlgorithmInfo(
            name=name,
            display_name=display_name,
            factory=factory,
            config_class=config_class,
            default_config=default_config or {},
            slow=slow,
            description=description,
        )

    def get(self, name: str) -> AlgorithmInfo:
        """Get a registered algorithm by name."""
        if name not in self._algorithms:
            raise KeyError(f"Unknown algorithm: {name}. Available: {list(self._algorithms)}")
        return self._algorithms[name]

    def list(self, include_slow: bool = True) -> list[str]:
        """List all registered algorithm names."""
        if include_slow:
            return list(self._algorithms.keys())
        return [name for name, info in self._algorithms.items() if not info.slow]

    def all(self, include_slow: bool = True) -> list[AlgorithmInfo]:
        """Get all registered algorithms."""
        if include_slow:
            return list(self._algorithms.values())
        return [info for info in self._algorithms.values() if not info.slow]


def create_default_process_registry() -> ProcessRegistry:
    """Create a registry with standard emic processes."""
    from emic.sources import BiasedCoinSource, EvenProcessSource, GoldenMeanSource

    registry = ProcessRegistry()

    registry.register(
        name="even_process",
        display_name="Even Process",
        factory=EvenProcessSource,
        parameters={"p": 0.5},
        ground_truth={"state_count": 2, "cmu": 1.0, "hmu": 1.0},
        description="Generates sequences where 1s always come in pairs",
    )

    registry.register(
        name="golden_mean",
        display_name="Golden Mean",
        factory=GoldenMeanSource,
        parameters={"p": 0.5},
        ground_truth={"state_count": 2, "cmu": 1.0, "hmu": 0.918296},
        description="No consecutive 1s allowed",
    )

    registry.register(
        name="biased_coin",
        display_name="Biased Coin",
        factory=BiasedCoinSource,
        parameters={"p": 0.7},
        ground_truth={"state_count": 1, "cmu": 0.0, "hmu": 0.881291},
        description="IID process with P(1)=0.7",
    )

    return registry


def create_default_algorithm_registry() -> AlgorithmRegistry:
    """Create a registry with standard emic algorithms."""
    from emic.inference import (
        BSI,
        CSM,
        CSSR,
        BSIConfig,
        CSMConfig,
        CSSRConfig,
        Spectral,
        SpectralConfig,
    )

    registry = AlgorithmRegistry()

    registry.register(
        name="cssr",
        display_name="CSSR",
        factory=CSSR,
        config_class=CSSRConfig,
        default_config={"max_history": 5, "significance": 0.05},
        slow=False,
        description="Causal State Splitting Reconstruction (Shalizi & Klinkner 2004)",
    )

    registry.register(
        name="spectral",
        display_name="Spectral",
        factory=Spectral,
        config_class=SpectralConfig,
        default_config={"rank": None, "max_history": 5},
        slow=False,
        description="Spectral learning algorithm (Hsu et al. 2012)",
    )

    registry.register(
        name="csm",
        display_name="CSM",
        factory=CSM,
        config_class=CSMConfig,
        default_config={"history_length": 5},
        slow=False,
        description="Causal State Merging",
    )

    registry.register(
        name="bsi",
        display_name="BSI",
        factory=BSI,
        config_class=BSIConfig,
        default_config={"max_states": 10, "n_samples": 100, "burnin": 20},
        slow=True,
        description="Bayesian Structural Inference (slow, thorough)",
    )

    return registry


# Module-level default registries
_default_process_registry: ProcessRegistry | None = None
_default_algorithm_registry: AlgorithmRegistry | None = None


def get_process_registry() -> ProcessRegistry:
    """Get the default process registry (lazy-initialized)."""
    global _default_process_registry
    if _default_process_registry is None:
        _default_process_registry = create_default_process_registry()
    return _default_process_registry


def get_algorithm_registry() -> AlgorithmRegistry:
    """Get the default algorithm registry (lazy-initialized)."""
    global _default_algorithm_registry
    if _default_algorithm_registry is None:
        _default_algorithm_registry = create_default_algorithm_registry()
    return _default_algorithm_registry
