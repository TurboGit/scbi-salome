
SCRDIR=$(HOME)/.config/scbi

all:
	mkdir -p $(SCRDIR)
	rm -f $(SCRDIR)/*~ scripts.d/*~
	cp scripts.d/* $(SCRDIR)
	cp scripts.d/.env* $(SCRDIR)
	cp scripts.d/.plan* $(SCRDIR)
