#!/usr/bin/env bash
# ===========================================================================
# build-all.sh — Build PDFs and arXiv tarballs for all publications
#
# Usage:
#   ./build-all.sh              # Build everything
#   ./build-all.sh pdf          # Build PDFs only
#   ./build-all.sh arxiv        # Package arXiv tarballs only (requires PDFs)
#   ./build-all.sh joss         # Build JOSS preview PDF (requires Docker)
#   ./build-all.sh clean        # Remove build artifacts
#
# Prerequisites:
#   - latexmk, pdflatex, bibtex, biber (for LaTeX builds)
#   - Docker (optional, for JOSS PDF preview)
# ===========================================================================
set -euo pipefail

# --- Configuration --------------------------------------------------------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$SCRIPT_DIR"
DIST="$ROOT/dist"

REVIEW="$ROOT/review-paper/tex"
TECHREPORT="$ROOT/technical-report/tex"
TUTORIAL="$ROOT/tutorial/tex"
JOSS="$ROOT/joss"
SHARED_BIB="$ROOT/shared/bibliography/references.bib"
BENCH_FIGS="$ROOT/../experiments/benchmarks/results/figures"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m'

info()  { echo -e "${GREEN}[INFO]${NC}  $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
error() { echo -e "${RED}[ERROR]${NC} $*" >&2; }

# --- Helpers --------------------------------------------------------------

require_cmd() {
    command -v "$1" >/dev/null 2>&1 || { error "Required command '$1' not found"; exit 1; }
}

# Build a LaTeX document with latexmk
build_pdf() {
    local dir="$1" main="$2" engine="${3:-pdflatex}"
    info "Building ${BOLD}${main}.pdf${NC} in $dir"
    pushd "$dir" > /dev/null
    if [[ "$engine" == "biber" ]]; then
        # biblatex needs biber; latexmk handles this via .latexmkrc
        latexmk -pdf -interaction=nonstopmode -halt-on-error "$main.tex" 2>&1 \
            | grep -E '^(! |Latexmk|Output written)' || true
    else
        latexmk -pdf -interaction=nonstopmode -halt-on-error "$main.tex" 2>&1 \
            | grep -E '^(! |Latexmk|Output written)' || true
    fi
    popd > /dev/null

    # Copy to dist/
    local pdf
    if [[ -f "$dir/out/$main.pdf" ]]; then
        pdf="$dir/out/$main.pdf"
    elif [[ -f "$dir/$main.pdf" ]]; then
        pdf="$dir/$main.pdf"
    else
        error "PDF not found for $main"
        return 1
    fi
    cp "$pdf" "$DIST/$main.pdf"
    info "  → ${BOLD}dist/$main.pdf${NC}"
}

# --- PDF Builds -----------------------------------------------------------

build_review_pdf() {
    build_pdf "$REVIEW" "review-paper"
}

build_techreport_pdf() {
    build_pdf "$TECHREPORT" "technical-report" "biber"
}

build_tutorial_pdf() {
    build_pdf "$TUTORIAL" "tutorial"
}

build_joss_pdf() {
    if command -v docker >/dev/null 2>&1; then
        info "Building ${BOLD}JOSS paper.pdf${NC} via Docker"
        docker run --rm \
            --volume "$JOSS:/data" \
            --user "$(id -u):$(id -g)" \
            --env JOURNAL=joss \
            openjournals/inara 2>&1 | tail -3
        cp "$JOSS/paper.pdf" "$DIST/joss-paper.pdf"
        info "  → ${BOLD}dist/joss-paper.pdf${NC}"
    else
        warn "Docker not available — skipping JOSS PDF preview"
        warn "  Install Docker or use the GitHub Action (see joss/README.md)"
    fi
}

build_all_pdfs() {
    build_review_pdf
    build_techreport_pdf
    build_tutorial_pdf
    build_joss_pdf
}

# --- arXiv Packaging ------------------------------------------------------

# Package a paper for arXiv submission.
# arXiv compiles from source, so we must:
#   1. Flatten all \input / \includegraphics paths to be relative
#   2. Include the .bbl (compiled bibliography), NOT the .bib
#   3. Include all figures as PDF/PNG (no nested ../.. paths)
#   4. Remove \addbibresource / \bibliography lines (replaced by .bbl)

arxiv_review() {
    info "Packaging ${BOLD}review-paper${NC} for arXiv"
    local out="$DIST/arxiv-review-paper"
    rm -rf "$out" && mkdir -p "$out"

    # Main .tex — rewrite bibliography path to local
    sed 's|\\bibliography{../../shared/bibliography/references}|\\bibliography{references}|g' \
        "$REVIEW/review-paper.tex" > "$out/review-paper.tex"

    # Compiled bibliography
    if [[ -f "$REVIEW/out/review-paper.bbl" ]]; then
        cp "$REVIEW/out/review-paper.bbl" "$out/review-paper.bbl"
    elif [[ -f "$REVIEW/review-paper.bbl" ]]; then
        cp "$REVIEW/review-paper.bbl" "$out/review-paper.bbl"
    else
        error "review-paper.bbl not found — build the PDF first"
        return 1
    fi

    # No external figures — TikZ is inline

    # Create tarball
    tar czf "$DIST/arxiv-review-paper.tar.gz" -C "$DIST" "arxiv-review-paper/"
    info "  → ${BOLD}dist/arxiv-review-paper.tar.gz${NC}"
}

arxiv_techreport() {
    info "Packaging ${BOLD}technical-report${NC} for arXiv"
    local out="$DIST/arxiv-technical-report"
    rm -rf "$out" && mkdir -p "$out/figures"

    # Main .tex — remove \addbibresource (biblatex .bbl is self-contained),
    # and rewrite external figure paths to local figures/ directory
    sed -e 's|\\addbibresource{../../shared/bibliography/references.bib}|% bibliography handled by .bbl|' \
        -e 's|../../experiments/benchmarks/results/figures/|figures/|g' \
        "$TECHREPORT/technical-report.tex" > "$out/technical-report.tex"

    # .latexmkrc for biber
    cp "$TECHREPORT/.latexmkrc" "$out/.latexmkrc" 2>/dev/null || true

    # Compiled bibliography (biblatex format)
    if [[ -f "$TECHREPORT/out/technical-report.bbl" ]]; then
        cp "$TECHREPORT/out/technical-report.bbl" "$out/technical-report.bbl"
    elif [[ -f "$TECHREPORT/technical-report.bbl" ]]; then
        cp "$TECHREPORT/technical-report.bbl" "$out/technical-report.bbl"
    else
        error "technical-report.bbl not found — build the PDF first"
        return 1
    fi

    # generated/ directory (input tables and macros)
    mkdir -p "$out/generated"
    cp "$TECHREPORT/generated/"*.tex "$out/generated/"

    # Local figures
    for f in "$TECHREPORT/figures/"*.pdf; do
        [[ -f "$f" ]] && cp "$f" "$out/figures/"
    done

    # External benchmark figures (flattened into figures/)
    local ext_figs=(
        runtime_scaling.pdf
        memory_scaling.pdf
        correctness_by_process.pdf
        algorithm_comparison.pdf
        runtime_by_process.pdf
    )
    for fig in "${ext_figs[@]}"; do
        if [[ -f "$BENCH_FIGS/$fig" ]]; then
            cp "$BENCH_FIGS/$fig" "$out/figures/$fig"
        else
            warn "Missing external figure: $fig"
        fi
    done

    # Create tarball
    tar czf "$DIST/arxiv-technical-report.tar.gz" -C "$DIST" "arxiv-technical-report/"
    info "  → ${BOLD}dist/arxiv-technical-report.tar.gz${NC}"
}

arxiv_tutorial() {
    info "Packaging ${BOLD}tutorial${NC} for arXiv"
    local out="$DIST/arxiv-tutorial"
    rm -rf "$out" && mkdir -p "$out/figures" "$out/generated"

    # Main .tex — rewrite bibliography path
    sed 's|\\bibliography{../../shared/bibliography/references}|\\bibliography{references}|g' \
        "$TUTORIAL/tutorial.tex" > "$out/tutorial.tex"

    # Compiled bibliography
    if [[ -f "$TUTORIAL/out/tutorial.bbl" ]]; then
        cp "$TUTORIAL/out/tutorial.bbl" "$out/tutorial.bbl"
    elif [[ -f "$TUTORIAL/tutorial.bbl" ]]; then
        cp "$TUTORIAL/tutorial.bbl" "$out/tutorial.bbl"
    else
        error "tutorial.bbl not found — build the PDF first"
        return 1
    fi

    # Figures and generated tables
    cp "$TUTORIAL/figures/"*.pdf "$out/figures/" 2>/dev/null || true
    cp "$TUTORIAL/generated/"*.tex "$out/generated/" 2>/dev/null || true

    # Create tarball
    tar czf "$DIST/arxiv-tutorial.tar.gz" -C "$DIST" "arxiv-tutorial/"
    info "  → ${BOLD}dist/arxiv-tutorial.tar.gz${NC}"
}

arxiv_all() {
    arxiv_review
    arxiv_techreport
    arxiv_tutorial
}

# --- Verify arXiv Package ------------------------------------------------

verify_arxiv() {
    local pkg="$1" main="$2"
    info "Verifying ${BOLD}$pkg${NC} compiles from source"
    local work
    work="$(mktemp -d)"
    tar xzf "$DIST/$pkg.tar.gz" -C "$work"
    pushd "$work/$pkg" > /dev/null
    latexmk -pdf -interaction=nonstopmode -halt-on-error "$main.tex" > /dev/null 2>&1
    local rc=$?
    popd > /dev/null
    rm -rf "$work"
    if [[ $rc -eq 0 ]]; then
        info "  ✓ ${BOLD}$pkg${NC} compiles successfully"
    else
        error "  ✗ ${BOLD}$pkg${NC} failed to compile"
        return 1
    fi
}

verify_all() {
    verify_arxiv "arxiv-review-paper" "review-paper"
    verify_arxiv "arxiv-technical-report" "technical-report"
    verify_arxiv "arxiv-tutorial" "tutorial"
}

# --- Clean ----------------------------------------------------------------

clean() {
    info "Cleaning dist/"
    rm -rf "$DIST"
}

# --- Main -----------------------------------------------------------------

main() {
    require_cmd latexmk
    require_cmd pdflatex
    mkdir -p "$DIST"

    local cmd="${1:-all}"
    case "$cmd" in
        pdf)
            build_all_pdfs
            ;;
        arxiv)
            arxiv_all
            ;;
        verify)
            verify_all
            ;;
        joss)
            build_joss_pdf
            ;;
        review)
            build_review_pdf
            ;;
        techreport)
            build_techreport_pdf
            ;;
        tutorial)
            build_tutorial_pdf
            ;;
        clean)
            clean
            ;;
        all)
            build_all_pdfs
            arxiv_all
            echo ""
            info "${BOLD}All builds complete.${NC} Artifacts in dist/:"
            ls -lh "$DIST"
            ;;
        *)
            echo "Usage: $0 {all|pdf|arxiv|verify|joss|review|techreport|tutorial|clean}"
            exit 1
            ;;
    esac
}

main "$@"
