from sys import argv


def split_file(text_in, text_out, start, n_lines):
    line_count = 0
    write_count = 0
    with open(text_out, 'w') as of:
        for line in open(text_in, 'r'):
            if line_count >= start:
                if line_count - start < n_lines:
                    of.write(line)
                    write_count += 1
                else:
                    break
            line_count += 1
    print("Wrote " + str(write_count) + " lines")
    return


if __name__ == '__main__':
    num_args = 5
    if len(argv) == num_args:
        infile, outfile, start_idx, num_lines = argv[1:num_args]
        split_file(infile, outfile, int(start_idx), int(num_lines))
    else:
        print("Wrong number of arguments")
