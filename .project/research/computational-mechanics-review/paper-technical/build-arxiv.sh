#!/usr/bin/env bash
# Build an arXiv submission bundle for the emic technical report.
#
# arXiv requires a flat archive containing:
#   - paper.tex (with paths adjusted to flat layout)
#   - paper.bbl (pre-compiled bibliography)
#   - All generated/*.tex files
#   - All figures/*.pdf files
#   - ai-usage-disclosure.tex snippet
#
# Usage:
#   cd paper-technical && bash build-arxiv.sh
#
# Output:
#   arxiv-submission/          — flat directory with all files
#   emic-technical-arxiv.tar.gz — ready to upload to arxiv.org

set -euo pipefail

OUTDIR="arxiv-submission"
TARBALL="emic-technical-arxiv.tar.gz"

echo "=== Building arXiv submission bundle ==="

# Clean previous build
rm -rf "$OUTDIR" "$TARBALL"
mkdir -p "$OUTDIR"

# 1. Ensure paper is compiled and .bbl exists
echo "1. Compiling paper to generate .bbl ..."
latexmk -pdf -interaction=nonstopmode paper.tex > /dev/null 2>&1 || true

if [[ ! -f paper.bbl ]]; then
    echo "ERROR: paper.bbl not found. Compilation may have failed."
    exit 1
fi

# 2. Copy the .bbl file (arXiv uses this instead of running biber)
cp paper.bbl "$OUTDIR/"

# 3. Copy generated data files
echo "2. Copying generated data files ..."
mkdir -p "$OUTDIR/generated"
cp generated/*.tex "$OUTDIR/generated/"

# 4. Copy figures
echo "3. Copying figures ..."
mkdir -p "$OUTDIR/figures"
cp figures/*.pdf "$OUTDIR/figures/"

# 5. Copy AI usage disclosure snippet
echo "4. Copying shared snippets ..."
# Flatten the path: change \input{../shared/snippets/...} to \input{...}
cp ../shared/snippets/ai-usage-disclosure.tex "$OUTDIR/"

# 6. Create modified paper.tex with flattened paths
echo "5. Creating flattened paper.tex ..."
sed \
    -e 's|\\addbibresource{../shared/bibliography/references.bib}|\\addbibresource{references.bib}|' \
    -e 's|\\input{../shared/snippets/ai-usage-disclosure.tex}|\\input{ai-usage-disclosure.tex}|' \
    paper.tex > "$OUTDIR/paper.tex"

# 7. Copy the .bib file too (some arXiv compilation paths want it)
cp ../shared/bibliography/references.bib "$OUTDIR/references.bib"

# 8. Create the tarball
echo "6. Creating tarball ..."
tar -czf "$TARBALL" -C "$OUTDIR" .

# 9. Report
FILE_COUNT=$(find "$OUTDIR" -type f | wc -l)
TARBALL_SIZE=$(du -h "$TARBALL" | cut -f1)
echo ""
echo "=== arXiv submission bundle ready ==="
echo "  Directory: $OUTDIR/ ($FILE_COUNT files)"
echo "  Tarball:   $TARBALL ($TARBALL_SIZE)"
echo ""
echo "Contents:"
find "$OUTDIR" -type f | sort | sed 's|^'"$OUTDIR"'/|  |'
echo ""
echo "Next steps:"
echo "  1. Go to https://arxiv.org/submit"
echo "  2. Upload $TARBALL"
echo "  3. Select category: cs.AI or nlin.AO (Adaptation and Self-Organizing Systems)"
echo "  4. Verify the compiled PDF renders correctly"
