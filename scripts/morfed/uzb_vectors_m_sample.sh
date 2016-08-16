#!/bin/sh

LOR_DIR='/g/ssli/data/lorelei/Software/Morfessor'
SCRIPT=$LOR_DIR"/morf/scripts/lang_vectors_m.py"
LEXICON=$LOR_DIR'/morf/resources/uzb-eng/uzb-eng_lexicon_m80.train'
COUNTS=$LOR_DIR'/morf/resources/counts'
OUTPUT_VECS=$LOR_DIR'/morf/output/vectors'

python3 $SCRIPT f $LEXICON $COUNTS $OUTPUT_VECS/uzb-80_m.0.vectors
