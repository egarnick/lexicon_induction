#!/bin/sh

MYHOME=/homes/egarnick
INPUTS=$MYHOME'/inputs-uzb_counts_m'
BOLTUZB=$MYHOME'/data/BOLT/uzb/monolingual_text'

for i in `seq 0 100`;
do
    mkdir $INPUTS/$i
    mkdir $INPUTS/$i/config
    mkdir $INPUTS/$i/data
    mkdir $INPUTS/$i/resources

    ln -s /homes/egarnick/config/file_group.$i.div $INPUTS/$i/config/file_group.$i.div

    ln -s $BOLTUZB/DF_ALL_UZB.ltf.zip $INPUTS/$i/data/DF_ALL_UZB.ltf.zip
    ln -s $BOLTUZB/NW_ALL_UZB.ltf.zip $INPUTS/$i/data/NW_ALL_UZB.ltf.zip
    ln -s $BOLTUZB/RF_WKP_UZB.ltf.zip $INPUTS/$i/data/RF_WKP_UZB.ltf.zip

    ln -s $MYHOME/resources/uzb_text/uzb-seg.all.counts $INPUTS/$i/resources/uzb-seg.all.counts
    ln -s $MYHOME/models/model-uzb.1m.bin $INPUTS/$i/resources/model-uzb.1m.bin
done
