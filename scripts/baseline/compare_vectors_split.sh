#!/bin/sh


LDIR='/s1/egarnick/temp'$1
INPUTS='/s1/egarnick/temp'$1'/inputs-comp_vectors_split/'$2
SCRDIR=/homes/egarnick/scripts

python3 $SCRDIR/baseline/compare_vectors.py $INPUTS/resources/uzb-eng_lexicon80.train $INPUTS/resources/emnlp.test.$2.rom $INPUTS/vectors/uzb-80.vectors $INPUTS/vectors/eng-80.vectors $LDIR/output/baseline.$2.trans
