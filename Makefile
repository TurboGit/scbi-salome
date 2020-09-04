
SCRDIR=$(HOME)/.config/scbi
VER=$(shell git describe)

all: clean.install
	mkdir -p $(SCRDIR) $(SCRDIR)/patches
	rm -f $(SCRDIR)/*~ scripts.d/*~ $(SCRDIR)/patches/*
	cp -r scripts.d/* $(SCRDIR)
	cp scripts.d/.env* $(SCRDIR)
	cp scripts.d/.plan* $(SCRDIR)
	echo "SALOME plugins : ${VER}" > $(SCRDIR)/.scbi_salome_version.txt

	cd scripts.d; find . -type f > $(SCRDIR)/.salome.plugins

clean.install:
	if [ -f $(SCRDIR)/.salome.plugins ]; then          \
		cat $(SCRDIR)/.salome.plugins |            \
			while read file; do                \
				rm -f $(SCRDIR)/$$file;    \
			done;                              \
		rm -f $(SCRDIR)/.salome.plugins;           \
		rm -f $(SCRDIR)/.scbi_salome_version.txt;  \
	fi

doc: force
	make -C doc
