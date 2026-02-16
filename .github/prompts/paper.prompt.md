# Research Paper Writing & Building

You are helping write, edit, and build academic papers for the **emic** computational mechanics project.

---

## Paper Portfolio

All papers live under `.project/research/computational-mechanics-review/`:

| Directory | Title | Format | Target Venue | Status |
|-----------|-------|--------|--------------|--------|
| `paper-joss/` | emic: A Python Framework for Epsilon-Machine Inference | Markdown | JOSS | Draft complete |
| `paper-tutorial/` | Computational Mechanics Tutorial | LaTeX (BibTeX) | University seminars | Draft (~31 pp) |
| `paper-review/` | Computational Mechanics Review | LaTeX (BibTeX) | Entropy / JMLR | Outline |
| `paper-technical/` | Benchmarks & Architecture | LaTeX (biblatex/biber) | Thesis chapter / arXiv | Draft (~40 pp) |
| `paper-framework/` | emic Framework Deep-Dive | LaTeX | arXiv | Early stage |

### Format Details

- **JOSS** (`paper-joss/`): Markdown front matter + `paper.md`, ~1000 words max. Built by GitHub Actions via `openjournals/openjournals-draft-action`. No local build needed — push to trigger CI.
- **LaTeX papers**: Each has `paper.tex` as the main file. Built with `latexmk -pdf`.
- **Technical report** uses `biblatex`/`biber` (not BibTeX). It has a `.latexmkrc` that sets `$bibtex_use = 2` and `$biber = 'biber %O %S'`.
- All other LaTeX papers use standard BibTeX via `\bibliography{../shared/bibliography/references}`.

---

## Shared Bibliography

**Single shared .bib file**: `shared/bibliography/references.bib`

**Canonical author metadata**: `shared/metadata/author-profile.yaml`

### Canonical Author Profile (use exactly)

- Name: John S Azariah
- Affiliation: University of Technology, Sydney (UTS)
- ORCID: 0009-0007-9870-1970
- Email: john.azariah@student.uts.edu.au

**Shared AI disclosure snippets**:
- Markdown: `shared/snippets/ai-usage-disclosure.md`
- LaTeX: `shared/snippets/ai-usage-disclosure.tex`

Before drafting a new paper, follow:
`paper-framework/new-paper-checklist.md`

### Citation Key Convention

Use `{first-author-name}{year}[{tag}]` format:

| Pattern | Example |
|---------|---------|
| `authoryear` | `crutchfield1989` |
| `authoryeartag` | `shalizi2001computational` |
| `authoryearx` | `crutchfield2012a`, `crutchfield2012b` |

### Adding a New Reference

1. Add the entry to `shared/bibliography/references.bib`
2. Use the `{first-author-name}{year}[{tag}]` key convention
3. Always include `doi` when available
4. The entry is immediately available to all papers

### JOSS Symlink

`paper-joss/paper.bib` may be maintained as a symlink to `../shared/bibliography/references.bib` for tool compatibility. The canonical source of truth is always `shared/bibliography/references.bib`.

---

## Building Papers

### Local Build

```bash
cd .project/research/computational-mechanics-review

# Build all PDFs
make pdf

# Build a specific paper
make review
make techreport
make tutorial

# Build all + arXiv packages
make all

# See all targets
make help
```

The build system uses `build-all.sh` which handles PDF compilation, arXiv packaging, and verification.

### JOSS Paper (CI only)

The JOSS paper builds via GitHub Actions (`draft-paper.yml`). Push changes to `paper-joss/` or `shared/bibliography/` to trigger a build. The workflow produces a PDF artifact.

### arXiv Packaging

```bash
make arxiv        # Package all arXiv tarballs
make verify       # Verify they compile from source
```

arXiv tarballs go to `dist/` and include the `.tex`, `.bbl`, and any figures.

---

## Writing Guidelines

### LaTeX Conventions

- **One sentence per line** — makes diffs cleaner and review easier
- Use `\cref{}` for cross-references where the package is loaded
- Define recurring symbols in a shared preamble or `\newcommand`:
  - `\eM` for epsilon-machine (εM)
  - `\Cmu` for statistical complexity (Cμ)
  - `\hmu` for entropy rate (hμ)
- Figures: prefer TikZ/pgfplots for reproducibility; place data in `generated/` subdirectories

### JOSS Conventions

- Markdown with YAML front matter
- References via `@citekey` syntax (pandoc-style)
- Maximum ~1000 words
- Must include: Summary, Statement of Need, References
- See [JOSS submission guidelines](https://joss.readthedocs.io/en/latest/submitting.html)

### General

- British English spelling (consistent with the rest of the project)
- Define acronyms on first use
- Every claim should be backed by a citation or experimental result
- Cross-reference between papers where appropriate (they form a coherent set)

## Review Paper Standard (Critical)

For `paper-review/`, treat the manuscript as a **state-of-the-art checkpoint**.
It is not sufficient to explain core concepts only.

### Required Characteristics

1. **Comprehensive citation depth**
  - Typical target: **100+ references** (preferred target: 120+)
  - Cover foundations, methods, extensions, and applications
  - Avoid heavy over-concentration on a small canonical subset

2. **Evolution-focused synthesis**
  - For each major topic, answer:
    - What was known originally?
    - What changed in later work?
    - What is now considered established vs tentative?
  - Include a dedicated “recent advances” synthesis (e.g., 2020 onward)

3. **Application mapping**
  - Summarize real usage across domains (physics, biology, neuroscience, linguistics, finance, etc.)
  - Distinguish conceptual proposals from validated deployments

4. **Evidence quality signaling**
  - Label claims as theorem-backed, benchmark-backed, case-study evidence, or speculative
  - Surface unresolved contradictions and replication gaps

5. **Actionable research outlook**
  - End with an open-problem matrix:
    - unresolved problem
    - best current methods
    - blocker
    - near-term experiment

### Practical Workflow for `paper-review/`

1. Build section taxonomy first (foundations, inference, extensions, applications, recent advances)
2. Populate synthesis tables before prose polishing
3. Track citation counts by category during drafting
4. Check for balance before each major draft freeze
5. Ensure final draft exceeds 100 references and includes broad domain coverage

---

## Paper Relationships

The papers form a progression:

```
Tutorial (learn the theory)
    → Review (formal treatment)
        → Technical Report (implementation + benchmarks)
            → JOSS (citable software)
                → Framework (deep architecture dive)
```

When writing one paper, be aware of what the others cover to avoid duplication and ensure cross-references are accurate.

---

## Workflow

1. **Before writing**: Read the paper's README and any existing outline
2. **Adding citations**: Add to shared bib, use consistent keys
3. **After editing LaTeX**: Build locally to verify compilation
4. **After editing JOSS**: Push to trigger CI build; check the artifact
5. **Generated content**: Experimental results go in `generated/` subdirectories; never hand-edit generated `.tex` files
6. **Figures**: Commit source (TikZ, plotting scripts); generated PDFs are build artifacts

## Consistency Stewardship

For repeatable cross-paper consistency checks, use:
`.github/prompts/journal-steward-agent.prompt.md`
