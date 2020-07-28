
SCRDIR=$(HOME)/.config/scbi
VER=$(shell git describe)

all:
	mkdir -p $(SCRDIR) $(SCRDIR)/patches
	rm -f $(SCRDIR)/*~ scripts.d/*~ $(SCRDIR)/patches/*
	cp -r scripts.d/* $(SCRDIR)
	cp scripts.d/.env* $(SCRDIR)
	cp scripts.d/.plan* $(SCRDIR)
	echo "SALOME plugins : ${VER}" > $(SCRDIR)/.scbi_salome_version.txt

doc: force
	make -C doc
