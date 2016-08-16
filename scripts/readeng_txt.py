from sys import argv
from glob import glob
import json
from math import log


MAX_COUNT = 0
STOPS = {"@": True, "<p>": True, "<h>": True, ",": True}
FINAL_PUNCT = {".": True, "?": True, "!": True}

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
    back2 = "BOS"
    back1 = ""
    for token in input_text:
        if FINAL_PUNCT.get(token):
            try:
                add_context(back1, "EOS")
            except KeyError:
                pass
            continue
        if not STOPS.get(token):
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


def get_files(path2files):
    if path2files[-1] != '/':
        path2files += '/'
    path2files += '*'
    # Find text files
    files_list = [f_path for f_path in glob(path2files) if f_path[-4:] == ".txt"]

    if not len(files_list):
        print("No files found at " + path2files)
        return

    for txt_file in files_list:
        print("Processing file ")
        # Extract text and split on whitespace
        with open(txt_file, 'r') as text_in:
            file_conts = []
            for line in text_in:
                file_conts += line.strip().split()
                # print(file_conts)
            count_vocab(file_conts)


def create_ll_vecs():
    for word in VOCABULARY:
        LOG_LIK_VECS[word] = {}
        for c_word in VOCABULARY[word][1]:
            if E_MAP.get(c_word):
                cw_index = E_MAP[c_word]
                ll_score = VOCABULARY[word][1][c_word] * \
                           log(MAX_COUNT / VOCABULARY[c_word][0] + 1)
                for idx in cw_index:
                    LOG_LIK_VECS[word][idx] = ll_score
        if not len(LOG_LIK_VECS[word]):
            LOG_LIK_VECS.pop(word)


if __name__ == '__main__':
    if len(argv) == 4:
        lexicon_file, path, out_file = argv[1:4]
        read_lexicon(lexicon_file)
        get_files(path)
        create_ll_vecs()
        with open(out_file, 'w') as lm_out:
            json.dump(LOG_LIK_VECS, lm_out)
    else:
        print("Incorrect number of arguments")

