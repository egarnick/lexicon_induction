from sys import argv
import matplotlib.pyplot as plt
import json


VOCABULARY = {}         # {seg: ct, ...}
VOC_SORTED = []         # [(seg, ct), ...]
COUNTS_OF_COUNTS = []   # [(ct, cofc), ...]


def create_vocab(morfed):
    for line in open(morfed, 'r'):
        segs = line.strip().split()
        for seg in segs:
            try:
                VOCABULARY[seg] += 1
            except KeyError:
                VOCABULARY[seg] = 1


def sort_voc():
    global VOC_SORTED
    VOC_SORTED = sorted([(seg, VOCABULARY[seg]) for seg in VOCABULARY],
                        key=lambda pair: pair[1])


def counts_of_counts(load=None):
    global COUNTS_OF_COUNTS
    if load:
        with open(load, 'r') as data_in:
            COUNTS_OF_COUNTS = json.load(data_in)
    else:
        cofc_dict = {}
        for pair in VOC_SORTED:
            try:
                cofc_dict[pair[1]] += 1
            except KeyError:
                cofc_dict[pair[1]] = 1
        COUNTS_OF_COUNTS = sorted([(ct, cofc_dict[ct]) for ct in cofc_dict],
                                  key=lambda cpair: cpair[1])


def plotting(data_sel):
    if data_sel == 'cofc':
        cts = [p[0] for p in COUNTS_OF_COUNTS]
        print(str(cts[-10:]))
        cofcs = [p[1] for p in COUNTS_OF_COUNTS]
        print(str(cofcs[-10:]))
        plt.plot(cts, cofcs, 'ro')
        plt.axis([0, 100 * 1.1, 0, 5100])
        plt.show()
    elif data_sel == 'test':
        xs = [1, 2, 3, 4]
        ys = [10, 20, 30, 40]
        plt.plot(xs, ys, 'ro')
        plt.axis([0, max(xs) * 1.1, 0, max(ys) * 1.1])
        plt.show()


def dump_data(data_sel, dump_dest):
    if data_sel == 'cofc':
        with open(dump_dest, 'w') as data_out:
            json.dump(COUNTS_OF_COUNTS, data_out)


if __name__ == '__main__':
    num_args = 4
    if len(argv) == num_args:
        morfed_text, dump_file, load_file = argv[1:num_args]
        if load_file == 'none':
            create_vocab(morfed_text)
            sort_voc()
            counts_of_counts()
            dump_data('cofc', dump_file)
        else:
            counts_of_counts(load_file)
            print(str(COUNTS_OF_COUNTS[-1]))
            plotting('cofc')
    else:
        print("Wrong number of args")
