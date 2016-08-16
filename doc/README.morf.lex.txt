This document describes how to process the BOLT Uzbek-English seed lexicon for
use in the lexicon induction pipeline with Morfessor segmentation.  All
software is either shell scripts or written in Python3.

Data files used:
----------------
/g/ssli/data/lorelei/Software/Morfessor/morf/data/lexicon/lexicon.v6.llf.xml

This is an xml-formatted file with Uzbek terms and corresponding English
translations.  Some Uzbek terms appear more than once in the file, and many
Uzbek terms have more than one associated English translation.  The formatting
of the English translations is highly inconsistent, but the lexicon processing
script handles most (if not all) formats.

/g/ssli/data/lorelei/Software/Morfessor/morf/resources/uzb_text/uzb-seg.all.counts

This file contains 77,105 segments from the Morfessor model with counts of
occurrences alone and combined with other segments for each segment.

/g/ssli/data/lorelei/Software/Morfessor/morf/resources/models/model-uzb.1m.bin

This is the Morfessor model trained on 1 million lines of Uzbek text.  It is
used to segment new text.

Software:
---------
/g/ssli/data/lorelei/Software/Morfessor/morf/scripts/process_lexicon_m.py
/g/ssli/data/lorelei/Software/Morfessor/morf/scripts/process_lexicon_m.sh

process_lexicon_m.py reads in the lexicon file, segments each token, selects
one segment as a word's root, creates data structures to represent
translations from Uzbek roots to English terms, and saves the data structures
as json files.  The lexicon can be split for training and testing purposes
with the final command line argument - an integer indicating the percentage to
use for the training split (e.g. 80 for 80% training and 20% testing).  If 100
or 0 are used, only a train file or test file will be created, respectively.

Output:
-------
Python dictionaries saved as json files:

/g/ssli/data/lorelei/Software/Morfessor/morf/resources/uzb-eng/uzb-eng_lexicon_m<split>.train
/g/ssli/data/lorelei/Software/Morfessor/morf/resources/uzb-eng/uzb-eng_lexicon_m<100 - split>.test

Example output file names for 80/20 split:
    uzb-eng_lexicon_m80.train
    uzb-eng_lexicon_m20.test

To run:
-------
./process_lexicon_m.sh <train_split>
