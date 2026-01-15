"""State diagram visualization using Graphviz."""

from __future__ import annotations

from collections.abc import Hashable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal, TypeVar

if TYPE_CHECKING:
    import graphviz

    from emic.types import EpsilonMachine

A = TypeVar("A", bound=Hashable)


@dataclass(frozen=True)
class DiagramStyle:
    """Configuration for state diagram rendering.

    Attributes:
        layout: Graphviz layout engine (dot, neato, circo, fdp).
        rankdir: Graph direction (LR=left-to-right, TB=top-to-bottom).
        node_shape: Shape of state nodes (circle, doublecircle, box).
        node_color: Fill color for nodes (hex or name).
        node_fontsize: Font size for node labels.
        node_width: Minimum width of nodes in inches.
        edge_fontsize: Font size for edge labels.
        edge_color: Color of edges.
        show_probabilities: Whether to show transition probabilities.
        probability_format: Format string for probabilities.
        state_labels: Custom labels for states (state_id -> label).
        symbol_labels: Custom labels for symbols (str(symbol) -> label).
        size: Figure size in inches (width, height).
        dpi: Resolution in dots per inch.
    """

    layout: Literal["dot", "neato", "circo", "fdp"] = "dot"
    rankdir: Literal["LR", "TB", "RL", "BT"] = "LR"
    node_shape: str = "circle"
    node_color: str = "#4a90d9"
    node_fontsize: int = 12
    node_width: float = 0.5
    edge_fontsize: int = 10
    edge_color: str = "#333333"
    show_probabilities: bool = True
    probability_format: str = ".2f"
    state_labels: dict[str, str] = field(default_factory=dict)
    symbol_labels: dict[str, str] = field(default_factory=dict)
    size: tuple[float, float] | None = None
    dpi: int = 150


def render_state_diagram(
    machine: EpsilonMachine[A],
    style: DiagramStyle | None = None,
) -> graphviz.Digraph:
    """Render an epsilon-machine as a state diagram.

    Creates a Graphviz directed graph representing the epsilon-machine.
    States are shown as nodes and transitions as labeled edges.

    Args:
        machine: The epsilon-machine to visualize.
        style: Rendering configuration. Uses defaults if not provided.

    Returns:
        A graphviz.Digraph object that can be rendered to various formats.

    Raises:
        ImportError: If graphviz is not installed.

    Example:
        >>> from emic.sources import GoldenMeanSource
        >>> from emic.output import render_state_diagram
        >>> machine = GoldenMeanSource(p=0.5).true_machine
        >>> diagram = render_state_diagram(machine)
        >>> diagram.render('golden_mean', format='pdf')
        'golden_mean.pdf'
    """
    try:
        import graphviz
    except ImportError as e:
        msg = "graphviz is required for diagram rendering. Install with: pip install graphviz"
        raise ImportError(msg) from e

    style = style or DiagramStyle()

    graph_attr: dict[str, str] = {
        "rankdir": style.rankdir,
        "dpi": str(style.dpi),
    }
    if style.size:
        graph_attr["size"] = f"{style.size[0]},{style.size[1]}"

    dot = graphviz.Digraph(
        engine=style.layout,
        graph_attr=graph_attr,
        node_attr={
            "shape": style.node_shape,
            "style": "filled",
            "fillcolor": style.node_color,
            "fontsize": str(style.node_fontsize),
            "width": str(style.node_width),
        },
        edge_attr={
            "fontsize": str(style.edge_fontsize),
            "color": style.edge_color,
        },
    )

    # Add nodes
    for state in machine.states:
        label = style.state_labels.get(state.id, state.id)
        dot.node(state.id, label)

    # Add edges
    for state in machine.states:
        for trans in state.transitions:
            symbol_str = str(trans.symbol)
            symbol = style.symbol_labels.get(symbol_str, symbol_str)
            if style.show_probabilities:
                label = f"{symbol} ({trans.probability:{style.probability_format}})"
            else:
                label = symbol
            dot.edge(state.id, trans.target, label)

    return dot


def display_state_diagram(
    machine: EpsilonMachine[A],
    style: DiagramStyle | None = None,
) -> None:
    """Display state diagram in Jupyter notebook.

    Renders the epsilon-machine as an inline SVG in Jupyter environments.

    Args:
        machine: The epsilon-machine to visualize.
        style: Rendering configuration. Uses defaults if not provided.

    Raises:
        ImportError: If graphviz or IPython is not installed.

    Example:
        >>> from emic.sources import GoldenMeanSource
        >>> from emic.output import display_state_diagram
        >>> display_state_diagram(GoldenMeanSource().true_machine)  # doctest: +SKIP
    """
    diagram = render_state_diagram(machine, style)
    try:
        from IPython.display import display
    except ImportError as e:
        msg = "IPython is required for notebook display"
        raise ImportError(msg) from e

    display(diagram)
