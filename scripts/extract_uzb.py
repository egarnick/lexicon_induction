from sys import argv
from zipfile import *
from glob import glob
import xml.etree.ElementTree as ET


"""
Given source directory of zipped folders, extract specified number of sentences
and write to specified output file starting at 0-based (sentence) start_index
"""


def dir_contents(src_dir, ext):
    path = src_dir if src_dir[-1] == '/' else src_dir + '/'
    contents = path + '*' + ext
    contents_list = glob(contents)
    print("Found " + str(len(contents_list)) + " matching files in directory")
    print(str(contents_list))
    return contents_list


def raw_sentences(xml_text):
    """
    Return list of all original sentences in xml_text
    :param xml_text: string: xml marked up text+data
    :return: list: [senta, sentb, ...]
    """
    sentences = []
    root = ET.fromstring(xml_text)
    for doc in root:
        for text in doc:
            for seg in text:
                for orig_txt in seg.findall('ORIGINAL_TEXT'):
                    sentences.append(orig_txt.text)
    return sentences


def write_sentences(zip_files, dest, start_idx, num_sents):
    """
    Extract xml files from zip_files and write raw sentences to dest file
    :param zip_files: list: [a.zip, b.zip, ...]
    :param dest: string: name of output file
    :param start_idx: int: index of starting sentence
    :param num_sents: int: desired number of sentences to process
    """
    num_xml_files = 0
    sent_count = 0
    text_out = open(dest, 'w')
    for z_file in zip_files:
        with ZipFile(z_file) as zip_read:
            for xml_file in (xml for xml in zip_read.namelist() if
                             xml[-3:] == 'xml'):
                num_xml_files += 1
                with zip_read.open(xml_file) as xml_read:
                    xml_contents = xml_read.read()
                    raw_sents = raw_sentences(xml_contents)
                    for raw_sent in raw_sents:
                        if sent_count >= start_idx:
                            text_out.write(raw_sent + '\n')
                        sent_count += 1
                        # Break early if indicated
                        if sent_count == num_sents + start_idx:
                            text_out.close()
                            print("Processed " + str(num_xml_files) +
                                  " xml files.")
                            print("Wrote " + str(sent_count - start_idx) +
                                  " sentences.")
                            return
    text_out.close()
    print("Processed " + str(num_xml_files) + " xml files.")
    print("Wrote " + str(sent_count) + " sentences.")


if __name__ == '__main__':
    num_args = 5
    if len(argv) == num_args:
        source_dir, destination_file, start_index, num_sentences = argv[1:5]
        zipped_files = dir_contents(source_dir, '.ltf.zip')
        write_sentences(zipped_files,
                        destination_file,
                        int(start_index),
                        int(num_sentences))
    else:
        print("Expected " + str(num_args) +
              " arguments.  Got " + str(len(argv)))
