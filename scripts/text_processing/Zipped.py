from zipfile import *


class Zipped:
    """
    A class to access the contents of zipped files
    """

    def __init__(self, path):
        self.path = path
        self.contents = []
        self.get_contents()

    def get_contents(self):
        """
        Fill self.contents with a list of names of files
        """
        with ZipFile(self.path) as zip_read:
            self.contents = zip_read.namelist()

    def ls(self):
        return self.contents

    def cat(self, target=""):
        """
        Print text of specified file in self.contents (no args if only 1 file)
        :param target: string: name of file to cat
        :return:
        """
        if not len(target) and len(self.contents) == 1:
            target = self.contents[0]
        elif len(target):
            target = target.strip('/')

        target_split = target.split('/')
        if target in ['/'.join(file.split('/')[-1 * len(target_split):]) for
                      file in self.contents]:
            lines = []
            with ZipFile(self.path) as zip_read:
                with zip_read.open(target) as contents_in:
                    for line in contents_in:
                        lines.append(line.decode('utf-8'))
                        # print(line.decode('utf-8'), end='')
            return lines
        else:
            print("target file " + target + " not found in " + self.path)

    def filesize(self, target):
        """
        Return size of target file
        :param target: string: name of target file
        :return: int: size of file in bytes(?)
        """
        target_split = target.split('/')
        if target in ['/'.join(file.split('/')[-1 * len(target_split):]) for
                      file in self.contents]:
            with ZipFile(self.path) as zip_f:
                return zip_f.getinfo(target).file_size
        else:
            print("target file " + target + " not found in " + self.path)

    def vec2vocab(self, target):
        """
        Print vocab from word vectors
        :param target: string: name of vectors file
        :return:
        """
        target_split = target.split('/')
        if target in ['/'.join(file.split('/')[-1 * len(target_split):]) for
                      file in self.contents]:
            with ZipFile(self.path) as zip_read:
                with zip_read.open(target) as contents_in:
                    for line in contents_in:
                        print(line.decode('utf-8').strip().split()[0])
        else:
            print("target file " + target + " not found in " + self.path)