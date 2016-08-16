#!/bin/sh

LDIR='/s0/egarnick/temp'$1
INPUTS='/s0/egarnick/temp'$1'/inputs-morf_model/'$2

morfessor-train -s $LDIR/output/model-uzb.1m.1.bin $INPUTS/uzb_lines.1m.1.clean
