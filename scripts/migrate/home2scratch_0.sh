#!/bin/sh

# Job number, input directory
JOBNUM=$1
DIRKEY=$2
INPUTDIR=$3

# environment
INPUTS='/s0/egarnick/temp'$DIRKEY'/'$INPUTDIR
MYHOME='/homes/egarnick'

# Copy data to local directory
if [ ! -d "$INPUTS" ]; then
    mkdir $INPUTS
fi

cp -Lr $MYHOME'/'$INPUTDIR'/'$1 $INPUTS