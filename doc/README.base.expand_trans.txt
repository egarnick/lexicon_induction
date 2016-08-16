This document describes how to create expanded translation hypotheses for the
baseline translations using GloVe word vectors.  All software is either shell
scripts or written in Python3.

Note:  This sample takes several minutes.

Data files used:
----------------
Glove word vectors zipfile:
/g/ssli/data/lorelei/Software/Morfessor/glove/data/glove.6B.zip

Sample translations:
/g/ssli/data/lorelei/Software/Morfessor/baseline/output/translations/sample.trans

Cached expansions for most common 200 English translations:
/g/ssli/data/lorelei/Software/Morfessor/glove/resources/base-top200.expanded

Software:
---------
/g/ssli/data/lorelei/Software/Morfessor/glove/scripts/expand_trans.py
/g/ssli/data/lorelei/Software/Morfessor/glove/scripts/expand_trans_t_sample.sh

expand_trans.py finds the GloVe vector for each translation hypothesis and
adds the English words from the 5 most closely related GloVe vectors to the
translation hypotheses.

expand_trans_t_sample.sh run the script to created expansions for testing.
This is in contrast to the possibility to run expand_trans.py to save a cache
of translation expansions for later use.

Output:
-------
The format is the same as for the translation files, only with longer lists of
translation hypotheses.  Text files have one Uzbek word and its English
translation hypotheses on each line.  The Uzbek word is separated from the
translations with a tab '\t', translations are separated from the score by a
comma ',' and translation/score pairs are separated by semicolon ';':

uzb_word<TAB><translation_1>,<trans_sim_score_1>;...<translation_n>,<trans_sim_score_n>

Output files saved to:

/g/ssli/data/lorelei/Software/Morfessor/glove/output/<file_name>.expanded

In this case the sample input file is:
    sample.trans
and the output is:
    sample.trans.expanded

To run:
-------
./expand_trans_t_sample.sh
