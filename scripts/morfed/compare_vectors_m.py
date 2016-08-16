from sys import argv
import json
import gzip
from math import sqrt
import morfessor


"""
gzipped vectors
"""

# Global constants
# ----------------
NUM_TRANS_HYPOS = 50    # Max hypotheses per Uzbek word
NUM_TRANS_CANDS = -1    # Number Uzbek words to translate (-1 for all)

# Loaded resources
# ----------------
TEST_VOCAB = {}         # {uzb: [], ...}

# vectors
FVEC = {}               # {token: {c_feat: ll_score, ...}, ...}
EVEC = {}               # {token: {c_feat: ll_score, ...}, ...}

# lexicon
F_MAP = {}              # {f_token: [index1, index2, ...], ...}
E_MAP = {}              # {e_token: [index], ...}

# morfessor
SEG_DICT = {}           # {segment: {'mono': ct, 'mult': ct}, ...}
MORF_MODEL = None
MORF_VOCAB = {}         # {token: [seg1, seg2, ...], ...}

# Created resources
# -----------------
TRANSLATIONS = {}       # {uzb: [(hyp, score), ...], ...}
EMAGS = {}              # {e_token: vector magnitude}


def read_lexicon(lex_file):
    global F_MAP
    global E_MAP
    with open(lex_file, 'r') as lex_in:
        indexed_lex = json.load(lex_in)
    F_MAP = indexed_lex["F_MAP"]
    E_MAP = indexed_lex["E_MAP"]


def load_vectors(fvec_file, evec_file):
    global FVEC, EVEC
    for fline in gzip.open(fvec_file, 'rb'):
        fline_split = fline.decode().strip().split(':')
        tok = ''.join(fline_split[:-1])
        vec = fline_split[-1]
        if F_MAP.get(tok):
            FVEC[tok] = {}
            for feat_val in vec.split(';'):
                feat, val = feat_val.split(',')
                FVEC[tok][int(feat)] = float(val)
    print("Uzbek vectors loaded: " + str(len(FVEC)))
    for eline in gzip.open(evec_file, 'rb'):
        eline_split = eline.decode().strip().split(':')
        tok = ''.join(eline_split[:-1])
        vec = eline_split[-1]
        if E_MAP.get(tok):
            EVEC[tok] = {}
            for feat_val in vec.split(';'):
                feat, val = feat_val.split(',')
                EVEC[tok][int(feat)] = float(val)
    print("English vectors loaded: " + str(len(EVEC)))


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


def load_test(test_voc_file):
    global TEST_VOCAB
    for line in open(test_voc_file, 'r'):
        TEST_VOCAB[line.strip().split('\t')[0]] = []
    print("Loaded " + str(len(TEST_VOCAB)) + " test items")


def calc_emags():
    """
    Cache magnitudes for all English word vectors
    :return:
    """
    global EMAGS
    for evec in EVEC:
        e_feats = EVEC[evec]
        EMAGS[evec] = sqrt(sum(pow(score, 2) for score in e_feats.values()))


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


def compare_vectors():
    """
    Save top N translation candidates from source test tokens
    :return:
    """
    global TRANSLATIONS
    counter = 0
    for test_tok in TEST_VOCAB:
        # Find word root
        tok_segs = segment_token(test_tok)
        test_root = morfed_root(tok_segs)
        # Only check known words
        if F_MAP.get(test_root) and FVEC.get(test_root):
            # Break early to test
            if counter == NUM_TRANS_CANDS:
                return
            counter += 1
            candidates = []         # [(translation_cand, sim_score), ...]
            f_feats = FVEC[test_root]
            print("Word: " + test_root)
            print("Features: " + str(f_feats))
            # Calculate denominator
            fmag = sqrt(sum(pow(score, 2) for score in f_feats.values()))
            for evec in EVEC:
                # Only check known words
                if E_MAP.get(evec):
                    e_feats = EVEC[evec]
                    # Get denominator
                    emag = EMAGS[evec]
                    # Find common features and update dot product for vectors
                    dot_prod = 0
                    for q_feat in f_feats:
                        try:
                            dot_prod += f_feats[q_feat] * e_feats[q_feat]
                        except KeyError:
                            pass
                    if dot_prod:
                        candidates.append((evec, dot_prod / (fmag * emag)))
                        candidates = sorted(candidates,
                                            key=lambda pair: pair[1],
                                            reverse=True)[:NUM_TRANS_HYPOS]
            if len(candidates):
                print("Adding hypotheses for: " + test_tok)
                TRANSLATIONS[test_tok] = candidates
            print("Number of words checked: " + str(counter))


def dump_translations(out_file):
    with open(out_file, 'w') as trans_out:
        for token_uz in TRANSLATIONS:
            trans_out.write(token_uz + '\t')
            # Write hypotheses
            first_trans = TRANSLATIONS[token_uz][0]
            trans_out.write(first_trans[0] + ',' + str(first_trans[1]))
            for trans_hyp in TRANSLATIONS[token_uz][1:]:
                trans_out.write(';' + trans_hyp[0] + ',' + str(trans_hyp[1]))
            trans_out.write('\n')


def clear_vectors():
    global FVEC, EVEC
    FVEC = {}
    EVEC = {}


if __name__ == '__main__':
    num_args = 8
    if len(argv) == num_args:
        lexicon, segments, morf_model, test_file, \
        f_vectors, e_vectors, output = argv[1:num_args]
        read_lexicon(lexicon)
        print("Lexicon loaded")
        load_segments(segments)
        print("Segments loaded")
        load_morf_model(morf_model)
        print("Morfessor model loaded")
        load_vectors(f_vectors, e_vectors)
        print("Feature vector files loaded")
        load_test(test_file)
        print("Test words loaded")
        calc_emags()
        print("English vector magnitudes calculated")
        compare_vectors()
        print("Vectors compared")
        dump_translations(output)
        print("Translation file written")
        clear_vectors()
        print("Cleared vector dictionaries")
    else:
        print("Incorrect number of arguments")

