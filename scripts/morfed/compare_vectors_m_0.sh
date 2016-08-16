#!/bin/sh

LDIR='/s0/egarnick/temp'$1
INPUTS='/s0/egarnick/temp'$1'/inputs-comp_vectors_m/'$2
SCRDIR=/homes/egarnick/scripts

python3 $SCRDIR/morfed/compare_vectors_m.2.py $INPUTS/resources/uzb-eng_lexicon_m.2.80.train $INPUTS/resources/uzb-seg.all.counts $INPUTS/resources/model-uzb.1m.1.bin $INPUTS/resources/lexicon_test.rom $INPUTS/vectors/uzb-80_m.2.vectors $INPUTS/vectors/eng-80_m.2.vectors $LDIR/output/lex_test_m.2.trans
