from sys import argv
from glob import glob


def fjoin(target_files):
    joined = []
    for t_file in target_files:
        for t_line in open(t_file, 'r'):
            joined.append(t_line)
    print("Joined " + str(len(joined)) + " lines")
    return joined


if __name__ == '__main__':
    num_args = 3
    if len(argv) == num_args:
        in_dir, out_file = argv[1:num_args]
        in_files = in_dir + '/*' if in_dir[-1] != '/' else in_dir + '*'
        files = glob(in_files)
        all_joined = fjoin(files)
        write_count = 0
        with open(out_file, 'w') as joined_out:
            for j_line in all_joined:
                joined_out.write(j_line)
                write_count += 1
        print("Wrote " + str(write_count) + " lines")
