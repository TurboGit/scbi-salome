
NAM = scbi-salome
TEX = $(NAM).tex
PDF = $(NAM).pdf

all: $(PDF)

force:

version: force
	echo '\\providecommand{\\version}{'$(VER)'}' > version.tex

# %.pdf: %.tex $(DIF) $(BIB)

$(PDF): $(TEX) $(DIF) $(BIB) version
	-latex $(TEX)
	-bibtex $(NAM)
	-makeindex $(NAM)
	-latex $(TEX)
	pdflatex $(TEX)

clean:
	rm -f *.bbl *.blg *.log *.out *.toc *.aux *.idx $(PDF)
