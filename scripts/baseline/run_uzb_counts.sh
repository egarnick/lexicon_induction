#!/bin/sh

# $1 is unique key for directory naming (generally a recently unused letter of the alphabet)

LOR_DIR="/g/ssli/data/lorelei/Software/Morfessor"
SCRIPTS=$LOR_DIR"/baseline/scripts"
UNIQUE_KEY=`date +%j`$1

python3 $SCRIPTS"/create_run_n.py" $LOR_DIR"/migrate/run101scripts.sh" 101 $UNIQUE_KEY
bash $LOR_DIR"/migrate/run_migrate.sh" 101
