from sys import argv


"""
Input whitespace separated text, determine number of unique types, write a
vocab file and print number of types
"""


def make_vocab(text_file):
    vocab = {}
    for line in open(text_file, 'r'):
        for token in line.strip().split():
            try:
                vocab[token] += 1
            except KeyError:
                vocab[token] = 1
    return vocab


def write_vocab(vocabulary, vocab_dest):
    with open(vocab_dest, 'w') as vocab_out:
        for token in vocabulary:
            vocab_out.write(token + '\t' + str(vocabulary[token]) + '\n')
    print("Total vocab count: " + str(len(vocabulary)))


if __name__ == '__main__':
    num_args = 3
    if len(argv) == num_args:
        input_text, vocab_out_file = argv[1:3]
        vocab = make_vocab(input_text)
        write_vocab(vocab, vocab_out_file)
    else:
        print("Expected args: input_text vocab_output")
