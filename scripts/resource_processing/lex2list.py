from sys import argv
import json


"""
Extract translations from test portion of seed lexicon and write to for testing
"""


# lexicon
I_LEX = {}          # {index: {'f': [f_token, ...], 'e': [e_token]}, ...}
F_MAP = {}          # {f_token: [index1, index2, ...], ...}
E_MAP = {}          # {e_token: [index], ...}


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


def write_list(destination):
    fword_count = 0
    with open(destination, 'w') as words_list_out:
        for f_word in F_MAP:
            output_line = f_word + '\t'
            for lex_idx in F_MAP[f_word]:
                e_word = I_LEX[str(lex_idx)]['e'][0]
                output_line += e_word + ';'
            output_line = output_line[:-1] + '\n'
            words_list_out.write(output_line)
            fword_count += 1
    print("Wrote " + str(fword_count) + " Uzbek words to " + destination)

if __name__ == '__main__':
    num_args = 3
    if len(argv) == num_args:
        lexicon_in, dest_file = argv[1:num_args]
        print("Loading lexicon")
        read_lexicon(lexicon_in)
        write_list(dest_file)
    else:
        print("Wrong number of arguments")
