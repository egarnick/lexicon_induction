from sys import argv
import re
from nltk.metrics import edit_distance


MAX_EDIT_DIST = 0.2

LEXICON_VOCAB = {}
VECTORS_VOCAB = {}


def load_lexv(lex_file):
    with open(lex_file, 'r') as lex_in:
        for line in lex_in:
            line_split = line.strip().split('\t')
            LEXICON_VOCAB[line_split[1]] = int(line_split[0])


def load_vecv(vec_file):
    with open(vec_file, 'r') as vec_in:
        for line in vec_in:
            VECTORS_VOCAB[line.strip().split()[0]] = True


def ness_stem(token):
    token = re.sub(r'(\w+)ness\b', r'\1', token)
    return re.sub(r'(\w+)i\b', r'\1', token)


def found_typo(misspelled):
    """
    Return most similar word found in VECTORS_VOCAB
    :param misspelled: string: unrecognized word
    :return: string: hypothesized fix for typo
    """
    fixed = ""
    dist = MAX_EDIT_DIST
    for vec_tok in VECTORS_VOCAB:
        new_dist = edit_distance(misspelled, vec_tok) / \
                   max(len(misspelled), len(vec_tok))
        if new_dist < dist:
            fixed = vec_tok
            dist = new_dist
    print(misspelled + " -> " + fixed)
    return fixed


def compare_vocabs(in_vec_file, diff_terms_file):
    overlap_count = 0
    overlap_out = open(in_vec_file, 'w')
    with open(diff_terms_file, 'w') as diff_out:
        for lex_tok in LEXICON_VOCAB:
            # Word found in vectors
            if VECTORS_VOCAB.get(lex_tok):
                overlap_out.write(str(LEXICON_VOCAB[lex_tok]) +
                                  '\t' + lex_tok + '\n')
                overlap_count += 1
            # Word found without hyphen
            elif VECTORS_VOCAB.get(re.sub(r'\-', '', lex_tok)):
                overlap_out.write(
                    str(LEXICON_VOCAB[lex_tok]) + '\t' +
                    re.sub(r'\-', '', lex_tok) + '\n')
                overlap_count += 1
            elif len(lex_tok.split()) == 2:
                if VECTORS_VOCAB.get(re.sub(r' ', '', lex_tok)):
                    overlap_out.write(str(LEXICON_VOCAB[lex_tok]) + '\t' +
                                      re.sub(r' ', '', lex_tok) + '\n')
                    overlap_count += 1
            else:
                unknown = True
                # -ness suffix removed
                if len(lex_tok.split()) == 1:
                    ness_stemmed = ness_stem(lex_tok)
                    if VECTORS_VOCAB.get(ness_stemmed):
                        overlap_out.write(str(LEXICON_VOCAB[lex_tok]) + '\t' +
                                          ness_stemmed + '\n')
                        overlap_count += 1
                        unknown = False


                    # fixed_tok = found_typo(lex_tok)
                    # # Fixed typo and found in VECTORS_VOCAB
                    # if len(fixed_tok) and VECTORS_VOCAB.get(fixed_tok):
                    #     overlap_out.write(str(LEXICON_VOCAB[lex_tok]) +
                    #                       '\t' + fixed_tok + '\n')
                    #     overlap_count += 1
                    #     unknown = False



                # Word not found
                if unknown:
                    diff_out.write(str(LEXICON_VOCAB[lex_tok]) +
                                   '\t' + lex_tok + '\n')
    print("Ratio of lexicon words in vectors: ")
    print(str(overlap_count) + '/' + str(len(LEXICON_VOCAB)))
    print("Ratio of vector words in lexicon: ")
    print(str(overlap_count) + '/' + str(len(VECTORS_VOCAB)))


if __name__ == '__main__':
    num_args = 5
    if len(argv) == num_args:
        lexicon_file, vectors_file, outside_vec, in_vec = argv[1:5]
        load_lexv(lexicon_file)
        load_vecv(vectors_file)
        compare_vocabs(in_vec, outside_vec)
    else:
        print("Expected " + str(num_args) + " arguments.  Got " +
              str(len(argv)))

