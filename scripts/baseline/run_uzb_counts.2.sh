#!/bin/sh

HOME_DIR='/homes/egarnick'
INPUTS_DIR=$HOME_DIR'/inputs-uzb_counts'
DATA_DIVS=$HOME_DIR'/config'
UZB_DATA=$HOME_DIR'/data/BOLT/uzb/monolingual_text'

# Establish inputs directory
rm -rf $INPUTS_DIR
mkdir $INPUTS_DIR
for i in `seq 0 100`;
do
    mkdir $INPUTS_DIR'/'$i
    mkdir $INPUTS_DIR'/'$i'/config'
    mkdir $INPUTS_DIR'/'$i'/data'
    ln -s $DATA_DIVS'/file_group.'$i'.div' $INPUTS_DIR'/'$i'/config/'
    ln -s $UZB_DATA/* $INPUTS_DIR'/'$i'/data/'
done

# Create run script

