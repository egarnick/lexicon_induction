This document describes how to process a sample of the Morfessor-segmented
Uzbek counts data and produce the corresponding word vectors with
log-likelihood scores for context words.  All software is either shell scripts
or written in Python3.

Data files used:
----------------
Processed, Morfessor-segmented Uzbek-English seed lexicon:
/g/ssli/data/lorelei/Software/Morfessor/morf/resources/uzb-eng/uzb-eng_lexicon_m80.train

Morfessor-segmented Uzbek corpus counts:
/g/ssli/data/lorelei/Software/Morfessor/morf/resources/counts/uzb.0.counts

Software:
---------
/g/ssli/data/lorelei/Software/Morfessor/morf/scripts/lang_vectors_m.py
/g/ssli/data/lorelei/Software/Morfessor/morf/scripts/uzb_vectors_m_sample.sh

lang_vectors_m.py aggregates word and context counts for all counts files in
the given counts directory and creates log-likelihood scores for each context
term in the word vector if that context term is found in the seed lexicon.

Output:
-------
Text files have one Uzbek word and its vector on each line.  Word is separated
from vector with colon ':', context terms and log-likelihood scores are comma-
separated and each context term/ll score pair is semicolon-separated:

uzb_word:<ctxt_word_idx1>,<ctxt_word_log-lik1>;...<ctxt_word_idxn>,<ctxt_word_log-likn>

Output files saved to:

/g/ssli/data/lorelei/Software/Morfessor/baseline/output/vectors/uzb-80_m.vectors

In this case the sample file is named differently because it only represents
vectors for uzb.0.counts:
    uzb-80_m.0.vectors

To run:
-------
./uzb_vectors_sample.sh
