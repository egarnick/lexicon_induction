#!/bin/sh

RESOURCES="/homes/egarnick/resources"
VECTORS="/homes/egarnick/output/vectors"
INPUTS="/homes/egarnick/inputs-comp_vectors_split"

for i in `seq 0 100`;
do
    mkdir $INPUTS/$i
    mkdir $INPUTS/$i/vectors
    mkdir $INPUTS/$i/resources
    ln -s $RESOURCES'/test_data/test_split/emnlp.test.'$i'.rom' $INPUTS'/'$i'/resources/emnlp.test.'$i'.rom'
    ln -s $VECTORS'/uzb-80.vectors' $INPUTS'/'$i'/vectors/uzb-80.vectors'
    ln -s $VECTORS'/eng-80.vectors' $INPUTS'/'$i'/vectors/eng-80.vectors'
    ln -s $RESOURCES'/uzb-eng_pickle/uzb-eng_lexicon80.train' $INPUTS'/'$i'/resources/uzb-eng_lexicon80.train'
done