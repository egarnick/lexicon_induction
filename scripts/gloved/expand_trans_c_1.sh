#!/bin/sh

# Run expand_trans.py to cache top translation hypotheses

# $1 - input file to expand
# $2 - ['yes'|'y']

MYHOME=/homes/egarnick/
LDIR='/s1/egarnick/temp'$1
INPUTS='/s1/egarnick/temp'$1'/inputs-cache_exp_m/'$2

GLOVE=$INPUTS'/resources/glove.6B.zip'
VECFILE='glove.6B.50d.txt'
DIV_FILE='tst_m-1000.'$2'.div'

python3 $MYHOME/scripts/gloved/expand_trans.py $GLOVE $VECFILE $INPUTS'/divs/'$DIV_FILE $LDIR'/output' y
