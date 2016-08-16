from sys import argv
import json

"""
Given pickled lexicon and text file, print the overlap between the two
"""


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


def text_vocab(input_file):
    vocab = {}
    for line in open(input_file, 'r'):
        for token in line.strip().split():
            try:
                vocab[token] += 1
            except KeyError:
                vocab[token] = 1
    return vocab


def calc_overlap(voc):
    overlap_count = 0
    for token in voc:
        if F_MAP.get(token):
            overlap_count += 1
    print("Tokens in common: " + str(overlap_count))
    print("Text vocab length: " + str(len(voc)))
    print("Lexicon vocab length: " + str(len(F_MAP)))


if __name__ == '__main__':
    num_args = 3
    if len(argv) == num_args:
        lexicon_file, text_file = argv[1:3]
        read_lexicon(lexicon_file)
        text_voc = text_vocab(text_file)
        calc_overlap(text_voc)

