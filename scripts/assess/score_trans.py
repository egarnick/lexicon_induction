from sys import argv


GOLD_TRANS = {}         # {uzb1: [eng1a, eng1b, ...], ...}


def load_gold(gs):
    global GOLD_TRANS
    for line in open(gs, 'r'):
        line_split = line.strip().split('\t')
        uzb = line_split[3].lower()
        try:
            GOLD_TRANS[uzb].append(line_split[5].lower())
        except KeyError:
            GOLD_TRANS[uzb] = [line_split[5].lower()]
    print("Total gold translations: " + str(len(GOLD_TRANS)))


def score_translations(trans_file):
    trans_count = 0
    for line in open(trans_file, 'r'):
        found_trans = False
        # try:
        uzb, trans_cands = line.split('\t')
        # except ValueError:
        #     print("BLANK: " + str([repr(char) for char in line]))
        #     return
        uzb = uzb.lower()
        trans_cands = [trans_cand.split(',')[0] for trans_cand in
                       trans_cands.split(';')]
        for tc_idx in range(len(trans_cands)):
            tc = trans_cands[tc_idx].lower()
            if tc in GOLD_TRANS[uzb]:
                found_trans = True
                print(uzb, tc, tc_idx)
        if found_trans:
            trans_count += 1
    print("Correctly translated words: " + str(trans_count))


if __name__ == '__main__':
    num_args = 3
    if len(argv) == num_args:
        gold_file, translations = argv[1:num_args]
        load_gold(gold_file)
        score_translations(translations)
