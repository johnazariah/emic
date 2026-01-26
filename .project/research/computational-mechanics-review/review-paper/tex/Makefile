# Review Paper Build

.PHONY: all clean view

# Output directory
OUT = out

# Main document
MAIN = review-paper

all: $(OUT)/$(MAIN).pdf

$(OUT)/$(MAIN).pdf: $(MAIN).tex
	@mkdir -p $(OUT)
	latexmk -pdf -outdir=$(OUT) -interaction=nonstopmode $(MAIN).tex

# Quick build without latexmk
quick:
	@mkdir -p $(OUT)
	pdflatex -output-directory=$(OUT) $(MAIN).tex
	bibtex $(OUT)/$(MAIN)
	pdflatex -output-directory=$(OUT) $(MAIN).tex
	pdflatex -output-directory=$(OUT) $(MAIN).tex

# Clean auxiliary files
clean:
	rm -rf $(OUT)/*.aux $(OUT)/*.log $(OUT)/*.bbl $(OUT)/*.blg \
	       $(OUT)/*.toc $(OUT)/*.out $(OUT)/*.fls $(OUT)/*.fdb_latexmk

# Full clean including PDF
distclean:
	rm -rf $(OUT)

# View the PDF
view: $(OUT)/$(MAIN).pdf
	@if command -v xdg-open > /dev/null; then \
		xdg-open $(OUT)/$(MAIN).pdf; \
	elif command -v open > /dev/null; then \
		open $(OUT)/$(MAIN).pdf; \
	fi

# Word count
count:
	@texcount -1 -sum $(MAIN).tex | tail -1
