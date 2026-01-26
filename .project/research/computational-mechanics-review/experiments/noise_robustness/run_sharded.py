#!/usr/bin/env python3
"""
EXP-002: Noise Robustness Analysis (Sharded Version)

Run individual algorithms with timeouts and incremental saving.

Usage:
    # Run single algorithm
    uv run python experiments/noise_robustness/run_sharded.py --algorithm CSSR

    # Run all fast algorithms
    uv run python experiments/noise_robustness/run_sharded.py --algorithm CSSR CSM Spectral NSD

    # Run BSI with timeout
    uv run python experiments/noise_robustness/run_sharded.py --algorithm BSI --timeout 180

    # Combine results from shards
    uv run python experiments/noise_robustness/run_sharded.py --combine
"""

from __future__ import annotations

import argparse
import gc
import json
import signal
import statistics
import sys
import time
import tracemalloc
from contextlib import contextmanager
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

from emic.inference.bsi import BSI, BSIConfig  # noqa: E402
from emic.inference.csm import CSM, CSMConfig  # noqa: E402
from emic.inference.cssr import CSSR, CSSRConfig  # noqa: E402
from emic.inference.nsd import NSD, NSDConfig  # noqa: E402
from emic.inference.spectral import Spectral, SpectralConfig  # noqa: E402
from emic.sources.synthetic.golden_mean import GoldenMeanSource  # noqa: E402
from emic.sources.transforms.noise import BitFlipNoise  # noqa: E402
from emic.sources.transforms.take import TakeN  # noqa: E402


class TimeoutError(Exception):
    """Raised when operation times out."""

    pass


@contextmanager
def timeout(seconds: int):
    """Context manager for timeout (Unix only)."""

    def handler(signum, frame):
        raise TimeoutError(f"Timed out after {seconds}s")

    old_handler = signal.signal(signal.SIGALRM, handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)


@dataclass
class NoiseResult:
    """Result from a single noisy inference run."""

    algorithm: str
    epsilon: float
    rep: int
    num_states: int
    expected_states: int
    runtime_seconds: float
    success: bool
    error: str | None = None
    timed_out: bool = False


@dataclass
class NoiseSummary:
    """Aggregated statistics for one (algorithm, epsilon) combination."""

    algorithm: str
    epsilon: float
    repetitions: int
    completed: int
    states_mean: float
    states_std: float
    states_median: float
    correct_rate: float
    oversplit_rate: float
    undersplit_rate: float
    runtime_mean: float
    timeout_rate: float


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
    timeout_seconds: int | None = None,
) -> NoiseResult:
    """Run a single noisy inference with optional timeout."""
    seed = seed_base + rep * 1000 + int(epsilon * 10000)
    data, alphabet = generate_noisy_data(process_p, sample_size, epsilon, seed)

    algorithm = create_algorithm(algorithm_name, algorithm_config)
    gc.collect()
    tracemalloc.start()
    start = time.perf_counter()

    try:
        if timeout_seconds:
            with timeout(timeout_seconds):
                result = algorithm.infer(data, alphabet=alphabet)
        else:
            result = algorithm.infer(data, alphabet=alphabet)

        elapsed = time.perf_counter() - start
        tracemalloc.stop()

        num_states = len(result.machine.states)
        return NoiseResult(
            algorithm=algorithm_name,
            epsilon=epsilon,
            rep=rep,
            num_states=num_states,
            expected_states=expected_states,
            runtime_seconds=elapsed,
            success=True,
        )
    except TimeoutError:
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
            error="timeout",
            timed_out=True,
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
    timed_out = [r for r in results if r.timed_out]

    if not successful:
        return NoiseSummary(
            algorithm=results[0].algorithm,
            epsilon=results[0].epsilon,
            repetitions=len(results),
            completed=0,
            states_mean=float("nan"),
            states_std=float("nan"),
            states_median=float("nan"),
            correct_rate=0.0,
            oversplit_rate=0.0,
            undersplit_rate=0.0,
            runtime_mean=float("nan"),
            timeout_rate=len(timed_out) / len(results),
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
        completed=len(successful),
        states_mean=statistics.mean(states),
        states_std=statistics.stdev(states) if len(states) > 1 else 0.0,
        states_median=statistics.median(states),
        correct_rate=correct / len(successful),
        oversplit_rate=over / len(successful),
        undersplit_rate=under / len(successful),
        runtime_mean=statistics.mean(r.runtime_seconds for r in successful),
        timeout_rate=len(timed_out) / len(results),
    )


def save_shard(
    algo_name: str,
    results: list[NoiseResult],
    summaries: list[NoiseSummary],
    output_dir: Path,
    metadata: dict,
) -> None:
    """Save results for a single algorithm shard."""
    shard_file = output_dir / f"shard_{algo_name.lower()}.json"
    with shard_file.open("w") as f:
        json.dump(
            {
                "metadata": {
                    **metadata,
                    "algorithm": algo_name,
                    "timestamp": datetime.now(UTC).isoformat(),
                },
                "results": [asdict(r) for r in results],
                "summaries": [asdict(s) for s in summaries],
            },
            f,
            indent=2,
        )
    print(f"  Shard saved to {shard_file}")


def run_algorithm(
    algo_name: str,
    algo_config: dict[str, Any],
    noise_levels: list[float],
    sample_size: int,
    repetitions: int,
    seed_base: int,
    expected_states: int,
    process_p: float,
    output_dir: Path,
    timeout_seconds: int | None = None,
    block_timeout: int | None = None,
) -> tuple[list[NoiseResult], list[NoiseSummary]]:
    """Run experiment for a single algorithm."""
    results: list[NoiseResult] = []
    total_runs = len(noise_levels) * repetitions
    run_count = 0

    print(f"\n{algo_name}:")
    print(f"  Runs: {total_runs} ({len(noise_levels)} levels × {repetitions} reps)")
    if timeout_seconds:
        print(f"  Per-run timeout: {timeout_seconds}s")
    if block_timeout:
        print(f"  Per-block timeout: {block_timeout}s")

    block_start = time.perf_counter()

    for epsilon in noise_levels:
        epsilon_start = time.perf_counter()
        epsilon_results = []

        for rep in range(repetitions):
            # Check block timeout
            if block_timeout:
                elapsed_block = time.perf_counter() - block_start
                if elapsed_block > block_timeout:
                    print(f"  Block timeout reached after {elapsed_block:.0f}s")
                    print(f"  Completed: {run_count}/{total_runs} runs")
                    # Save partial results
                    summaries = []
                    for eps in noise_levels:
                        group = [r for r in results if r.epsilon == eps]
                        if group:
                            summaries.append(compute_summary(group))
                    return results, summaries

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
                timeout_seconds,
            )
            results.append(result)
            epsilon_results.append(result)

        # Summary for this epsilon
        elapsed_eps = time.perf_counter() - epsilon_start
        successes = sum(1 for r in epsilon_results if r.success)
        timeouts = sum(1 for r in epsilon_results if r.timed_out)
        avg_states = (
            statistics.mean(r.num_states for r in epsilon_results if r.success) if successes else 0
        )

        print(
            f"  ε={epsilon:.2f}: {successes}/{repetitions} ok, "
            f"{timeouts} timeouts, "
            f"mean_states={avg_states:.1f}, "
            f"time={elapsed_eps:.1f}s"
        )

    # Compute all summaries
    summaries = []
    for epsilon in noise_levels:
        group = [r for r in results if r.epsilon == epsilon]
        if group:
            summaries.append(compute_summary(group))

    # Final stats
    success_rate = sum(1 for r in results if r.success) / len(results)
    timeout_rate = sum(1 for r in results if r.timed_out) / len(results)
    print(f"  Done. Success: {success_rate:.1%}, Timeouts: {timeout_rate:.1%}")

    return results, summaries


def combine_shards(output_dir: Path) -> None:
    """Combine all shard files into a single results file."""
    shard_files = list(output_dir.glob("shard_*.json"))
    if not shard_files:
        print("No shard files found")
        return

    all_results = []
    all_summaries = []
    metadata = None

    for shard_file in sorted(shard_files):
        print(f"Loading {shard_file.name}...")
        with shard_file.open() as f:
            data = json.load(f)

        if metadata is None:
            metadata = {
                k: v for k, v in data["metadata"].items() if k not in ["algorithm", "timestamp"]
            }

        all_results.extend(data["results"])
        all_summaries.extend(data["summaries"])

    # Save combined
    combined_file = output_dir / "noise_results.json"
    with combined_file.open("w") as f:
        json.dump(
            {
                "metadata": {
                    **metadata,
                    "timestamp": datetime.now(UTC).isoformat(),
                    "combined_from": [f.name for f in shard_files],
                },
                "results": all_results,
                "summaries": all_summaries,
            },
            f,
            indent=2,
        )

    print(f"\nCombined {len(shard_files)} shards -> {combined_file}")
    print(f"  Total results: {len(all_results)}")
    print(f"  Total summaries: {len(all_summaries)}")


def plot_results(summaries: list[NoiseSummary], output_dir: Path) -> None:
    """Generate noise robustness plots."""
    # Group by algorithm
    by_algo: dict[str, list[NoiseSummary]] = {}
    for s in summaries:
        by_algo.setdefault(s.algorithm, []).append(s)

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

    # Plot 2: Correct Rate
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

    print(f"Plots saved to {output_dir}")


def main() -> None:
    """Run the noise robustness experiment."""
    parser = argparse.ArgumentParser(description="Noise robustness experiment (sharded)")
    parser.add_argument(
        "--algorithm",
        "-a",
        nargs="+",
        help="Algorithm(s) to run: CSSR, CSM, BSI, Spectral, NSD",
    )
    parser.add_argument(
        "--timeout",
        "-t",
        type=int,
        default=None,
        help="Timeout per individual run in seconds",
    )
    parser.add_argument(
        "--block-timeout",
        "-b",
        type=int,
        default=None,
        help="Timeout for entire algorithm block in seconds (saves partial results)",
    )
    parser.add_argument(
        "--combine",
        "-c",
        action="store_true",
        help="Combine existing shard files into final results",
    )
    parser.add_argument(
        "--plot",
        "-p",
        action="store_true",
        help="Generate plots from combined results",
    )
    args = parser.parse_args()

    # Load config
    config_path = Path(__file__).parent / "config.yaml"
    with config_path.open() as f:
        config = yaml.safe_load(f)

    output_dir = Path(__file__).parent / "results"
    output_dir.mkdir(exist_ok=True)

    # Combine mode
    if args.combine:
        combine_shards(output_dir)
        return

    # Plot mode
    if args.plot:
        results_file = output_dir / "noise_results.json"
        if not results_file.exists():
            print("No results file. Run --combine first.")
            return
        with results_file.open() as f:
            data = json.load(f)
        summaries = [NoiseSummary(**s) for s in data["summaries"]]
        plot_results(summaries, output_dir)
        return

    # Run mode
    if not args.algorithm:
        print("Specify algorithm(s) with --algorithm, or use --combine/--plot")
        print("Available: CSSR, CSM, BSI, Spectral, NSD")
        return

    # Parameters
    params = config["parameters"]
    process_p = params["process"]["params"]["p"]
    expected_states = params["process"]["true_states"]
    noise_levels = params["noise_models"][0]["levels"]
    sample_size = params["sample_size"]
    repetitions = params["repetitions"]
    seed_base = config["execution"]["seed_base"]

    # Algorithm configs from file
    algo_configs = {a["name"]: a["config"] for a in params["algorithms"]}

    metadata = {
        "experiment": "noise_robustness",
        "process": f"GoldenMean(p={process_p})",
        "sample_size": sample_size,
        "repetitions": repetitions,
        "noise_levels": noise_levels,
    }

    print("Noise Robustness Experiment (Sharded)")
    print(f"  Process: GoldenMean(p={process_p})")
    print(f"  Sample size: {sample_size}")
    print(f"  Noise levels: {noise_levels}")
    print(f"  Repetitions: {repetitions}")

    for algo_name in args.algorithm:
        if algo_name not in algo_configs:
            print(f"Unknown algorithm: {algo_name}")
            continue

        results, summaries = run_algorithm(
            algo_name=algo_name,
            algo_config=algo_configs[algo_name],
            noise_levels=noise_levels,
            sample_size=sample_size,
            repetitions=repetitions,
            seed_base=seed_base,
            expected_states=expected_states,
            process_p=process_p,
            output_dir=output_dir,
            timeout_seconds=args.timeout,
            block_timeout=args.block_timeout,
        )

        save_shard(algo_name, results, summaries, output_dir, metadata)


if __name__ == "__main__":
    main()
