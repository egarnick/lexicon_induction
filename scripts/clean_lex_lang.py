from sys import argv
import json
import re


LEXICON = {}        # {e_token: index, ...}

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


def create_lex(lang):
    # print(str(len(E_MAP)))
    for dict_pair_idx in I_LEX:
        dict_pair = I_LEX[dict_pair_idx]
        token_cluster = dict_pair[lang]
        # print(token_cluster)
        tokens = [tok.strip(',') for tok in token_cluster]
        for cand_tok in tokens:
            cand_tok = re.sub(r'\([a-z ]+\)', '', cand_tok)
            cand_tok = re.sub(r'\Abe ', '', cand_tok)
            cand_tok = re.sub(r'\Ato ', '', cand_tok)
            cand_tok = re.sub(r'\Aget ', '', cand_tok)
            cand_tok = re.sub(r' sb$', '', cand_tok).strip(' ()')
            if len(cand_tok):
                LEXICON[cand_tok] = dict_pair_idx


def write_clean_lex(destination):
    with open(destination, 'w') as lex_out:
        for token in LEXICON:
            lex_out.write(str(LEXICON[token]) + '\t' + token + '\n')


if __name__ == '__main__':
    num_args = 4
    if len(argv) == num_args:
        lexicon, output_file, lang_choice = argv[1:4]  # file file e|f
        read_lexicon(lexicon)
        create_lex(lang_choice)
        write_clean_lex(output_file)
    else:
        print("Expected " + str(num_args) + " arguments.  Got " +
              str(len(argv)))

