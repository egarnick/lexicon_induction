#!/bin/sh

LDIR='/s1/egarnick/temp'$1
INPUTS='/s1/egarnick/temp'$1'/inputs-comb_seg_counts/'$2

python3 /homes/egarnick/scripts/morfed/combine_seg_counts.py $INPUTS'/segcounts' $LDIR'/output/uzb-seg.all.counts'
