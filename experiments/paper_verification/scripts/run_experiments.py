import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import yaml

from emic.analysis.measures import entropy_rate, statistical_complexity
from emic.inference.cssr import CSSR, CSSRConfig
from emic.output.diagram import render_state_diagram
from emic.types import Symbol

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.append(str(PROJECT_ROOT))


def load_config():
    config_path = Path(__file__).parent.parent / "config.yaml"
    with config_path.open() as f:
        return yaml.safe_load(f)


def generate_golden_mean(length: int, p: float = 0.5, seed: int = 42) -> list[Symbol]:
    """Generates a Golden Mean process sequence."""
    rng = np.random.default_rng(seed)
    sequence = []
    # State 0 is A (can go to 0 or 1), State 1 is B (must go to A/0)
    # Using 0 for '0' and 1 for '1'.
    # Generator: A (0) --(0)--> B (1), A (0) --(1)--> A (0), B (1) --(1)--> A (0)

    current_state = 0  # A
    for _ in range(length):
        if current_state == 0:  # A
            if rng.random() < p:
                # Emit 1, go to A (loop)
                sequence.append("1")
                current_state = 0
            else:
                # Emit 0, go to B
                sequence.append("0")
                current_state = 1
        else:  # B
            # Must emit 1, go to A
            sequence.append("1")
            current_state = 0

    return sequence


def plot_machine(machine, filename):
    """Plots the epsilon machine using Graphviz."""
    print(f"Generating figure: {filename}")
    try:
        # Render to Dot object
        dot = render_state_diagram(machine)
        # Render to file (Graphviz adds extension, so we strip it from filename if present)
        fn_path = Path(filename)
        # render method requires the path without extension, and format argument
        output_path = str(fn_path.with_suffix(""))
        dot.render(output_path, format=fn_path.suffix.lstrip("."), cleanup=True)
    except Exception as e:
        print(f"Graphviz plotting failed ({e}), falling back to placeholder.")
        _fig, ax = plt.subplots()
        ax.text(0.5, 0.5, f"Graphviz Error:\n{e}", ha="center", va="center")
        ax.axis("off")
        plt.savefig(filename)
        plt.close()


def run_basics(config):
    print("Running Section I: From Data to Machines...")

    # 1. Generate Data
    # config structure is experiment -> verification -> ...
    ver_config = config["experiment"]["verification"]

    length = ver_config["sequence_length"]
    data = generate_golden_mean(length)

    # 2. Run CSSR
    alphabet = set(data)
    cssr_config = CSSRConfig(max_history=ver_config["history_length"], significance=0.001)
    cssr = CSSR(cssr_config)
    result = cssr.infer(data, alphabet=alphabet)
    machine = result.machine

    # 3. Calculate Properties
    c_mu = statistical_complexity(machine)
    h_mu = entropy_rate(machine)

    print(f"Inferred {len(machine.states)} states.")
    print(f"C_mu: {c_mu:.4f} bits")
    print(f"h_mu: {h_mu:.4f} bits")

    # 4. Generate Artifacts for LaTeX
    output_dir = Path(__file__).parent.parent / "tex"
    (output_dir / "figures").mkdir(exist_ok=True, parents=True)  # ensure figure dir exists

    # Save Plot
    plot_machine(machine, output_dir / "figures/golden_mean_machine.pdf")

    # Save Stationary Distribution Table
    probs = machine.stationary_distribution
    with (output_dir / "tables/gm_stationary_dist.tex").open("w") as f:
        f.write(r"\begin{itemize}" + "\n")
        # Note: keys are likely StateId objects, need string repr
        # Assuming states are somewhat generic, we iterate
        for i, (_state, prob) in enumerate(probs.probs.items()):
            label = "A" if i == 0 else "B"
            f.write(f"    \\item $P({label}) \\approx {prob:.3f}$\n")
        f.write(r"\end{itemize}" + "\n")

    print("Basics complete.")


def run_theorems(config):
    print("Running Section II: The Logic of Structure...")
    output_dir = Path(__file__).parent.parent / "tex/figures"
    output_dir.mkdir(exist_ok=True, parents=True)

    # 1. Setup
    # Use a shorter length to allow "noise" to be interpreted as structure
    # at high alpha (overfitting). With 100k samples, it is too clean to overfit.
    length = 1000
    data = generate_golden_mean(length)
    alphabet = set(data)
    history_len = config["experiment"]["verification"]["history_length"]

    # 2. Alpha Scan
    # We scan alpha from very small (under-fitting/merging) to very large (over-fitting/splitting).
    # Small alpha = strict test = hard to split = fewer states.
    # Large alpha = loose test = easy to split = more states.
    alphas = [1e-100, 1e-50, 1e-20, 1e-10, 1e-5, 1e-3, 0.01, 0.05, 0.1, 0.3, 0.5, 0.7, 0.9, 0.99]

    results_c = []
    results_h = []
    used_alphas = []

    print(f"Scanning {len(alphas)} alpha values for Optimality Curve...")

    for alpha in alphas:
        try:
            # Recreate CSSR for each alpha
            cssr_config = CSSRConfig(max_history=history_len, significance=alpha)
            cssr = CSSR(cssr_config)
            result = cssr.infer(data, alphabet=alphabet)
            machine = result.machine

            c = statistical_complexity(machine)
            h = entropy_rate(machine)

            results_c.append(c)
            results_h.append(h)
            used_alphas.append(alpha)
        except Exception as e:
            print(f"Skipping alpha {alpha} due to error: {e}")

    # 3. Plotting
    _fig, ax = plt.subplots(figsize=(8, 6))

    # Scatter plot
    # x axis: Complexity (Cost)
    # y axis: Entropy Rate (Uncertainty / Inverse Accuracy)
    sc = ax.scatter(
        results_c,
        results_h,
        c=np.log10(used_alphas),
        cmap="viridis",
        s=60,
        edgecolors="k",
        zorder=10,
    )
    cbar = plt.colorbar(sc)
    cbar.set_label(r"$\log_{10}(\alpha)$")

    ax.set_xlabel(r"Statistical Complexity $C_\mu$ (bits)")
    ax.set_ylabel(r"Prediction Uncertainty $h_\mu$ (bits)")
    ax.set_title(r"Optimality Curve: Complexity vs. Prescience")

    # Theoretical Truth
    true_c = 0.918
    true_h = 0.667
    ax.axvline(x=true_c, color="r", linestyle="--", alpha=0.5, label=r"Theoretical $C_\mu$")
    ax.axhline(y=true_h, color="r", linestyle="--", alpha=0.5, label=r"Theoretical $h_\mu$")

    # Annotate regions
    # Under-fitting: Low C_mu, High h_mu
    # Over-fitting: High C_mu, Low h_mu (optimal h_mu)
    ax.text(
        0.1,
        0.9,
        "Under-fitting\n(Non-prescient)",
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment="top",
    )
    ax.text(
        0.9,
        0.2,
        "Over-fitting\n(Redundant)",
        transform=ax.transAxes,
        fontsize=10,
        horizontalalignment="right",
    )

    ax.legend(loc="upper right")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_dir / "optimality_curve.pdf")
    plt.close()
    print("Theorems section complete.")


def run_chaos(config):
    print("Running Section III: The Emergence of Complexity...")
    output_dir = Path(__file__).parent.parent / "tex/figures"
    output_dir.mkdir(exist_ok=True, parents=True)

    app_config = config["experiment"]["application"]["logistic_map"]
    r_start = app_config["r_start"]
    r_end = app_config["r_end"]
    n_r_steps = app_config["steps"]
    n_discard = app_config["discard"]
    length = app_config["length"]

    # Grid of r values
    rs = np.linspace(r_start, r_end, n_r_steps)

    c_mu_values = []

    # For bifurcation diagram
    bifurcation_x = []
    bifurcation_r = []

    print(f"Scanning {n_r_steps} values of r from {r_start} to {r_end}...")

    for r in rs:
        # 1. Simulate Logistic Map
        x = np.random.rand()
        # Transients
        for _ in range(n_discard):
            x = r * x * (1 - x)

        # Collection
        sequence_vals = []
        symbolic_seq = []

        # We collect points for both inference and bifurcation plotting
        for _ in range(length):
            x = r * x * (1 - x)
            sequence_vals.append(x)
            symbolic_seq.append("0" if x < 0.5 else "1")

        # Store last few points for bifurcation plot to see the attractor
        points_to_plot = sequence_vals[-50:]
        bifurcation_x.extend(points_to_plot)
        bifurcation_r.extend([r] * len(points_to_plot))

        # 2. Infer Machine
        try:
            # We reuse the history length from verification config for consistency
            hist_len = config["experiment"]["verification"]["history_length"]

            alphabet = set(symbolic_seq)
            # Use strict alpha to avoid getting spurious states in the chaotic regime
            cssr_config = CSSRConfig(max_history=hist_len, significance=0.001)
            cssr = CSSR(cssr_config)
            result = cssr.infer(symbolic_seq, alphabet=alphabet)
            machine = result.machine

            c_mu = statistical_complexity(machine)
        except Exception:
            # If inference fails (e.g. only one symbol seen), complexity is 0
            c_mu = 0.0

        c_mu_values.append(c_mu)

    # 3. Plotting
    _fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    # Top subplot: Bifurcation diagram
    ax1.scatter(bifurcation_r, bifurcation_x, s=0.1, color="black", alpha=0.5)
    ax1.set_ylabel(r"$x_n$")
    ax1.set_title(r"Logistic Map Bifurcation Diagram")
    ax1.grid(True, alpha=0.1)

    # Bottom: Statistical Complexity
    ax2.plot(rs, c_mu_values, color="blue", linewidth=1.5)
    ax2.set_ylabel(r"Statistical Complexity $C_\mu$ (bits)")
    ax2.set_xlabel(r"Parameter $r$")
    ax2.set_title(r"Structural Complexity")
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(output_dir / "logistic_complexity.pdf")
    plt.close()

    print("Chaos section complete.")


if __name__ == "__main__":
    config = load_config()

    # Ensure dirs exist
    (Path(__file__).parent.parent / "tex/figures").mkdir(exist_ok=True, parents=True)
    (Path(__file__).parent.parent / "tex/tables").mkdir(exist_ok=True, parents=True)

    run_basics(config)
    run_theorems(config)
    run_chaos(config)
