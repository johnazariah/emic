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

### Citation Key Convention

Use `firstauthor_year` format with optional disambiguator:

| Pattern | Example |
|---------|---------|
| `author_year` | `crutchfield1989` |
| `author_yeartopic` | `shalizi2001computational` |
| `author_yearX` | `crutchfield2012a`, `crutchfield2012b` |

### Adding a New Reference

1. Add the entry to `shared/bibliography/references.bib`
2. Use the `firstauthor_year` key convention
3. Always include `doi` when available
4. The entry is immediately available to all papers

### JOSS Symlink

`paper-joss/paper.bib` is a **symlink** to `../shared/bibliography/references.bib`. Do not replace it with a regular file. The JOSS front matter references `bibliography: paper.bib` which resolves through the symlink.

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
