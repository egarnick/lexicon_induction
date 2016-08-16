from sys import argv
import json
import xml.etree.ElementTree as ET
import re


# Loaded resources:
I_LEX_R = {}          # {index: {'f': [f_token, ...], 'e': [e_token, ...]}, ...}
F_MAP_R = {}          # {f_token: index, ...}
E_MAP_R = {}          # {e_token: [index1, index2, ...], ...}

I_LEX_S = {}          # {index: {'f': [f_token, ...], 'e': [e_token, ...]}, ...}
F_MAP_S = {}          # {f_token: index, ...}
E_MAP_S = {}          # {e_token: [index1, index2, ...], ...}


def read_lexicon_r(lex_json):
    global I_LEX_R
    global F_MAP_R
    global E_MAP_R
    with open(lex_json, 'r') as lex_in:
        indexed_lex = json.load(lex_in)
    I_LEX_R = indexed_lex["I_LEX"]
    F_MAP_R = indexed_lex["F_MAP"]
    E_MAP_R = indexed_lex["E_MAP"]


def read_lexicon_s(lex_json):
    global I_LEX_S
    global F_MAP_S
    global E_MAP_S
    with open(lex_json, 'r') as lex_in:
        indexed_lex = json.load(lex_in)
    I_LEX_S = indexed_lex["I_LEX"]
    F_MAP_S = indexed_lex["F_MAP"]
    E_MAP_S = indexed_lex["E_MAP"]


def lang_overlap(orig_lex_file):

    source_types = {}
    total_tokens = 0

    target_types = {}

    # Save all uzbek words
    lex_tree = ET.parse(orig_lex_file)
    lex_root = lex_tree.getroot()
    for entry in lex_root:
        total_tokens += 1
        # Get foreign (Uzbek) word
        s_token = entry.findtext("WORD").lower()
        source_types[s_token] = True

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
        t_tokens = list(set(re.sub(r'[!\.\?\[\]\d]+', '', token.lower()) for
                            token in t_tokens_cleaner if len(token)))
        for t_tok in t_tokens:
            target_types[t_tok] = True

    print("Total source tokens: " + str(total_tokens))
    print("Source types: " + str(len(source_types)))
    print("Target types: " + str(len(target_types)))

    # Check for lost source words
    lost_types = []
    for orig_type in source_types:
        if F_MAP_R.get(orig_type) is None and F_MAP_S.get(orig_type) is None:
            lost_types.append(orig_type)
    print("Total lost source types: " + str(len(lost_types)))
    for lost_type in lost_types:
        print(lost_type)

    # Check for lost target words
    lost_types = []
    for orig_type in target_types:
        if E_MAP_R.get(orig_type) is None and E_MAP_S.get(orig_type) is None:
            lost_types.append(orig_type)
    print("Total lost target types: " + str(len(lost_types)))
    for lost_type in lost_types:
        print(lost_type)

    # Type check for index as key (str) and value (int)
    print("Type of F_MAP_R values: " + str(type(list(F_MAP_R.values())[0])))
    print("Type of I_LEX_R keys: " + str(type(list(I_LEX_R.keys())[0])))
    mismatch = False
    # Check that source and target words correspond (R)
    for f_token in F_MAP_R:
        f_idx = str(F_MAP_R[f_token])
        if f_token not in I_LEX_R[f_idx]['f']:
            print("Mismatch f_token F_MAP_R to I_LEX_R: " + f_token)
            mismatch = True
        for e_token in I_LEX_R[f_idx]['e']:
            if int(f_idx) not in E_MAP_R[e_token]:
                print("Mismatch e_token I_LEX_R to E_MAP_R: " + e_token)
                mismatch = True

    # Check that source and target words correspond (S)
    for f_token in F_MAP_S:
        f_idx = str(F_MAP_S[f_token])
        if f_token not in I_LEX_S[f_idx]['f']:
            print("Mismatch f_token F_MAP_S to I_LEX_S: " + f_token)
            mismatch = True
        for e_token in I_LEX_S[f_idx]['e']:
            if int(f_idx) not in E_MAP_S[e_token]:
                print("Mismatch e_token I_LEX_S to E_MAP_S: " + e_token)
                mismatch = True

    if not mismatch:
        print("All indexes match")

    try:
        print("Context for metamorphism: " + str(I_LEX_R['22924']['e']))
    except KeyError:
        print("Context for metamorphism: " + str(I_LEX_S['22924']['e']))

    try:
        print("Index for 'metamorphism': " + str(E_MAP_R['metamorphism']))
    except KeyError:
        print("Index for 'metamorphism': " + str(E_MAP_S['metamorphism']))


if __name__ == '__main__':
    num_args = 4
    if len(argv) == num_args:
        original_lexicon, lexicon_json_r, lexicon_json_s = argv[1:num_args]
        read_lexicon_r(lexicon_json_r)
        read_lexicon_s(lexicon_json_s)
        lang_overlap(original_lexicon)
    else:
        print("Wrong number of input arguments")

