#!/bin/sh

LOR_DIR='/g/ssli/data/lorelei/Software/Morfessor'
SCRIPT=$LOR_DIR'/baseline/scripts/compare_vectors.py'
LEXICON=$LOR_DIR'/baseline/resources/uzb-eng/saved/uzb-eng_lexicon80.train'
TEST_DATA=$LOR_DIR'/baseline/data/test/emnlp.test.sample'
VECTORS=$LOR_DIR'/baseline/resources/vectors'
TRANS=$LOR_DIR'/baseline/output/translations'

python3 $SCRIPT $LEXICON $TEST_DATA $VECTORS/uzb-80.vectors $VECTORS/eng-80.vectors $TRANS/sample.trans
