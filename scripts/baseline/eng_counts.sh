#!/bin/sh

MYHOME=/home2/egarnick/courses/LOR

NUM_FILES='$1'
OFFSET='$2'

python3 $MYHOME/scripts/baseline/eng_counts.1.py $NUM_FILES $OFFSET /corpora/LDC/LDC11T07/data/ $MYHOME/resources/counts/eng_ll.$NUM_FILES.$OFFSET.counts
