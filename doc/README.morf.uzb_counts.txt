This document describes how to process a sample of the BOLT Uzbek monolingual
text data to collect word co-occurrence counts for roots of Morfessor-segmented
words.  All software is either shell scripts or written in Python3.

Data files used:
----------------
Corpus data:
/g/ssli/data/lorelei/Software/Morfessor/data/DF_ALL_UZB.ltf.zip
/g/ssli/data/lorelei/Software/Morfessor/data/NW_ALL_UZB.ltf.zip
/g/ssli/data/lorelei/Software/Morfessor/data/RF_WKP_UZB.ltf.zip

Sample files processed:
DF_ALL_UZB.ltf.zip/ltf/DF_ZIY_UZB_019767_20140900.ltf.xml
NW_ALL_UZB.ltf.zip/ltf/NW_UZA_UZB_189753_20140805.ltf.xml
RF_WKP_UZB.ltf.zip/ltf/RF_WKP_UZB_110114_20140900.ltf.xml

These are xml-formatted files with Uzbek sentences.  Each sentence is given
both in its raw form and as a list of tokens.

Document list files (101 divisions):
/g/ssli/data/lorelei/Software/Morfessor/morf/config/file_group.0.div
...
/g/ssli/data/lorelei/Software/Morfessor/morf/config/file_group.100.div

Each file is a list of document names in the BOLT Uzbek monolingual data to be
processed in a specific batch.

/g/ssli/data/lorelei/Software/Morfessor/morf/resources/uzb_text/uzb-seg.all.counts

This file contains 77,105 segments from the Morfessor model with counts of
occurrences alone and combined with other segments for each segment.

/g/ssli/data/lorelei/Software/Morfessor/morf/resources/models/model-uzb.1m.bin

This is the Morfessor model trained on 1 million lines of Uzbek text.  It is
used to segment new text.

Sample data:
------------
The Uzbek xml files processed in this example have been extracted and saved
for reference at:

/g/ssli/data/lorelei/Software/Morfessor/data/sample/DF_ZIY_UZB_019767_20140900.ltf.xml
/g/ssli/data/lorelei/Software/Morfessor/data/sample/NW_UZA_UZB_189753_20140805.ltf.xml
/g/ssli/data/lorelei/Software/Morfessor/data/sample/RF_WKP_UZB_110114_20140900.ltf.xml

Software:
---------
/g/ssli/data/lorelei/Software/Morfessor/baseline/scripts/uzb_counts_m.py
/g/ssli/data/lorelei/Software/Morfessor/baseline/scripts/uzb_counts_m_sample.sh

uzb_counts_m.py reads in a file specifying a subset of Uzbek documents to
extract from the zip files and process.  The subset is read in, segmented
according to the Morfessor model and counts for heuristically-proposed roots
and their co-occurring context roots are recorded.  The output is saved as a
text file with the counts for the given Uzbek document subset.

Output:
-------
Text files formatted:

uzb_word<TAB><count><TAB><ctxt_word1>,<ctxt_count1><TAB>...<ctxt_wordn>,<ctxt_countn>

Output files saved to:

/g/ssli/data/lorelei/Software/Morfessor/morf/output/counts/uzb.<s>.counts

for split index s of Uzbek data.

Example output file name for first split:
    uzb.0.counts

To run:
-------
./uzb_counts_m_sample.sh

This produces output for the first 3 documents in split 0 (the first portion
of Uzbek monolingual data).
