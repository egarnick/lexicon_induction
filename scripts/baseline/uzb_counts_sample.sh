#!/bin/sh

# Change final arg for 1/3 cutoff
LOR_DIR='/g/ssli/data/lorelei/Software/Morfessor'
INPUTS=$LOR_DIR'/inputs-uzb_counts/0'

python3 $LOR_DIR/baseline/scripts/uzb_counts.py $INPUTS $INPUTS/config/file_group.0.div $LOR_DIR/baseline/output/counts 1
