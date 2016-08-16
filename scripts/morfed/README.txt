This file describes how to recreate uzb_seg.counts, a file of counts for
Morfessor segmentation output over BOLT Uzbek monolingual data.  Counts
indicate occurrences of each segment either as its own word ('mono'), or as
joined with other segments to form a word ('mult').

 -----------------------
|  Directory Structure  |
 -----------------------

The structure of the Morfessor directory is:

Morfessor/
  data/
  doc/
  resources/
  scripts/

The data/ directory contains externally collected data (BOLT Uzbek monolingual
data).  This currently contains symbolic links to the files in
/homes/egarnick/data/BOLT/uzb/monolingual_text.  This data is split into three
zipped folders:

data/
  DF_ALL_UZB.ltf.zip
  NW_ALL_UZB.ltf.zip
  RF_WKP_UZB.ltf.zip

The doc/ directory contains this README file and any other documentation
produced for working with Morfessor and related output.  Currently:

doc/
  README.txt

The resources/ directory contains resources created as a part of this process,
including the final resulting file.  Current contents are:

resources/
  model-uzb.1m.bin
  uzb_lines.1m.clean
  uzb_lines.1m.txt
  uzb_seg.counts
  divisions/
    file_group.<n>.div (n = 0-100)

The scripts/ directory is for scripts used to create resources.  The scripts
are written in Python 3 or Bash.  Currently:

scripts/
  clean_text.py
  combine_seg_counts.py
  delegate_files.py
  extract_uzb.py
  morf_model.sh
  uzb_seg_counts.py


 -----------------------
|  Process description  |
 -----------------------

The process of creating segment occurrence counts is described in 6 steps:

1.  Extract raw text from xml
2.  Clean raw text of punctuation and numbers
3.  Train Morfessor model
4.  Create divisions of Uzbek xml files
5.  Create counts files for each division in parallel
6.  Combine counts files


1.  Extract raw text from BOLT Uzbek monolingual xml files:
-----------------------------------------------------------
Create a file of raw text, one sentence per line, extracted from BOLT Uzbek
xml files.  The output from this step is uzb_lines.1m.txt.

python3 extract_uzb.py <source_dir> <destination_file> <start_index> <num_sentences>

source_dir         Currently this would be Morfessor/data (wherever the .zip
                   files are located).

destination_file   This is the name of the file where the extracted sentences
                   will be written.

start_index        This is a zero-based integer index for the starting
                   sentence to write to output.  Generally this will be 0, but
                   may change in the case of extracting separate sets for
                   training and testing.

num_sentences      This is an integer for the number of sentences to extract.
                   For the purpose of training the current Morfessor model,
                   1000000 (1 million) was used.


2.  Clean raw text (normalize numbers, remove punctuation, lowercase text):
---------------------------------------------------------------------------
First replace all occurrences of a number, either alone or mixed with other
characters with '_NUM'.  This is done using the regex /(\S*\d+\S*)+/.  Next
remove the following punctuation [\.,\!\?\-\(\)\:\–\—»«].  Finally, convert
all text to lowercase.  The output from this step is uzb_lines.1m.clean.

python3 clean_text.py <source_file> <results_file>

source_file   This is the name of the file containing raw text.  In this case
              uzb_lines.1m.txt.

results_file  The file to write the cleaned text into.


3.  Train Morfessor model:
--------------------------
This requires having Morfessor installed locally (instructions at
http://morfessor.readthedocs.io/en/latest/installation.html).  Morfessor can
be used both as a Python module and as a command-line tool.  In this step, the
model is trained using the command-line tools.  The command is given in
morf_model.sh (for use with condor since training can take up to a few hours).
This is run simply as:

./morf_model.sh

The command, found on the Morfessor website is:

morfessor-train -s <model> <input_text>

model       Name for morfessor model.  In this case model-uzb.1m.bin

input_text  Training text file of space-separated words (uzb_lines.1m.clean).


4.  Create divisions of Uzbek xml files:
----------------------------------------
This step is done solely for the purpose of efficiency and saving time.  I
divided the xml files into 101 roughly equal divisions.  Each division takes
several minutes to process, and run in parallel takes about 10 minutes, rather
than many hours.  The output of this step is n (e.g. 101) text files having
the name of one xml file per line.  To run:

python3 delegate_files.py <source_dir> <output_file> <num_divisions>

source_dir      Currently this is Morfessor/data (wherever the .zip files are
                located).

output_file     Base name of all divison files.  This will be appended with
                '.<div_num>.div' (e.g. file_group.0.div)

The 101 originally used divisions are in resources/divisions/.


5.  Create counts files for divisions:
--------------------------------------
This step reads the raw Uzbek text from all BOLT Uzbek monolingual text data
(rather than only the 1 million sentences previously gathered for training
Morfessor).  Raw text is read from all xml files specified in the given
division file, cleaned by the same process as the original text cleaning in
step 2, and segmented using the Morfessor model created in step 3.  The
Morfessor model in this case is loaded within a Python script.  The format of
output is text files with one unique segment per line with counts for
occurrence alone as a whole word and with other segments as part of a word.
Each of the 5 fields is tab-separated:

<segment><TAB><'mono'><mono_count><'mult'><mult_count>

The command for one segment in this step is as follows.  A shell script with
101 similar lines could be used to process all divisions in parallel.

python3 uzb_seg_counts.py <source_dir> <division_file> <morf_model> <output_dir> <cutoff>

source_dir        Currently this is Morfessor/data (wherever the .zip files are
                  located).

division_file     One file output from step 4 (e.g. file_group.0.div)

morf_model        The morfessor model created in step 3 (model-uzb.1m.bin)

output_dir        The location for writing the segment counts file.  Each file
                  name is formatted automatically within the script as
                  uzb-seg.<div_num>.counts (e.g. uzb-seg.0.counts)

cutoff            This is an integer used only for testing and should normally
                  be 0 to process all files.  Otherwise cutoff indicates the
                  number of files from each zipped folder to process.

6.  Combine counts files:
-------------------------
This step produces the final segment count file.  The result has the same
format as the output of step 5 and has counts for each unique segment
aggregated from all segment count files for all divisions.  To run:

python3 combine_seg_counts.py <division_counts_dir> <combined_counts_file>

division_counts_dir    The directory with all division counts files produced
                       in step 5.

combined_counts_file   The name for the file counts file (uzb_seg.counts)

Division counts files are not included in the interest of saving space and
reducing clutter.



Scripts and documentation created by Eric Garnick 06/2016.
Contact: egarnick@gmail.com
