from sys import argv
from zipfile import *
import gzip
import glob
import xml.etree.ElementTree as ET
from time import time
import re
import morfessor

"""
gzipped counts files

Print, tab separated, on each line: vocab item, count, context vector
"""

# REGEX
URL_TOKEN = re.compile(r'\b(\S*http\S+)|(\S*www\S+)\b')
NUM_TOKEN = re.compile(r'(\S*\d+\S*)+')
PUNCTUATION = re.compile(r'[\.,!\?\-\(\):–—»«\[\]/\{\}=<>\|;ʻ\"\+]')

# not used
DOLLAR_TOKEN = re.compile(r'[A-Z]{,3}\$\d+(,\d+)*(\.\d+)*[a-zA-Z]*')

# CONSTANTS

# COMMENT TO TEST
REL2ZIPPED = "/data/"
# COMMENT TO TEST
# REL2ZIPPED = "/"

# GLOBAL VARIABLES
START_TIME = 0

# RESOURCE DICTIONARIES
VOCABULARY = {}     # {word : [ct, {ctx1 : ct, ctx2 : ct, ...}], ...}
FILE_GROUP = {}     # {a.xml: True, b.xml: True, ...}
SEG_DICT = {}       # {segment: {'mono': ct, 'mult': ct}, ...}
MORF_MODEL = None
MORF_VOCAB = {}     # {token: [seg1, seg2, ...], ...}


def load_division(div_file):
    for line in (open(div_file, 'r')):
        FILE_GROUP[line.strip()] = True


def load_segments(seg_file):
    global SEG_DICT
    for line in open(seg_file, 'r'):
        line_split = line.strip().split('\t')
        SEG_DICT[line_split[0]] = {line_split[1]: int(line_split[2]),
                                   line_split[3]: int(line_split[4])}


def load_morf_model(morf_model_file):
    global MORF_MODEL
    MORF_MODEL = morfessor.MorfessorIO()\
        .read_binary_model_file(morf_model_file)


def segment_token(tkn):
    global MORF_VOCAB
    try:
        tk_morfed = MORF_VOCAB[tkn]
    except KeyError:
        tk_morfed = MORF_MODEL.viterbi_segment(tkn)[0]
        MORF_VOCAB[tkn] = tk_morfed
    return tk_morfed


def morfed_root(tkn_morfed):
    """
    Return segment with highest mono/mult ratio, or the first novel segment
    :param tkn_morfed: list: segmented token
    :return: string: proposed root
    """
    if len(tkn_morfed) == 1:
        return tkn_morfed[0]
    else:
        max_mono = -1.0
        argmax_mono = ""
        for seg in tkn_morfed:
            try:
                mono_mult = SEG_DICT[seg]
                try:
                    mono_ratio = mono_mult['mono'] / mono_mult['mult']
                # Never seen with other morphology
                except ZeroDivisionError:
                    return seg
                if mono_ratio > max_mono:
                    max_mono = mono_ratio
                    argmax_mono = seg
            # Novel terms are open class
            except KeyError:
                return seg
        return argmax_mono


def add_context(word, ctx):
    if len(ctx):
        try:
            VOCABULARY[word][1][ctx] += 1
        except KeyError:
            VOCABULARY[word][1][ctx] = 1


def count_vocab(xml_text):
    """
    Parse input xml and update VOCABULARY
    :param xml_text: str: text extracted from xml files
    """
    root = ET.fromstring(xml_text)
    if not VOCABULARY.get("_BOS"):
        VOCABULARY["_BOS"] = [0, {}]
    for doc in root:
        for text in doc:
            for seg in text:
                back2 = "_BOS"
                back1 = ""
                VOCABULARY["_BOS"][0] += 1
                tokens = seg.findall('TOKEN')
                for token in (tk for tk in tokens if
                              tk.get('pos') != 'punct'):
                    tk_text = token.text
                    # tk_text = DOLLAR_TOKEN.sub('_DOL', tk_text)
                    tk_text = tk_text.strip('-').lower()
                    tk_text = URL_TOKEN.sub('_URL', tk_text)
                    tk_text = NUM_TOKEN.sub('_NUM', tk_text)
                    tk_text = PUNCTUATION.sub('', tk_text)
                    tk_segs = segment_token(tk_text)
                    tk_text = morfed_root(tk_segs)
                    if len(tk_text):
                        if not VOCABULARY.get(tk_text):
                            VOCABULARY[tk_text] = [1, {}]
                        else:
                            # Increase count for current token
                            VOCABULARY[tk_text][0] += 1
                        add_context(tk_text, back2)
                        add_context(tk_text, back1)
                        if VOCABULARY.get(back1):
                            add_context(back1, tk_text)
                        if VOCABULARY.get(back2):
                            add_context(back2, tk_text)
                        back2 = back1
                        back1 = tk_text
                try:
                    add_context(back1, "_EOS")
                except KeyError:
                    pass


def get_zipped_files(path2lang, cut):
    """
    Pass text from each xml file in zipped dir of given lang to count_vocab()
    :param path2lang: string: absolute path to language folder
    :param cut: int: number of files to process from each zipped directory (0 for all)
    """
    global START_TIME
    START_TIME = time()
    if path2lang[-1] == '/':
        path2lang = path2lang[:-1]
    abs2zipped = path2lang + REL2ZIPPED
    zipped_files = glob.glob(abs2zipped + '/*.ltf.*')
    if len(zipped_files):
        if cut:
            print("Reading " + str(len(zipped_files) * cut) + " Uzbek documents")
        else:
            print("Reading " + str(len(FILE_GROUP)) + " Uzbek documents")
        for z_file in [zf for zf in zipped_files if zf[-8:] == '.ltf.zip']:
            file_counter = 0
            with ZipFile(z_file) as zip_read:
                for xml_file in (xml for xml in zip_read.namelist() if
                                 FILE_GROUP.get(xml)):
                    with zip_read.open(xml_file) as xml_read:
                        xml_contents = xml_read.read()
                        count_vocab(xml_contents)
                    # Keep track of progress and cut early if cut != 0
                    file_counter += 1
                    if cut:
                        print("Read Uzbek document: " + xml_file)
                        if not file_counter % 100:
                            print(str(file_counter) + " files in " +
                                  str(time() - START_TIME) + " seconds")
                        if file_counter == cut:
                            break
    else:
        print("Couldn't find any files at " + abs2zipped)


def dump_counts(outfile_name):
    # Format:
    # word \t count \t context_word,ctxt_count \t ...
    with gzip.open(outfile_name, 'wb') as lm_out:
        for word in VOCABULARY:
            cnt_ctxt = VOCABULARY[word]
            line_out = word + '\t' + str(cnt_ctxt[0])
            contexts = cnt_ctxt[1]
            for ctx_tok in contexts:
                line_out += '\t' + ctx_tok + ',' + str(contexts[ctx_tok])
            line_out += '\n'
            lm_out.write(line_out.encode('utf-8'))


if __name__ == '__main__':
    num_args = 7
    if len(argv) == num_args:
        # Arguments:
        # path: path to home directory containing data folder with zipped language files
        # division: file containing names of zipped language data files to process
        # output: directory for output file
        # cutoff: number of files to process from each zipped directory (0 to process all)
        path, division, segments, morf_model, output, cutoff = argv[1:num_args]
        load_division(division)
        print("Division loaded")
        load_segments(segments)
        print("Segments loaded")
        load_morf_model(morf_model)
        print("Morfessor model loaded")
        get_zipped_files(path, int(cutoff))
        print("Counts finished")
        output_name = output + "/uzb." + division.split('.')[-2] + '.counts'
        print("Writing counts file " + output_name)
        dump_counts(output_name)
    else:
        print("Incorrect number of arguments")
