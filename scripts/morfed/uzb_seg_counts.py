from sys import argv
from zipfile import *
import glob
import xml.etree.ElementTree as ET
import re
from time import time
import morfessor


"""
Print, tab separated, on each line: segment 'mono' mono_count 'mult' mult_count
for a division of target language XML files
"""

# REGEX
URL_TOKEN = re.compile(r'\b(\S*http\S+)|(\S*www\S+)\b')
NUM_TOKEN = re.compile(r'(\S*\d+\S*)+')
PUNCTUATION = re.compile(r'[\.,!\?\-\(\):–—»«\[\]/\{\}=<>\|;ʻ\"\+]')

# Global Variables
MAX_COUNT = 0
START_TIME = 0

# Global data
SEG_CACHE = {}     # {word: [seg1, seg2, ...], ...}
SEG_COUNTS = {}     # {segment: {'mono': ct, 'mult': ct}}
FILE_GROUP = {}     # {a.xml: True, b.xml: True, ...}
MORF_MODEL = None


def load_division(div_file):
    for line in (open(div_file, 'r')):
        FILE_GROUP[line.strip()] = True
    print("Division length: " + str(len(FILE_GROUP)) + " files")


def load_morf_model(morf_model_file):
    global MORF_MODEL
    MORF_MODEL = morfessor.MorfessorIO()\
        .read_binary_model_file(morf_model_file)


def count_vocab(xml_text):
    """
    Parse input xml and update SEG_CACHE and SEG_COUNTS
    :param xml_text: string: entire text of xml file
    :return: int: number of words processed
    """
    global SEG_CACHE, SEG_COUNTS
    root = ET.fromstring(xml_text)
    word_count = 0
    for doc in root:
        for text in doc:
            for seg in text:
                tokens = seg.findall('TOKEN')
                for token in (tk for tk in tokens if
                              tk.get('pos') != 'punct'):
                    tk_text = URL_TOKEN.sub('_URL', token.text.lower())
                    tk_text = NUM_TOKEN.sub('_NUM', tk_text)
                    tk_text = PUNCTUATION.sub('', tk_text)
                    if tk_text not in ['\'', '\"', '\\', '/', '.', ',', ';',
                                       ':', '?', '!', ')', '(', '-', '–'] and \
                            len(tk_text):
                        # Check if morfessor output for tk_text already cached
                        try:
                            tk_morfed = SEG_CACHE[tk_text]
                        # Segment tk_text with morfessor and cache results
                        except KeyError:
                            tk_morfed = MORF_MODEL.viterbi_segment(tk_text)[0]
                            SEG_CACHE[tk_text] = tk_morfed
                        # Record counts of each segment's context type
                        for seg in tk_morfed:
                            try:
                                if len(tk_morfed) == 1:
                                    SEG_COUNTS[seg]['mono'] += 1
                                else:
                                    SEG_COUNTS[seg]['mult'] += 1
                            except KeyError:
                                SEG_COUNTS[seg] = {'mono': 0, 'mult': 0}
                                word_count += 1
                                if len(tk_morfed) == 1:
                                    SEG_COUNTS[seg]['mono'] += 1
                                else:
                                    SEG_COUNTS[seg]['mult'] += 1
    return word_count


def get_zipped_files(path2lang, cut):
    """
    Pass text from each xml file in zipped dir to count_vocab()
    :param path2lang: string: absolute path to folder with zipped xml files
    :param cut: int: number of files to process per directory (all if 0)
    """
    global START_TIME
    START_TIME = time()
    total_wc = 0
    abs2zipped = path2lang.rstrip('/')
    zipped_files = glob.glob(abs2zipped + '/*.ltf.*')
    if len(zipped_files):
        for z_file in [zf for zf in zipped_files if zf[-8:] == '.ltf.zip']:
            file_counter = 0
            with ZipFile(z_file) as zip_read:
                for xml_file in (xml for xml in zip_read.namelist() if
                                 FILE_GROUP.get(xml)):
                    with zip_read.open(xml_file) as xml_read:
                        xml_contents = xml_read.read()
                        total_wc += count_vocab(xml_contents)
                    # Keep track of progress and cut early if cut != 0
                    file_counter += 1
                    if cut:
                        if not file_counter % 100:
                            print(str(file_counter) + " files in " +
                                  str(time() - START_TIME) + " seconds")
                        if file_counter == cut:
                            break
    else:
        print("Couldn't find any files at " + abs2zipped)
    print("Total words processed: " + str(total_wc))


def dump_vocab(out_file):
    # Format output file name
    output_name = out_file + "/uzb-seg." + \
                  division.split('.')[-2] + '.counts'
    with open(output_name, 'w') as lm_out:
        for token in SEG_COUNTS:
            counts = SEG_COUNTS[token]
            lm_out.write('\t'.join(
                [token, 'mono', str(counts['mono']),
                 'mult', str(counts['mult'])]) + '\n')


if __name__ == '__main__':
    if len(argv) == 6:
        # Arguments:
        # path - absolute path to directory with zipped Uzbek xml files
        # division - file of the list of Uzbek xml files to process 
        #            (for batch processing)
        # morf_model - morfessor model file (version 2 - .bin type)
        # output - destination directory for output file
        # cutoff - integer number of files to process from each zipped folder
        #          (used for testing a few files, otherwise 0 for all files)
        path, division, morf_model, output, cutoff = argv[1:6]
        load_division(division)
        print("Division loaded.")
        load_morf_model(morf_model)
        print("Morfessor model loaded")
        get_zipped_files(path, int(cutoff))
        print("Counts finished")
        dump_vocab(output)
        print("Max count: " + str(MAX_COUNT))
    else:
        print("Incorrect number of arguments")
