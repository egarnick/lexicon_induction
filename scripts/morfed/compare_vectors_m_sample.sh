#!/bin/sh

LOR_DIR='/g/ssli/data/lorelei/Software/Morfessor'
SCRIPT=$LOR_DIR'/morf/scripts/compare_vectors_m_old.py'
LEXICON=$LOR_DIR'/morf/resources/uzb-eng/saved/uzb-eng_lexicon_m80.train'
SEGS=$LOR_DIR"/morf/resources/uzb_text/uzb-seg.all.counts"
MODEL=$LOR_DIR"/morf/resources/models/model-uzb.1m.bin"
TEST_DATA=$LOR_DIR'/morf/data/test/emnlp.test.sample'
VECTORS=$LOR_DIR'/morf/resources/vectors'
TRANS=$LOR_DIR'/morf/output/translations'

python3 $SCRIPT $LEXICON $SEGS $MODEL $TEST_DATA $VECTORS/uzb-80_m.vectors $VECTORS/eng-80.vectors $TRANS/sample.trans
