from sys import argv


def mwe_ratio(vocab):
    mwe_count = 0
    total_lines = 0
    for line in open(vocab, 'r'):
        total_lines += 1
        if len(line.strip().split()) > 1:
            mwe_count += 1
    print("MWE count: " + str(mwe_count))
    print("Total type count: " + str(total_lines))
    print("Ratio of MWEs to total type count: " + str(mwe_count / total_lines))


if __name__ == '__main__':
    num_args = 2
    if len(argv) == num_args:
        vocab_file = argv[1]
        mwe_ratio(vocab_file)
    else:
        print("Requires 1 argument: vocabulary file")
