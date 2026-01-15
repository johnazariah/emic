"""Tests for output module."""

from __future__ import annotations

import json

import pytest

from emic.analysis import analyze
from emic.output import (
    DiagramStyle,
    from_json,
    to_dot,
    to_json,
    to_latex_table,
    to_mermaid,
    to_tikz,
)
from emic.sources import BiasedCoinSource, GoldenMeanSource


class TestDiagramStyle:
    """Tests for DiagramStyle configuration."""

    def test_default_values(self) -> None:
        """Test default style values."""
        style = DiagramStyle()
        assert style.layout == "dot"
        assert style.rankdir == "LR"
        assert style.show_probabilities is True
        assert style.node_color == "#4a90d9"

    def test_custom_values(self) -> None:
        """Test custom style values."""
        style = DiagramStyle(
            layout="neato",
            rankdir="TB",
            show_probabilities=False,
            node_color="#ff0000",
        )
        assert style.layout == "neato"
        assert style.rankdir == "TB"
        assert style.show_probabilities is False
        assert style.node_color == "#ff0000"

    def test_frozen(self) -> None:
        """Test that DiagramStyle is immutable."""
        style = DiagramStyle()
        with pytest.raises(AttributeError):
            style.layout = "circo"  # type: ignore[misc]


class TestRenderStateDiagram:
    """Tests for render_state_diagram function."""

    def test_render_golden_mean(self) -> None:
        """Test rendering Golden Mean machine."""
        pytest.importorskip("graphviz")
        from emic.output import render_state_diagram

        machine = GoldenMeanSource(p=0.5).true_machine
        diagram = render_state_diagram(machine)

        # Check it's a graphviz object
        assert hasattr(diagram, "source")
        assert "A" in diagram.source  # State A should be in the source
        assert "B" in diagram.source  # State B should be in the source

    def test_render_with_custom_style(self) -> None:
        """Test rendering with custom style."""
        pytest.importorskip("graphviz")
        from emic.output import render_state_diagram

        machine = GoldenMeanSource(p=0.5).true_machine
        style = DiagramStyle(
            show_probabilities=False,
            node_shape="doublecircle",
        )
        diagram = render_state_diagram(machine, style)
        assert "doublecircle" in diagram.source


class TestToTikz:
    """Tests for TikZ export."""

    def test_tikz_structure(self) -> None:
        """Test TikZ output has correct structure."""
        machine = GoldenMeanSource(p=0.5).true_machine
        tikz = to_tikz(machine)

        assert r"\begin{tikzpicture}" in tikz
        assert r"\end{tikzpicture}" in tikz
        assert r"\node[state]" in tikz
        assert r"\path" in tikz

    def test_tikz_with_custom_labels(self) -> None:
        """Test TikZ output with custom labels."""
        machine = GoldenMeanSource(p=0.5).true_machine
        style = DiagramStyle(
            state_labels={"A": "\\sigma_0", "B": "\\sigma_1"},
        )
        tikz = to_tikz(machine, style)

        assert "\\sigma_0" in tikz
        assert "\\sigma_1" in tikz


class TestToLatexTable:
    """Tests for LaTeX table export."""

    def test_table_structure(self) -> None:
        """Test LaTeX table has correct structure."""
        results = [
            ("Golden Mean", analyze(GoldenMeanSource(p=0.5).true_machine)),
            ("Biased Coin", analyze(BiasedCoinSource(p=0.7).true_machine)),
        ]
        latex = to_latex_table(results)

        assert r"\begin{table}" in latex
        assert r"\end{table}" in latex
        assert r"\begin{tabular}" in latex
        assert r"\toprule" in latex
        assert r"\bottomrule" in latex
        assert "Golden Mean" in latex
        assert "Biased Coin" in latex

    def test_custom_measures(self) -> None:
        """Test table with custom measures."""
        results = [
            ("Test", analyze(GoldenMeanSource(p=0.5).true_machine)),
        ]
        latex = to_latex_table(
            results,
            measures=["num_states", "entropy_rate"],
            caption="Custom Table",
            label="tab:custom",
        )

        assert "Custom Table" in latex
        assert "tab:custom" in latex
        assert r"$|\mathcal{S}|$" in latex
        assert r"$h_\mu$" in latex


class TestJsonSerialization:
    """Tests for JSON serialization."""

    def test_round_trip(self) -> None:
        """Test JSON serialization round-trip."""
        machine = GoldenMeanSource(p=0.5).true_machine
        json_str = to_json(machine)
        restored = from_json(json_str)

        assert len(restored) == len(machine)
        assert restored.alphabet == machine.alphabet
        assert restored.start_state == machine.start_state

    def test_json_valid(self) -> None:
        """Test that output is valid JSON."""
        machine = GoldenMeanSource(p=0.5).true_machine
        json_str = to_json(machine)

        # Should not raise
        data = json.loads(json_str)
        assert "alphabet" in data
        assert "states" in data
        assert "start_state" in data

    def test_json_contains_transitions(self) -> None:
        """Test that JSON contains all transitions."""
        machine = GoldenMeanSource(p=0.5).true_machine
        json_str = to_json(machine)
        data = json.loads(json_str)

        # Golden Mean has 2 states
        assert len(data["states"]) == 2

        # Check transitions exist
        for state in data["states"]:
            assert "transitions" in state
            assert len(state["transitions"]) > 0


class TestToDot:
    """Tests for DOT format export."""

    def test_dot_structure(self) -> None:
        """Test DOT output has correct structure."""
        machine = GoldenMeanSource(p=0.5).true_machine
        dot = to_dot(machine)

        assert "digraph {" in dot
        assert "rankdir=LR" in dot
        assert "->" in dot
        assert "}" in dot

    def test_dot_contains_states(self) -> None:
        """Test DOT contains all states."""
        machine = GoldenMeanSource(p=0.5).true_machine
        dot = to_dot(machine)

        assert '"A"' in dot
        assert '"B"' in dot


class TestToMermaid:
    """Tests for Mermaid export."""

    def test_mermaid_structure(self) -> None:
        """Test Mermaid output has correct structure."""
        machine = GoldenMeanSource(p=0.5).true_machine
        mermaid = to_mermaid(machine)

        assert "stateDiagram-v2" in mermaid
        assert "-->" in mermaid

    def test_mermaid_contains_transitions(self) -> None:
        """Test Mermaid contains transitions with labels."""
        machine = GoldenMeanSource(p=0.5).true_machine
        mermaid = to_mermaid(machine)

        # Should have transition labels
        assert "|" in mermaid  # Separator between symbol and probability
