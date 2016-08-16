from sys import argv
from glob import glob

from Zipped import Zipped


"""
Given a directory containing zipped files, create groups of files and write
each group to individual output files.  Prepares data for parallel processing.
"""


NUM_GROUPS = 11
ZIPFILE_GROUPS = []


class ZipfileGroup:
    def __init__(self, size=0):
        self.size = size
        self.zipfiles = []

    def add_file(self, file_name, file_size):
        self.zipfiles.append(file_name)
        self.size += file_size


def set_divisions(num_divs):
    global NUM_GROUPS
    NUM_GROUPS = num_divs


def init_zfile_groups():
    while len(ZIPFILE_GROUPS) < NUM_GROUPS:
        ZIPFILE_GROUPS.append(ZipfileGroup())


def delegate(zf_list):
    num_files = 0
    # For each zipped directory
    for zf in zf_list:
        # print("New z_obj")
        z_obj = Zipped(zf)
        # For each xml file in the zipped directory
        content_files = z_obj.ls()
        for content_file in content_files:
            if content_file[-4:] == '.xml':
                num_files += 1
                # print("Next content file")
                shortest = min(ZIPFILE_GROUPS, key=lambda zfg: len(zfg.zipfiles))
                # print("found min group")
                shortest.add_file(content_file, 0)
                # print("found file size")
    print("Delegated " + str(num_files) + " files")


if __name__ == '__main__':
    num_args = 4
    if len(argv) == num_args:
        # Arguments:
        # zipfilesdirectory - contains zipped folders of xml files (i.e. data/)
        # outputfile - general name for output to be appended with '.<num>.div'
        #              for each division file
        # numberofdivisions - desired number of divisions of resources
        zipfilesdirectory, outputfile, numberofdivisions = argv[1:4]
        set_divisions(int(numberofdivisions))
        init_zfile_groups()
        zf_dir = zipfilesdirectory + '*' if \
            zipfilesdirectory[-1] == '/' else zipfilesdirectory + '/*'
        zfiles = glob(zf_dir)
        delegate(zfiles)
        div_number = -1
        for group in ZIPFILE_GROUPS:
            div_number += 1
            with open('.'.join([outputfile, str(div_number), 'div']), 'w') as \
                    groups_out:
                for filename in sorted(group.zipfiles, key=lambda el: el[4:6]):
                    groups_out.write(filename + '\n')
    else:
        print("Expected arguments: zipfiles_dir output_file num_divisions")

