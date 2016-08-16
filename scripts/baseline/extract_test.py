from sys import argv

"""
Given name of test data file, extract 4th column of words and save in output.
"""


def extract_words(test_f, out_f):
    test_words = {}
    line_idx = 0
    for line in open(test_f, 'r'):
        test_word = line.strip().split('\t')[3]
        try:
            test_words[test_word].append(line_idx)
        except KeyError:
            test_words[test_word] = [line_idx]
        line_idx += 1

    with open(out_f, 'w') as test_out:
        for word in test_words:
            test_out.write(word + '\t' + str(test_words[word]) + '\n')


if __name__ == '__main__':
    num_args = 3
    if len(argv) == num_args:
        test_file, output_file = argv[1:num_args]
        extract_words(test_file, output_file)
