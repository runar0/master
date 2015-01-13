
LATEX=pdflatex
VIEWER=xdg-open

MAIN=thesis.tex
PDF=thesis.pdf

build:
	$(LATEX) $(MAIN)
	$(LATEX) $(MAIN)

show: build
	$(VIEWER) $(PDF)

clean:
	rm -f *log *aux *lof *lot *toc

purge: clean
	rm -f $(PDF)
