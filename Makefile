
SCRDIR=$(HOME)/.config/scbi

all:
	mkdir -p $(SCRDIR) $(SCRDIR)/patches
	rm -f $(SCRDIR)/*~ scripts.d/*~ $(SCRDIR)/patches/*
	cp scripts.d/* $(SCRDIR)
	cp scripts.d/.env* $(SCRDIR)
	cp scripts.d/.plan* $(SCRDIR)

	if [ -d "patches" ]; then         \
		cp -r patches/* $(SCRDIR)/patches;  \
	fi
