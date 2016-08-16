#!/bin/sh

# args
NUMJOBS="$1"

# environment
LDIR='/n/bar/s1/egarnick'
MYHOME='/homes/egarnick'

# Make sure s1 is available
space_req s1

# Establish directory structure 
rm -rf $LDIR/temp
mkdir $LDIR/temp
mkdir $LDIR/temp/output/

# Copy data to local directory
cp -Lr $MYHOME/inputs-uzb_vectors $LDIR/temp

# Run it
migrate -file $MYHOME'/scripts/migrate/run_'$NUMJOBS'shells.sh' -no-desktops -J $NUMJOBS -verbose

# Copy results back home
cp -r $LDIR/temp/output/* $MYHOME/output 
