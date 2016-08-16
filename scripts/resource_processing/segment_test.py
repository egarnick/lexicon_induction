from sys import argv
import morfessor

"""
Segment test list and output vocabulary size
"""


SEG_DICT = {}       # {segment: {'mono': ct, 'mult': ct}, ...}
MORF_MODEL = None


def load_morf_model(morf_model_file):
    global MORF_MODEL
    MORF_MODEL = morfessor.MorfessorIO()\
        .read_binary_model_file(morf_model_file)


def load_segments(seg_file):
    global SEG_DICT
    for line in open(seg_file, 'r'):
        line_split = line.strip().split('\t')
        SEG_DICT[line_split[0]] = {line_split[1]: int(line_split[2]),
                                   line_split[3]: int(line_split[4])}


def morfed_root(tkn_morfed):
    """
    Return segment with highest mono/mult ratio, or the first novel segment
    :param tkn_morfed: list: segmented token
    :return: string: proposed root
    """
    if len(tkn_morfed) == 1:
        return tkn_morfed[0]
    else:
        max_mono = -1.0
        argmax_mono = ""
        for seg in tkn_morfed:
            try:
                mono_mult = SEG_DICT[seg]
                try:
                    mono_ratio = mono_mult['mono'] / mono_mult['mult']
                # Never seen with other morphology
                except ZeroDivisionError:
                    return seg
                if mono_ratio > max_mono:
                    max_mono = mono_ratio
                    argmax_mono = seg
            # Novel terms are open class
            except KeyError:
                return seg
        return argmax_mono


def morf_test(test_file):
    morfed_dict = {}
    for line in open(test_file, 'r'):
        tkn = line.strip().split('\t')[0]
        tk_morfed = MORF_MODEL.viterbi_segment(tkn)[0]
        root = morfed_root(tk_morfed)
        morfed_dict[root] = True
    return morfed_dict


if __name__ == '__main__':
    num_args = 4
    if len(argv) == num_args:
        test_list, morf_model, seg_counts = argv[1:num_args]
        load_morf_model(morf_model)
        print("Loaded morfessor model")
        load_segments(seg_counts)
        print("Loaded segment counts")
        morfed_test = morf_test(test_list)
        print("Morfed roots count: " + str(len(morfed_test)))
    else:
        print("Wrong number of arguments")

