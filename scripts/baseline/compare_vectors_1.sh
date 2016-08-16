#!/bin/sh


LDIR='/s1/egarnick/temp'$1
INPUTS='/s1/egarnick/temp'$1'/inputs-comp_vectors/'$2
SCRDIR=/homes/egarnick/scripts

python3 $SCRDIR/baseline/compare_vectors.2.py $INPUTS/resources/uzb-eng_lexicon.2.80.train $INPUTS/resources/uzb.dev.subset.oov.rom $INPUTS/vectors/uzb-80.2.vectors $INPUTS/vectors/eng-80.2.vectors $LDIR/output/dev.oov.2.trans
