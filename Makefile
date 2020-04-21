
SCRDIR=$(HOME)/.config/scbi

all:
	mkdir -p $(SCRDIR) $(SCRDIR)/patches
	rm -f $(SCRDIR)/*~ scripts.d/*~ $(SCRDIR)/patches/*
	cp -r scripts.d/* $(SCRDIR)
	cp scripts.d/.env* $(SCRDIR)
	cp scripts.d/.plan* $(SCRDIR)

doc: force
	make -C doc
