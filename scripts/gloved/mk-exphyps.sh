#!/bin/sh

MYHOME=/homes/egarnick
INPUTS=$MYHOME'/inputs-expand_hyps'
GLOVE=$MYHOME'/data/GloVe/glove.6B.zip'
CACHE=$MYHOME'/expanded/tst-top1k.expanded'

for i in `seq 0 99`;
do
    mkdir $INPUTS/$i
    mkdir $INPUTS/$i/divs
    mkdir $INPUTS/$i/resources

    ln -s $MYHOME/output/translations/divs/tst/tst_trans-136.$i.div $INPUTS/$i/divs/

    ln -s $CACHE $INPUTS/$i/resources/
    ln -s $GLOVE $INPUTS/$i/resources/
done
