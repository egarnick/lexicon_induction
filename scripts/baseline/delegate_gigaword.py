from sys import argv
import os
from glob import glob


def split_files(path2data, num_divs):
    divisions = []
    for div_num in range(num_divs):
        divisions.append([])
        for corp_dir in glob(path2data + '/*'):
            corp_dir_contents = sorted(glob(corp_dir + '/*.gz'))
            div_length = len(corp_dir_contents) // num_divs
            if div_num < len(corp_dir_contents) % num_divs:
                div_length += 1
                first_file_idx = div_num * div_length
            else:
                first_file_idx = div_num * div_length + \
                                 len(corp_dir_contents) % num_divs
            divisions[div_num] += \
                corp_dir_contents[first_file_idx:first_file_idx + div_length]
    return divisions


def dump_divisions(divisions, destination):
    for div_num in range(len(divisions)):
        os.system('mkdir ' + destination + '/' + str(div_num))
        for file_name in divisions[div_num]:
            os.system('ln -s ' + file_name + ' ' +
                      destination + '/' + str(div_num) + '/' +
                      file_name.split('/')[-1])


if __name__ == '__main__':
    num_args = 4
    if len(argv) == num_args:
        data_dir, num_divisions, output_dir = argv[1:num_args]
        dir_divs = split_files(data_dir, int(num_divisions))
        dump_divisions(dir_divs, output_dir)
    else:
        print("Wrong number of arguments.")
