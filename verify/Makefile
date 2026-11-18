COQMFFLAGS := -Q . BusyCoq

ALLVFILES := LibTactics.v Helper.v Pigeonhole.v TM.v Compute.v Flip.v Permute.v DirectedCompute.v Subtape.v \
	Cyclers.v TranslatedCyclers.v BackwardsReasoning.v Bouncers.v Individual.v \
	BB52.v Individual52.v FixedBin.v ShiftOverflow.v ShiftOverflowBins.v Skelet15.v Skelet26.v Skelet33.v Skelet34.v Skelet35.v \
	Skelet10.v Skelet17.v Skelet1.v Finned.v Finned1.v Finned2.v Finned3.v Finned4.v Finned5.v Extraction.v \
	BB33.v Individual33.v BB33_494.v

LINE36VFILES := Line36Matching.v Line36Word.v Line36Machine.v Line36Physical.v \
    Line36Tiles.v Line36TileShield.v Line36Reference.v Line36Cover.v Line36Right.v \
    Line36Halo.v Line36Seed.v Line36Safety.v Line36HighDebt.v Line36Splice.v
ALLVFILES += $(LINE36VFILES)

all: check verify skelet1

line36: Makefile.coq
	$(MAKE) -f Makefile.coq $(LINE36VFILES:.v=.vo)

Makefile.coq: Makefile $(ALLVFILES)
	coq_makefile $(COQMFFLAGS) -o Makefile.coq $(ALLVFILES)

check: Makefile.coq
	$(MAKE) -f Makefile.coq

%.vo: %.v Makefile.coq

clean::
	if [ -e Makefile.coq ]; then $(MAKE) -f Makefile.coq cleanall; fi
	$(RM) $(wildcard Makefile.coq Makefile.coq.conf) extraction.ml extraction.mli skelet1.mli skelet1.ml *.cmi *.cmx *.o verify skelet1

verify: extraction.mli extraction.ml main.ml
	ocamlopt.opt -o $@ $^

skelet1: skelet1.mli skelet1.ml skelet1_main.ml
	ocamlopt -o $@ $^

extraction.mli extraction.ml: Extraction.vo
skelet1.mli skelet1.ml: Skelet1.vo

-include Makefile.coq

.PHONY: build clean line36
