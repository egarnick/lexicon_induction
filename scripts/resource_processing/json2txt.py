from sys import argv
import json


VOCABULARY = {}     # {word : [ct, {ctx1 : ct, ctx2 : ct, ...}], ...}


def load_json(json_f):
    global VOCABULARY
    with open(json_f, 'r') as json_in:
        VOCABULARY = json.load(json_in)


def dump_counts(outfile_name):
    # word \t count \t context_word,ctxt_count \t ...
    with open(outfile_name, 'w') as lm_out:
        for word in VOCABULARY:
            cnt_ctxt = VOCABULARY[word]
            line_out = word + '\t' + str(cnt_ctxt[0])
            contexts = cnt_ctxt[1]
            for ctx_tok in contexts:
                line_out += '\t' + ctx_tok + ',' + str(contexts[ctx_tok])
            lm_out.write(line_out + '\n')


if __name__ == '__main__':
    num_args = 3
    if len(argv) == num_args:
        json_file, dest_file = argv[1:num_args]
        load_json(json_file)
        dump_counts(dest_file)
    else:
        print("Wrong number of arguments")
