#!/usr/bin/env python3
"""
EXP-002: Noise Robustness Analysis

Measures how epsilon-machine inference algorithms behave under observation noise.

Usage:
    uv run python experiments/noise_robustness/run.py
"""

from __future__ import annotations

import gc
import json
import statistics
import sys
import time
import tracemalloc
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from itertools import islice
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import yaml

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from emic.analysis.measures import entropy_rate, statistical_complexity  # noqa: E402
from emic.inference.bsi import BSI, BSIConfig  # noqa: E402
from emic.inference.csm import CSM, CSMConfig  # noqa: E402
from emic.inference.cssr import CSSR, CSSRConfig  # noqa: E402
from emic.inference.nsd import NSD, NSDConfig  # noqa: E402
from emic.inference.spectral import Spectral, SpectralConfig  # noqa: E402
from emic.sources.synthetic.golden_mean import GoldenMeanSource  # noqa: E402
from emic.sources.transforms.noise import BitFlipNoise  # noqa: E402
from emic.sources.transforms.take import TakeN  # noqa: E402


@dataclass
class NoiseResult:
    """Result from a single noisy inference run."""

    algorithm: str
    epsilon: float  # Noise level
    rep: int
    num_states: int
    expected_states: int
    runtime_seconds: float
    success: bool
    error: str | None = None
    entropy_rate: float | None = None
    statistical_complexity: float | None = None


@dataclass
class NoiseSummary:
    """Aggregated statistics for one (algorithm, epsilon) combination."""

    algorithm: str
    epsilon: float
    repetitions: int
    states_mean: float
    states_std: float
    states_median: float
    correct_rate: float
    oversplit_rate: float  # States > expected
    undersplit_rate: float  # States < expected
    runtime_mean: float


def generate_noisy_data(
    p: float, sample_size: int, epsilon: float, seed: int
) -> tuple[list[int], frozenset[int]]:
    """Generate noisy Golden Mean data."""
    base_seed = seed
    noise_seed = seed + 1_000_000

    source = GoldenMeanSource(p=p, _seed=base_seed)

    if epsilon > 0:
        noisy = BitFlipNoise[int](flip_prob=epsilon, seed=noise_seed)(source)
        data = list(TakeN[int](sample_size)(noisy))
    else:
        data = list(islice(source, sample_size))

    alphabet = frozenset(data)
    return data, alphabet


def create_algorithm(name: str, config: dict[str, Any]) -> Any:
    """Create an inference algorithm instance."""
    if name == "CSSR":
        return CSSR(
            CSSRConfig(
                max_history=config.get("max_history", 5),
                significance=config.get("significance", 0.001),
            )
        )
    elif name == "Spectral":
        return Spectral(
            SpectralConfig(
                max_history=config.get("max_history", 5),
                rank_threshold=config.get("rank_threshold", 0.01),
            )
        )
    elif name == "CSM":
        return CSM(
            CSMConfig(
                history_length=config.get("history_length", 5),
                merge_threshold=config.get("merge_threshold", 0.1),
            )
        )
    elif name == "BSI":
        return BSI(
            BSIConfig(
                max_states=config.get("max_states", 5),
                n_samples=config.get("n_samples", 100),
                burnin=config.get("burnin", 200),
            )
        )
    elif name == "NSD":
        return NSD(
            NSDConfig(
                max_states=config.get("max_states", 5),
                history_length=config.get("history_length", 5),
            )
        )
    else:
        raise ValueError(f"Unknown algorithm: {name}")


def run_single(
    algorithm_name: str,
    algorithm_config: dict[str, Any],
    epsilon: float,
    sample_size: int,
    rep: int,
    seed_base: int,
    expected_states: int,
    process_p: float,
) -> NoiseResult:
    """Run a single noisy inference."""
    seed = seed_base + rep * 1000 + int(epsilon * 10000)
    data, alphabet = generate_noisy_data(process_p, sample_size, epsilon, seed)

    algorithm = create_algorithm(algorithm_name, algorithm_config)
    gc.collect()
    tracemalloc.start()
    start = time.perf_counter()

    try:
        result = algorithm.infer(data, alphabet=alphabet)
        elapsed = time.perf_counter() - start
        tracemalloc.stop()

        num_states = len(result.machine.states)

        # Compute complexity measures
        try:
            h_mu = entropy_rate(result.machine)
            c_mu = statistical_complexity(result.machine)
        except Exception:
            h_mu = None
            c_mu = None

        return NoiseResult(
            algorithm=algorithm_name,
            epsilon=epsilon,
            rep=rep,
            num_states=num_states,
            expected_states=expected_states,
            runtime_seconds=elapsed,
            success=True,
            entropy_rate=h_mu,
            statistical_complexity=c_mu,
        )
    except Exception as e:
        elapsed = time.perf_counter() - start
        tracemalloc.stop()
        return NoiseResult(
            algorithm=algorithm_name,
            epsilon=epsilon,
            rep=rep,
            num_states=0,
            expected_states=expected_states,
            runtime_seconds=elapsed,
            success=False,
            error=str(e),
        )


def compute_summary(results: list[NoiseResult]) -> NoiseSummary:
    """Compute summary statistics."""
    successful = [r for r in results if r.success]
    if not successful:
        return NoiseSummary(
            algorithm=results[0].algorithm,
            epsilon=results[0].epsilon,
            repetitions=len(results),
            states_mean=float("nan"),
            states_std=float("nan"),
            states_median=float("nan"),
            correct_rate=0.0,
            oversplit_rate=0.0,
            undersplit_rate=0.0,
            runtime_mean=float("nan"),
        )

    states = [r.num_states for r in successful]
    expected = successful[0].expected_states

    correct = sum(1 for s in states if s == expected)
    over = sum(1 for s in states if s > expected)
    under = sum(1 for s in states if s < expected)

    return NoiseSummary(
        algorithm=results[0].algorithm,
        epsilon=results[0].epsilon,
        repetitions=len(results),
        states_mean=statistics.mean(states),
        states_std=statistics.stdev(states) if len(states) > 1 else 0.0,
        states_median=statistics.median(states),
        correct_rate=correct / len(successful),
        oversplit_rate=over / len(successful),
        undersplit_rate=under / len(successful),
        runtime_mean=statistics.mean(r.runtime_seconds for r in successful),
    )


def plot_results(summaries: list[NoiseSummary], output_dir: Path) -> None:
    """Generate noise robustness plots."""
    # Group by algorithm
    by_algo: dict[str, list[NoiseSummary]] = {}
    for s in summaries:
        by_algo.setdefault(s.algorithm, []).append(s)

    # Sort each algorithm's summaries by epsilon
    for algo in by_algo:
        by_algo[algo].sort(key=lambda s: s.epsilon)

    # Plot 1: States vs Epsilon
    fig, ax = plt.subplots(figsize=(10, 6))
    for algo, sums in by_algo.items():
        eps = [s.epsilon for s in sums]
        means = [s.states_mean for s in sums]
        stds = [s.states_std for s in sums]
        ax.errorbar(eps, means, yerr=stds, marker="o", label=algo, capsize=3)

    ax.axhline(y=2, color="black", linestyle="--", label="True states")
    ax.set_xlabel("Noise Level (ε)")
    ax.set_ylabel("Inferred States")
    ax.set_title("Inferred States vs Observation Noise")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.savefig(output_dir / "states_vs_noise.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # Plot 2: Correct Rate vs Epsilon
    fig, ax = plt.subplots(figsize=(10, 6))
    for algo, sums in by_algo.items():
        eps = [s.epsilon for s in sums]
        rates = [s.correct_rate for s in sums]
        ax.plot(eps, rates, marker="o", label=algo)

    ax.set_xlabel("Noise Level (ε)")
    ax.set_ylabel("Correct Rate")
    ax.set_title("Algorithm Accuracy vs Observation Noise")
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_ylim(-0.05, 1.05)
    fig.savefig(output_dir / "accuracy_vs_noise.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    # Plot 3: Over/Under-splitting
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    for algo, sums in by_algo.items():
        eps = [s.epsilon for s in sums]
        over = [s.oversplit_rate for s in sums]
        under = [s.undersplit_rate for s in sums]
        axes[0].plot(eps, over, marker="o", label=algo)
        axes[1].plot(eps, under, marker="o", label=algo)

    axes[0].set_xlabel("Noise Level (ε)")
    axes[0].set_ylabel("Over-splitting Rate")
    axes[0].set_title("Over-splitting (states > true)")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    axes[1].set_xlabel("Noise Level (ε)")
    axes[1].set_ylabel("Under-splitting Rate")
    axes[1].set_title("Under-splitting (states < true)")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    fig.savefig(output_dir / "splitting_errors.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    """Run the noise robustness experiment."""
    # Load config
    config_path = Path(__file__).parent / "config.yaml"
    with config_path.open() as f:
        config = yaml.safe_load(f)

    # Parameters
    params = config["parameters"]
    process_p = params["process"]["params"]["p"]
    expected_states = params["process"]["true_states"]
    noise_levels = params["noise_models"][0]["levels"]
    sample_size = params["sample_size"]
    repetitions = params["repetitions"]
    seed_base = config["execution"]["seed_base"]

    # Algorithms
    algorithms = {a["name"]: a["config"] for a in params["algorithms"]}

    # Output directory
    output_dir = Path(__file__).parent / "results"
    output_dir.mkdir(exist_ok=True)

    # Run experiment
    all_results: list[NoiseResult] = []
    total_runs = len(algorithms) * len(noise_levels) * repetitions
    run_count = 0

    print("Running noise robustness experiment")
    print(f"  Process: GoldenMean(p={process_p})")
    print(f"  Sample size: {sample_size}")
    print(f"  Noise levels: {len(noise_levels)}")
    print(f"  Repetitions: {repetitions}")
    print(f"  Total runs: {total_runs}")
    print()

    for algo_name, algo_config in algorithms.items():
        print(f"{algo_name}:")
        for epsilon in noise_levels:
            for rep in range(repetitions):
                run_count += 1
                result = run_single(
                    algo_name,
                    algo_config,
                    epsilon,
                    sample_size,
                    rep,
                    seed_base,
                    expected_states,
                    process_p,
                )
                all_results.append(result)

                # Progress
                if run_count % 50 == 0:
                    pct = 100 * run_count / total_runs
                    print(f"  Progress: {run_count}/{total_runs} ({pct:.0f}%)")

        # Quick summary for this algorithm
        algo_results = [r for r in all_results if r.algorithm == algo_name]
        success_rate = sum(1 for r in algo_results if r.success) / len(algo_results)
        print(f"  Done. Success rate: {success_rate:.1%}")
        print()

    # Compute summaries
    summaries: list[NoiseSummary] = []
    for algo_name in algorithms:
        for epsilon in noise_levels:
            group = [r for r in all_results if r.algorithm == algo_name and r.epsilon == epsilon]
            if group:
                summaries.append(compute_summary(group))

    # Save results
    results_file = output_dir / "noise_results.json"
    with results_file.open("w") as f:
        json.dump(
            {
                "metadata": {
                    "experiment": "noise_robustness",
                    "timestamp": datetime.now(UTC).isoformat(),
                    "process": f"GoldenMean(p={process_p})",
                    "sample_size": sample_size,
                    "repetitions": repetitions,
                    "noise_levels": noise_levels,
                },
                "results": [asdict(r) for r in all_results],
                "summaries": [asdict(s) for s in summaries],
            },
            f,
            indent=2,
        )

    print(f"Results saved to {results_file}")

    # Generate plots
    plot_results(summaries, output_dir)
    print(f"Plots saved to {output_dir}")

    # Print summary table
    print("\n" + "=" * 70)
    print("NOISE ROBUSTNESS SUMMARY")
    print("=" * 70)
    print(f"{'Algorithm':<12} {'ε=0.0':<12} {'ε=0.05':<12} {'ε=0.1':<12} {'ε=0.2':<12}")
    print("-" * 70)

    key_levels = [0.0, 0.05, 0.1, 0.2]
    for algo_name in algorithms:
        row = f"{algo_name:<12}"
        for epsilon in key_levels:
            s = next(
                (x for x in summaries if x.algorithm == algo_name and x.epsilon == epsilon),
                None,
            )
            if s:
                row += f"{s.correct_rate:>6.0%} ±{s.states_std:.1f}  "
            else:
                row += f"{'N/A':<12}"
        print(row)

    print("=" * 70)


if __name__ == "__main__":
    main()
