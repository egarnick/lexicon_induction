#!/bin/sh

for i in `seq 0 100`;
do
    python3 scripts/resource_processing/json2txt.py output/counts/uzb.$i.counts output/counts_txt/uzb.$i.counts
    rm -f output/counts/uzb.$i.counts
done
