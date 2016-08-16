This document describes how to use score_trans.py to assess translation
hypotheses as produced by compare_vectors.py.  score_trans.py is written in
Python3.

Data files used:
----------------
/g/ssli/data/lorelei/Software/Morfessor/baseline/data/test/emnlp.test.lex
/g/ssli/data/lorelei/Software/Morfessor/baseline/output/translations/<translation_file>

This is the original test list with Uzbek spelling, romanized transliteration
and English translations.

Software:
---------
/g/ssli/data/lorelei/Software/Morfessor/baseline/scripts/score_trans.py

This reads each Uzbek word in the translations file and finds the position
of the correct translation in the list of translation hypotheses (if such a
correct translation is present).  The results are printed to standard output.

Output:
-------
Lines printed to std output such that the first line indicates the number of
unique Uzbek words in the test word file (emnlp.test.lex), following lines
give each correctly translated Uzbek word with its English translation and the
position of that translation in the list of translation hypotheses.  The final
line indicates the number of correct translations.  Format:

<uzbek_word> <english_trans> <trans_position>

Sample output has been redirected and saved to the file:
/g/ssli/data/lorelei/Software/Morfessor/baseline/results/sample.res

To run:
-------
python3 score_trans.py <test_file> <translation_file>

e.g.
python3 score_trans.py emnlp.test.lex sample.trans > results/sample.res
