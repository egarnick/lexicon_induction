from sys import argv
import xml.etree.ElementTree as ET
import re
import json
import math
import random
import morfessor

"""
Create training and test portions of bilingual lexicon
Input:
  lexicon output training_split_%
"""

SEG_DICT = {}       # {segment: {'mono': ct, 'mult': ct}, ...}
MORF_MODEL = None
MORF_VOCAB = {}     # {token: [seg1, seg2, ...], ...}

# s_token - "source token", t_token - "target token"
# f_token - "foreign token", e_token - "english token"

LEXICON = {}        # {s_token: [t_token, ...], ...}

I_LEX = {}          # {index: {'f': [f_token, ...], 'e': [e_token, ...]}, ...}
F_MAP = {}          # {f_token: index, ...}
E_MAP = {}          # {e_token: index, ...}


def load_segments(seg_file):
    global SEG_DICT
    for line in open(seg_file, 'r'):
        line_split = line.strip().split('\t')
        try:
            SEG_DICT[line_split[0]] = {line_split[1]: int(line_split[2]),
                                       line_split[3]: int(line_split[4])}
        except IndexError:
            print("Error with line:\n" + line)


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


def populate_lexicon(lex_file):
    lex_tree = ET.parse(lex_file)
    lex_root = lex_tree.getroot()
    # print("xml root: " + lex_root.tag)
    for entry in lex_root:
        # Get foreign (Uzbek) word and lowercase
        s_token = entry.findtext("WORD").lower()

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

        # segment source token
        s_token_segs = segment_token(s_token)
        # Find root segment
        s_token = morfed_root(s_token_segs)

        # In case s_token was already entered
        if LEXICON.get(s_token):
            for t_tok in t_tokens:
                if t_tok not in LEXICON[s_token]:
                    LEXICON[s_token].append(t_tok)
        else:
            LEXICON[s_token] = t_tokens
    # Add _bos, _num
    LEXICON["_BOS"] = "_BOS"
    LEXICON["_num"] = "_num"


# NEW
def index_lexicon():
    token_index = 0
    for f_token in LEXICON:
        e_tokens = LEXICON[f_token]
        # Update F_MAP
        F_MAP[f_token] = token_index
        # Update E_MAP
        for e_tok in e_tokens:
            try:
                E_MAP[e_tok].append(token_index)
            except KeyError:
                E_MAP[e_tok] = [token_index]
        # Update I_LEX
        I_LEX[token_index] = {'f': [f_token], 'e': e_tokens}
        token_index += 1
    # print("First in I_LEX: " + str(I_LEX[0]['f']))
    # print("Last in I_LEX: " + str(I_LEX[token_index - 1]['f']))


def write_lexicon(out_file, split_perc):
    # indexed_lex = {"F_MAP": F_MAP, "E_MAP": E_MAP, "I_LEX": I_LEX}

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
                f_map_tr[f_token] = F_MAP[f_token]
            for e_token in I_LEX[il_idx]['e']:
                e_map_tr[e_token] = E_MAP[e_token]
        # Add to testing split
        else:
            i_lex_ts[il_idx] = I_LEX[il_idx]
            for f_token in I_LEX[il_idx]['f']:
                f_map_ts[f_token] = F_MAP[f_token]
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
    num_args = 6
    if len(argv) == num_args:
        lexicon, segments, morf_model, output, tr_split_perc = argv[1:num_args]
        print("Loading segment counts")
        load_segments(segments)
        print("Loading Morfessor model")
        load_morf_model(morf_model)
        print("Reading raw lexicon")
        populate_lexicon(lexicon)
        print("Indexing lexicon items")
        index_lexicon()
        print("Saving lexicon json files")
        write_lexicon(output, int(tr_split_perc))
    else:
        print("Input args should be: lexicon_file output_file train_split")
