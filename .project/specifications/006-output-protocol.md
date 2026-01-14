# Specification 006: Output Protocol

## Status
📋 Draft

## Overview

This specification defines the **Output Protocol** — interfaces for visualizing, exporting, and serializing epsilon-machines and analysis results.

Outputs serve:
- **Exploration**: Interactive visualization in notebooks
- **Publication**: LaTeX-ready figures and tables
- **Persistence**: Save/load machines for later use
- **Interoperability**: Export to standard formats

## Design Principles

- **Separation of concerns**: Rendering logic separate from data
- **Multiple backends**: Same interface, different outputs
- **Publication-ready**: High-quality default aesthetics
- **Configurable**: Customizable styles and formats

---

## 1. Visualization

### 1.1 State Diagram

The canonical visualization: a directed graph with states as nodes and transitions as labeled edges.

```python
from dataclasses import dataclass
from typing import Literal

@dataclass(frozen=True)
class DiagramStyle:
    """Configuration for state diagram rendering."""
    
    # Layout
    layout: Literal['dot', 'neato', 'circo', 'fdp'] = 'dot'
    rankdir: Literal['LR', 'TB', 'RL', 'BT'] = 'LR'  # Left-to-right
    
    # Nodes
    node_shape: str = 'circle'
    node_color: str = '#4a90d9'
    node_fontsize: int = 12
    node_width: float = 0.5
    
    # Edges
    edge_fontsize: int = 10
    edge_color: str = '#333333'
    show_probabilities: bool = True
    probability_format: str = '.2f'
    
    # Labels
    state_labels: dict[str, str] | None = None  # Custom labels
    symbol_labels: dict[str, str] | None = None
    
    # Size
    size: tuple[float, float] | None = None  # (width, height) in inches
    dpi: int = 150


def render_state_diagram(
    machine: EpsilonMachine[A],
    style: DiagramStyle | None = None,
) -> 'graphviz.Digraph':
    """
    Render an epsilon-machine as a state diagram.
    
    Args:
        machine: The epsilon-machine to visualize
        style: Rendering configuration
    
    Returns:
        A graphviz.Digraph object
    
    Example:
        >>> from emic.output import render_state_diagram
        >>> machine = GoldenMeanSource().true_machine
        >>> diagram = render_state_diagram(machine)
        >>> diagram.render('golden_mean', format='pdf')
    """
    import graphviz
    
    style = style or DiagramStyle()
    
    dot = graphviz.Digraph(
        engine=style.layout,
        graph_attr={
            'rankdir': style.rankdir,
            'size': f'{style.size[0]},{style.size[1]}' if style.size else '',
            'dpi': str(style.dpi),
        },
        node_attr={
            'shape': style.node_shape,
            'style': 'filled',
            'fillcolor': style.node_color,
            'fontsize': str(style.node_fontsize),
            'width': str(style.node_width),
        },
        edge_attr={
            'fontsize': str(style.edge_fontsize),
            'color': style.edge_color,
        },
    )
    
    # Add nodes
    for state in machine.states:
        label = (style.state_labels or {}).get(state.id, state.id)
        dot.node(state.id, label)
    
    # Add edges
    for state in machine.states:
        for trans in state.transitions:
            symbol = (style.symbol_labels or {}).get(str(trans.symbol), str(trans.symbol))
            if style.show_probabilities:
                label = f'{symbol} ({trans.probability:{style.probability_format}})'
            else:
                label = symbol
            dot.edge(state.id, trans.target, label)
    
    return dot


def display_state_diagram(
    machine: EpsilonMachine[A],
    style: DiagramStyle | None = None,
) -> None:
    """
    Display state diagram in Jupyter notebook.
    
    Uses IPython display for inline rendering.
    """
    diagram = render_state_diagram(machine, style)
    from IPython.display import display
    display(diagram)
```

### 1.2 Transition Matrix Heatmap

```python
def render_transition_heatmap(
    machine: EpsilonMachine[A],
    symbol: A | None = None,
    figsize: tuple[float, float] = (8, 6),
) -> 'matplotlib.figure.Figure':
    """
    Render transition matrix as a heatmap.
    
    Args:
        machine: The epsilon-machine
        symbol: If provided, show matrix for this symbol only.
                If None, show combined transition probabilities.
        figsize: Figure size in inches
    
    Returns:
        Matplotlib figure
    """
    import matplotlib.pyplot as plt
    import numpy as np
    
    state_ids = sorted(s.id for s in machine.states)
    n = len(state_ids)
    state_to_idx = {s: i for i, s in enumerate(state_ids)}
    
    if symbol is not None:
        # Single symbol matrix
        matrix = np.zeros((n, n))
        for state in machine.states:
            i = state_to_idx[state.id]
            for trans in state.transitions:
                if trans.symbol == symbol:
                    j = state_to_idx[trans.target]
                    matrix[i, j] = trans.probability
        title = f'Transition Matrix for symbol "{symbol}"'
    else:
        # Combined (sum over symbols)
        matrix = np.zeros((n, n))
        for state in machine.states:
            i = state_to_idx[state.id]
            for trans in state.transitions:
                j = state_to_idx[trans.target]
                matrix[i, j] += trans.probability
        title = 'Combined Transition Matrix'
    
    fig, ax = plt.subplots(figsize=figsize)
    im = ax.imshow(matrix, cmap='Blues', vmin=0, vmax=1)
    
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(state_ids)
    ax.set_yticklabels(state_ids)
    ax.set_xlabel('Target State')
    ax.set_ylabel('Source State')
    ax.set_title(title)
    
    plt.colorbar(im, ax=ax, label='Probability')
    
    # Annotate cells
    for i in range(n):
        for j in range(n):
            if matrix[i, j] > 0:
                ax.text(j, i, f'{matrix[i, j]:.2f}',
                       ha='center', va='center', fontsize=10)
    
    return fig
```

### 1.3 Complexity Curve

```python
def render_complexity_curve(
    results: list[InferenceResult[A]],
    parameter_name: str,
    parameter_values: list[float],
    measures: list[str] = ['C_mu', 'h_mu'],
    figsize: tuple[float, float] = (10, 6),
) -> 'matplotlib.figure.Figure':
    """
    Plot complexity measures vs. a parameter.
    
    Useful for showing how complexity changes with:
    - History length L
    - Process parameter (e.g., bias p)
    - Sample size
    
    Args:
        results: List of inference results
        parameter_name: Label for x-axis
        parameter_values: Values of the parameter
        measures: Which measures to plot
        figsize: Figure size
    
    Returns:
        Matplotlib figure
    """
    import matplotlib.pyplot as plt
    
    fig, ax = plt.subplots(figsize=figsize)
    
    for measure in measures:
        values = []
        for result in results:
            summary = analyze(result.machine)
            values.append(getattr(summary, measure.replace('_', '_')))
        ax.plot(parameter_values, values, 'o-', label=measure)
    
    ax.set_xlabel(parameter_name)
    ax.set_ylabel('Bits')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    return fig
```

---

## 2. LaTeX Export

### 2.1 TikZ State Diagram

```python
def to_tikz(
    machine: EpsilonMachine[A],
    style: DiagramStyle | None = None,
) -> str:
    """
    Generate TikZ code for a state diagram.
    
    Args:
        machine: The epsilon-machine
        style: Rendering configuration
    
    Returns:
        LaTeX/TikZ code as a string
    
    Example:
        >>> tikz_code = to_tikz(machine)
        >>> print(tikz_code)
        \\begin{tikzpicture}[->,>=stealth',shorten >=1pt,auto,node distance=2.5cm]
        ...
    """
    style = style or DiagramStyle()
    
    lines = [
        r'\begin{tikzpicture}[->,>=stealth\',shorten >=1pt,auto,node distance=2.5cm]',
        r'  \tikzstyle{state}=[circle,draw,minimum size=1cm]',
    ]
    
    # Add nodes
    state_list = list(machine.states)
    for i, state in enumerate(state_list):
        label = (style.state_labels or {}).get(state.id, state.id)
        x = i * 3  # Simple horizontal layout
        lines.append(f'  \\node[state] ({state.id}) at ({x},0) {{{label}}};')
    
    # Add edges
    for state in machine.states:
        for trans in state.transitions:
            symbol = (style.symbol_labels or {}).get(str(trans.symbol), str(trans.symbol))
            if style.show_probabilities:
                label = f'{symbol}/{trans.probability:{style.probability_format}}'
            else:
                label = symbol
            
            if trans.target == state.id:
                # Self-loop
                lines.append(f'  \\path ({state.id}) edge [loop above] node {{{label}}} ({state.id});')
            else:
                lines.append(f'  \\path ({state.id}) edge node {{{label}}} ({trans.target});')
    
    lines.append(r'\end{tikzpicture}')
    
    return '\n'.join(lines)
```

### 2.2 Analysis Table

```python
def to_latex_table(
    summaries: list[tuple[str, AnalysisSummary]],
    measures: list[str] | None = None,
    caption: str = 'Epsilon-machine analysis',
    label: str = 'tab:analysis',
) -> str:
    """
    Generate LaTeX table of analysis results.
    
    Args:
        summaries: List of (name, summary) pairs
        measures: Which measures to include (default: all)
        caption: Table caption
        label: LaTeX label
    
    Returns:
        LaTeX table code
    
    Example:
        >>> results = [
        ...     ('Golden Mean', analyze(golden_mean_machine)),
        ...     ('Even Process', analyze(even_process_machine)),
        ... ]
        >>> print(to_latex_table(results))
    """
    measures = measures or ['num_states', 'C_mu', 'h_mu', 'E']
    
    # Header
    header_map = {
        'num_states': r'$|\mathcal{S}|$',
        'C_mu': r'$C_\mu$',
        'h_mu': r'$h_\mu$',
        'E': r'$E$',
        'chi': r'$\chi$',
    }
    
    headers = ['Process'] + [header_map.get(m, m) for m in measures]
    
    lines = [
        r'\begin{table}[htbp]',
        r'\centering',
        r'\caption{' + caption + '}',
        r'\label{' + label + '}',
        r'\begin{tabular}{l' + 'c' * len(measures) + '}',
        r'\toprule',
        ' & '.join(headers) + r' \\',
        r'\midrule',
    ]
    
    for name, summary in summaries:
        values = [name]
        for m in measures:
            v = getattr(summary, m)
            if isinstance(v, float):
                values.append(f'{v:.4f}')
            else:
                values.append(str(v))
        lines.append(' & '.join(values) + r' \\')
    
    lines.extend([
        r'\bottomrule',
        r'\end{tabular}',
        r'\end{table}',
    ])
    
    return '\n'.join(lines)
```

---

## 3. Serialization

### 3.1 JSON

```python
import json
from typing import Any

def to_json(machine: EpsilonMachine[A]) -> str:
    """
    Serialize epsilon-machine to JSON.
    
    Args:
        machine: The epsilon-machine
    
    Returns:
        JSON string
    """
    def serialize_value(v: Any) -> Any:
        if isinstance(v, frozenset):
            return list(v)
        if hasattr(v, '__dict__'):
            return {k: serialize_value(val) for k, val in v.__dict__.items()}
        return v
    
    data = {
        'alphabet': list(machine.alphabet),
        'start_state': machine.start_state,
        'stationary_distribution': dict(machine.stationary_distribution._probs),
        'states': [
            {
                'id': s.id,
                'transitions': [
                    {
                        'symbol': t.symbol,
                        'probability': t.probability,
                        'target': t.target,
                    }
                    for t in s.transitions
                ]
            }
            for s in machine.states
        ],
    }
    
    return json.dumps(data, indent=2)


def from_json(json_str: str) -> EpsilonMachine[Any]:
    """
    Deserialize epsilon-machine from JSON.
    
    Args:
        json_str: JSON string
    
    Returns:
        EpsilonMachine
    """
    data = json.loads(json_str)
    
    states = frozenset(
        CausalState(
            id=s['id'],
            transitions=frozenset(
                Transition(
                    symbol=t['symbol'],
                    probability=t['probability'],
                    target=t['target'],
                )
                for t in s['transitions']
            )
        )
        for s in data['states']
    )
    
    return EpsilonMachine(
        alphabet=frozenset(data['alphabet']),
        states=states,
        start_state=data['start_state'],
        stationary_distribution=Distribution(data['stationary_distribution']),
    )
```

### 3.2 Pickle (for Internal Use)

```python
import pickle

def save_machine(machine: EpsilonMachine[A], path: str) -> None:
    """Save machine to pickle file."""
    with open(path, 'wb') as f:
        pickle.dump(machine, f)


def load_machine(path: str) -> EpsilonMachine[Any]:
    """Load machine from pickle file."""
    with open(path, 'rb') as f:
        return pickle.load(f)
```

### 3.3 DOT Format

```python
def to_dot(machine: EpsilonMachine[A]) -> str:
    """
    Export to Graphviz DOT format.
    
    Can be rendered with `dot`, `neato`, etc.
    """
    diagram = render_state_diagram(machine)
    return diagram.source
```

---

## 4. Notebook Integration

### 4.1 Rich Display

```python
class MachineDisplay:
    """
    Rich display object for epsilon-machines in Jupyter.
    
    Automatically renders as state diagram with analysis summary.
    """
    
    def __init__(self, machine: EpsilonMachine[A]):
        self.machine = machine
        self._summary = analyze(machine)
    
    def _repr_html_(self) -> str:
        """HTML representation for Jupyter."""
        diagram = render_state_diagram(self.machine)
        svg = diagram.pipe(format='svg').decode('utf-8')
        
        html = f'''
        <div style="display: flex; align-items: start; gap: 20px;">
            <div>{svg}</div>
            <div style="font-family: monospace; font-size: 12px;">
                <strong>ε-Machine Analysis</strong><br>
                States: {self._summary.num_states}<br>
                C<sub>μ</sub>: {self._summary.statistical_complexity:.4f} bits<br>
                h<sub>μ</sub>: {self._summary.entropy_rate:.4f} bits/symbol<br>
                E: {self._summary.excess_entropy:.4f} bits
            </div>
        </div>
        '''
        return html
    
    def _repr_latex_(self) -> str:
        """LaTeX representation."""
        return to_tikz(self.machine)


def display_machine(machine: EpsilonMachine[A]) -> None:
    """Display machine richly in Jupyter."""
    from IPython.display import display
    display(MachineDisplay(machine))
```

---

## 5. Module Structure

```
emic/output/
├── __init__.py           # Re-exports
├── visualization/
│   ├── __init__.py
│   ├── diagram.py        # State diagrams
│   ├── heatmap.py        # Transition matrices
│   └── curves.py         # Complexity curves
├── latex/
│   ├── __init__.py
│   ├── tikz.py           # TikZ export
│   └── tables.py         # LaTeX tables
├── serialization/
│   ├── __init__.py
│   ├── json.py           # JSON import/export
│   ├── dot.py            # DOT format
│   └── pickle.py         # Pickle helpers
└── notebook/
    ├── __init__.py
    └── display.py        # Rich display
```

---

## 6. Usage Examples

### In Jupyter Notebook

```python
from emic.sources import GoldenMeanSource
from emic.output import display_machine, render_state_diagram

# Quick display
machine = GoldenMeanSource().true_machine
display_machine(machine)

# Custom styling
from emic.output import DiagramStyle

style = DiagramStyle(
    layout='circo',
    node_color='#90EE90',
    state_labels={'A': 'Ready', 'B': 'Waiting'},
)
render_state_diagram(machine, style)
```

### For Publication

```python
from emic.output import to_tikz, to_latex_table

# Generate TikZ figure
tikz = to_tikz(machine, DiagramStyle(show_probabilities=True))
with open('figures/golden_mean.tex', 'w') as f:
    f.write(tikz)

# Generate comparison table
results = [
    ('Golden Mean', analyze(golden_mean)),
    ('Even Process', analyze(even_process)),
    ('Fair Coin', analyze(fair_coin)),
]
table = to_latex_table(results, caption='Complexity of canonical processes')
print(table)
```

---

## Acceptance Criteria

- [ ] State diagram rendering (Graphviz)
- [ ] Transition matrix heatmaps (Matplotlib)
- [ ] TikZ export for LaTeX
- [ ] LaTeX table generation
- [ ] JSON serialization/deserialization
- [ ] Rich display in Jupyter
- [ ] DOT format export
- [ ] Configurable styling
- [ ] Unit tests for all formats
- [ ] Gallery of example outputs

## Dependencies

- `graphviz` (Python bindings)
- `matplotlib`
- `numpy`
- IPython (optional, for notebook display)

## Related Specifications

- Spec 002: Core Types (machines to render)
- Spec 005: Analysis Protocol (summaries to display)
