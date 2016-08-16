#!/bin/sh

NUM_SPLITS=$[$1 - 1]
GIGA_DIR='/corpora/LDC/LDC11T07/data'
LOR_HOME='/home2/egarnick/courses/LOR'

for i in `seq 0 $NUM_SPLITS`;
do
  mkdir $LOR_HOME'/delegates/'$i
  for corpdir in `ls $GIGA_DIR`;
    do
      DIR_LEN=`ls $GIGA_DIR/$corpdir/*.gz | wc -l`
      echo $corpdir
      echo $DIR_LEN
      echo $[$DIR_LEN % $1]
      for corpfile in `ls $GIGA_DIR/$corpdir/*.gz`;
      do

        echo $corpfile
      done
    done
done
echo 'Created ' $[$NUM_SPLITS + 1] ' directories in ' $LOR_HOME'/delegates'
