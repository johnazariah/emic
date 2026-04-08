# Agent Prompt: Make a Repository JOSS-Ready

You are preparing a Python software repository for submission to the **Journal of Open Source Software (JOSS)**. The repo currently has private research content (notes, papers, literature reviews, experiment logs) mixed in with the public software — typically under a `.project/` directory. Your job is to clean it up, separate concerns, and make it submission-ready.

---

## Context

JOSS reviews **software**, not papers. The paper is a short (1–2 page) summary pointing reviewers at the code. JOSS checklist items include: installation, documentation, tests, CI, a clear README, a CITATION.cff, community guidelines (CONTRIBUTING.md), and an archived DOI (Zenodo).

---

## Steps

### 1. Audit the Repository

Identify files that should NOT be in a public software repo:

- Private research notes, journals, roadmaps, reading notes
- Literature references / PDFs (especially copyrighted)
- Unpublished paper drafts (LaTeX sources, rejected arXiv submissions)
- Experiment logs, hypothesis documents, research questions
- Any credentials, API keys, or personal data

Run:
```bash
git ls-files | head -300
find .project/ -type f 2>/dev/null | head -100
```

Categorize everything into **public software** vs **private research**.

### 2. Create a Private Research Repository

Create a separate private repo (e.g., `<project>-research`) for all research content:

```bash
mkdir -p /workspace/<project>-research
cd /workspace/<project>-research
git init
```

Migrate research content with directory structure:
- `papers/` — paper drafts (LaTeX, markdown)
- `research/` — experiments, hypotheses, questions
- `notes/` — reading notes, meeting notes
- `references/` — literature summaries (NOT copyrighted PDFs)
- `plan/` — roadmaps, journals, work plans
- `record/` — decision records, logs

Create a README.md explaining the repo's relationship to the public software repo.

Add, commit, create a private GitHub repo, and push:
```bash
gh repo create <owner>/<project>-research --private
git remote add origin https://github.com/<owner>/<project>-research.git
git push -u origin main
```

### 3. Clean the Public Repository

**Update .gitignore** to exclude research paths:
```gitignore
# Private research content (lives in <project>-research repo)
.project/notes/
.project/plan/
.project/record/
.project/references/
.project/research/
.project/experiments/

# External research repo
<project>-research/
```

**Remove research files from git tracking** (but keep on disk if needed):
```bash
git rm -r --cached .project/notes/ .project/research/ .project/references/ ...
git commit -m "chore: remove private research content from tracking"
```

**Update any internal docs** (copilot-instructions.md, CONTRIBUTING.md) that reference moved content. Add a note like:
> Research planning lives in the private `<project>-research` repo. This repo focuses on the public software.

### 4. Prepare the JOSS Paper

Create a `joss/` directory at the repo root with two files:

**`joss/paper.md`** — JOSS paper in Pandoc Markdown with YAML frontmatter:
```markdown
---
title: "<Title>: <Subtitle>"
tags:
  - Python
  - <domain-specific tags>
authors:
  - name: <Full Name>
    orcid: <ORCID>
    affiliation: 1
affiliations:
  - name: <Institution, City, Country>
    index: 1
date: <DD Month YYYY>
bibliography: paper.bib
---

# Summary

<1-2 paragraphs: what the software does and why it matters>

# Statement of Need

<Who needs this? What gap does it fill? How does it compare to alternatives?>

# Key Features

<Bullet points or short sections on the main capabilities>

# Design and Implementation

<Architecture overview, key design decisions>

# Validation

<How correctness is verified — tests, benchmarks, comparisons to known results>

# Availability

<Where to get it, how to install, where docs live>

# Acknowledgements

<Funding, supervision, contributors>

# References
```

**`joss/paper.bib`** — BibTeX bibliography. Include citations for:
- The foundational work your software builds on
- Key algorithms implemented
- Competing/related software packages
- Any datasets or benchmarks used

**Critical rules for the JOSS paper:**
- Do NOT cite unpublished preprints or rejected submissions
- Do NOT reference companion papers that don't exist yet
- Every `@citation` in paper.md must resolve to an entry in paper.bib
- Keep it under 1000 words (JOSS guideline)
- Must include: Summary, Statement of Need, References sections minimum

### 5. Set Up Draft Paper CI Workflow

Create **`.github/workflows/draft-paper.yml`**:
```yaml
name: Draft JOSS Paper

on:
  workflow_dispatch:
  push:
    tags-ignore:
      - 'v*'
    paths:
      - 'joss/**'
      - '.github/workflows/draft-paper.yml'
  pull_request:
    paths:
      - 'joss/**'

jobs:
  paper:
    name: Build JOSS Paper PDF
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build draft PDF
        uses: openjournals/openjournals-draft-action@master
        with:
          journal: joss
          paper-path: joss/paper.md

      - name: Upload paper PDF
        uses: actions/upload-artifact@v4
        with:
          name: joss-paper
          path: joss/paper.pdf
```

If the release workflow bundles JOSS paper artifacts, update those paths from any old location to `joss/paper.md` and `joss/paper.bib`.

Delete any workflows for LaTeX publications that were moved to the research repo.

### 6. Ensure CITATION.cff Exists and Is Current

Create or update `CITATION.cff` at the repo root:
```yaml
cff-version: 1.2.0
message: "If you use this software, please cite it as below."
title: "<Project Title>"
authors:
  - family-names: <Last>
    given-names: <First>
    orcid: "https://orcid.org/<ORCID>"
version: <current version>
date-released: <YYYY-MM-DD>
license: MIT
repository-code: https://github.com/<owner>/<repo>
keywords:
  - <keyword1>
  - <keyword2>
type: software
```

### 7. README Badges

Ensure the README has these badges near the top:
```markdown
[![CI](https://github.com/<owner>/<repo>/actions/workflows/ci.yml/badge.svg)](https://github.com/<owner>/<repo>/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/<package>)](https://pypi.org/project/<package>/)
[![Docs](https://github.com/<owner>/<repo>/actions/workflows/docs.yml/badge.svg)](https://<owner>.github.io/<repo>/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![DOI](https://zenodo.org/badge/DOI/<DOI>.svg)](https://doi.org/<DOI>)
```

The DOI badge requires Zenodo integration (Step 8).

### 8. Zenodo Integration

1. Go to https://zenodo.org and log in with GitHub
2. Enable the repository in Zenodo's GitHub settings
3. Tag a release (`git tag v<X.Y.Z> && git push origin v<X.Y.Z>`)
4. Zenodo will automatically mint a DOI
5. Add the DOI badge to README.md
6. Update CITATION.cff with the DOI if desired

### 9. Pre-Submission Checklist

Before submitting, verify:

- [ ] **Installation works**: `pip install <package>` from PyPI succeeds
- [ ] **Tests pass**: CI is green, good coverage
- [ ] **Docs are live**: hosted documentation accessible
- [ ] **README** has: description, installation, quickstart, badges, citation info
- [ ] **CONTRIBUTING.md** exists with contribution guidelines
- [ ] **LICENSE** file exists (MIT, BSD, Apache, etc.)
- [ ] **CITATION.cff** is correct and current
- [ ] **JOSS paper compiles**: trigger the draft-paper workflow and confirm success
- [ ] **No private content**: `git ls-files` shows only public software files
- [ ] **No broken citations**: every `@ref` in paper.md has a paper.bib entry
- [ ] **Zenodo DOI** is minted and badge is on README
- [ ] **Version tag** matches pyproject.toml version

### 10. Submit to JOSS

Go to https://joss.theoj.org/papers/new and fill in:

| Field | Value |
|-------|-------|
| Repository URL | `https://github.com/<owner>/<repo>` |
| Branch | `main` |
| Software version | `v<X.Y.Z>` |
| Title | From paper.md frontmatter |
| Languages | Python |
| Subject | Pick the closest match |
| Message | Brief description, note no prior publication, no conflicts |

---

## Common Pitfalls

1. **Citing unpublished work** — JOSS reviewers will flag this. Only cite published, accessible references.
2. **Workflow paths out of date** — If you move files (e.g., paper from `.project/research/.../paper.md` to `joss/paper.md`), update ALL workflow files that reference the old paths.
3. **Forgetting `workflow_dispatch`** — Add it to the draft-paper workflow so you can trigger builds manually.
4. **CITATION.cff version drift** — Keep it in sync with pyproject.toml version.
5. **Copyrighted PDFs in git history** — Even after `git rm`, they're in history. Consider `git filter-repo` if needed, or note that JOSS reviewers look at the current state, not history.
6. **Docker not available locally** — You can't test JOSS compilation locally without Docker. Use the GitHub Action workflow instead.
