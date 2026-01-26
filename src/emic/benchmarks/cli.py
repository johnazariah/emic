"""
Command-line interface for emic benchmarks.

Usage:
    emic-benchmark --all              # Run all experiments
    emic-benchmark accuracy           # Run specific experiment
    emic-benchmark --quick            # Quick mode (reduced params)
    emic-benchmark --list             # List available experiments
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog="emic-benchmark",
        description="Run emic benchmarks and collect performance data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    emic-benchmark --all              Run all experiments
    emic-benchmark accuracy           Run the accuracy experiment
    emic-benchmark --quick            Quick mode (reduced sample sizes, skip slow algos)
    emic-benchmark --list             List available experiments
    emic-benchmark --config my.yaml   Use custom configuration

Output:
    Results are saved to experiments/results/<timestamp>/
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

    return parser


def list_experiments() -> None:
    """Print available experiments."""
    from emic.benchmarks.config import create_default_config

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


def main(argv: list[str] | None = None) -> int:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args(argv)

    # Handle --list
    if args.list_experiments:
        list_experiments()
        return 0

    # Validate arguments
    if not args.all and not args.experiment:
        parser.print_help()
        print("\nError: Specify --all or an experiment name")
        return 1

    # Load configuration
    from emic.benchmarks.config import load_config
    from emic.benchmarks.runner import BenchmarkRunner

    config = load_config(path=args.config, quick_mode=args.quick)

    # Create runner
    runner = BenchmarkRunner(
        config=config,
        output_dir=str(args.output_dir) if args.output_dir else None,
        verbose=not args.quiet,
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
