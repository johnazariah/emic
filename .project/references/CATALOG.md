# References Catalog

This directory contains academic papers relevant to the emic project. Each PDF has a corresponding folder with full text extraction in markdown format.

## Quick Reference

| Paper | Authors | Year | Topic | Pages |
|-------|---------|------|-------|-------|
| [Computational Mechanics](9907176v2/) | Shalizi, Crutchfield | 2000 | Core CM theory | 29 |
| [Calculi of Emergence](Calculus_Of_Emergence_Crutchfield/) | Crutchfield | 1994 | Emergence, complexity | 61 |
| [Extreme Quantum Advantage (Ising)](aghamohammadi2017extreme/) | Aghamohammadi, Mahoney, Crutchfield | 2017 | Quantum CM, Ising | 9 |
| [Extreme Quantum Advantage (Rare Events)](aghamohammadi2018rare/) | Aghamohammadi, Loomis, Mahoney, Crutchfield | 2018 | Quantum rare-event sampling | 11 |
| [Closing the Loop (PSR)](boots2011closing/) | Boots | 2009 | Predictive state representations | 10 |
| [Causal Architecture (PhD Thesis)](cosma-shalizi-thesis/) | Shalizi | 2001 | Complete CM framework | 182 |
| [Unbounded Memory Advantage](garner2017unbounded/) | Garner, Liu, Thompson, Vedral, Gu | 2017 | Quantum advantage, random walks | 12 |
| [Occam's Quantum Razor](gu2012quantum/) | Gu, Wiesner, Rieper, Vedral | 2012 | Quantum CM foundations | 6 |
| [Spectral Algorithm for HMMs](hsu2012spectral/) | Hsu, Kakade, Zhang | 2012 | Spectral learning | 30 |
| [Anatomy of a Bit](james2011anatomy/) | James, Ellison, Crutchfield | 2011 | Information anatomy | 15 |
| [Strong/Weak Optimizations](loomis2019strong/) | Loomis, Crutchfield | 2019 | Quantum model minimality | 14 |
| [Computational Mechanics (JSP)](shalizi2001computational/) | Shalizi, Crutchfield | 2001 | Core CM, JSP version | 29 |
| [CSSR Algorithm](shalizi2004algorithm/) | Shalizi, Klinkner | 2004 | CSSR implementation | 8 |
| [Mathematical Theory of Communication](shannon1948mathematical/) | Shannon | 1948 | Information theory foundations | 55 |
| [Towards Quantifying Complexity](tan2014towards/) | Tan, Terno, Thompson, Vedral, Gu | 2014 | Quantum complexity measure | 10 |
| [Causal Asymmetry](thompson2018causal/) | Thompson, Garner, Vedral, Gu | 2018 | Time asymmetry, quantum CM | 14 |
| [HMM Tutorial](tutorial_on_hmm_and_applications/) | Rabiner | 1989 | HMM foundations | 30 |

## Directory Structure

```
references/
├── CATALOG.md              # This file
├── extract_pdf.py          # Extraction script
├── <paper_name>.pdf        # Original PDF
└── <paper_name>/
    ├── <paper_name>_full.md    # Full text extraction
    └── README.md               # (if extraction failed)
```

## Categories

### Core Computational Mechanics
- `shalizi2001computational/` - Foundational JSP paper
- `9907176v2/` - Earlier arXiv version
- `cosma-shalizi-thesis/` - Complete treatment (PhD thesis)
- `Calculus_Of_Emergence_Crutchfield/` - Emergence theory
- `shalizi2004algorithm/` - CSSR algorithm details

### Information Theory
- `shannon1948mathematical/` - Shannon's original paper
- `james2011anatomy/` - Information decomposition

### Quantum Computational Mechanics
- `gu2012quantum/` - Occam's Quantum Razor (foundational)
- `garner2017unbounded/` - Unbounded advantage proof
- `tan2014towards/` - Quantum complexity measure Cq
- `thompson2018causal/` - Causal asymmetry
- `aghamohammadi2017extreme/` - Ising model advantage
- `aghamohammadi2018rare/` - Rare event sampling
- `loomis2019strong/` - Strong/weak minimality

### Spectral Methods
- `hsu2012spectral/` - Spectral HMM learning
- `boots2011closing/` - Predictive state representations

### Hidden Markov Models
- `tutorial_on_hmm_and_applications/` - Rabiner's HMM tutorial (image-based, no extraction)

## Usage

### Extract a new PDF
```bash
python3 extract_pdf.py path/to/paper.pdf
```

### Search across all papers
```bash
grep -r "causal state" */
```

## Notes

- Full text extractions preserve the original paper structure
- Some mathematical notation may be garbled (LaTeX conversion not applied)
- The HMM tutorial PDF is image-based and requires OCR
