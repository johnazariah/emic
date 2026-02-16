# Benchmark and Report Pipeline
# Usage: make report

PROJECT_ROOT = ../..
WORKSPACE = ../../../..
REPORT_DIR = $(PROJECT_ROOT)/technical-report/tex
RESULTS_DIR = results

.PHONY: all benchmarks analyze report test-stats clean

# Default: run everything
all: report

# Run benchmarks (slow - ~10 min)
benchmarks:
	@echo "Running benchmarks..."
	uv run python run.py
	@echo "Benchmarks complete. Results in $(RESULTS_DIR)/"

# Run tests and collect stats (test count + coverage)
test-stats:
	@echo "Collecting test statistics..."
	cd $(WORKSPACE) && uv run pytest --collect-only -q 2>/dev/null | grep -o '[0-9]* tests' | head -1
	cd $(WORKSPACE) && uv run pytest --cov=src/emic --cov-report=term -q --tb=no 2>&1 | grep "TOTAL"

# Analyze results and generate LaTeX tables + macros
analyze: $(RESULTS_DIR)/summaries.json
	@echo "Generating LaTeX tables and macros..."
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
