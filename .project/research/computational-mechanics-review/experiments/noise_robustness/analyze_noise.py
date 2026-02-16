#!/usr/bin/env python3
"""
Analyze noise robustness results and generate LaTeX tables/figures.

Outputs:
    - generated/tab-noise-robustness.tex: Main results table
    - generated/noise-data.tex: LaTeX macros for prose
    - results/states_vs_noise.pdf: Figure (converted from PNG)
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def load_results() -> pd.DataFrame:
    """Load noise robustness results from JSON."""
    results_dir = Path(__file__).parent / "results"

    # Try new file with measures first, fall back to original
    new_file = results_dir / "noise_with_measures.json"
    old_file = results_dir / "noise_results.json"

    if new_file.exists():
        results_file = new_file
    elif old_file.exists():
        results_file = old_file
    else:
        raise FileNotFoundError(
            f"Results file not found in {results_dir}\nRun the experiment first with run.py"
        )

    with results_file.open() as f:
        data = json.load(f)

    return pd.DataFrame(data["results"])


def compute_summaries(df: pd.DataFrame) -> pd.DataFrame:
    """Compute summary statistics per algorithm and noise level."""
    summaries = []

    for algo in df["algorithm"].unique():
        for eps in sorted(df["epsilon"].unique()):
            group = df[(df["algorithm"] == algo) & (df["epsilon"] == eps)]
            successful = group[group["success"]]

            if len(successful) > 0:
                states = successful["num_states"]
                expected = successful["expected_states"].iloc[0]
                correct = (states == expected).sum()
                over = (states > expected).sum()
                under = (states < expected).sum()

                summaries.append(
                    {
                        "algorithm": algo,
                        "epsilon": eps,
                        "n_runs": len(group),
                        "n_success": len(successful),
                        "states_mean": states.mean(),
                        "states_std": states.std() if len(states) > 1 else 0,
                        "correct_rate": correct / len(successful),
                        "oversplit_rate": over / len(successful),
                        "undersplit_rate": under / len(successful),
                        "runtime_mean": successful["runtime_seconds"].mean(),
                    }
                )

    return pd.DataFrame(summaries)


def write_latex(filename: str, content: str, output_dir: str = "generated") -> None:
    """Write LaTeX content to generated directory."""
    # Support both tutorial and technical-report output dirs
    base = Path(__file__).parent.parent.parent

    for doc in ["paper-tutorial", "paper-technical"]:
        path = base / doc / output_dir / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        print(f"  Written: {path}")


def generate_noise_table(summaries: pd.DataFrame) -> None:
    """Generate the main noise robustness table."""
    # Key noise levels to show
    key_levels = [0.0, 0.05, 0.1, 0.2, 0.5]
    algorithms = ["CSSR", "CSM", "Spectral", "NSD", "BSI"]

    # Build table rows
    rows = []
    for algo in algorithms:
        algo_data = summaries[summaries["algorithm"] == algo]
        cols = [algo]

        for eps in key_levels:
            row = algo_data[algo_data["epsilon"] == eps]
            if len(row) > 0:
                mean = row["states_mean"].iloc[0]
                std = row["states_std"].iloc[0]
                cols.append(f"{mean:.1f}$\\pm${std:.1f}")
            else:
                cols.append("---")

        rows.append(" & ".join(cols) + r" \\")

    latex = (
        r"""\begin{tabular}{lccccc}
\toprule
\textbf{Algorithm} & \textbf{$\varepsilon=0$} & \textbf{$\varepsilon=0.05$} & \textbf{$\varepsilon=0.1$} & \textbf{$\varepsilon=0.2$} & \textbf{$\varepsilon=0.5$} \\
\midrule
"""
        + "\n".join(rows)
        + r"""
\bottomrule
\end{tabular}
"""
    )

    write_latex("tab-noise-robustness.tex", latex)


def generate_noise_macros(summaries: pd.DataFrame) -> None:
    """Generate LaTeX macros for noise results."""
    macros = [
        "% Auto-generated noise robustness macros",
        "% Do not edit manually - regenerate with analyze_noise.py",
        "",
    ]

    algorithms = ["CSSR", "CSM", "Spectral", "NSD", "BSI"]
    key_levels = [0.0, 0.05, 0.1, 0.2, 0.5]

    for algo in algorithms:
        algo_data = summaries[summaries["algorithm"] == algo]
        algo_lower = algo.lower()

        for eps in key_levels:
            row = algo_data[algo_data["epsilon"] == eps]
            if len(row) > 0:
                mean = row["states_mean"].iloc[0]
                std = row["states_std"].iloc[0]
                correct = row["correct_rate"].iloc[0] * 100

                eps_str = f"{eps:.2f}".replace(".", "")
                macros.append(f"\\newcommand{{\\{algo_lower}NoiseStates{eps_str}}}{{{mean:.1f}}}")
                macros.append(f"\\newcommand{{\\{algo_lower}NoiseStd{eps_str}}}{{{std:.1f}}}")
                macros.append(
                    f"\\newcommand{{\\{algo_lower}NoiseCorrect{eps_str}}}{{{correct:.0f}}}"
                )

        # Best noise level (where correct rate is highest)
        best_row = algo_data.loc[algo_data["correct_rate"].idxmax()]
        macros.append(f"\\newcommand{{\\{algo_lower}NoiseBestEps}}{{{best_row['epsilon']:.2f}}}")
        macros.append(
            f"\\newcommand{{\\{algo_lower}NoiseBestCorrect}}{{{best_row['correct_rate'] * 100:.0f}}}"
        )
        macros.append("")

    # Overall summary macros
    zero_noise = summaries[summaries["epsilon"] == 0.0]
    perfect_at_zero = zero_noise[zero_noise["correct_rate"] == 1.0]["algorithm"].tolist()
    macros.append(f"\\newcommand{{\\noisePerfectAtZero}}{{{', '.join(perfect_at_zero)}}}")

    # Which algorithms oversplit vs undersplit at high noise
    high_noise = summaries[summaries["epsilon"] == 0.5]
    oversplitters = high_noise[high_noise["states_mean"] > 2.5]["algorithm"].tolist()
    undersplitters = high_noise[high_noise["states_mean"] < 1.5]["algorithm"].tolist()
    macros.append(
        f"\\newcommand{{\\noiseOversplittersHigh}}{{{', '.join(oversplitters) or 'none'}}}"
    )
    macros.append(
        f"\\newcommand{{\\noiseUndersplittersHigh}}{{{', '.join(undersplitters) or 'none'}}}"
    )

    write_latex("noise-data.tex", "\n".join(macros))


def generate_noise_plot(summaries: pd.DataFrame) -> None:
    """Generate publication-quality noise robustness plot."""
    fig, ax = plt.subplots(figsize=(10, 6))

    algorithms = ["CSSR", "CSM", "Spectral", "NSD", "BSI"]
    markers = ["o", "s", "^", "D", "v"]

    for algo, marker in zip(algorithms, markers, strict=False):
        algo_data = summaries[summaries["algorithm"] == algo].sort_values("epsilon")
        ax.errorbar(
            algo_data["epsilon"],
            algo_data["states_mean"],
            yerr=algo_data["states_std"],
            marker=marker,
            label=algo,
            capsize=3,
            linewidth=1.5,
            markersize=6,
        )

    ax.axhline(y=2, color="black", linestyle="--", linewidth=1, label="True states")
    ax.set_xlabel("Noise Level (ε)", fontsize=12)
    ax.set_ylabel("Inferred States", fontsize=12)
    ax.set_title("Algorithm Robustness to Observation Noise", fontsize=14)
    ax.legend(loc="upper left")
    ax.grid(True, alpha=0.3)
    ax.set_xlim(-0.02, 0.52)
    ax.set_ylim(0, 5)

    # Save to results and figures directories
    results_dir = Path(__file__).parent / "results"
    fig.savefig(results_dir / "states_vs_noise.pdf", dpi=150, bbox_inches="tight")
    fig.savefig(results_dir / "states_vs_noise.png", dpi=150, bbox_inches="tight")

    # Copy to figure directories
    base = Path(__file__).parent.parent.parent
    for doc in ["paper-tutorial/figures", "paper-technical/figures"]:
        fig_dir = base / doc
        fig_dir.mkdir(parents=True, exist_ok=True)
        fig.savefig(fig_dir / "states_vs_noise.pdf", dpi=150, bbox_inches="tight")

    plt.close(fig)
    print("  Generated: states_vs_noise.pdf")


def generate_complexity_plots(df: pd.DataFrame) -> None:
    """Generate entropy rate and statistical complexity vs noise plots."""
    # Filter to successful runs with valid measures
    valid = df[
        (df["success"]) & (df["entropy_rate"].notna()) & (df["statistical_complexity"].notna())
    ]

    if len(valid) == 0:
        print("  No complexity data available (run experiment with updated script)")
        return

    # Compute means and stds
    summaries = []
    for algo in valid["algorithm"].unique():
        for eps in sorted(valid["epsilon"].unique()):
            group = valid[(valid["algorithm"] == algo) & (valid["epsilon"] == eps)]
            if len(group) > 0:
                summaries.append(
                    {
                        "algorithm": algo,
                        "epsilon": eps,
                        "h_mu_mean": group["entropy_rate"].mean(),
                        "h_mu_std": group["entropy_rate"].std() if len(group) > 1 else 0,
                        "c_mu_mean": group["statistical_complexity"].mean(),
                        "c_mu_std": group["statistical_complexity"].std() if len(group) > 1 else 0,
                    }
                )

    if not summaries:
        return

    summary_df = pd.DataFrame(summaries)

    algorithms = ["CSSR", "CSM", "Spectral", "NSD", "BSI"]
    markers = ["o", "s", "^", "D", "v"]

    # True Golden Mean values (p=0.5)
    true_h_mu = 0.6667  # approximately log2(3/2)
    true_c_mu = 1.0  # 1 bit for 2 equiprobable states

    # Figure 1: Entropy Rate vs Noise
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    for algo, marker in zip(algorithms, markers, strict=False):
        algo_data = summary_df[summary_df["algorithm"] == algo].sort_values("epsilon")
        if len(algo_data) > 0:
            ax1.errorbar(
                algo_data["epsilon"],
                algo_data["h_mu_mean"],
                yerr=algo_data["h_mu_std"],
                marker=marker,
                label=algo,
                capsize=3,
                linewidth=1.5,
                markersize=6,
            )

    ax1.axhline(
        y=true_h_mu, color="black", linestyle="--", linewidth=1, label=f"True h_μ ≈ {true_h_mu:.2f}"
    )
    ax1.set_xlabel("Noise Level (ε)", fontsize=12)
    ax1.set_ylabel("Entropy Rate h_μ (bits)", fontsize=12)
    ax1.set_title("Inferred Entropy Rate vs Observation Noise", fontsize=14)
    ax1.legend(loc="best")
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(-0.02, 0.52)

    # Figure 2: Statistical Complexity vs Noise
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    for algo, marker in zip(algorithms, markers, strict=False):
        algo_data = summary_df[summary_df["algorithm"] == algo].sort_values("epsilon")
        if len(algo_data) > 0:
            ax2.errorbar(
                algo_data["epsilon"],
                algo_data["c_mu_mean"],
                yerr=algo_data["c_mu_std"],
                marker=marker,
                label=algo,
                capsize=3,
                linewidth=1.5,
                markersize=6,
            )

    ax2.axhline(
        y=true_c_mu, color="black", linestyle="--", linewidth=1, label=f"True C_μ = {true_c_mu:.1f}"
    )
    ax2.set_xlabel("Noise Level (ε)", fontsize=12)
    ax2.set_ylabel("Statistical Complexity C_μ (bits)", fontsize=12)
    ax2.set_title("Inferred Statistical Complexity vs Observation Noise", fontsize=14)
    ax2.legend(loc="best")
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(-0.02, 0.52)

    # Save figures
    results_dir = Path(__file__).parent / "results"
    fig1.savefig(results_dir / "entropy_rate_vs_noise.pdf", dpi=150, bbox_inches="tight")
    fig2.savefig(results_dir / "complexity_vs_noise.pdf", dpi=150, bbox_inches="tight")

    # Copy to figure directories
    base = Path(__file__).parent.parent.parent
    for doc in ["paper-tutorial/figures", "paper-technical/figures"]:
        fig_dir = base / doc
        fig_dir.mkdir(parents=True, exist_ok=True)
        fig1.savefig(fig_dir / "entropy_rate_vs_noise.pdf", dpi=150, bbox_inches="tight")
        fig2.savefig(fig_dir / "complexity_vs_noise.pdf", dpi=150, bbox_inches="tight")

    plt.close(fig1)
    plt.close(fig2)
    print("  Generated: entropy_rate_vs_noise.pdf")
    print("  Generated: complexity_vs_noise.pdf")


def main() -> None:
    """Analyze noise results and generate outputs."""
    print("Loading noise robustness results...")
    df = load_results()
    print(f"  Loaded {len(df)} results")

    print("\nComputing summaries...")
    summaries = compute_summaries(df)
    print(f"  {len(summaries)} summary rows")

    print("\nGenerating LaTeX table...")
    generate_noise_table(summaries)

    print("\nGenerating LaTeX macros...")
    generate_noise_macros(summaries)

    print("\nGenerating plots...")
    generate_noise_plot(summaries)
    generate_complexity_plots(df)

    print("\nDone!")


if __name__ == "__main__":
    main()
