
LATEX=pdflatex
BIBTEX=bibtex
VIEWER=xdg-open

MAIN=thesis
PDF=thesis.pdf
FPDF=thesis-final.pdf

build:
	$(LATEX) $(MAIN).tex
	$(BIBTEX) $(MAIN).aux
	makeglossaries $(MAIN)
	$(LATEX) $(MAIN).tex
	$(LATEX) $(MAIN).tex
	qpdf --linearize $(PDF) $(FPDF)

show: build
	$(VIEWER) $(PDF)

clean:
	rm -f *log *aux *lof *lot *toc

purge: clean
	rm -f $(PDF) $(FPDF)
