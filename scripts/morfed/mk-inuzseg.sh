#!/bin/sh

INPUTS=/homes/egarnick/inputs-uzb_segs

for i in `seq 0 100`;
do
    mkdir $INPUTS/$i
    mkdir $INPUTS/$i/config
    mkdir $INPUTS/$i/data
    mkdir $INPUTS/$i/model

    ln -s /homes/egarnick/config/file_group.$i.div $INPUTS/$i/config/
    ln -s /homes/egarnick/data/BOLT/uzb/monolingual_text/* $INPUTS/$i/data/
    ln -s /homes/egarnick/models/model-uzb.1m.1.bin $INPUTS/$i/model/
done
