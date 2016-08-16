from sys import argv
from zipfile import *
import glob
import xml.etree.ElementTree as ET
from time import time
import re
import json
import morfessor


SEG_DICT = {}       # {segment: {'mono': ct, 'mult': ct}, ...}
MORF_MODEL = None
MORF_VOCAB = {}     # {token: [seg1, seg2, ...], ...}

# lexicon
I_LEX = {}          # {index: {'f': f_token, 'e': e_token}, ...}
F_MAP = {}          # {f_token: {e_token: idx1, e_token: idx2, ...}, ...}
E_MAP = {}          # {e_token: {f_token: idx1, f_token: idx2, ...}, ...}


def read_lexicon(lex_file):
    global I_LEX
    global F_MAP
    global E_MAP
    with open(lex_file, 'r') as lex_in:
        indexed_lex = json.load(lex_in)
    I_LEX = indexed_lex["I_LEX"]
    F_MAP = indexed_lex["F_MAP"]
    E_MAP = indexed_lex["E_MAP"]
    print("Loaded I_LEX: " + str(len(I_LEX)))
    print("Loaded F_MAP: " + str(len(F_MAP)))
    print("Loaded E_MAP: " + str(len(E_MAP)))


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


def morf_lexicon():
    """
    Return lexicon dictionaries with Morfessor-segment Uzbek terms
    :return: dict: {"I_LEX": <ilex_morfed>,
                    "F_MAP": <fmap_morfed>,
                    "E_MAP": <emap_morfed>}
    """
    ilex_morfed = {}
    fmap_morfed = {}
    emap_morfed = {}

    idx_new = 0
    for f_tok in F_MAP:
        tok_segs = segment_token(f_tok)
        f_root = morfed_root(tok_segs)
        if len(f_root.strip()):
            for e_tok in F_MAP[f_tok].keys():
                # Already seen this e_tok
                if emap_morfed.get(e_tok):
                    # Already seen this pair
                    if emap_morfed[e_tok].get(f_root):
                        continue
                    # New f_root for seen e_tok
                    else:
                        # Update emap
                        emap_morfed[e_tok][f_root] = idx_new
                        # Update fmap
                        try:
                            fmap_morfed[f_root][e_tok] = idx_new
                        except KeyError:
                            fmap_morfed[f_root] = {e_tok: idx_new}
                        # Update ilex
                        ilex_morfed[idx_new] = {'f': f_root, 'e': e_tok}
                        idx_new += 1
                # New e_tok
                else:
                    # Update emap
                    emap_morfed[e_tok] = {f_root: idx_new}
                    # Update fmap
                    try:
                        fmap_morfed[f_root][e_tok] = idx_new
                    except KeyError:
                        fmap_morfed[f_root] = {e_tok: idx_new}
                    # Update ilex
                    ilex_morfed[idx_new] = {'f': f_root, 'e': e_tok}
                    idx_new += 1

    # for idx_old in I_LEX:
    #     ilex_morfed[idx_old] = {'f': '', 'e': ''}
    #     e_tok = I_LEX[idx_old]['e']
    #     f_tok = I_LEX[idx_old]['f']
    #     tok_segs = segment_token(f_tok)
    #     f_root = morfed_root(tok_segs)
    #     if len(f_root.strip()):
    #         # Update ilex
    #         ilex_morfed[idx_old]['e'] = e_tok
    #         ilex_morfed[idx_old]['f'] = f_root
    #         # Update fmap
    #         try:
    #             fmap_morfed[f_root][e_tok] = idx_old
    #         except KeyError:
    #             fmap_morfed[f_root] = {e_tok: idx_old}
    #         # Update emap
    #         try:
    #             emap_morfed[e_tok][f_root] = idx_old
    #         except KeyError:
    #             emap_morfed[e_tok] = {f_root: idx_old}

    print("New I_LEX length: " + str(len(ilex_morfed)))
    print("New F_MAP length: " + str(len(fmap_morfed)))
    print("New E_MAP length: " + str(len(emap_morfed)))

    return {"I_LEX": ilex_morfed,
            "F_MAP": fmap_morfed,
            "E_MAP": emap_morfed}


def dump_lexicon(lexicon, output_name):
    with open(output_name, 'w') as lex_m_out:
        json.dump(lexicon, lex_m_out)


if __name__ == '__main__':
    num_args = 4
    if len(argv) == num_args:
        processed_lexicon, segments, morf_model = argv[1:num_args]
        read_lexicon(processed_lexicon)
        print("Lexicon loaded")
        load_segments(segments)
        print("Segments loaded")
        load_morf_model(morf_model)
        print("Morfessor model loaded")
        morfed_lexicon = morf_lexicon()
        print("Lexicon processed")
        out_name_split = processed_lexicon.split('.')
        out_name_split[0] += '_m'
        out_name = '.'.join(out_name_split)
        dump_lexicon(morfed_lexicon, out_name)
        print("Morfessor-split lexicon written: " + out_name)
    else:
        print("Wrong number of arguments")
