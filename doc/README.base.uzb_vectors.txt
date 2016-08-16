This document describes how to process a sample of the Uzbek counts data and
produce the corresponding word vectors with log-likelihood scores for context
words.  All software is either shell scripts or written in Python3.

Data files used:
----------------
Processed Uzbek-English seed lexicon:
/g/ssli/data/lorelei/Software/Morfessor/baseline/resources/uzb-eng/uzb-eng_lexicon80.train

Uzbek corpus counts:
/g/ssli/data/lorelei/Software/Morfessor/baseline/resources/counts/uzb.0.counts

Software:
---------
/g/ssli/data/lorelei/Software/Morfessor/baseline/scripts/lang_vectors.py
/g/ssli/data/lorelei/Software/Morfessor/baseline/scripts/uzb_vectors_sample.sh

lang_vectors.py aggregates word and context counts for all counts files in the
given counts directory and creates log-likelihood scores for each context term
in the word vector if that context term is found in the seed lexicon.

Output:
-------
Text files have one Uzbek word and its vector on each line.  Word is separated
from vector with colon ':', context terms and log-likelihood scores are comma-
separated and each context term/ll score pair is semicolon-separated:

uzb_word:<ctxt_word_idx1>,<ctxt_word_log-lik1>;...<ctxt_word_idxn>,<ctxt_word_log-likn>

Output files saved to:

/g/ssli/data/lorelei/Software/Morfessor/baseline/output/vectors/uzb-80.vectors

In this case the sample file is named differently because it only represents
vectors for uzb.0.counts:
    uzb-80.0.vectors

To run:
-------
./uzb_vectors_sample.sh
