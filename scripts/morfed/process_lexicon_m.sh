#!/bin/sh

CUR_HOME="/g/ssli/data/lorelei/Software/Morfessor"
SCRIPT=$CUR_HOME"/morf/scripts/process_lexicon_m.py"
BOLT_LEX=$CUR_HOME"/morf/data/lexicon/lexicon.v6.llf.xml"
SEGS=$CUR_HOME"/morf/resources/uzb_text/uzb-seg.all.counts"
MODEL=$CUR_HOME"/morf/resources/models/model-uzb.1m.bin"
OUTPUT=$CUR_HOME"/morf/resources/uzb-eng/uzb-eng_lexicon_m"

TR_SPLIT=$1

python3 $SCRIPT $BOLT_LEX $SEGS $MODEL $OUTPUT $TR_SPLIT
