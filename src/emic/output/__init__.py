"""Output and visualization for epsilon-machines.

This module provides functions for visualizing, exporting, and serializing
epsilon-machines and analysis results.

Functions:
    render_state_diagram: Render machine as Graphviz diagram
    display_state_diagram: Display diagram in Jupyter
    to_tikz: Export machine as TikZ code
    to_mermaid: Export machine as Mermaid diagram
    to_dot: Export machine as DOT format
    to_json: Serialize machine to JSON
    from_json: Deserialize machine from JSON
    to_latex_table: Format analysis results as LaTeX table

Example:
    >>> from emic.sources import GoldenMeanSource
    >>> from emic.output import render_state_diagram, to_tikz
    >>> machine = GoldenMeanSource(p=0.5).true_machine
    >>> diagram = render_state_diagram(machine)
    >>> diagram.render('golden_mean', format='pdf')
    >>> print(to_tikz(machine))
"""

from emic.output.diagram import (
    DiagramStyle,
    display_state_diagram,
    render_state_diagram,
)
from emic.output.latex import to_latex_table, to_tikz
from emic.output.serialization import from_json, to_dot, to_json, to_mermaid

__all__ = [
    "DiagramStyle",
    "display_state_diagram",
    "from_json",
    "render_state_diagram",
    "to_dot",
    "to_json",
    "to_latex_table",
    "to_mermaid",
    "to_tikz",
]
