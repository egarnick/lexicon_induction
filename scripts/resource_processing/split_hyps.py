from sys import argv
from math import ceil
import split_text
from split_text import split_file


if __name__ == '__main__':
    num_args = 5
    if len(argv) == num_args:
        infile, outfile, file_length, num_splits = argv[1:num_args]
        lines_left = int(file_length)
        splits_left = int(num_splits)
        cur_div = 0
        while splits_left:
            split_len = ceil(lines_left / splits_left)
            next_start = int(file_length) - lines_left
            print("Starting at " + str(next_start))
            print("Writing " + str(split_len) + " lines")
            outfile_name = outfile + '-' + str(file_length) + '.' + \
                           str(cur_div) + '.div'
            split_file(infile, outfile_name, next_start, split_len)
            lines_left -= split_len
            splits_left -= 1
            cur_div += 1
    else:
        print("Wrong number of arguments")

