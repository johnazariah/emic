"""LaTeX export for epsilon-machines and analysis results."""

from __future__ import annotations

from collections.abc import Hashable
from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from emic.analysis import AnalysisSummary
    from emic.output.diagram import DiagramStyle
    from emic.types import EpsilonMachine

A = TypeVar("A", bound=Hashable)


def to_tikz(
    machine: EpsilonMachine[A],
    style: DiagramStyle | None = None,
) -> str:
    """Generate TikZ code for a state diagram.

    Creates LaTeX/TikZ code that can be included in documents to render
    a publication-quality state diagram.

    Args:
        machine: The epsilon-machine to export.
        style: Rendering configuration for labels and formatting.

    Returns:
        LaTeX/TikZ code as a string.

    Example:
        >>> from emic.sources import GoldenMeanSource
        >>> from emic.output import to_tikz
        >>> machine = GoldenMeanSource(p=0.5).true_machine
        >>> tikz = to_tikz(machine)
        >>> print(tikz)  # doctest: +ELLIPSIS
        \\begin{tikzpicture}...
    """
    from emic.output.diagram import DiagramStyle

    style = style or DiagramStyle()

    lines = [
        r"\begin{tikzpicture}[->,>=stealth',shorten >=1pt,auto,node distance=2.5cm]",
        r"  \tikzstyle{state}=[circle,draw,minimum size=1cm,fill=blue!20]",
    ]

    # Add nodes with positions
    state_list = list(machine.states)
    for i, state in enumerate(state_list):
        label = style.state_labels.get(state.id, state.id)
        x = i * 3  # Simple horizontal layout
        lines.append(f"  \\node[state] ({state.id}) at ({x},0) {{${label}$}};")

    # Add edges
    for state in machine.states:
        for trans in state.transitions:
            symbol_str = str(trans.symbol)
            symbol = style.symbol_labels.get(symbol_str, symbol_str)
            if style.show_probabilities:
                label = f"{symbol}/{trans.probability:{style.probability_format}}"
            else:
                label = symbol

            if trans.target == state.id:
                # Self-loop
                lines.append(
                    f"  \\path ({state.id}) edge [loop above] node {{${label}$}} ({state.id});"
                )
            else:
                lines.append(f"  \\path ({state.id}) edge node {{${label}$}} ({trans.target});")

    lines.append(r"\end{tikzpicture}")

    return "\n".join(lines)


def to_latex_table(
    summaries: list[tuple[str, AnalysisSummary]],
    measures: list[str] | None = None,
    caption: str = "Epsilon-machine analysis",
    label: str = "tab:analysis",
) -> str:
    """Generate LaTeX table of analysis results.

    Creates a publication-ready LaTeX table comparing complexity measures
    across multiple processes or machines.

    Args:
        summaries: List of (name, summary) pairs to include.
        measures: Which measures to include. Defaults to common measures.
        caption: Table caption.
        label: LaTeX label for cross-referencing.

    Returns:
        LaTeX table code as a string.

    Example:
        >>> from emic.sources import GoldenMeanSource, BiasedCoinSource
        >>> from emic.analysis import analyze
        >>> from emic.output import to_latex_table
        >>> results = [
        ...     ("Golden Mean", analyze(GoldenMeanSource(p=0.5).true_machine)),
        ...     ("Biased Coin", analyze(BiasedCoinSource(p=0.7).true_machine)),
        ... ]
        >>> latex = to_latex_table(results)
        >>> print(latex)  # doctest: +ELLIPSIS
        \\begin{table}...
    """
    measures = measures or [
        "num_states",
        "statistical_complexity",
        "entropy_rate",
        "excess_entropy",
    ]

    # Header mapping to LaTeX math notation
    header_map = {
        "num_states": r"$|\mathcal{S}|$",
        "num_transitions": r"$|\mathcal{T}|$",
        "statistical_complexity": r"$C_\mu$",
        "entropy_rate": r"$h_\mu$",
        "excess_entropy": r"$E$",
        "topological_complexity": r"$C_0$",
    }

    headers = ["Process"] + [header_map.get(m, m) for m in measures]

    lines = [
        r"\begin{table}[htbp]",
        r"\centering",
        r"\caption{" + caption + "}",
        r"\label{" + label + "}",
        r"\begin{tabular}{l" + "c" * len(measures) + "}",
        r"\toprule",
        " & ".join(headers) + r" \\",
        r"\midrule",
    ]

    for name, summary in summaries:
        values = [name]
        for m in measures:
            v = getattr(summary, m, None)
            if v is None:
                values.append("--")
            elif isinstance(v, float):
                values.append(f"{v:.4f}")
            else:
                values.append(str(v))
        lines.append(" & ".join(values) + r" \\")

    lines.extend(
        [
            r"\bottomrule",
            r"\end{tabular}",
            r"\end{table}",
        ]
    )

    return "\n".join(lines)
