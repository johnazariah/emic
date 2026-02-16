# Benchmark and Report Pipeline
# Usage:
#   make                    # One-stop: run benchmarks + generate tables
#   make fast               # Same but skip BSI (~5 min vs ~30 min)
#   make analyze            # Just regenerate tables from existing data

PROJECT_ROOT = ../..
WORKSPACE = ../../../..
REPORT_DIR = $(PROJECT_ROOT)/technical-report/tex
RESULTS_DIR = results

.PHONY: all fast benchmarks benchmarks-fast analyze report clean

# Default: run benchmarks + generate tables
all: benchmarks analyze

# Fast mode: skip BSI
fast: benchmarks-fast analyze

# Run full benchmarks via emic-experiment
benchmarks:
	@echo "Running full benchmarks..."
	cd $(WORKSPACE) && uv run emic-experiment --all --timeout 300
	@mkdir -p $(RESULTS_DIR)
	@cp $(WORKSPACE)/experiments/runs/latest/results.json $(RESULTS_DIR)/ 2>/dev/null || true
	@cp $(WORKSPACE)/experiments/runs/latest/results.parquet $(RESULTS_DIR)/ 2>/dev/null || true

# Fast benchmarks: skip BSI
benchmarks-fast:
	@echo "Running fast benchmarks (skip BSI)..."
	cd $(WORKSPACE) && uv run emic-experiment --all --algorithms cssr,spectral,csm,nsd --timeout 120
	@mkdir -p $(RESULTS_DIR)
	@cp $(WORKSPACE)/experiments/runs/latest/results.json $(RESULTS_DIR)/ 2>/dev/null || true
	@cp $(WORKSPACE)/experiments/runs/latest/results.parquet $(RESULTS_DIR)/ 2>/dev/null || true

# Run tests and collect stats (test count + coverage)
test-stats:
	@echo "Collecting test statistics..."
	cd $(WORKSPACE) && uv run pytest --collect-only -q 2>/dev/null | grep -o '[0-9]* tests' | head -1
	cd $(WORKSPACE) && uv run pytest --cov=src/emic --cov-report=term -q --tb=no 2>&1 | grep "TOTAL"

# Generate LaTeX tables
analyze:
	@echo "Generating LaTeX tables..."
	uv run python analyze_results.py
	@echo "Tables written to $(REPORT_DIR)/generated/"

# Compile technical report
report: analyze
	@echo "Compiling technical report..."
	cd $(REPORT_DIR) && pdflatex -interaction=nonstopmode technical-report.tex
	cd $(REPORT_DIR) && biber technical-report || true
	cd $(REPORT_DIR) && pdflatex -interaction=nonstopmode technical-report.tex
	@echo "Report: $(REPORT_DIR)/technical-report.pdf"

# Clean generated files
clean:
	rm -rf $(RESULTS_DIR)
	rm -f $(REPORT_DIR)/generated/*.tex
