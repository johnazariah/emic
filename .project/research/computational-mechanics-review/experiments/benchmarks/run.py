#!/usr/bin/env python3
"""
EXP-005: Algorithm Performance Benchmarks

Measures runtime and memory usage of inference algorithms
across different data sizes and processes.

Usage:
    uv run python experiments/benchmarks/run.py
"""

from __future__ import annotations

import gc
import json
import platform
import statistics
import sys
import time
import tracemalloc
from dataclasses import dataclass
from datetime import UTC, datetime
from itertools import islice
from pathlib import Path
from typing import TYPE_CHECKING, Any

import matplotlib.pyplot as plt
import numpy as np
import yaml

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from emic.inference.bsi import BSI, BSIConfig  # noqa: E402
from emic.inference.csm import CSM, CSMConfig  # noqa: E402
from emic.inference.cssr import CSSR, CSSRConfig  # noqa: E402
from emic.inference.nsd import NSD, NSDConfig  # noqa: E402
from emic.inference.spectral import Spectral, SpectralConfig  # noqa: E402
from emic.sources.synthetic.biased_coin import BiasedCoinSource  # noqa: E402
from emic.sources.synthetic.even_process import EvenProcessSource  # noqa: E402
from emic.sources.synthetic.golden_mean import GoldenMeanSource  # noqa: E402
from emic.sources.synthetic.periodic import PeriodicSource  # noqa: E402

if TYPE_CHECKING:
    from emic.types import Symbol


@dataclass
class BenchmarkResult:
    """Result from a single benchmark run."""

    algorithm: str
    process: str
    sample_size: int
    run_index: int
    runtime_seconds: float
    peak_memory_bytes: int
    num_states: int
    expected_states: int
    correct: bool  # Whether num_states matches expected
    success: bool
    error: str | None = None


@dataclass
class BenchmarkSummary:
    """Aggregated statistics for a benchmark configuration."""

    algorithm: str
    process: str
    sample_size: int
    expected_states: int
    repetitions: int
    runtime_mean: float
    runtime_std: float
    runtime_median: float
    runtime_min: float
    runtime_max: float
    memory_mean: float
    memory_std: float
    memory_median: float
    num_states_mode: int
    correct_rate: float  # Fraction that got correct state count
    success_rate: float


@dataclass
class SystemInfo:
    """Information about the system running benchmarks."""

    platform: str
    platform_release: str
    platform_version: str
    architecture: str
    processor: str
    cpu_count: int
    total_memory_gb: float
    python_version: str
    timestamp: str

    def summary(self) -> str:
        """Return a one-line summary for reports."""
        return (
            f"{self.platform} {self.architecture}, "
            f"{self.processor}, "
            f"{self.cpu_count} cores, "
            f"{self.total_memory_gb:.1f} GB RAM, "
            f"Python {self.python_version}"
        )


def get_system_info() -> SystemInfo:
    """Collect system information for reproducibility."""
    import os

    # Get total memory
    try:
        with Path("/proc/meminfo").open() as f:
            for line in f:
                if line.startswith("MemTotal:"):
                    # Value is in kB
                    mem_kb = int(line.split()[1])
                    total_memory_gb = mem_kb / (1024 * 1024)
                    break
            else:
                total_memory_gb = 0.0
    except (FileNotFoundError, ValueError):
        total_memory_gb = 0.0

    return SystemInfo(
        platform=platform.system(),
        platform_release=platform.release(),
        platform_version=platform.version(),
        architecture=platform.machine(),
        processor=platform.processor() or "unknown",
        cpu_count=os.cpu_count() or 1,
        total_memory_gb=total_memory_gb,
        python_version=platform.python_version(),
        timestamp=datetime.now(UTC).isoformat(),
    )


def generate_data(
    process_name: str, params: dict[str, Any], length: int, seed: int
) -> list[Symbol]:
    """Generate synthetic data for a given process."""
    if process_name == "golden_mean":
        source = GoldenMeanSource(p=params.get("p", 0.5), _seed=seed)
    elif process_name == "even_process":
        source = EvenProcessSource(p=params.get("p", 0.5), _seed=seed)
    elif process_name == "biased_coin":
        source = BiasedCoinSource(p=params.get("p", 0.5), _seed=seed)
    elif process_name == "periodic":
        pattern = tuple(params.get("pattern", [0, 1]))
        source = PeriodicSource(pattern=pattern)
    else:
        raise ValueError(f"Unknown process: {process_name}")

    return list(islice(source, length))


def create_algorithm(name: str, config: dict[str, Any]) -> Any:
    """Create an inference algorithm instance."""
    if name == "cssr":
        return CSSR(
            CSSRConfig(
                max_history=config.get("max_history", 5),
                significance=config.get("significance", 0.001),
            )
        )
    elif name == "spectral":
        return Spectral(
            SpectralConfig(
                max_history=config.get("max_history", 5),
                rank_threshold=config.get("rank_threshold", 0.01),
            )
        )
    elif name == "csm":
        return CSM(
            CSMConfig(
                history_length=config.get("history_length", 5),
                merge_threshold=config.get("merge_threshold", 0.1),
            )
        )
    elif name == "bsi":
        return BSI(
            BSIConfig(
                max_states=config.get("max_states", 5),
                n_samples=config.get("n_samples", 100),
            )
        )
    elif name == "nsd":
        return NSD(
            NSDConfig(
                max_states=config.get("max_states", 5),
                history_length=config.get("history_length", 5),
            )
        )
    else:
        raise ValueError(f"Unknown algorithm: {name}")


def run_single_benchmark(
    algorithm_name: str,
    algorithm_config: dict[str, Any],
    process_name: str,
    process_params: dict[str, Any],
    sample_size: int,
    run_index: int,
    seed: int,
    expected_states: int,
) -> BenchmarkResult:
    """Run a single benchmark iteration."""
    # Generate fresh data for each run
    run_seed = seed + run_index * 1000 + sample_size
    data = generate_data(process_name, process_params, sample_size, run_seed)
    alphabet = set(data)

    # Create algorithm
    algorithm = create_algorithm(algorithm_name, algorithm_config)

    # Force garbage collection before measurement
    gc.collect()

    # Measure memory and time
    tracemalloc.start()
    start_time = time.perf_counter()

    try:
        result = algorithm.infer(data, alphabet=alphabet)
        end_time = time.perf_counter()
        _, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        num_states = len(result.machine.states)
        correct = num_states == expected_states

        return BenchmarkResult(
            algorithm=algorithm_name,
            process=process_name,
            sample_size=sample_size,
            run_index=run_index,
            runtime_seconds=end_time - start_time,
            peak_memory_bytes=peak_memory,
            num_states=num_states,
            expected_states=expected_states,
            correct=correct,
            success=True,
            error=None,
        )
    except Exception as e:
        end_time = time.perf_counter()
        _, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        return BenchmarkResult(
            algorithm=algorithm_name,
            process=process_name,
            sample_size=sample_size,
            run_index=run_index,
            runtime_seconds=end_time - start_time,
            peak_memory_bytes=peak_memory,
            num_states=0,
            expected_states=expected_states,
            correct=False,
            success=False,
            error=str(e),
        )


def compute_summary(results: list[BenchmarkResult]) -> BenchmarkSummary:
    """Compute summary statistics from benchmark results."""
    successful = [r for r in results if r.success]
    correct = [r for r in results if r.correct]

    if not successful:
        return BenchmarkSummary(
            algorithm=results[0].algorithm,
            process=results[0].process,
            sample_size=results[0].sample_size,
            repetitions=len(results),
            runtime_mean=float("nan"),
            runtime_std=float("nan"),
            runtime_median=float("nan"),
            runtime_min=float("nan"),
            runtime_max=float("nan"),
            memory_mean=float("nan"),
            memory_std=float("nan"),
            memory_median=float("nan"),
            num_states_mode=0,
            expected_states=results[0].expected_states,
            success_rate=0.0,
            correct_rate=0.0,
        )

    runtimes = [r.runtime_seconds for r in successful]
    memories = [r.peak_memory_bytes for r in successful]
    states = [r.num_states for r in successful]

    return BenchmarkSummary(
        algorithm=results[0].algorithm,
        process=results[0].process,
        sample_size=results[0].sample_size,
        repetitions=len(results),
        runtime_mean=statistics.mean(runtimes),
        runtime_std=statistics.stdev(runtimes) if len(runtimes) > 1 else 0.0,
        runtime_median=statistics.median(runtimes),
        runtime_min=min(runtimes),
        runtime_max=max(runtimes),
        memory_mean=statistics.mean(memories),
        memory_std=statistics.stdev(memories) if len(memories) > 1 else 0.0,
        memory_median=statistics.median(memories),
        num_states_mode=max(set(states), key=states.count),
        expected_states=results[0].expected_states,
        success_rate=len(successful) / len(results),
        correct_rate=len(correct) / len(results),
    )


def format_bytes(n: float) -> str:
    """Format bytes as human-readable string."""
    for unit in ["B", "KB", "MB", "GB"]:
        if abs(n) < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


def format_time(seconds: float) -> str:
    """Format seconds as human-readable string."""
    if seconds < 0.001:
        return f"{seconds * 1_000_000:.1f} µs"
    elif seconds < 1:
        return f"{seconds * 1000:.1f} ms"
    else:
        return f"{seconds:.2f} s"


def run_benchmarks(config: dict[str, Any]) -> tuple[list[BenchmarkResult], list[BenchmarkSummary]]:
    """Run all benchmarks according to configuration."""
    bench_config = config["experiment"]["benchmark"]

    repetitions = bench_config["repetitions"]
    warmup_runs = bench_config.get("warmup_runs", 2)
    seed = bench_config["seed"]
    sample_sizes = bench_config["sample_sizes"]
    processes = bench_config["processes"]
    algorithms = bench_config["algorithms"]

    all_results: list[BenchmarkResult] = []
    all_summaries: list[BenchmarkSummary] = []

    total_configs = len(algorithms) * len(processes) * len(sample_sizes)
    current_config = 0

    for algo in algorithms:
        algo_name = algo["name"]
        algo_config = algo.get("config", {})

        for proc in processes:
            proc_name = proc["name"]
            proc_params = proc.get("params", {})
            expected_states = proc.get("expected_states", 0)

            for size in sample_sizes:
                current_config += 1
                print(
                    f"\n[{current_config}/{total_configs}] {algo_name} / {proc_name} / n={size:,}"
                )

                # Warmup runs (not recorded)
                print(f"  Warmup ({warmup_runs} runs)...", end=" ", flush=True)
                for i in range(warmup_runs):
                    run_single_benchmark(
                        algo_name,
                        algo_config,
                        proc_name,
                        proc_params,
                        size,
                        -i - 1,
                        seed,
                        expected_states,
                    )
                print("done")

                # Actual benchmark runs
                config_results: list[BenchmarkResult] = []
                for i in range(repetitions):
                    print(f"  Run {i + 1}/{repetitions}...", end=" ", flush=True)
                    result = run_single_benchmark(
                        algo_name,
                        algo_config,
                        proc_name,
                        proc_params,
                        size,
                        i,
                        seed,
                        expected_states,
                    )
                    config_results.append(result)
                    all_results.append(result)

                    status = "✓" if result.success else "✗"
                    correct_str = (
                        " ✓correct"
                        if result.correct
                        else f" ✗wrong({result.num_states}/{expected_states})"
                    )
                    print(f"{status} {format_time(result.runtime_seconds)}{correct_str}")

                # Compute summary for this configuration
                summary = compute_summary(config_results)
                all_summaries.append(summary)

                print(
                    f"  Summary: {format_time(summary.runtime_mean)} ± "
                    f"{format_time(summary.runtime_std)} "
                    f"(median: {format_time(summary.runtime_median)})"
                )
                print(f"  Memory:  {format_bytes(summary.memory_mean)}")
                print(f"  States:  {summary.num_states_mode} (expected: {summary.expected_states})")
                print(f"  Correct: {summary.correct_rate * 100:.0f}%")

    return all_results, all_summaries


def save_results(
    results: list[BenchmarkResult],
    summaries: list[BenchmarkSummary],
    system_info: SystemInfo,
    output_dir: Path,
) -> None:
    """Save benchmark results to files."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save system info
    with (output_dir / "system_info.json").open("w") as f:
        json.dump(system_info.__dict__, f, indent=2)

    # Save raw results as JSON
    results_data = [r.__dict__ for r in results]
    with (output_dir / "results.json").open("w") as f:
        json.dump(results_data, f, indent=2)

    # Save summaries as JSON
    summaries_data = [s.__dict__ for s in summaries]
    with (output_dir / "summaries.json").open("w") as f:
        json.dump(summaries_data, f, indent=2)

    # Save summaries as CSV for easy viewing
    csv_path = output_dir / "summaries.csv"
    with csv_path.open("w") as f:
        headers = list(summaries[0].__dict__.keys())
        f.write(",".join(headers) + "\n")
        for s in summaries:
            values = [str(getattr(s, h)) for h in headers]
            f.write(",".join(values) + "\n")

    # Try to save as parquet if pandas available
    try:
        import pandas as pd

        df_results = pd.DataFrame([r.__dict__ for r in results])
        df_results.to_parquet(output_dir / "results.parquet")

        df_summaries = pd.DataFrame([s.__dict__ for s in summaries])
        df_summaries.to_parquet(output_dir / "summaries.parquet")
    except ImportError:
        print("pandas not available, skipping parquet output")

    print(f"\nResults saved to {output_dir}/")


def generate_latex_table(
    summaries: list[BenchmarkSummary], system_info: SystemInfo, output_dir: Path
) -> None:
    """Generate LaTeX table for technical report."""
    # Group by sample size and algorithm
    latex_lines = [
        "% Auto-generated benchmark table",
        "% Generated: " + datetime.now(UTC).isoformat(),
        f"% System: {system_info.summary()}",
        r"\begin{table}[h]",
        r"\centering",
        r"\begin{tabular}{llrrr}",
        r"\toprule",
        r"\textbf{Algorithm} & \textbf{Process} & \textbf{N} & \textbf{Time (mean $\pm$ std)} & \textbf{Memory} \\",
        r"\midrule",
    ]

    for s in summaries:
        time_str = f"{s.runtime_mean:.3f}s $\\pm$ {s.runtime_std:.3f}s"
        mem_str = format_bytes(s.memory_mean)
        proc_name = s.process.replace("_", " ").title()
        latex_lines.append(
            f"{s.algorithm.upper()} & {proc_name} & {s.sample_size:,} & {time_str} & {mem_str} \\\\"
        )

    # Create caption with system info
    caption = (
        r"Inference time and memory usage by algorithm and data length. "
        f"Benchmarks run on {system_info.platform} {system_info.architecture}, "
        f"{system_info.cpu_count} cores, {system_info.total_memory_gb:.1f} GB RAM, "
        f"Python {system_info.python_version}."
    )

    latex_lines.extend(
        [
            r"\bottomrule",
            r"\end{tabular}",
            r"\caption{" + caption + r"}",
            r"\label{tab:benchmarks}",
            r"\end{table}",
        ]
    )

    output_path = output_dir / "benchmark_table.tex"
    with output_path.open("w") as f:
        f.write("\n".join(latex_lines))

    print(f"LaTeX table saved to {output_path}")


def generate_plots(summaries: list[BenchmarkSummary], output_dir: Path) -> None:
    """Generate publication-quality plots for the technical report."""
    figures_dir = output_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    # Set up matplotlib style for publication
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.size": 10,
            "axes.labelsize": 11,
            "axes.titlesize": 12,
            "legend.fontsize": 9,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "figure.figsize": (6, 4),
            "figure.dpi": 150,
            "savefig.dpi": 300,
            "savefig.bbox": "tight",
        }
    )

    # Group summaries by algorithm
    algorithms = sorted({s.algorithm for s in summaries})
    processes = sorted({s.process for s in summaries})
    sample_sizes = sorted({s.sample_size for s in summaries})

    # Color scheme (all 5 algorithms)
    colors = {
        "cssr": "#2962FF",
        "spectral": "#00C853",
        "csm": "#FF6D00",
        "bsi": "#AA00FF",
        "nsd": "#D50000",
    }
    markers = {"cssr": "o", "spectral": "s", "csm": "^", "bsi": "D", "nsd": "v"}

    # === Plot 1: Overall Runtime Scaling (log-log) - all algorithms ===
    fig, ax = plt.subplots()
    for algo in algorithms:
        algo_data = [s for s in summaries if s.algorithm == algo]
        # Average across processes for each sample size
        sizes = []
        times = []
        errors = []
        for size in sample_sizes:
            size_data = [s for s in algo_data if s.sample_size == size]
            if size_data:
                sizes.append(size)
                times.append(np.mean([s.runtime_mean for s in size_data]))
                errors.append(np.mean([s.runtime_std for s in size_data]))

        ax.errorbar(
            sizes,
            times,
            yerr=errors,
            label=algo.upper(),
            color=colors.get(algo, "gray"),
            marker=markers.get(algo, "o"),
            markersize=6,
            capsize=3,
            linewidth=1.5,
        )

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Sequence Length (N)")
    ax.set_ylabel("Runtime (seconds)")
    ax.set_title("Inference Runtime Scaling (All Algorithms)")
    ax.legend(loc="upper left")
    ax.grid(True, alpha=0.3, which="both")

    plt.savefig(figures_dir / "runtime_scaling.pdf")
    plt.savefig(figures_dir / "runtime_scaling.png")
    plt.close()
    print("  - runtime_scaling.pdf")

    # === Plot 2: Memory Scaling ===
    fig, ax = plt.subplots()
    for algo in algorithms:
        algo_data = [s for s in summaries if s.algorithm == algo]
        sizes = []
        mems = []
        for size in sample_sizes:
            size_data = [s for s in algo_data if s.sample_size == size]
            if size_data:
                sizes.append(size)
                mems.append(np.mean([s.memory_mean / 1024 for s in size_data]))  # KB

        ax.plot(
            sizes,
            mems,
            label=algo.upper(),
            color=colors.get(algo, "gray"),
            marker=markers.get(algo, "o"),
            markersize=6,
            linewidth=1.5,
        )

    ax.set_xscale("log")
    ax.set_xlabel("Sequence Length (N)")
    ax.set_ylabel("Peak Memory (KB)")
    ax.set_title("Memory Usage Scaling")
    ax.legend(loc="upper left")
    ax.grid(True, alpha=0.3)

    plt.savefig(figures_dir / "memory_scaling.pdf")
    plt.savefig(figures_dir / "memory_scaling.png")
    plt.close()
    print("  - memory_scaling.pdf")

    # === Plot 3: Correctness Rate by Algorithm/Process ===
    fig, ax = plt.subplots(figsize=(8, 5))

    x = np.arange(len(processes))
    width = 0.15
    n_algos = len(algorithms)
    offsets = np.linspace(-width * (n_algos - 1) / 2, width * (n_algos - 1) / 2, n_algos)

    for i, algo in enumerate(algorithms):
        correct_rates = []
        for proc in processes:
            # Aggregate correct_rate across all sample sizes
            data = [s for s in summaries if s.algorithm == algo and s.process == proc]
            if data:
                correct_rates.append(np.mean([s.correct_rate for s in data]) * 100)
            else:
                correct_rates.append(0)

        ax.bar(
            x + offsets[i],
            correct_rates,
            width * 0.9,
            label=algo.upper(),
            color=colors.get(algo, "gray"),
        )

    ax.set_xlabel("Process")
    ax.set_ylabel("Correctness Rate (%)")
    ax.set_title("Algorithm Correctness by Process (Averaged Over All Sample Sizes)")
    ax.set_xticks(x)
    ax.set_xticklabels([p.replace("_", " ").title() for p in processes], rotation=15, ha="right")
    ax.set_ylim(0, 110)
    ax.axhline(y=100, color="green", linestyle="--", alpha=0.5, label="_nolegend_")
    ax.legend(loc="upper right")
    ax.grid(True, alpha=0.3, axis="y")

    plt.tight_layout()
    plt.savefig(figures_dir / "correctness_by_process.pdf")
    plt.savefig(figures_dir / "correctness_by_process.png")
    plt.close()
    print("  - correctness_by_process.pdf")

    # === Plot 4: Per-Source Runtime Graphs (only correct results) ===
    # Create a separate figure for each process showing algorithms that achieve correctness
    for proc in processes:
        fig, ax = plt.subplots(figsize=(6, 4))

        proc_data = [s for s in summaries if s.process == proc]
        has_data = False

        for algo in algorithms:
            algo_proc_data = [s for s in proc_data if s.algorithm == algo]

            # Only include data points where correct_rate > 0
            sizes = []
            times = []
            errors = []
            for size in sample_sizes:
                size_data = [
                    s for s in algo_proc_data if s.sample_size == size and s.correct_rate > 0
                ]
                if size_data:
                    sizes.append(size)
                    times.append(size_data[0].runtime_mean)
                    errors.append(size_data[0].runtime_std)

            if sizes:
                has_data = True
                ax.errorbar(
                    sizes,
                    times,
                    yerr=errors,
                    label=algo.upper(),
                    color=colors.get(algo, "gray"),
                    marker=markers.get(algo, "o"),
                    markersize=6,
                    capsize=3,
                    linewidth=1.5,
                )

        if has_data:
            ax.set_xscale("log")
            ax.set_yscale("log")
            ax.set_xlabel("Sequence Length (N)")
            ax.set_ylabel("Runtime (seconds)")
            proc_title = proc.replace("_", " ").title()
            ax.set_title(f"{proc_title}: Runtime (Correct Results Only)")
            ax.legend(loc="upper left")
            ax.grid(True, alpha=0.3, which="both")

            plt.tight_layout()
            plt.savefig(figures_dir / f"runtime_{proc}.pdf")
            plt.savefig(figures_dir / f"runtime_{proc}.png")
            print(f"  - runtime_{proc}.pdf")
        else:
            print(f"  - Skipping {proc}: no correct results")

        plt.close()

    # === Plot 5: Algorithm Comparison Bar Chart (for largest N with correct results) ===
    largest_n = max(sample_sizes)
    fig, ax = plt.subplots(figsize=(8, 5))

    x = np.arange(len(processes))
    width = 0.15
    n_algos = len(algorithms)
    offsets = np.linspace(-width * (n_algos - 1) / 2, width * (n_algos - 1) / 2, n_algos)

    for i, algo in enumerate(algorithms):
        times = []
        errors = []
        for proc in processes:
            data = [
                s
                for s in summaries
                if s.algorithm == algo
                and s.process == proc
                and s.sample_size == largest_n
                and s.correct_rate > 0
            ]
            if data:
                times.append(data[0].runtime_mean)
                errors.append(data[0].runtime_std)
            else:
                times.append(0)  # No bar for incorrect/missing
                errors.append(0)

        ax.bar(
            x + offsets[i],
            times,
            width * 0.9,
            label=algo.upper(),
            color=colors.get(algo, "gray"),
            yerr=errors,
            capsize=3,
        )

    ax.set_xlabel("Process")
    ax.set_ylabel("Runtime (seconds)")
    ax.set_title(f"Algorithm Comparison (N = {largest_n:,}, Correct Results Only)")
    ax.set_xticks(x)
    ax.set_xticklabels([p.replace("_", " ").title() for p in processes], rotation=15, ha="right")
    ax.legend()
    ax.grid(True, alpha=0.3, axis="y")

    plt.tight_layout()
    plt.savefig(figures_dir / "algorithm_comparison.pdf")
    plt.savefig(figures_dir / "algorithm_comparison.png")
    plt.close()
    print("  - algorithm_comparison.pdf")

    # === Plot 6: Runtime by Process Panel (with correctness annotation) ===
    n_cols = min(len(processes), 2)
    n_rows = (len(processes) + n_cols - 1) // n_cols
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(5 * n_cols, 4 * n_rows), squeeze=False)
    axes = axes.flatten()

    for idx, proc in enumerate(processes):
        ax = axes[idx]
        for algo in algorithms:
            data = [s for s in summaries if s.algorithm == algo and s.process == proc]
            if data:
                # Mark correct vs incorrect
                correct_data = [s for s in data if s.correct_rate > 0]
                incorrect_data = [s for s in data if s.correct_rate == 0]

                if correct_data:
                    sizes = [s.sample_size for s in correct_data]
                    times = [s.runtime_mean for s in correct_data]
                    errors = [s.runtime_std for s in correct_data]
                    ax.errorbar(
                        sizes,
                        times,
                        yerr=errors,
                        label=algo.upper(),
                        color=colors.get(algo, "gray"),
                        marker=markers.get(algo, "o"),
                        markersize=5,
                        capsize=2,
                        linewidth=1.5,
                    )

                # Plot incorrect with X markers (faded)
                if incorrect_data:
                    sizes = [s.sample_size for s in incorrect_data]
                    times = [s.runtime_mean for s in incorrect_data]
                    ax.scatter(
                        sizes,
                        times,
                        color=colors.get(algo, "gray"),
                        marker="x",
                        s=50,
                        alpha=0.4,
                        label=f"{algo.upper()} (wrong)" if not correct_data else "_nolegend_",
                    )

        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel("N")
        ax.set_title(proc.replace("_", " ").title())
        ax.grid(True, alpha=0.3, which="both")
        ax.set_ylabel("Runtime (s)")
        ax.legend(loc="upper left", fontsize=7)

    # Hide any unused axes
    for idx in range(len(processes), len(axes)):
        axes[idx].set_visible(False)

    plt.suptitle("Runtime Scaling by Process (X = incorrect result)", y=1.02)
    plt.tight_layout()
    plt.savefig(figures_dir / "runtime_by_process.pdf")
    plt.savefig(figures_dir / "runtime_by_process.png")
    plt.close()
    print("  - runtime_by_process.pdf")

    print(f"\nFigures saved to {figures_dir}/")


def main() -> int:
    """Main entry point."""
    print("=" * 60)
    print("EXP-005: Algorithm Performance Benchmarks")
    print("=" * 60)

    # Load configuration
    config_path = Path(__file__).parent / "config.yaml"
    with config_path.open() as f:
        config = yaml.safe_load(f)

    # Collect system information
    system_info = get_system_info()
    print(f"\nSystem: {system_info.platform} {system_info.platform_release}")
    print(f"Python: {system_info.python_version}")
    print(f"Timestamp: {system_info.timestamp}")

    # Run benchmarks
    results, summaries = run_benchmarks(config)

    # Save results
    output_dir = Path(__file__).parent / config["experiment"]["output"]["results_dir"]
    save_results(results, summaries, system_info, output_dir)

    # Generate LaTeX table
    generate_latex_table(summaries, system_info, output_dir)

    # Generate plots
    print("\nGenerating plots...")
    generate_plots(summaries, output_dir)

    print("\n" + "=" * 60)
    print("Benchmarks complete!")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
