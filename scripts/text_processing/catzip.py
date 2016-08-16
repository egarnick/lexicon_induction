from sys import argv
from Zipped import Zipped


if __name__ == '__main__':
    num_args = 3
    if len(argv) == num_args or len(argv) == num_args - 1:
        target_file = "" if len(argv) == 2 else argv[2]
        z_obj = Zipped(argv[1])
        # print(str(z_obj.filesize(target_file)))
        for line in z_obj.cat(target_file):
            print(line, end='')
    else:
        print("Input zipfile path as first arg, target file as second arg.")
