from sys import argv
import json


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


def print_matches(res_file):
    for line in open(res_file, 'r'):
        word_cands = line.strip(']').split('[')
        word = word_cands[0]
        cands = word_cands[1]
        cands_split = [cand.strip(',') for cand in cands.split()]
        cand_words = [cand_pair.split()[0].strip(",'") for cand_pair in cands_split]

        target_idx = F_MAP[word]
        target_translations = I_LEX[str(target_idx)]['e']
        print(word + ": ", end='')
        print(target_translations)
        print(cand_words)
        for word in cand_words:
            if word in target_translations:
                print('\t' + word)


def count_lex():
    eng_words = 0
    max_idx = 0
    for new_idx in I_LEX:
        eng_words += len(I_LEX[new_idx]['e'])
        if int(new_idx) > max_idx:
            max_idx = int(new_idx)
    print("Total translation sets: " + str(max_idx))
    print("Total English translations: " + str(eng_words))


if __name__ == '__main__':
    # results_file = argv[1]
    read_lexicon('lex_file')
    # print_matches(results_file)
    count_lex()

