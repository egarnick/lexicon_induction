from sys import argv
from glob import glob


def directory_contents(src_dir, extension):
    """
    Return list of everything in src_dir ending with given extension
    :param src_dir: string: name of source directory
    :param extension: string: optional file extension
    :return: list: path+name to all files in src_dir with given extension
    """
    path = src_dir if src_dir[-1] == '/' else src_dir + '/'
    return glob(path + '*' + extension)


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
    num_args = [3, 4]
    if len(argv) in num_args:
        source_dir, output_file = argv[1:3]
        ext = ""
        if len(argv) == 4:
            ext = argv[3]
        print("Copied: " +
              str(concat_files(output_file,
                               directory_contents(source_dir, ext))) +
              " lines")
    else:
        print("Expected " + str(num_args[0]) + " or " + str(num_args[1]) +
              " arguments.  Got " + str(len(argv)))
