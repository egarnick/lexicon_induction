#!/bin/sh

NUMJOBS="$1"

# Run it
migrate -file '/homes/egarnick/scripts/migrate/run'$NUMJOBS'scripts_1.sh' -no-desktops -J $NUMJOBS -verbose
