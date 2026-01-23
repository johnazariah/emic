# Visualization Gallery

This gallery showcases epsilon-machine state diagrams for canonical stochastic processes used in computational mechanics.

## Overview

State diagrams visualize the causal structure of epsilon-machines:

- **Nodes** represent causal states
- **Edges** represent transitions between states
- **Labels** show the emitted symbol and transition probability

## Canonical Processes

### Biased Coin (IID Process)

The simplest stochastic process — each symbol is independent of the past.

```python
from emic.sources import BiasedCoinSource
from emic.output import render_state_diagram, DiagramStyle

source = BiasedCoinSource(p=0.7)
diagram = render_state_diagram(source.true_machine)
diagram.render("biased_coin", format="svg")
```

**Properties:**

- **States:** 1 (single state, no memory required)
- **Statistical Complexity (Cμ):** 0 bits
- **Entropy Rate (hμ):** H(p) = -p log₂(p) - (1-p) log₂(1-p)

```
    ┌─────────────────────┐
    │     ╭───────────╮   │
    │     │           │   │
0 (p)────▶│     S     │◀───── 1 (1-p)
          │           │
          ╰───────────╯
```

---

### Golden Mean Process

A process that forbids consecutive 1s — after emitting a 1, must emit a 0.

```python
from emic.sources import GoldenMeanSource
from emic.output import render_state_diagram

source = GoldenMeanSource(p=0.5)
diagram = render_state_diagram(source.true_machine)
diagram.render("golden_mean", format="svg")
```

**Properties:**

- **States:** 2
- **Constraint:** No "11" substring allowed
- **Named for:** The golden ratio φ appears in its entropy calculation

```
          0 (p)                    0 (1.0)
    ╭───────────╮              ╭───────────╮
    │           │              │           │
    ▼           │              ▼           │
╭───────╮       │        ╭───────╮         │
│       │───────╯        │       │─────────╯
│   A   │                │   B   │
│       │───────────────▶│       │
╰───────╯    1 (1-p)     ╰───────╯
```

---

### Even Process

A process where 1s must appear in runs of even length (pairs).

```python
from emic.sources import EvenProcessSource
from emic.output import render_state_diagram

source = EvenProcessSource(p=0.5)
diagram = render_state_diagram(source.true_machine)
diagram.render("even_process", format="svg")
```

**Properties:**

- **States:** 2
- **Constraint:** 1s always come in pairs
- **Characteristic:** After one 1, must emit another 1

```
          0 (p)                    1 (1.0)
    ╭───────────╮              ╭───────────╮
    │           │              │           │
    ▼           │              ▼           │
╭───────╮       │        ╭───────╮         │
│       │───────╯        │       │─────────╯
│   A   │                │   B   │
│       │───────────────▶│       │
╰───────╯    1 (1-p)     ╰───────╯
```

---

### Periodic Processes

Deterministic processes that cycle through a fixed pattern.

#### Period-2 (Alternating)

```python
from emic.sources import PeriodicSource
from emic.output import render_state_diagram

source = PeriodicSource(pattern=(0, 1))
diagram = render_state_diagram(source.true_machine)
diagram.render("period_2", format="svg")
```

**Properties:**

- **Pattern:** 0, 1, 0, 1, 0, 1, ...
- **States:** 2
- **Statistical Complexity:** log₂(2) = 1 bit
- **Entropy Rate:** 0 (fully deterministic)

```
╭───────╮   0 (1.0)   ╭───────╮
│       │────────────▶│       │
│   A   │             │   B   │
│       │◀────────────│       │
╰───────╯   1 (1.0)   ╰───────╯
```

#### Period-3

```python
source = PeriodicSource(pattern=(0, 1, 2))
diagram = render_state_diagram(source.true_machine)
diagram.render("period_3", format="svg")
```

**Properties:**

- **Pattern:** 0, 1, 2, 0, 1, 2, ...
- **States:** 3
- **Statistical Complexity:** log₂(3) ≈ 1.58 bits

```
    ╭───────╮
    │       │
    │   A   │─────0 (1.0)────▶╭───────╮
    │       │                 │       │
    ╰───────╯                 │   B   │
         ▲                    │       │
         │                    ╰───────╯
    2 (1.0)                        │
         │                    1 (1.0)
    ╭───────╮                      │
    │       │◀─────────────────────╯
    │   C   │
    │       │
    ╰───────╯
```

---

## Rendering Options

The `DiagramStyle` class provides extensive customization:

```python
from emic.output import render_state_diagram, DiagramStyle

style = DiagramStyle(
    layout="circo",           # Circular layout
    node_color="#6c5ce7",     # Purple nodes
    show_probabilities=True,  # Show edge probabilities
    probability_format=".3f", # 3 decimal places
    node_shape="doublecircle",
)

diagram = render_state_diagram(machine, style=style)
```

### Available Layouts

| Layout | Description | Best For |
|--------|-------------|----------|
| `dot`  | Hierarchical | Tree-like structures |
| `neato`| Spring model | General graphs |
| `circo`| Circular | Cyclic processes |
| `fdp`  | Force-directed | Complex machines |

### Output Formats

```python
# Save as SVG (vector, best for web)
diagram.render("machine", format="svg")

# Save as PDF (vector, best for papers)
diagram.render("machine", format="pdf")

# Save as PNG (raster, for presentations)
diagram.render("machine", format="png")

# Get SVG source as string
svg_source = diagram.pipe(format="svg").decode()
```

---

## Jupyter Notebook Display

In Jupyter notebooks, use `display_state_diagram` for inline rendering:

```python
from emic.output import display_state_diagram
from emic.sources import GoldenMeanSource

source = GoldenMeanSource(p=0.5)
display_state_diagram(source.true_machine)
```

---

## Inferred Machines

Visualize machines inferred from data:

```python
from emic.sources import GoldenMeanSource
from emic.sources.transforms import TakeN
from emic.inference import CSSR, CSSRConfig
from emic.output import render_state_diagram

# Generate data
source = GoldenMeanSource(p=0.5, _seed=42)
sequence = list(TakeN(10000)(source))

# Infer machine
config = CSSRConfig(max_history=5, significance=0.01)
result = CSSR(config).infer(sequence)

# Visualize
diagram = render_state_diagram(result.machine)
diagram.render("inferred_golden_mean", format="svg")
```

---

## Algorithm Comparison

Compare machines inferred by different algorithms:

```python
from emic.inference import CSSR, CSM, BSI, NSD, Spectral
from emic.output import render_state_diagram

algorithms = [
    ("CSSR", CSSR(CSSRConfig(max_history=5))),
    ("CSM", CSM(CSMConfig(history_length=5))),
    ("BSI", BSI(BSIConfig(max_states=5))),
    ("NSD", NSD(NSDConfig(max_states=5))),
    ("Spectral", Spectral(SpectralConfig(max_history=5))),
]

for name, algo in algorithms:
    result = algo.infer(sequence)
    diagram = render_state_diagram(result.machine)
    diagram.render(f"comparison_{name.lower()}", format="svg")
    print(f"{name}: {len(result.machine.states)} states")
```

---

## Custom State Labels

Use meaningful names instead of auto-generated IDs:

```python
style = DiagramStyle(
    state_labels={
        "s0": "After 0",
        "s1": "After 1",
    },
    symbol_labels={
        "0": "L",  # Left
        "1": "R",  # Right
    },
)

diagram = render_state_diagram(machine, style=style)
```
