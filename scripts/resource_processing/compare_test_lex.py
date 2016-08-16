from sys import argv
import json

I_LEX = {}          # {index: {'f': [f_token, ...], 'e': [e_token, ...]}, ...}
F_MAP = {}          # {f_token: index, ...}
E_MAP = {}          # {e_token: index, ...}

LL_VECS = {}        # {uzb_word: True, ...}


def read_lexicon(lex_file):
    global I_LEX
    global F_MAP
    global E_MAP
    with open(lex_file, 'r') as lex_in:
        indexed_lex = json.load(lex_in)
    I_LEX = indexed_lex["I_LEX"]
    print("length of I_LEX: " + str(len(I_LEX)))
    F_MAP = indexed_lex["F_MAP"]
    print("length of F_MAP: " + str(len(F_MAP)))
    E_MAP = indexed_lex["E_MAP"]
    print("length of E_MAP: " + str(len(E_MAP)))


def load_vectors(vector_file):
    global LL_VECS
    for line in open(vector_file, 'r'):
        uzb_word = line.strip().split(':')[0]
        LL_VECS[uzb_word] = True


def compare_test_lex(test_file, out_file):
    overlap_count = 0
    with open(out_file, 'w') as unique_out:
        for line in open(test_file, 'r'):
            uzb_word = line.strip().split('\t')[0]
            if F_MAP.get(uzb_word):
                overlap_count += 1
            else:
                unique_out.write(uzb_word + '\n')
    print("Number of test items in seed lexicon: " + str(overlap_count))


def compare_test_vec(test_file, out_file):
    overlap_count = 0
    with open(out_file, 'w') as unique_out:
        for line in open(test_file, 'r'):
            uzb_word = line.strip().split('\t')[0]
            if LL_VECS.get(uzb_word):
                overlap_count += 1
            else:
                unique_out.write(uzb_word + '\n')
    print("Number of test items in log likelihood vectors: " + str(overlap_count))


if __name__ == '__main__':
    num_args = 4
    if len(argv) == num_args:
        test_list, compare_file, output_dest = argv[1:num_args]
        read_lexicon(compare_file)
        # compare_test_lex(test_list, output_dest)
        # load_vectors(compare_file)
        # compare_test_vec(test_list, output_dest)
    else:
        print("Wrong number of arguments")

