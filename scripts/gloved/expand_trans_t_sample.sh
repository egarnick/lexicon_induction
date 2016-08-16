#!/bin/sh

# Run expand_trans.py to produce expanded translation hypotheses for test items
# $1 - input file to expand

CUR_DIR=/g/ssli/data/lorelei/Software/Morfessor
SCRIPT=$CUR_DIR'/glove/scripts/expand_trans.py'
GLOVE=$CUR_DIR'/glove/data/glove.6B.zip'
VECFILE='glove.6B.50d.txt'
DIV_FILE=$CUR_DIR'/baseline/output/translations/sample.trans'
CACHE=$CUR_DIR'/glove/resources/base-top200.expanded'

python3 $SCRIPT $GLOVE $VECFILE $DIV_FILE $CUR_DIR'/glove/output' $CACHE
