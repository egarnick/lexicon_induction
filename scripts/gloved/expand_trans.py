from sys import argv
from zipfile import ZipFile
from math import *
import re

"""
Rewrite input file with expanded translation hypotheses based on GloVe wordvec
"""

EN = 5
SIM_CACHE = {}              # {word: {sim_word1: sim_score1, ...}}
VECTORS = {}                # {word: (sqrtd, [feat1, feat2, ...]), ...}


def loadvec(directory, target_file):
    """
    Load word vectors file in VECTORS dict
    :param directory: string: zipped directory of vector files
    :param target_file: string: name of vector file in zipped directory
    """
    global VECTORS

    # For testing
    tok_count = 0

    with ZipFile(directory) as zip_open:
        content_files = zip_open.namelist()
        print("Zipdir contents: " + str(content_files))
        if target_file not in content_files:
            print(target_file + " not found in " + directory)
        for line in zip_open.open(target_file):
            line_split = line.strip().split()
            word = line_split[0].decode('utf-8')
            vector = [float(feat.decode('utf-8')) for feat in line_split[1:]]
            # Cache sqrtd to save computation later
            VECTORS[word] = (square_rooted(vector), vector)
            tok_count += 1
    print("Loaded " + str(len(VECTORS)) + " word vectors from GloVe file")


def load_cache(sim_cache):
    global SIM_CACHE
    for line in open(sim_cache):
        try:
            cache_word, cache_sims = line.strip().split('\t')
        except ValueError:
            continue
        SIM_CACHE[cache_word] = {}
        for pair in cache_sims.split(';'):
            sim_w, sim_s = pair.rsplit(',', 1)
            SIM_CACHE[cache_word][sim_w] = float(sim_s)
    print("Loaded " + str(len(SIM_CACHE)) + " cached expansions")


def square_rooted(x):
    return sqrt(sum([a*a for a in x]))


def cosine_similarity(x_pair, y_pair):
    numerator = sum(a * b for a, b in zip(x_pair[1], y_pair[1]))
    denominator = x_pair[0] * y_pair[0]
    return numerator/float(denominator)


def compare_vecs(w1, w2):
    print("Similarity of " + w1 + ' ' + w2 + ": " +
          str(cosine_similarity(VECTORS[w1], VECTORS[w2])))


def worst_kv(d):
    worst_v = min(d.values())
    for k in d:
        if d[k] == worst_v:
            return k, worst_v


def update_min_best(best_dict, new_word, new_score):
    best_dict[new_word] = new_score
    if len(best_dict) > EN:
        best_dict.pop(worst_kv(best_dict)[0])
    return worst_kv(best_dict)[1]


def most_similar(query, q_score):
    """
    Return dictionary of N words most similar to query with their sim scores
    :param query: string: target word to find similar terms
    :param q_score: float: original translation score for query
    :return: dict: most similar n words with sim scores
    """
    print("Expanding: " + query)
    query = re.sub(r'\'s', '', query)
    # Check if cached
    try:
        bestn = SIM_CACHE[query]
    # Calculate new
    except KeyError:
        try:
            q_vec = VECTORS[query.lower()]
            bestn = {"": 0}
            min_best_sim = 0
            for word in VECTORS:
                if word != query and word not in \
                        ['\'', '\"', '\\', '/', '.', ',', ';',
                         ':', '?', '!', ')', '(', '-', '–']:
                    cos_sim = cosine_similarity(q_vec, VECTORS[word])
                    if cos_sim > min_best_sim:
                        min_best_sim = update_min_best(bestn, word, cos_sim)
        # query not in vectors
        except KeyError:
            bestn = {}
    # Adjust similarities by original query translation score
    for new_w in bestn:
        bestn[new_w] *= q_score
    return bestn


def load_eng_c(trans_file):
    trans_init = {}             # initial translations:
                                # {eng: {sim_word1: sim_score1, ...}}
    for line in open(trans_file, 'r'):
        eng = line.strip()
        trans_init[eng] = {}
    return trans_init


def load_eng_t(trans_file):
    trans_init = {}             # initial translations:
                                # {uzb: {trans1: score1, ...}}
    for line in open(trans_file, 'r'):
        uzb, hyps = line.strip().split('\t')
        trans_init[uzb] = {}
        trans_hyps = [pair.split(',') for pair in hyps.split(';')]
        for pair in trans_hyps:
            trans_init[uzb][pair[0]] = float(pair[1])
    return trans_init


def expand_translations_c(initials, res_file):
    """
    Rewrite trans_file with expanded translation hypotheses to res_file
    :param initials: dict: initial English words to expand
            {eng: {sim_word1: sim_score1, ...}}
    :param res_file: string: name of destination to write expanded translations
    """
    # Expand translations
    with open(res_file, 'w') as expanded_out:
        for eng_word in initials:
            exp_dict = most_similar(eng_word, 1)
            output_line = eng_word + '\t'
            eng_exp_sorted = sorted([eng_exp + ',' + str(exp_dict[eng_exp])
                                     for eng_exp in exp_dict],
                                    key=lambda pair: pair.split(',')[1],
                                    reverse=True)
            output_line += ';'.join(eng_exp_sorted) + '\n'
            expanded_out.write(output_line)


def expand_translations_t(trans_init, res_file):
    """
    Rewrite trans_file with expanded translation hypotheses to res_file
    :param trans_init: dict: {uzb: {trans1: score1, ...}}
    :param res_file: string: name of destination to write expanded translations
    """
    # Expand translations
    write_count = 0
    extra_translations = 0
    with open(res_file, 'w') as expanded_out:
        for uzb_word in trans_init:
            trans_expanded = {}
            hyps_init = trans_init[uzb_word]
            for hyp in hyps_init:
                hyp_score = hyps_init[hyp]
                # Save initial translation hypothesis
                trans_expanded[hyp] = hyp_score
                new_hyps = most_similar(hyp, hyp_score)
                # Add new hypotheses using highest similarity score
                for new_hyp in new_hyps:
                    try:
                        trans_expanded[new_hyp] = max(new_hyps[new_hyp],
                                                      trans_expanded[new_hyp])
                    except KeyError:
                        trans_expanded[new_hyp] = new_hyps[new_hyp]
            output_line = uzb_word + '\t'
            trans_ex_sorted = sorted([t_hyp + ',' + str(trans_expanded[t_hyp]) for
                                      t_hyp in trans_expanded],
                                     key=lambda pair: pair.split(',')[1], reverse=True)
            output_line += ';'.join(trans_ex_sorted) + '\n'
            expanded_out.write(output_line)
            write_count += 1
            extra_translations += len(trans_expanded)
    print("Wrote " + str(extra_translations) + " extra translations")
    print("in " + str(write_count) + " lines")
    print("to " + res_file)


if __name__ == '__main__':
    num_args = 6
    if len(argv) == num_args:
        # Arguments:
        # zipdir - path to zipped directory with word vector files
        # vec_file - name of vector file in zipdir
        # translations - original translations file
        # expanded - output file for expanded translations
        # cache - [yes|y] | cache_file
        zipdir, vec_file, translations, out_dir, cache = argv[1:num_args]
        out_dir += '/' if out_dir[-1] != '/' else ''
        outfile_dest = out_dir + translations.split('/')[-1] + '.expanded'
        loadvec(zipdir, vec_file)
        if cache in ['yes', 'y']:
            eng_init = load_eng_c(translations)
            expand_translations_c(eng_init, outfile_dest)
        else:
            load_cache(cache)
            eng_init = load_eng_t(translations)
            print("Loaded " + str(len(eng_init)) + " initial translations")
            expand_translations_t(eng_init, outfile_dest)
    else:
        print("Wrong number of arguments")
