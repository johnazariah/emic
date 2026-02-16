# JOSS Paper

**Target:** [Journal of Open Source Software](https://joss.theoj.org/)
**Status:** Draft

## Files

- `paper.md` — The paper (Markdown with YAML front matter, required by JOSS)
- `paper.bib` — BibTeX references

## Format

JOSS **requires Markdown** (`paper.md` + `paper.bib`). LaTeX is not accepted.
JOSS compiles the PDF from Markdown via Pandoc/ConTeXt internally upon
submission. Authors can preview the compiled PDF locally before submitting.

## Preview PDF Locally

### Option 1: Docker (recommended)

```bash
docker run --rm \
    --volume "$PWD:/data" \
    --user "$(id -u):$(id -g)" \
    --env JOURNAL=joss \
    openjournals/inara
```

This produces `paper.pdf` in the current directory.

### Option 2: GitHub Action

Add the [Open Journals PDF Generator](https://github.com/marketplace/actions/open-journals-pdf-generator)
action to `.github/workflows/`. The compiled PDF will appear as a build artifact.

```yaml
# .github/workflows/joss-paper.yml
name: JOSS Paper PDF
on:
  push:
    paths:
      - 'paper-joss/**'
  pull_request:
    paths:
      - 'paper-joss/**'

jobs:
  paper:
    runs-on: ubuntu-latest
    name: Compile JOSS Paper
    steps:
      - uses: actions/checkout@v4
      - uses: openjournals/openjournals-draft-action@master
        with:
          journal: joss
          paper-path: paper-joss/paper.md
      - uses: actions/upload-artifact@v4
        with:
          name: joss-paper
          path: paper-joss/paper.pdf
```

## Including in Release Artifacts

To include the compiled JOSS paper PDF in GitHub releases, add a step to the
release workflow that builds the PDF and attaches it:

```yaml
# Add to your existing release workflow (.github/workflows/release.yml)
  joss-paper:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: openjournals/openjournals-draft-action@master
        with:
          journal: joss
          paper-path: paper-joss/paper.md
      - uses: actions/upload-artifact@v4
        with:
          name: joss-paper
          path: paper-joss/paper.pdf

  # Then in your release job, download and attach:
  release:
    needs: [joss-paper]
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: joss-paper
      - name: Attach paper to release
        uses: softprops/action-gh-release@v2
        with:
          files: paper.pdf
```

## Submission Checklist

Before submitting to JOSS:

- [ ] Paper compiles to PDF without errors
- [ ] Word count is 750–1750 words
- [ ] All required sections present (Summary, Statement of Need, State of the
      Field, Software Design, Research Impact Statement, AI Usage Disclosure)
- [ ] `paper.md` and `paper.bib` are in the main repository (not a submodule)
- [ ] Associated publications (review paper, technical report) submitted to arXiv
- [ ] Software version tagged and archived on Zenodo
- [ ] Package available on PyPI
- [ ] README, documentation, and tests are up to date
- [ ] AI Usage Disclosure is complete and accurate

## Submission

1. Ensure `paper.md` and `paper.bib` are in the repo (can be in a branch)
2. Go to https://joss.theoj.org/papers/new
3. Fill in the short submission form
4. Wait for a pre-review issue at https://github.com/openjournals/joss-reviews

## Associated Publications

- **Technical report**: "emic: A Python Framework for ε-Machine Inference" (arXiv, forthcoming)
  — includes Appendix B: "Computational Mechanics: A Modern Review" with full proofs
- **Review paper**: to be developed as a standalone journal submission (in progress)

## See Also

- [JOSS submission guide](https://joss.readthedocs.io/en/latest/submitting.html)
- [JOSS paper format](https://joss.readthedocs.io/en/latest/paper.html)
- [JOSS review criteria](https://joss.readthedocs.io/en/latest/review_criteria.html)
- [Publication Strategy](../publication-strategy.md)
