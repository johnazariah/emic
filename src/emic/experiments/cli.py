"""
Command-line interface for emic experiments.

Usage:
    emic-experiment --all              # Run all experiments
    emic-experiment accuracy           # Run specific experiment
    emic-experiment --quick            # Quick mode (reduced params)
    emic-experiment --list             # List available experiments
    emic-experiment --shard 0/4        # Run shard 0 of 4 (for parallelism)
    emic-experiment --parallel 4       # Auto-spawn 4 parallel processes
    emic-experiment --combine <dir>    # Combine shard results
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog="emic-experiment",
        description="Run emic experiments and collect performance data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    emic-experiment --all              Run all experiments
    emic-experiment accuracy           Run the accuracy experiment
    emic-experiment --quick            Quick mode (reduced sample sizes, skip slow algos)
    emic-experiment --list             List available experiments
    emic-experiment --config my.yaml   Use custom configuration

Output:
    Results are saved to experiments/runs/<timestamp>/
    A 'latest' symlink points to the most recent run.
        """,
    )

    # Experiment selection
    parser.add_argument(
        "experiment",
        nargs="?",
        help="Name of experiment to run (see --list for options)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all experiments",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        dest="list_experiments",
        help="List available experiments and exit",
    )

    # Configuration
    parser.add_argument(
        "--config",
        "-c",
        type=Path,
        help="Path to YAML configuration file",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        type=Path,
        help="Output directory for results (default: experiments/results)",
    )

    # Mode flags
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Quick mode: reduced sample sizes, skip slow algorithms",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Suppress progress output",
    )

    # Timeout
    parser.add_argument(
        "--timeout",
        type=int,
        default=120,
        help="Per-run timeout in seconds (default: 120)",
    )

    # Filtering
    parser.add_argument(
        "--algorithms",
        type=str,
        help="Comma-separated list of algorithms to run (e.g., --algorithms cssr,spectral)",
    )

    # Sharding and parallelism
    parser.add_argument(
        "--shard",
        type=str,
        metavar="M/N",
        help="Run shard M of N total shards (e.g., --shard 0/4)",
    )
    parser.add_argument(
        "--parallel",
        type=int,
        metavar="N",
        help="Spawn N parallel processes, each running a different shard",
    )
    parser.add_argument(
        "--combine",
        type=Path,
        metavar="DIR",
        help="Combine shard results in DIR into a single results file",
    )

    return parser


def list_experiments() -> None:
    """Print available experiments."""
    from emic.experiments.config import create_default_config

    config = create_default_config()

    print("Available experiments:")
    print()
    for exp in config.experiments:
        print(f"  {exp.name}")
        print(f"    {exp.description}")
        print(f"    Algorithms: {', '.join(exp.algorithms)}")
        print(f"    Processes: {', '.join(exp.processes)}")
        print(f"    Sample sizes: {exp.sample_sizes}")
        print(f"    Total runs: {exp.total_runs}")
        print()


def parse_shard(shard_str: str) -> tuple[int, int]:
    """
    Parse shard specification like '0/4' into (shard_index, total_shards).

    Args:
        shard_str: Shard specification in format "M/N"

    Returns:
        Tuple of (shard_index, total_shards)

    Raises:
        ValueError: If format is invalid
    """
    try:
        parts = shard_str.split("/")
        if len(parts) != 2:
            raise ValueError("Expected format M/N")
        shard_index = int(parts[0])
        total_shards = int(parts[1])
        if shard_index < 0 or total_shards <= 0:
            raise ValueError("Shard index must be >= 0, total must be > 0")
        if shard_index >= total_shards:
            raise ValueError(f"Shard index {shard_index} must be < total {total_shards}")
        return shard_index, total_shards
    except ValueError as e:
        raise ValueError(f"Invalid shard format '{shard_str}': {e}") from e


def run_parallel(args: argparse.Namespace, n_workers: int) -> int:
    """
    Spawn parallel worker processes, each running a different shard.

    Args:
        args: Parsed command-line arguments
        n_workers: Number of parallel workers to spawn

    Returns:
        Exit code (0 if all workers succeed)
    """
    import subprocess

    # Build base command from original args
    base_cmd = [sys.executable, "-m", "emic.experiments.cli"]

    if args.all:
        base_cmd.append("--all")
    elif args.experiment:
        base_cmd.append(args.experiment)

    if args.config:
        base_cmd.extend(["--config", str(args.config)])
    if args.output_dir:
        base_cmd.extend(["--output-dir", str(args.output_dir)])
    if args.quick:
        base_cmd.append("--quick")
    if args.quiet:
        base_cmd.append("--quiet")
    if args.timeout != 120:
        base_cmd.extend(["--timeout", str(args.timeout)])

    print(f"Spawning {n_workers} parallel workers...")

    # Spawn workers
    processes: list[subprocess.Popen] = []
    for i in range(n_workers):
        cmd = [*base_cmd, "--shard", f"{i}/{n_workers}"]
        print(f"  Worker {i}: {' '.join(cmd)}")
        proc = subprocess.Popen(cmd)
        processes.append(proc)

    # Wait for all workers
    print("\nWaiting for workers to complete...")
    exit_codes = [p.wait() for p in processes]

    # Report results
    failed = sum(1 for c in exit_codes if c != 0)
    if failed:
        print(f"\n{failed}/{n_workers} workers failed")
        return 1

    print(f"\nAll {n_workers} workers completed successfully")
    print("Use --combine <dir> to merge shard results")
    return 0


def combine_results(results_dir: Path) -> int:
    """
    Combine shard result files into a single results file.

    Args:
        results_dir: Directory containing shard files

    Returns:
        Exit code (0 on success)
    """
    from emic.experiments.schema import combine_shard_results

    try:
        output_path = combine_shard_results(results_dir)
        print(f"Combined results written to: {output_path}")
        return 0
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Error combining results: {e}")
        return 1


def main(argv: list[str] | None = None) -> int:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args(argv)

    # Handle --combine
    if args.combine:
        return combine_results(args.combine)

    # Handle --list
    if args.list_experiments:
        list_experiments()
        return 0

    # Validate arguments
    if not args.all and not args.experiment:
        parser.print_help()
        print("\nError: Specify --all or an experiment name")
        return 1

    # Handle --parallel
    if args.parallel:
        if args.shard:
            print("Error: Cannot use --parallel and --shard together")
            return 1
        return run_parallel(args, args.parallel)

    # Parse shard if specified
    shard_info: tuple[int, int] | None = None
    if args.shard:
        try:
            shard_info = parse_shard(args.shard)
        except ValueError as e:
            print(f"Error: {e}")
            return 1

    # Load configuration
    from emic.experiments.config import load_config
    from emic.experiments.runner import ExperimentRunner

    config = load_config(path=args.config, quick_mode=args.quick)

    # Create runner
    runner = ExperimentRunner(
        config=config,
        output_dir=str(args.output_dir) if args.output_dir else None,
        verbose=not args.quiet,
        shard=shard_info,
        algorithms_filter=args.algorithms.split(",") if args.algorithms else None,
    )

    # Run benchmarks
    try:
        if args.all:
            runner.run_all()
        else:
            runner.run_by_name(args.experiment)
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        return 130
    except KeyError as e:
        print(f"Error: {e}")
        print("Use --list to see available experiments")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
