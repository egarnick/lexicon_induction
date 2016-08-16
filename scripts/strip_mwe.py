from sys import argv


def rewrite_vocab(in_file, out_file):
    old_vocab_count = 0
    new_vocab_count = 0
    with open(out_file, 'w') as vocab_out:
        for line in open(in_file, 'r'):
            old_vocab_count += 1
            if len(line.strip().split()) == 1:
                vocab_out.write(line)
                new_vocab_count += 1
    print("Old vocab length: " + str(old_vocab_count))
    print("New vocab length: " + str(new_vocab_count))


if __name__ == '__main__':
    num_args = 3
    if len(argv) == num_args:
        orig_vocab, strp_vocab = argv[1:3]
        rewrite_vocab(orig_vocab, strp_vocab)
    else:
        print("Expecting arguments: orig_vocab_in new_vocab_out")
