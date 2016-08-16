#!/bin/sh

SCRIPT='/homes/egarnick/scripts/baseline/uzb_counts.py'
LDIR='/s1/egarnick/temp'$1
INPUTS='/s1/egarnick/temp'$1'/inputs-uzb_counts/'$2

# Change final arg for 1/3 cutoff
python3 $SCRIPT $INPUTS $INPUTS/config/file_group.$2.div $LDIR/output 0
