This document describes how to use extract_test.py to prepare the test item
list file for use with compare_vectors.py in order to produce translation
hypotheses.  extract_test.py is written in Python3.

Data files used:
----------------
/g/ssli/data/lorelei/Software/Morfessor/baseline/data/test/emnlp.test.lex

This is the original test list with Uzbek spelling, romanized transliteration
and English translations.

Software:
---------
/g/ssli/data/lorelei/Software/Morfessor/baseline/scripts/extract_test.py

This file extracts the romanized Uzbek terms from the fourth column of each
row.  The Uzbek terms are saved to the specified output file with 0-based
row count for each row in the original file where that term appears.

Output:
-------
A text file with each romanized Uzbek word on a separate line with the indexes
of its line in the original test file.  There may be multiple line index
values because Uzbek words are repeated for each English translation, and many
Uzbek words have multiple English translations:

<uzbek_word><TAB>[<line_idx_1,...line_idx_n>]

Output file name is up to the user.  The sample output provided is:
/g/ssli/data/lorelei/Software/Morfessor/baseline/resources/test/emnlp.test.rom

To run:
-------
python3 extract_test.py <test_file> <extracted_file>

e.g.
python3 extract_test.py emnlp.test.lex emnlp.test.rom
