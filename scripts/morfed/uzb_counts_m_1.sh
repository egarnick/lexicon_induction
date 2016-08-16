#!/bin/sh

LDIR='/s1/egarnick/temp'$1
INPUTS='/s1/egarnick/temp'$1'/inputs-uzb_counts_m/'$2

# Change final arg for 1/3 cutoff
python3 /homes/egarnick/scripts/morfed/uzb_counts_m.2.py $INPUTS $INPUTS/config/file_group.$2.div $INPUTS/resources/uzb-seg.all.counts $INPUTS/resources/model-uzb.1m.1.bin $LDIR/output 0
