#!/bin/sh

LDIR='/s1/egarnick/temp'$1
INPUTS='/s1/egarnick/temp'$1'/inputs-uzb_vectors/'$2

python3 /homes/egarnick/scripts/baseline/lang_vectors.2.py f $INPUTS/resources/uzb-eng_lexicon.2.80.train $INPUTS/counts $LDIR/output/uzb-80.2.vectors
