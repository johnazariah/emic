# Review Paper Build

.PHONY: all clean watch

MAIN  = paper
TEX   = $(MAIN).tex
PDF   = $(MAIN).pdf
BIB   = ../shared/bibliography/references.bib
DEPS  = $(wildcard figures/*) $(BIB)

all: $(PDF)

$(PDF): $(TEX) $(DEPS)
	latexmk -pdf -interaction=nonstopmode $(TEX)

watch:
	latexmk -pdf -pvc $(TEX)

clean:
	latexmk -C
	rm -f *.bbl *.run.xml *.synctex.gz

wordcount:
	@texcount -inc -brief $(TEX) 2>/dev/null || echo "(install texcount for word counts)"
