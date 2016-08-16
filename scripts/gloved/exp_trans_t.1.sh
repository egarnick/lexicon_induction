#!/bin/sh

# $1 - input file to expand

MYHOME=/homes/egarnick/
INPUTS='/homes/egarnick/inputs-expand_hyps/'$1

GLOVE=$INPUTS'/resources/glove.6B.zip'
VECFILE='glove.6B.50d.txt'
DIV_FILE='base_hyps-1948.'$1'.div'
CACHE=$INPUTS'/resources/base-top200.expanded'

python3 $MYHOME/scripts/gloved/expand_trans.py $GLOVE $VECFILE $INPUTS'/divs/'$DIV_FILE '/homes/egarnick/output/translations/test_exp/' $CACHE
