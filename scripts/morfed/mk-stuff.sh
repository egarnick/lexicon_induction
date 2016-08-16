#!/bin/sh

INPUTS=/homes/egarnick/inputs-uzb_counts_m

for i in `seq 0 100`;
do
    rm $INPUTS/$i/resources/model*
    ln -s /homes/egarnick/models/model-uzb.1m.1.bin $INPUTS/$i/resources/
done
