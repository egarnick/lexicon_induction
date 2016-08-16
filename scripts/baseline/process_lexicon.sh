#!/bin/sh

# $1 is percent of lexicon to use for training

CUR_HOME="/g/ssli/data/lorelei/Software/Morfessor"
SCRIPTS=$CUR_HOME"/baseline/scripts"
LEXICON=$CUR_HOME"/baseline/data/lexicon/lexicon.v6.llf.xml"

python3 $SCRIPTS"/process_lexicon.py" $LEXICON $CUR_HOME"/baseline/resources/uzb-eng/uzb-eng_lexicon" $1
