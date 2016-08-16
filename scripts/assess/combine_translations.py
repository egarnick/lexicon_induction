from sys import argv


def extract_translations(t_file):
    t_dict = {}                     # {word: {hyp: score, ...}, ...}
    for line in open(t_file, 'r'):
        word, translations = line.strip().split('\t')
        t_dict[word] = {}
        for hyp_score in translations.split(';'):
            hyp, score = hyp_score.split(',')
            t_dict[word][hyp] = float(score)
    print("Extracted " + str(len(t_dict)) + " translations")
    return t_dict


def merge_translations(hyps1, hyps2):
    merged = {}
    for hyp in hyps1:
        try:
            merged[hyp] = (hyps1[hyp] + hyps2[hyp]) / 2
        except KeyError:
            merged[hyp] = hyps1[hyp]
    for hyp in hyps2:
        if not merged.get(hyp):
            try:
                merged[hyp] = (hyps1[hyp] + hyps2[hyp]) / 2
            except KeyError:
                merged[hyp] = hyps2[hyp]
    return dict(sorted([(hyp, merged[hyp]) for hyp in merged],
                       key=lambda pair: pair[1], reverse=True)[:50])


def combine_translations(translations1, translations2):
    t_all = {}
    t1 = extract_translations(translations1)
    t2 = extract_translations(translations2)
    for word in t1:
        try:
            t_all[word] = merge_translations(t1[word], t2[word])
        except KeyError:
            t_all[word] = t1[word]
    for word in t2:
        if not t_all.get(word):
            try:
                t_all[word] = merge_translations(t1[word], t2[word])
            except KeyError:
                t_all[word] = t2[word]
    print("Combined translations: " + str(len(t_all)))
    return t_all


def dump_combined(combined, output):
    with open(output, 'w') as combined_out:
        for word in combined:
            line_out = word + '\t'
            for hyp in combined[word]:
                line_out += hyp + ',' + str(combined[word][hyp]) + ';'
            line_out = line_out[:-1] + '\n'
            combined_out.write(line_out)


if __name__ == '__main__':
    num_args = 4
    if len(argv) == num_args:
        trans1, trans2, out_file = argv[1:num_args]
        trans_combined = combine_translations(trans1, trans2)
        dump_combined(trans_combined, out_file)
