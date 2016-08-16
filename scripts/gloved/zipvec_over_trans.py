from sys import argv
from zipfile import ZipFile

"""
Input zipped directory name, GloVe file name and uzb-eng translation file
"""

TOP_N = 200

VEC_VOC = {}
TXT_VOC = {}
TXT_ONLY = []


def loadvec(directory, target_file):
    global VEC_VOC
    tok_count = 0
    with ZipFile(directory) as zip_open:
        content_files = zip_open.namelist()
        print("Zipdir contents: " + str(content_files))
        if target_file not in content_files:
            print(target_file + " not found in " + directory)
        for line in zip_open.open(target_file):
            VEC_VOC[line.split()[0]] = True
            tok_count += 1
    print("Loaded " + str(len(VEC_VOC)) + " words from GloVe file")


def loadtxt(text_file):
    global TXT_VOC
    tok_count = 0
    for line in open(text_file):
        hyp_vec = line.strip().split('\t')[1]
        for word in [pair.split(',')[0] for pair in hyp_vec.split(';')]:
            try:
                TXT_VOC[word] += 1
            except KeyError:
                TXT_VOC[word] = 1
            tok_count += 1
    print("Loaded " + str(len(TXT_VOC)) + " types, " +
          str(tok_count) + " tokens from txt file")


def dump_common():
    tvoc_list = sorted([(word, TXT_VOC[word]) for word in TXT_VOC],
                       key=lambda pair: pair[1], reverse=True)
    print(str(trans_hyps) + " most common translations:")
    for trans in tvoc_list[:TOP_N]:
        print(trans)
    print("Account for: " + str(sum(pair[1] for pair in tvoc_list[:200])) + " translations")


def compare_vocab():
    txt_only_voc = []
    overlap_ct = 0
    for word in TXT_VOC:
        if not VEC_VOC.get(word):
            overlap_ct += 1
        else:
            txt_only_voc.append(word)
    print("Overlap: " + str(overlap_ct))
    print("Not in vectors: " + str(len(txt_only_voc)))
    return txt_only_voc


def dump_uncovered(t_only, dest):
    with open(dest, 'w') as diff_out:
        for word in sorted(t_only):
            diff_out.write(word + '\n')


if __name__ == '__main__':
    num_args = 5
    if len(argv) == num_args:
        zipdir, glovefile, trans_hyps, txt_only_file = argv[1:num_args]
        # loadvec(zipdir, glovefile)
        loadtxt(trans_hyps)
        dump_common()
        # t_only_voc = compare_vocab()
        # dump_uncovered(t_only_voc, txt_only_file)
    else:
        print("Wrong number of arguments")

