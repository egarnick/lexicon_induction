#!/bin/sh

# environment
LDIR='/s1/egarnick/temp'$1
MYHOME='/homes/egarnick'

# Copy results back home
cp -r $LDIR/output/* $MYHOME/output/$2

# Clean up scratch disk
#rm -rf $LDIR/temp