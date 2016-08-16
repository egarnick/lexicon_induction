from sys import argv
from nltk.metrics import distance


def cognate_rate(trans_file):
    cognate_ct = 0
    translations_ct = 0
    for line in open(trans_file, 'r'):
        translations_ct += 1
        uzb, eng = line.strip().split()[:2]
        if distance.edit_distance(uzb, eng) <= 2:
            cognate_ct += 1
    print("Total cognates: " + str(cognate_ct))
    print("Total translations: " + str(translations_ct))


if __name__ == '__main__':
    num_args = 2
    if len(argv) == num_args:
        translation_file = argv[1]
        cognate_rate(translation_file)
    else:
        print("Incorrect number of arguments")
