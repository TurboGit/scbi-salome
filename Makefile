
SCRDIR=$(HOME)/.config/scbi
VER=$(shell git describe)

all: clean.install core
	mkdir -p $(SCRDIR) $(SCRDIR)/patches
	rm -f $(SCRDIR)/*~ scripts.d/*~
	rm -f $(SCRDIR)/.*~ scripts.d/.*~
	cp -r scripts.d/* $(SCRDIR)
	cp scripts.d/.env* $(SCRDIR)
	cp scripts.d/.plan* $(SCRDIR)
	cp scripts.d/.pkgs* $(SCRDIR)
	echo "SALOME plugins : ${VER}" > $(SCRDIR)/.scbi_salome_version.txt

	cd scripts.d; find . -type f > $(SCRDIR)/.salome.plugins

clean.install:
	if [ -f $(SCRDIR)/.salome.plugins ]; then          \
		cat $(SCRDIR)/.salome.plugins |            \
			while read file; do                \
				echo $(SCRDIR)/$$file;     \
			done | xargs -n 25 rm -f ;         \
		rm -f $(SCRDIR)/.salome.plugins;           \
		rm -f $(SCRDIR)/.scbi_salome_version.txt;  \
	fi

lint:
	scbi lint --error scripts.d/s-*
	echo No problem detected

doc: force core.doc
	make VER=$(VER) -C doc

core:
	make -C scbi

core.doc:
	-make -C scbi doc

force:
