#!/bin/sh

MYHOME='/n/basie/home/egarnick'

python3 $MYHOME/scripts/text_processing/extract_uzb.py $MYHOME/data/BOLT/uzb/monolingual_text $MYHOME/resources/uzb_lines.500000.txt 0 500000
