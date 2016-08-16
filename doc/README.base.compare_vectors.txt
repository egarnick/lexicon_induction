This document describes how to create translation hypotheses for a list of
Uzbek words using Uzbek and English vector files.  All software is either
shell scripts or written in Python3.

This description assumes the test list has already been prepared such that
each test item appears at the start of its own line and any addition text on
a line is tab-separated (but will be ignored).

Note:  The word vectors take several minutes to load (over 380,000 for Uzbek,
over 4 million for English).

Data files used:
----------------
Processed Uzbek-English seed lexicon:
/g/ssli/data/lorelei/Software/Morfessor/baseline/resources/uzb-eng/uzb-eng_lexicon80.train

Uzbek word vectors:
/g/ssli/data/lorelei/Software/Morfessor/baseline/resources/vectors/uzb-80.vectors

English word vectors:
/g/ssli/data/lorelei/Software/Morfessor/baseline/resources/vectors/eng-80.vectors

Test data file:
/g/ssli/data/lorelei/Software/Morfessor/baseline/data/test/emnlp.test.sample

Software:
---------
/g/ssli/data/lorelei/Software/Morfessor/baseline/scripts/compare_vectors.py
/g/ssli/data/lorelei/Software/Morfessor/baseline/scripts/compare_vectors_sample.sh

compare_vectors.py compares Uzbek word vectors for each test item with English
word vectors using cosine similarity in order to find the 50 English terms
most similar to the target Uzbek word.  Translation hypotheses are saved as a
text file with one Uzbek word and its corresponding translations per line

Output:
-------
Text files have one Uzbek word and its English translation hypotheses on each
line.  Word is separated from vector with a tab '\t', translations are
separated from the score by a comma ',' and translation/score pairs are
separated by semicolon ';':

uzb_word<TAB><translation_1>,<trans_sim_score_1>;...<translation_n>,<trans_sim_score_n>

Output files saved to:

/g/ssli/data/lorelei/Software/Morfessor/baseline/output/translations/<file_name>.trans

In this case the sample file is:
    sample.trans

To run:
-------
./compare_vectors_sample.sh
