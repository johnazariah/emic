"""Serialization and export formats for epsilon-machines."""

from __future__ import annotations

import json
from collections.abc import Hashable
from typing import TYPE_CHECKING, Any, TypeVar

if TYPE_CHECKING:
    from emic.types import EpsilonMachine

A = TypeVar("A", bound=Hashable)


def to_json(machine: EpsilonMachine[A]) -> str:
    """Serialize an epsilon-machine to JSON.

    Creates a JSON representation that can be saved to a file or
    transmitted over a network. Use `from_json` to deserialize.

    Args:
        machine: The epsilon-machine to serialize.

    Returns:
        JSON string representation.

    Example:
        >>> from emic.sources import GoldenMeanSource
        >>> from emic.output import to_json, from_json
        >>> machine = GoldenMeanSource(p=0.5).true_machine
        >>> json_str = to_json(machine)
        >>> restored = from_json(json_str)
        >>> len(restored) == len(machine)
        True
    """
    states_list: list[dict[str, Any]] = []
    for state in machine.states:
        state_data: dict[str, Any] = {
            "id": state.id,
            "transitions": [
                {
                    "symbol": t.symbol,
                    "target": t.target,
                    "probability": t.probability,
                }
                for t in state.transitions
            ],
        }
        states_list.append(state_data)

    data: dict[str, Any] = {
        "alphabet": list(machine.alphabet),
        "start_state": machine.start_state,
        "states": states_list,
    }

    # Include stationary distribution if available
    if machine.stationary_distribution:
        data["stationary_distribution"] = {
            state_id: float(prob)
            for state_id, prob in machine.stationary_distribution.probs.items()
        }

    return json.dumps(data, indent=2)


def from_json(json_str: str) -> EpsilonMachine[Any]:
    """Deserialize an epsilon-machine from JSON.

    Reconstructs an epsilon-machine from its JSON representation
    created by `to_json`.

    Args:
        json_str: JSON string representation.

    Returns:
        The reconstructed epsilon-machine.

    Raises:
        ValueError: If the JSON is malformed or missing required fields.
        json.JSONDecodeError: If the string is not valid JSON.

    Example:
        >>> from emic.output import from_json
        >>> json_str = '''{"alphabet": [0, 1], "start_state": "A",
        ...     "states": [{"id": "A", "transitions": [
        ...         {"symbol": 0, "target": "A", "probability": 0.5},
        ...         {"symbol": 1, "target": "A", "probability": 0.5}
        ...     ]}]}'''
        >>> machine = from_json(json_str)
        >>> len(machine)
        1
    """
    from emic.types import EpsilonMachineBuilder

    data = json.loads(json_str)

    builder: EpsilonMachineBuilder[Any] = EpsilonMachineBuilder()

    for state_data in data["states"]:
        state_id = state_data["id"]
        for trans in state_data["transitions"]:
            builder.add_transition(
                source=state_id,
                symbol=trans["symbol"],
                target=trans["target"],
                probability=trans["probability"],
            )

    if "start_state" in data:
        builder.with_start_state(data["start_state"])

    return builder.build()


def to_dot(machine: EpsilonMachine[A]) -> str:
    """Export epsilon-machine as DOT format.

    Creates a DOT (Graphviz) representation that can be rendered
    by Graphviz tools or imported into other visualization software.

    Args:
        machine: The epsilon-machine to export.

    Returns:
        DOT format string.

    Example:
        >>> from emic.sources import GoldenMeanSource
        >>> from emic.output import to_dot
        >>> machine = GoldenMeanSource(p=0.5).true_machine
        >>> dot = to_dot(machine)
        >>> print(dot)  # doctest: +ELLIPSIS
        digraph {
        ...
    """
    lines = [
        "digraph {",
        "  rankdir=LR;",
        '  node [shape=circle, style=filled, fillcolor="#4a90d9"];',
    ]

    # Add nodes
    for state in machine.states:
        lines.append(f'  "{state.id}";')

    # Add edges
    for state in machine.states:
        for trans in state.transitions:
            label = f"{trans.symbol} ({trans.probability:.2f})"
            lines.append(f'  "{state.id}" -> "{trans.target}" [label="{label}"];')

    lines.append("}")
    return "\n".join(lines)


def to_mermaid(machine: EpsilonMachine[A]) -> str:
    """Export epsilon-machine as Mermaid diagram.

    Creates a Mermaid state diagram that can be rendered in Markdown
    documents on GitHub, GitLab, and other platforms.

    Args:
        machine: The epsilon-machine to export.

    Returns:
        Mermaid diagram code.

    Example:
        >>> from emic.sources import GoldenMeanSource
        >>> from emic.output import to_mermaid
        >>> machine = GoldenMeanSource(p=0.5).true_machine
        >>> mermaid = to_mermaid(machine)
        >>> print(mermaid)  # doctest: +ELLIPSIS
        stateDiagram-v2
        ...
    """
    lines = ["stateDiagram-v2"]

    for state in machine.states:
        for trans in state.transitions:
            label = f"{trans.symbol} | {trans.probability:.2f}"
            lines.append(f"    {state.id} --> {trans.target} : {label}")

    return "\n".join(lines)
