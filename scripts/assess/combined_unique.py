from sys import argv


def load_trans(trans_file):
    trans_dict = {}
    for line in open(trans_file):
        uzb, eng = line.strip().split()[:2]
        try:
            if eng not in trans_dict[uzb]:
                trans_dict[uzb].append(eng)
        except KeyError:
            trans_dict[uzb] = [eng]
    return trans_dict


def combine_dicts(d_whole, d_part):
    for uzb in d_part:
        if d_whole.get(uzb):
            for trans in d_part[uzb]:
                if trans not in d_whole[uzb]:
                    d_whole[uzb].append(trans)
        else:
            d_whole[uzb] = d_part[uzb]


def combined_unique(file1, file2):
    trans_1 = load_trans(file1)
    trans_2 = load_trans(file2)
    trans_c = {}
    combine_dicts(trans_c, trans_1)
    combine_dicts(trans_c, trans_2)
    # print("Combined Uzbek words translated: " + str(len(trans_c)))
    # print("Total combined translations: " +
    #       str(sum(len(val) for val in trans_c.values())))
    dump_combined(trans_c)


def dump_combined(combined):
    for uzb in combined:
        for eng in combined[uzb]:
            print(uzb + ' ' + eng)


if __name__ == '__main__':
    num_args = 3
    if len(argv) == num_args:
        scored1, scored2 = argv[1:num_args]
        combined_unique(scored1, scored2)
    else:
        print("Wrong number of arguments")
