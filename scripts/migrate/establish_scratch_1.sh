#!/bin/sh

# unique temp in scratch
LDIR='/s1/egarnick/temp'$1

# Make sure s1 is available
space_req s1

# Establish directory structure
if [ ! -d "$LDIR" ]; then
    rm -rf /s1/egarnick/temp*
    mkdir $LDIR
    mkdir $LDIR/output/
fi
