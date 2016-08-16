from sys import argv

"""
Rewrite translation file so that correct translations appear first in the list
of translation hypotheses.  Inputs: original translations, correct translations
file, output name
"""


def correct_translations(correct_file):
    correct_dict = {}           # {uzb: {'trans': <trans>, 'pos': <position>}}
    for line in open(correct_file, 'r'):
        line_split = line.strip().split()
        correct_dict[line_split[0]] = \
            {'trans': line_split[1], 'idx': int(line_split[2])}
    return correct_dict


def reorder_translations(original_file, correct_dict, destination):
    with open(destination, 'w') as reord_out:
        for line in open(original_file, 'r'):
            uzb, hyp_list = line.strip().split('\t')
            hyps = hyp_list.split(';')
            if correct_dict.get(uzb):
                target_idx = correct_dict[uzb]['idx']
                reordered = [hyps[target_idx]] + \
                            hyps[:target_idx] + \
                            hyps[target_idx + 1:]
            else:
                reordered = hyps
            reord_out.write(uzb + '\t' + ';'.join(reordered) + '\n')


if __name__ == '__main__':
    num_args = 4
    if len(argv) == num_args:
        trans_orig, trans_correct, reordered_out = argv[1:num_args]
        correct = correct_translations(trans_correct)
        reorder_translations(trans_orig, correct, reordered_out)
    else:
        print("Wrong number of arguments")
