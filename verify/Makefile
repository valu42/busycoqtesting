COQMFFLAGS := -Q . BusyCoq

ALLVFILES := LibTactics.v Helper.v Pigeonhole.v TM.v Compute.v Flip.v Permute.v DirectedCompute.v Subtape.v \
	Cyclers.v TranslatedCyclers.v BackwardsReasoning.v Bouncers.v Individual.v \
	BB52.v Individual52.v FixedBin.v ShiftOverflow.v ShiftOverflowBins.v Skelet15.v Skelet26.v Skelet33.v Skelet34.v Skelet35.v \
	Skelet10.v Skelet17.v Skelet1.v Finned.v Finned1.v Finned2.v Finned3.v Finned4.v Finned5.v Extraction.v \
	BB33.v Individual33.v BB33_494.v

LINE36_BASE := Line36Matching.v Line36Word.v Line36Machine.v Line36Physical.v \
    Line36Tiles.v Line36TileShield.v Line36Reference.v Line36Cover.v Line36Right.v \
    Line36Halo.v Line36Seed.v Line36Safety.v Line36HighDebt.v Line36Splice.v
ALLVFILES += $(LINE36_BASE)

# The large reflective check is rebuilt only on an explicit line36 target.
LINE36VFILES := $(sort $(wildcard Line36*.v) Line36CapData.v)
LINE36_PROJECT := $(sort $(ALLVFILES) $(LINE36VFILES))

all: check verify skelet1

line36: Makefile.line36.coq
	$(MAKE) -f Makefile.line36.coq $(LINE36VFILES:.v=.vo)

Makefile.line36.coq: Makefile $(LINE36_PROJECT)
	coq_makefile $(COQMFFLAGS) -o $@ $(LINE36_PROJECT)

.line36-cap-generator: ../research/bb2x5/line36_right_cap.cpp
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -O2 -std=c++17 -o $@ $<

Line36CapData.v: .line36-cap-generator ../research/bb2x5/BB2x5_Rocq_holdouts_37.txt
	cd ../research/bb2x5 && "$(abspath $<)" --rocq-data "$(abspath $@).tmp"
	mv $@.tmp $@

Makefile.coq: Makefile $(ALLVFILES)
	coq_makefile $(COQMFFLAGS) -o Makefile.coq $(ALLVFILES)

check: Makefile.coq
	$(MAKE) -f Makefile.coq

%.vo: %.v Makefile.coq

clean::
	if [ -e Makefile.line36.coq ]; then $(MAKE) -f Makefile.line36.coq cleanall; fi
	$(RM) Makefile.line36.coq Makefile.line36.coq.conf Line36CapData.v Line36CapData.v.tmp .line36-cap-generator
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
