#!/bin/sh

LOCALDIR='/n/bar/s1/egarnick/'
MYHOME='/n/basie/home/egarnick/'

TRAIN='resources/uzb_lines.500000.clean'
MODEL='models/model-uzb.500000.segm'
TEST=$TRAIN'.final'


mkdir resources
mkdir models
cp $MYHOME$TRAIN $LOCALDIR/resources

morfessor -t $TRAIN -S $MODEL -T $TEST
