from sys import argv
from Zipped import Zipped


if __name__ == '__main__':
    num_args = 3
    if len(argv) == num_args:
        target_file = argv[2]
        z_obj = Zipped(argv[1])
        z_obj.vec2vocab(target_file)
    else:
        print("Input zipfile path as first arg, target file as second arg.")
