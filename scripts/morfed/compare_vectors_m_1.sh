#!/bin/sh

LDIR='/s1/egarnick/temp'$1
INPUTS='/s1/egarnick/temp'$1'/inputs-comp_vectors_m/'$2
SCRDIR=/homes/egarnick/scripts

python3 $SCRDIR/morfed/compare_vectors_m.2.py $INPUTS/resources/uzb-eng_lexicon_m.2.80.train $INPUTS/resources/uzb-seg.all.counts $INPUTS/resources/model-uzb.1m.1.bin $INPUTS/resources/uzb.dev.subset.oov.rom $INPUTS/vectors/uzb-80_m.2.vectors $INPUTS/vectors/eng-80_m.2.vectors $LDIR/output/dev.oov_m.2.trans
