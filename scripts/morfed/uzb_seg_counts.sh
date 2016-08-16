#!/bin/sh

LDIR='/s1/egarnick/temp'$1
INPUTS='/s1/egarnick/temp'$1'/inputs-uzb_segs/'$2

python3 /homes/egarnick/scripts/morfed/uzb_seg_counts.py $INPUTS/data $INPUTS/config/file_group.$2.div $INPUTS/model/model-uzb.1m.1.bin $LDIR/output 0
