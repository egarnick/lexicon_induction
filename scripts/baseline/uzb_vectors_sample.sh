#!/bin/sh

LOR_DIR='/g/ssli/data/lorelei/Software/Morfessor'
LEXICON=$LOR_DIR'/baseline/resources/uzb-eng/uzb-eng_lexicon80.train'
COUNTS=$LOR_DIR'/baseline/resources/counts'
OUTPUT_VECS=$LOR_DIR'/baseline/output/vectors'

python3 $LOR_DIR/baseline/scripts/lang_vectors.py f $LEXICON $COUNTS $OUTPUT_VECS/uzb-80.0.vectors
