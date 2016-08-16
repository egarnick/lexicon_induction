from sys import argv


VOCABULARY = {}


def count_types(data_file):
    for line in open(data_file, 'r'):
        for token in line.strip().split():
            VOCABULARY[token] = True
    print("Total number of types: ")
    print(str(len(VOCABULARY)))


if __name__ == '__main__':
    num_args = 2
    if len(argv) == num_args:
        text_file = argv[1]
        count_types(text_file)
    else:
        print("Expected " + str(num_args) + " arguments.  Got " +
              str(len(argv)))
