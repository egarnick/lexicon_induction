from sys import argv
import gzip
import glob
from lxml import html
import json
from time import time
from math import log
import nltk.data
import re


# Constant resources
print("Loading tokenizer")
SENT_TOKENIZER = nltk.data.load('tokenizers/punkt/english.pickle')

# REGEX
DOLLAR_TOKEN = re.compile(r'[A-Z]{,3}\$\d+')
NUM_TOKEN = re.compile(r'(\W*\d+\W*)+')
URL_TOKEN = re.compile(r'.+\.\w{2,3}')

# Global Variables
MAX_COUNT = 0
START_TIME = 0
NUM_FILES = 0

# Resource dictionaries
VOCABULARY = {}     # {word : [ct, {ctx1 : ct, ctx2 : ct, ...}], ...}
LOG_LIK_VECS = {}   # {token: {c_feat: ll_score, ...}, ...}
I_LEX = {}          # {index: {'f': [f_token, ...], 'e': [e_token, ...]}, ...}
F_MAP = {}          # {f_token: index, ...}
E_MAP = {}          # {e_token: index, ...}


def read_lexicon(lex_file):
    global I_LEX
    global F_MAP
    global E_MAP
    with open(lex_file, 'r') as lex_in:
        indexed_lex = json.load(lex_in)
    I_LEX = indexed_lex["I_LEX"]
    F_MAP = indexed_lex["F_MAP"]
    E_MAP = indexed_lex["E_MAP"]


def add_context(word, ctx):
    global MAX_COUNT
    if len(ctx):
        try:
            VOCABULARY[word][1][ctx] += 1
            if VOCABULARY[word][1][ctx] > MAX_COUNT:
                MAX_COUNT = VOCABULARY[word][1][ctx]
        except KeyError:
            VOCABULARY[word][1][ctx] = 1


def count_vocab(input_text):
    if not VOCABULARY.get("BOS"):
        VOCABULARY["BOS"] = [1, {}]
    print("Processing " + str(len(input_text)) + " sentences")
    counter = 0
    for sentence in input_text:
        # counter += 1
        # if not counter % 10000:
        #     print("Sentence " + str(counter) + ": ")
        #     print(sentence)
        back2 = "BOS"
        back1 = ""
        for token in sentence.split():
            token = token.strip("\'\"\\/.,;:?!)(")
            token = DOLLAR_TOKEN.sub('DOL', token)
            token = NUM_TOKEN.sub('NUM', token)
            token = URL_TOKEN.sub('URL', token)
            if len(token):
                if VOCABULARY.get(token.lower()):
                    token = token.lower()
                if not VOCABULARY.get(token):
                    VOCABULARY[token] = [1, {}]
                else:
                    VOCABULARY[token][0] += 1
                add_context(token, back2)
                add_context(token, back1)
                if VOCABULARY.get(back1):
                    add_context(back1, token)
                if VOCABULARY.get(back2):
                    add_context(back2, token)
                back2 = back1
                back1 = token


def parse_xml_data(xml_text):
    text = ""
    xml_text = html.fromstring(xml_text)
    for doc in xml_text:
        for texttag in (stag for stag in doc if stag.tag == 'text'):
            if len(texttag.findall('p')):
                for paragraph in texttag:
                    text += paragraph.text
            elif texttag.text:
                text += texttag.text
    sentences_split = SENT_TOKENIZER.tokenize(text.strip())
    count_vocab(sentences_split)


def get_gz_files(path2gz):
    """
    Pass text from each gz file in source dir of corpus to parse_xml_data()
    :param path2gz: string: absolute path to data directory
    :return:
    """
    START_TIME = time()
    if path2gz[-1] != '/':
        path2gz += '/'
    path2sources = path2gz + '*_eng'
    source_dirs = glob.glob(path2sources)
    for src_dir in source_dirs:
        if NUM_FILES:
            source_files = glob.glob(src_dir + '/*.gz')[:NUM_FILES]
        else:
            source_files = glob.glob(src_dir + '/*.gz')
        for src_f in source_files:
            text = ""
            with gzip.open(src_f, 'rb') as gz_read:
                line_count = 0
                for line in gz_read:
                    text += line.decode('utf-8')
                    line_count += 1
                print(str(line_count))
                parse_xml_data(text)


def create_ll_vecs():
    for word in VOCABULARY:
        LOG_LIK_VECS[word] = {}
        for c_word in VOCABULARY[word][1]:
            if E_MAP.get(c_word):
                cw_index = E_MAP[c_word]
                ll_score = VOCABULARY[word][1][c_word] * \
                           (log(MAX_COUNT / VOCABULARY[c_word][0]) + 1)
                for idx in cw_index:
                    LOG_LIK_VECS[word][idx] = ll_score
        if not len(LOG_LIK_VECS[word]):
            LOG_LIK_VECS.pop(word)


if __name__ == '__main__':
    num_args = 5
    if len(argv) == num_args:
        num_files, lexicon_file, path, out_file = argv[1:5]
        NUM_FILES = int(num_files)
        print("Reading lexicon")
        read_lexicon(lexicon_file)
        print("Getting gz files")
        get_gz_files(path)
        print("VOCABULARY length: " + str(len(VOCABULARY)))
        print("Creating ll vectors")
        create_ll_vecs()
        print("Writing output")
        with open(out_file, 'w') as lm_out:
            json.dump(LOG_LIK_VECS, lm_out)
        print("Done")
    else:
        print("Got " + str(len(argv)) + " args.  Expected " + str(num_args))
