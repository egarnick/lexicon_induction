from sys import argv


def count_uniques(trans_file):
    translations = {}
    trans_count = 0
    for line in open(trans_file, 'r'):
        trans_count += 1
        uzb, eng, psn = line.strip().split()
        try:
            translations[uzb].append(eng)
        except KeyError:
            translations[uzb] = [eng]

    print("Unique Uzbek words: " + str(len(translations)))
    print("Total translations: " + str(trans_count))


if __name__ == '__main__':
    num_args = 2
    if len(argv) == num_args:
        scored_trans = argv[1]
        count_uniques(scored_trans)
    else:
        print("Wrong number of arguments")
