from sys import argv
from math import ceil


def read_file(input_file):
    input_text = []
    for line in open(input_file, 'r'):
        input_text.append(line.strip())
    return input_text


def split_text(text, splits, input_name, dest):
        for split_num in range(splits):
            in_split = input_name.split('/')[-1].rsplit('.', 1)
            if dest[-1] != '/':
                dest += '/'
            output_name = dest + \
                          '.'.join([in_split[0], str(split_num), in_split[1]])
            num_lines = ceil(len(text) / splits)
            with open(output_name, 'w') as split_out:
                for line in text[:num_lines]:
                    split_out.write(line + '\n')
            text = text[num_lines:]
            splits -= 1


if __name__ == '__main__':
    num_args = 4
    if len(argv) == num_args:
        text_file, num_splits, dest_dir = argv[1:num_args]
        file_text = read_file(text_file)
        split_text(file_text, int(num_splits), text_file, dest_dir)
    else:
        print("Wrong number of arguments")
