from sys import argv
from Zipped import Zipped


if __name__ == '__main__':
    num_args = 2
    if len(argv) == num_args:
        z_obj = Zipped(argv[1])
        for content_file in z_obj.ls():
            print(content_file)
    else:
        print("Input zipfile path as first argument.")
