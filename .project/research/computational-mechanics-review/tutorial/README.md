# Tutorial: A Practical Guide to Computational Mechanics

**Status:** Drafting
**Target:** University seminars, workshops, online course
**Format:** PDF + Slides (via Quarto or Beamer)

## Build

```bash
# Build PDF
cd tex && latexmk -pdf main.tex

# Build slides (if using Quarto)
quarto render slides.qmd
```

## Structure

See `tex/main.tex` for the document and `../publication-strategy.md` for the full outline.
