#!/bin/sh

LOR=/g/ssli/data/lorelei/Software/Morfessor
INPUTS=$LOR'/baseline/inputs-uzb_counts'
BOLTUZB=$LOR'/data'

for i in `seq 0 100`;
do
    mkdir $INPUTS/$i
    mkdir $INPUTS/$i/config
    mkdir $INPUTS/$i/data

    ln -s $LOR/baseline/config/file_group.$i.div $INPUTS/$i/config/file_group.$i.div

    ln -s $BOLTUZB/DF_ALL_UZB.ltf.zip $INPUTS/$i/data/DF_ALL_UZB.ltf.zip
    ln -s $BOLTUZB/NW_ALL_UZB.ltf.zip $INPUTS/$i/data/NW_ALL_UZB.ltf.zip
    ln -s $BOLTUZB/RF_WKP_UZB.ltf.zip $INPUTS/$i/data/RF_WKP_UZB.ltf.zip
done
