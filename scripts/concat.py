from sys import argv


def handle_input():
    """
    Check for valid number and type of input args
    :return: True when all args are good, otherwise False
    """
    in_args = argv
    while len(in_args) < 3:
        in_args = input("Enter output_file followed by list of input files\n").split()
        in_args.insert(0, 0)
    for f_name in in_args[2:]:
        try:
            in_file = open(f_name, 'r')
            in_file.close()
        except FileNotFoundError:
            print("Could not find file: " + f_name)
            return []
    return in_args[1:]


def concat_files(output_name, input_names_arr):
    """
    Write all input files concatenated to output file
    :param output_name: string: desired name of output file
    :param input_names_arr: list of input train files
    :return number of lines written
    """
    lines_written = 0
    with open(output_name, 'w') as out_file:
        for in_name in input_names_arr:
            with open(in_name, 'r') as train_in:
                for line in train_in:
                    lines_written += 1
                    out_file.write(line)
    return lines_written


if __name__ == '__main__':
    good_args = []
    while not len(good_args):
        good_args = handle_input()
    catted = good_args[0]
    train_files = good_args[1:]
    print("Copied: " + str(concat_files(catted, train_files)) + " lines")
