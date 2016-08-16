from sys import argv
import re

"""
Remove all [\.,\!\?\-\(\)\:\–\—»«], lowercase text and normalize numbers, urls
"""
# REGEX
URL_TOKEN = re.compile(r'\b(\S*http\S+)|(\S*www\S+)\b')
NUM_TOKEN = re.compile(r'(\S*\d+\S*)+')
PUNCTUATION = re.compile(r'[\.,!\?\-\(\):–—»«\[\]/\{\}=<>\|;ʻ\"\+]')

# Currently not used: URL pattern replaces too much
DOLLAR_TOKEN = re.compile(r'[A-Z]{,3}\$\d+(,\d+)*(\.\d+)*[a-zA-Z]*')


def clean_text(input_file, output_file):
    with open(output_file, 'w') as clean_out:
        for line in open(input_file, 'r'):
            line_url = URL_TOKEN.sub('_URL', line.strip().lower())
            line_num = NUM_TOKEN.sub('_NUM', line_url)
            line_pnc = PUNCTUATION.sub('', line_num)
            clean_out.write(line_pnc + '\n')


if __name__ == '__main__':
    num_args = 3
    if len(argv) == num_args:
        source_file, results_file = argv[1:num_args]
        clean_text(source_file, results_file)
    else:
        print("Required arguments: source_text output_file")
