from sys import argv


def load_test(test_file):
    test_orig = []                  # [(uzb, eng), ...]
    for line in open(test_file, 'r'):
        line_split = line.strip().split()
        test_orig.append((line_split[3].lower(), line_split[5].lower()))
    print("Loaded original " + str(len(test_orig)) + " translation pairs")
    return test_orig


def order_trans(test_orig, trans_file):
    """
    Add translations to test_orig
    :param test_orig:
    :param trans_file:
    :return:
    """
    # Fill translation hypotheses
    trans_count = 0
    for line in open(trans_file, 'r'):
        line_split = line.strip().split('\t')
        uzb = line_split[0]
        eng_hyps = [pair.split(',')[0] for pair in line_split[1].split(';')]
        for idx in range(len(test_orig)):
            if test_orig[idx][0] == uzb and test_orig[idx][1] in eng_hyps:
                test_orig[idx] = line.strip()
                trans_count += 1
    print("Ordered " + str(trans_count) + " translations")


def dump_ordered(ordered_data, dest):
    with open(dest, 'w') as data_out:
        for line in ordered_data:
            if type(line) == str:
                data_out.write(line + '\n')
            else:
                data_out.write(line[0] + '\t_UNK,0\n')
    print("Wrote " + str(len(ordered_data)) + " translations")


if __name__ == '__main__':
    num_args = 4
    if len(argv) == num_args:
        translations, test_list, output = argv[1:num_args]
        test_data = load_test(test_list)
        order_trans(test_data, translations)
        dump_ordered(test_data, output)
    else:
        print("Wrong number of arguments")
