from sys import argv
from glob import glob
import json
import gzip
from time import time
from math import log

"""
Write vectors gzipped
"""

"""
Print, tab separated, on each line: vocab item, count, context vector
"""

# Global variables
MAX_COUNT = 0
START_TIME = 0

# Global constants
REL2ZIPPED = "/data/"

# Global data structures
VOCABULARY = {}     # {word : [ct, {ctx1 : ct, ctx2 : ct, ...}], ...}
LOG_LIK_VECS = {}   # {token: {c_feat: ll_score, ...}, ...}
F_MAP = {}          # {f_token: [index1, index2, ...], ...}
E_MAP = {}          # {e_token: [index], ...}
FILE_GROUP = {}     # {a.xml: True, b.xml: True, ...}


def read_lexicon(lex_file):
    global F_MAP
    global E_MAP
    with open(lex_file, 'r') as lex_in:
        indexed_lex = json.load(lex_in)
    F_MAP = indexed_lex["F_MAP"]
    E_MAP = indexed_lex["E_MAP"]


def load_vocab(counts_file):
    vocab_dict = {}
    for line in gzip.open(counts_file, 'rb'):
        line_split = line.decode().strip().split('\t')
        word = line_split[0]
        count = int(line_split[1])
        vocab_dict[word] = [count, {}]
        for ctxt_ct in line_split[2:]:
            ctxt, ct = ctxt_ct.rsplit(',', 1)
            vocab_dict[word][1][ctxt] = int(ct)
    return vocab_dict


def load_counts(cts_dir):
    """
    Aggregate counts from each .counts file into VOCABULARY
    :param cts_dir:
    """
    global VOCABULARY, MAX_COUNT, START_TIME
    START_TIME = time()
    if cts_dir[-1] != '/':
        cts_dir += '/'
    cts_files = glob(cts_dir + '*')
    print("Number of counts files: " + str(len(cts_files)))
    processed = 0
    for cts_file in cts_files:
        print("Processing " + cts_file)
        if cts_file[-7:] == '.counts':
            processed += 1
            new_vocab = load_vocab(cts_file)
            for token in new_vocab:
                try:
                    VOCABULARY[token][0] += new_vocab[token][0]
                    for ctxt in new_vocab[token][1]:
                        try:
                            VOCABULARY[token][1][ctxt] += \
                                new_vocab[token][1][ctxt]
                        except KeyError:
                            VOCABULARY[token][1][ctxt] = \
                                new_vocab[token][1][ctxt]
                except KeyError:
                    VOCABULARY[token] = \
                        [new_vocab[token][0], new_vocab[token][1]]
    if processed != len(cts_files):
        print("Only processed: " + str(processed))
    # Set MAX_COUNT, skipping _BOS and _num
    MAX_COUNT = max([VOCABULARY[word][0] for word in VOCABULARY if
                     word[0] != '_'])


def create_ll_vecs(lang_option):
    global LOG_LIK_VECS
    if lang_option == 'f':
        lang_map = F_MAP
    elif lang_option == 'e':
        lang_map = E_MAP
    print("creating ll vectors after " + str(time() - START_TIME))
    # For each corpus word, try to create an entry in LOG_LIK_VECS
    for word in VOCABULARY:
        LOG_LIK_VECS[word] = {}
        # For each context word seen with corpus word get the
        # indexes of each of its translations from the lexicon
        for c_word in VOCABULARY[word][1]:
            if lang_map.get(c_word):
                for cw_index in lang_map[c_word]:
                    # Create tf-idf value for context word, add to vocabulary
                    try:
                        c_count_in_context = VOCABULARY[word][1][c_word]
                        c_count = VOCABULARY[c_word][0]
                        ll_score = c_count_in_context * \
                                   (log(MAX_COUNT / c_count) + 1)
                        LOG_LIK_VECS[word][cw_index] = ll_score
                    except ValueError:
                        print("Problem values: word in context count - " + str(VOCABULARY[word][1][c_word]) +
                              " MAX_COUNT - " + str(MAX_COUNT) + " cword count - " + str(VOCABULARY[c_word][0]))
                        return
        if not len(LOG_LIK_VECS[word]):
            LOG_LIK_VECS.pop(word)
    print("Total vocabulary: " + str(len(VOCABULARY)))
    print("Finished ll vectors after " + str(time() - START_TIME))


def dump_vectors(out_file):
    with gzip.open(out_file, 'wb') as lm_out:
        for tok in LOG_LIK_VECS:
            output_line = tok + ':'
            # lm_out.write(tok + ':')
            ccount = 0
            for cword_i in LOG_LIK_VECS[tok]:
                output_line += str(cword_i) + ',' + \
                               str(LOG_LIK_VECS[tok][cword_i])
                # lm_out.write(str(cword_i) + ',' +
                #              str(LOG_LIK_VECS[tok][cword_i]))
                ccount += 1
                if ccount < len(LOG_LIK_VECS[tok]):
                    output_line += ';'
                    # lm_out.write(';')
                else:
                    output_line += '\n'
                    # lm_out.write('\n')
            lm_out.write(output_line.encode('utf-8'))


if __name__ == '__main__':
    num_args = 5
    if len(argv) == num_args:
        # lang - f|e
        lang, lexicon_file, counts_dir, output = argv[1:num_args]
        read_lexicon(lexicon_file)
        print("Lexicon loaded.")
        load_counts(counts_dir)
        print("Counts loaded.")
        create_ll_vecs(lang)
        dump_vectors(output)
        print("Max count: " + str(MAX_COUNT))
    else:
        print("Incorrect number of arguments")
