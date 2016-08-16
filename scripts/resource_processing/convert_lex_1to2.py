from sys import argv
import json

"""
Convert lexicon in version 1 format: unique indexes for each uzb-eng pair
to version 2 format: unique index for each eng term
"""


# Version 1
I_LEX = {}          # {index: {'f': f_token, 'e': e_token}, ...}
F_MAP = {}          # {f_token: {e_token: idx1, e_token: idx2, ...}, ...}
E_MAP = {}          # {e_token: {f_token: idx1, f_token: idx2, ...}, ...}

# Version 3
# I_LEX = {}          # {index: {'f': [f_token, ...], 'e': [e_token]}, ...}
# F_MAP = {}          # {f_token: [index1, index2, ...], ...}
# E_MAP = {}          # {e_token: [index], ...}


def read_lexicon(lex_file):
    global I_LEX
    global F_MAP
    global E_MAP
    with open(lex_file, 'r') as lex_in:
        indexed_lex = json.load(lex_in)
    I_LEX = indexed_lex["I_LEX"]
    F_MAP = indexed_lex["F_MAP"]
    E_MAP = indexed_lex["E_MAP"]
    print("Original I_LEX: " + str(len(I_LEX)))
    print("Original F_MAP: " + str(len(F_MAP)))
    print("Original E_MAP: " + str(len(E_MAP)))


def convert_lex():
    ilex2 = {}
    fmap2 = {}
    emap2 = {}
    index = 0
    for etok in E_MAP:
        # Update ilex2
        ilex2[index] = {'f': list(E_MAP[etok].keys()), 'e': etok}
        # Update fmap2
        for ftok in E_MAP[etok].keys():
            try:
                fmap2[ftok].append(index)
            except KeyError:
                fmap2[ftok] = [index]
        # Update emap2
        emap2[etok] = [index]
        index += 1
    print("Converted I_LEX: " + str(len(ilex2)))
    print("Converted F_MAP: " + str(len(fmap2)))
    print("Converted E_MAP: " + str(len(emap2)))

    return {"I_LEX": ilex2, "F_MAP": fmap2, "E_MAP": emap2}


def dump_lex(lexicon, output_file):
    out_file = '.'.join([output_file.split('.')[0]] + ['2'] +
                        output_file.split('.')[2:])
    with open(out_file, 'w') as tr_lex_out:
        json.dump(lexicon, tr_lex_out)


if __name__ == '__main__':
    num_args = 2
    if len(argv) == num_args:
        lex_f_v1 = argv[1]
        print("Loading original lexicon")
        read_lexicon(lex_f_v1)
        print("Converting lexicon")
        lex_v2 = convert_lex()
        print("Writing converted lexicon")
        dump_lex(lex_v2, lex_f_v1)
    else:
        print("Wrong number of arguments")
