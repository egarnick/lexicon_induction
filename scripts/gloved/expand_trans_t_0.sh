#!/bin/sh

# Run expand_trans.py to cache top translation hypotheses

# $1 - input file to expand

MYHOME=/homes/egarnick/
LDIR='/s0/egarnick/temp'$1
INPUTS='/s0/egarnick/temp'$1'/inputs-expand_hyps/'$2

GLOVE=$INPUTS'/resources/glove.6B.zip'
VECFILE='glove.6B.50d.txt'
DIV_FILE='baseline.2-3137.'$2'.div'
CACHE=$INPUTS'/resources/baseline-top1000.2.expanded'

python3 $MYHOME/scripts/gloved/expand_trans.py $GLOVE $VECFILE $INPUTS'/divs/'$DIV_FILE $LDIR'/output' $CACHE
