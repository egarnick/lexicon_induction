from sys import argv


def load_hyps(trans_file):
    hyps = {}
    for line in open(trans_file, 'r'):
        uzb, eng = line.strip().split()
        for pair in eng.split(';'):
            eng = pair.split(',')[0]
            try:
                hyps[eng] += 1
            except KeyError:
                hyps[eng] = 1

    print("Total unique hypotheses: " + str(len(hyps)))
    print("Total summed hypotheses: " + str(sum(hyps.values())))

    return hyps


def write_top_n(hyps, n, dest):
    hyps_sorted = sorted([(trans, hyps[trans]) for trans in hyps],
                         key=lambda pair: pair[1], reverse=True)
    print("Translation count for top " + str(n) + " : " +
          str(sum(pair[1] for pair in hyps_sorted[:n])))

    write_count = 0
    with open(dest, 'w') as top_n_out:
        for top_trans in hyps_sorted[:n]:
            top_n_out.write(top_trans[0] + '\n')
            write_count += 1

    print("Wrote top " + str(write_count) + " translations to " + dest)


if __name__ == '__main__':
    num_args = 3
    if len(argv) == num_args:
        raw_trans_file, en = argv[1:num_args]
        hypotheses = load_hyps(raw_trans_file)
        in_split = raw_trans_file.split('.', 1)
        output_name = in_split[0] + '-top' + en + '.' + in_split[1]
        write_top_n(hypotheses, int(en), output_name)
    else:
        print("Wrong number of arguments")
