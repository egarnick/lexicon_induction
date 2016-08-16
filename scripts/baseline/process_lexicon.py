from sys import argv
import xml.etree.ElementTree as ET
import re
import json
import math
import random

"""
Unique indexes for English
"""

"""
Create training and test portions of bilingual lexicon
Input:
  lexicon output training_split_%
"""

# s_token - "source token", t_token - "target token"
# f_token - "foreign token", e_token - "english token"

LEXICON = {}        # {t_token: [s_token, ...], ...}

I_LEX = {}          # {index: {'f': [f_token, ...], 'e': [e_token]}, ...}
F_MAP = {}          # {f_token: [index1, index2, ...], ...}
E_MAP = {}          # {e_token: [index], ...}


def populate_lexicon(lex_file):
    lex_tree = ET.parse(lex_file)
    lex_root = lex_tree.getroot()
    # print("xml root: " + lex_root.tag)
    for entry in lex_root:
        # Get foreign (Uzbek) word and lowercase
        s_token = entry.findtext("WORD").lower()
        # Remove chr(699) to match test set spelling
        s_token = re.sub('ʻ', '', s_token)

        # First pass: get all English glosses as is
        t_tokens_messy = [gloss.text for gloss in entry.findall("GLOSS") if
                          gloss.text]
        if not len(t_tokens_messy):
            continue

        # Second pass: split list-y glosses
        t_tokens_cleaner = []
        for token in t_tokens_messy:
            try:
                t_tokens_cleaner += [tkn.strip() for tkn in
                                     re.split(r'[,;:/]', token) if len(token)]
            except TypeError:
                print("Error with " + s_token + " total glosses " +
                      str(len(t_tokens_messy)))

        # Third pass: remove blank and duplicate glosses, lowercase words,
        # strip more punctuation
        t_tokens = [tkn for tkn in
                    set(re.sub(r'[!\.\?\[\]\d]+', '', token.lower()) for
                        token in t_tokens_cleaner) if len(tkn)]

        for t_tok in t_tokens:
            try:
                if s_token not in LEXICON[t_tok]:
                    LEXICON[t_tok].append(s_token)
            except KeyError:
                LEXICON[t_tok] = [s_token]

    # Add _bos, _num
    LEXICON["_BOS"] = "_BOS"
    LEXICON["_num"] = "_num"


def index_lexicon():
    token_index = 0
    for e_token in LEXICON:
        f_tokens = LEXICON[e_token]
        # Update E_MAP
        E_MAP[e_token] = [token_index]
        # Update E_MAP
        for f_tok in f_tokens:
            try:
                F_MAP[f_tok].append(token_index)
            except KeyError:
                F_MAP[f_tok] = [token_index]
        # Update I_LEX
        I_LEX[token_index] = {'e': [e_token], 'f': f_tokens}
        token_index += 1
    # print("First in I_LEX: " + str(I_LEX[0]['f']))
    # print("Last in I_LEX: " + str(I_LEX[token_index - 1]['f']))


def write_lexicon(out_file, split_perc):

    # train split
    f_map_tr = {}
    e_map_tr = {}
    i_lex_tr = {}
    train_file = out_file + str(split_perc) + '.train'

    # test split
    f_map_ts = {}
    e_map_ts = {}
    i_lex_ts = {}
    test_file = out_file + str(100 - split_perc) + '.test'

    num_train = int(math.ceil((split_perc / 100) * len(I_LEX)))
    train_idxs = random.sample(range(len(I_LEX)), num_train)
    for il_idx in I_LEX:
        # Add to training split
        if int(il_idx) in train_idxs:
            i_lex_tr[il_idx] = I_LEX[il_idx]
            for f_token in I_LEX[il_idx]['f']:
                try:
                    f_map_tr[f_token].append(il_idx)
                except KeyError:
                    f_map_tr[f_token] = [il_idx]
            for e_token in I_LEX[il_idx]['e']:
                e_map_tr[e_token] = E_MAP[e_token]
        # Add to testing split
        else:
            i_lex_ts[il_idx] = I_LEX[il_idx]
            for f_token in I_LEX[il_idx]['f']:
                try:
                    f_map_ts[f_token].append(il_idx)
                except KeyError:
                    f_map_ts[f_token] = [il_idx]
            for e_token in I_LEX[il_idx]['e']:
                e_map_ts[e_token] = E_MAP[e_token]

    print("train split length: " + str(len(i_lex_tr)))
    print("test split length: " + str(len(i_lex_ts)))
    tr_indexed_lex = {"F_MAP": f_map_tr, "E_MAP": e_map_tr, "I_LEX": i_lex_tr}
    ts_indexed_lex = {"F_MAP": f_map_ts, "E_MAP": e_map_ts, "I_LEX": i_lex_ts}
    if split_perc > 0:
        with open(train_file, 'w') as tr_lex_out:
            json.dump(tr_indexed_lex, tr_lex_out)
    if split_perc < 100:
        with open(test_file, 'w') as ts_lex_out:
            json.dump(ts_indexed_lex, ts_lex_out)


if __name__ == '__main__':
    num_args = 4
    if len(argv) == num_args:
        lexicon, output, tr_split_perc = argv[1:num_args]
        print("Reading raw lexicon")
        populate_lexicon(lexicon)
        print("Indexing lexicon items")
        index_lexicon()
        print("Saving lexicon json files")
        write_lexicon(output, int(tr_split_perc))
    else:
        print("Input args should be: <lexicon_file> <output_file> <train_split>")
