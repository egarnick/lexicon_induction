#!/bin/sh

# Change final arg for 1/3 cutoff
LDIR='/s1/egarnick/temp'$1
INPUTS='/s1/egarnick/temp'$1'/inputs-uzb_counts/'$2

python3 /homes/egarnick/scripts/baseline/uzb_counts.py $INPUTS $INPUTS/config/file_group.$2.div $LDIR/output 0
