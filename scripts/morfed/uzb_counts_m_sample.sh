#!/bin/sh

LOR_DIR="/g/ssli/data/lorelei/Software/Morfessor"
SCRIPT=$LOR_DIR"/morf/scripts/uzb_counts_m.py"
DIV=$LOR_DIR"/inputs-uzb_counts/0/config/file_group.0.div"
SEGS=$LOR_DIR"/morf/resources/uzb_text/uzb-seg.all.counts"
MODEL=$LOR_DIR"/morf/resources/models/model-uzb.1m.bin"

# Change final arg for 1/3 cutoff
python3 $SCRIPT $LOR_DIR $DIV $SEGS $MODEL $LOR_DIR/morf/output/counts 1
