This document describes how to process the BOLT Uzbek-English seed lexicon for
use in the lexicon induction pipeline.  All software is either shell scripts
or written in Python3.

Data files used:
----------------
/g/ssli/data/lorelei/Software/Morfessor/baseline/data/lexicon/lexicon.v6.llf.xml

This is an xml-formatted file with Uzbek terms and corresponding English
translations.  Some Uzbek terms appear more than once in the file, and many
Uzbek terms have more than one associated English translation.  The formatting
of the English translations is highly inconsistent, but the lexicon processing
script handles most (if not all) formats.

Software:
---------
/g/ssli/data/lorelei/Software/Morfessor/baseline/scripts/process_lexicon.py
/g/ssli/data/lorelei/Software/Morfessor/baseline/scripts/process_lexicon.sh

process_lexicon.py reads in the lexicon file, creates data structures to
represent translations, and saves the data structures as json files.  The
lexicon can be split for training and testing purposes with the final command
line argument - an integer indicating the percentage to use for the training
split (e.g. 80 for 80% training and 20% testing).  If 100 or 0 are used, only
a train file or test file will be created, respectively.

Output:
-------
Python dictionaries saved as json files:

/g/ssli/data/lorelei/Software/Morfessor/baseline/resources/uzb-eng/uzb-eng_lexicon<split>.train
/g/ssli/data/lorelei/Software/Morfessor/baseline/resources/uzb-eng/uzb-eng_lexicon<100 - split>.test

Example output file names for 80/20 split:
    uzb-eng_lexicon80.train
    uzb-eng_lexicon20.test

To run:
-------
./process_lexicon.sh <train_split>
