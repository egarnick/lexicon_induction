#!/bin/sh

MYHOME=/homes/egarnick
INPUTS=$MYHOME'/inputs-cache_exp_m'
GLOVE=$MYHOME'/data/GloVe/glove.6B.zip'

for i in `seq 0 99`;
do
    mkdir $INPUTS/$i
    mkdir $INPUTS/$i/divs
    mkdir $INPUTS/$i/resources

    ln -s $MYHOME/top-trans/tst_oov_m/tst_m-1000.$i.div $INPUTS/$i/divs/

    ln -s $GLOVE $INPUTS/$i/resources/
done
