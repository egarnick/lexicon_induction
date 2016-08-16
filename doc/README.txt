


BASELINE:
---------

  DESCRIPTION:

  Tokens:
  Tokens are strings of characters separated by whitespace.  Any token
  containing a digit is replaced with '_NUM'.  English tokens are stripped of
  all leading and trailing [\'\"\\/.,;:?!)(].  Uzbek tokens are taken from
  tokenized results of xml files with punctuation stripped.

  Counts:
  Occurrences of each unique token are counted along with the counts of tokens
  that appear within a window of 2 on both sides.  _BOS tokens are counted as
  context only for sentence-initial tokens, ignoring the 2-token window.

  Vectors:
  Feature value for each context word is:

    (nfk) * (log((n) / (nk)) + 1)

    nfk = count of token and context token cooccurrence
    n = max count for any token in data
    nk = total count of context token


  PROCESS:

  Uzbek vectors (bar.ee.washington.edu):
  --------------------------------------

  1.  Make divisions of zipped xml files (generally use 101 divisions):

        delegate_files.py <inputs_dir> <output_name> <num_divisions>

  2.  Set up run101scripts.sh for inputs-uzb_counts and scripts/baseline/uzb_counts.sh

        bash scripts/migrate/run_migrate.sh 101

  3.  Set up run1scripts.sh for inputs-uzb_vectors and scripts/baseline/uzb_vectors.sh

        bash scripts/migrate/run_migrate.sh 1

  English vectors (dryas.ling.washington.edu):
  ----------------

  1.  Create English counts

        bash run_eng_counts.sh

  2.  Create English vectors

        condor_submit eng_vectors.cmd

  Translation hypotheses (bar.ee.washington.edu):
  -----------------------------------------------

  1.  Transfer English vectors from dryas to bar

        sftp egarnick@dryas.ling.washington.edu
        get output/eng-80.vectors output/vectors_base

  2.  Set up run1scripts.sh for inputs-comp_vectors scripts/baseline/compare_vectors.sh

        bash scripts/migrate/run_migrate.sh 1














          ##########################
          #                        #
          #   Data and Resources   #
          #                        #
          ##########################

Data:
-----
    Original BOLT Uzbek data.  This includes bilingual lexicon and monolingual
    text.

Resources:
----------
    Text and other files created from original data for using to derive
    results.  This includes:
     - English vocabulary file
     - Lines of Uzbek text, which punctuation and cleaned of punctuation
     - Pickle files of Uzbek-English bilingual lexicon (split for training and
       testing).

    eng_text:
      eng_vocab_all.txt - This file contains all English definitions from the
      BOLT Uzbek bilingual lexicon, including MWEs.  Total length 23,478
      definitions

      eng_vocab_no-mwe.txt - This file contains all single-term English
      definitions from the BOLT Uzbek bilingual lexicon (no MWEs by
      whitespace).  Total length: 17,801

      lex_out-of_vec.txt - This file contains all single English terms in the
      BOLT Uzbek bilingual lexicon not in the GloVe vectors.  Length without
      dropping hyphens: 2,337.  Length after dropping hyphens: 2,145


-------------------------------------------------------------------------------
-------------------------------------------------------------------------------



          #################
          #               #
          #   Zipped.py   #
          #               #
          #################


Description:
------------
    Object for interacting with zipped directories.

Use:
----
    Command line:
    -------------
    lszip.py
        arg 1: path to zipfile
    catzip.py
        arg 1: path to zipfile
        arg 2: name of target file in zipfile directory
               (no target gives first content file)


-------------------------------------------------------------------------------
-------------------------------------------------------------------------------



          ###############################
          #                             #
          #  Process bilingual lexicon  #
          #                             #
          ###############################


Assumptions:
------------
    lexicon file in xml format as lexicon.v6.llf.xml

Process:
--------

    A.

    process_lexicon.py creates a training and test split of the lexicon saved
    as json files of python dictionaries.  To run:

    python3 process_lexicon.py lex_file.xml output_name training_split_%

    If training_split_% is 0, only test file is written.  If training_split_%
    is 100, only training file is written.

    B.

    clean_eng_lex.py creates a file with each English vocabulary item on its
    own line.  Some repetition is now possible with clusters that contained
    the same term.  To run:

    python3 clean_eng_lex.py lexicon_pickle output_file_name

Related options:
----------------

    1.  Calculate ratio of MWEs in a vocabulary file containing one term per
        line.  To run:

        mwe_ratio.py vocabulary_file


-------------------------------------------------------------------------------
-------------------------------------------------------------------------------



          ############################
          #                          #
          #  Prepare clean uzb text  #
          #                          #
          ############################


Assumptions:
------------
Text is xml formatted as BOLT Uzbek monolingual text.

Process:
--------

    A.

    python3 extract_uzb.py zip_text_dir dest_file start_idx num_lines

    Where zip_text_dir contains zipped text files of xml, dest_file is the
    name of the file for the extracted text (e.g. uzb_lines.1000.txt),
    start_idx is usually 0, num_lines is big (100000+?)

    B.

    python3 clean_text.py punctuated_text clean_text

    Where arguments are names for input and output files respectively.


-------------------------------------------------------------------------------
-------------------------------------------------------------------------------



          ############################
          #                          #
          #  Command line Morfessor  #
          #                          #
          ############################


morfessor -t $TRAIN -S $MODEL -T $TEST


LOCALDIR='/n/bar/s1/egarnick/'
MYHOME='/n/basie/home/egarnick/'

TRAIN='resources/uzb_text/uzb_lines.10000.clean'
MODEL='models/model-uzb.10000.segm'
TEST=$TRAIN'.final'

space_req s1

mkdir $LOCALDIR'resources'
mkdir $LOCALDIR'models'
cp $MYHOME$TRAIN $LOCALDIR'resources'


-------------------------------------------------------------------------------
-------------------------------------------------------------------------------



          ##################################
          #                                #
          #  Process Uzbek XML -> Vectors  #
          #                                #
          ##################################

Divide up text files:
---------------------

Run (do for argv[4] 101):
python3 scripts/baseline/delegate_files.py zipfiles_directory outputfile numberofdivisions


Collect counts:
---------------

Set run_migrate.sh line 19:
cp -Lr $MYHOME/inputs-uzb_counts $LDIR/temp

To run:
bash scripts/migrate/run_migrate.sh 101


Convert counts to vectors:
--------------------------

Set scripts/migrate/run_migrate.sh line 19:
cp -Lr $MYHOME/inputs-uzb_vectors $LDIR/temp

Set scripts/migrate/run_1shells.sh:
bash /homes/egarnick/scripts/baseline/uzb_vectors.sh

To run:
bash scripts/migrate/run_migrate.sh 1


          ####################################
          #                                  #
          #  Process English XML -> Vectors  #
          #                                  #
          ####################################




Bilingual eng-uzb lexicon: 36,623:
    tr: 29,299
    ts: 7,324


















