from sys import argv
import gzip
import glob
from lxml import html
from time import time
import nltk.data
import re


"""
Write gzipped counts file
"""

# Constant resources
print("Loading tokenizer")
SENT_TOKENIZER = nltk.data.load('tokenizers/punkt/english.pickle')

# REGEX
URL_TOKEN = re.compile(r'\b(\S*http\S+)|(\S*www\S+)\b')
NUM_TOKEN = re.compile(r'(\S*\d+\S*)+')
PUNCTUATION = re.compile(r'[\.,!\?\(\):–—»«`\[\]/\{\}=<>\|;ʻ\"\+]')
HYP_INIT = re.compile(r'(^|[\s])-+')
HYP_FIN = re.compile(r'-+($|[\s])')

# not used
DOLLAR_TOKEN = re.compile(r'[A-Z]{,3}\$\d+(,\d+)*(\.\d+)*[a-zA-Z]*')

# Global Variables
MAX_COUNT = 0
START_TIME = 0

# Resource dictionaries
VOCABULARY = {}     # {word : [ct, {ctx1 : ct, ctx2 : ct, ...}], ...}


def add_context(word, ctx):
    global MAX_COUNT
    if len(ctx):
        try:
            VOCABULARY[word][1][ctx] += 1
            if VOCABULARY[word][1][ctx] > MAX_COUNT:
                MAX_COUNT = VOCABULARY[word][1][ctx]
        except KeyError:
            VOCABULARY[word][1][ctx] = 1


def count_vocab(input_text):
    if not VOCABULARY.get("_BOS"):
        VOCABULARY["_BOS"] = [0, {}]
    print("Processing " + str(len(input_text)) + " sentences")
    counter = 0
    for sentence in input_text:
        # counter += 1
        # if not counter % 10000:
        #     print("Sentence " + str(counter) + ": ")
        #     print(sentence)
        back2 = "_BOS"
        back1 = ""
        VOCABULARY["_BOS"][0] += 1
        for token in sentence.split():
            token = token.strip("\'\"\\/.,;:?!)(-")
            token = URL_TOKEN.sub('_URL', token)
            token = NUM_TOKEN.sub('_NUM', token)
            token = PUNCTUATION.sub('', token)
            if len(token):
                # if VOCABULARY.get(token.lower()):
                #     token = token.lower()
                if not VOCABULARY.get(token):
                    VOCABULARY[token] = [1, {}]
                else:
                    VOCABULARY[token][0] += 1
                add_context(token, back2)
                add_context(token, back1)
                if VOCABULARY.get(back1):
                    add_context(back1, token)
                if VOCABULARY.get(back2):
                    add_context(back2, token)
                back2 = back1
                back1 = token


def parse_xml_data(xml_text):
    text = ""
    xml_text = html.fromstring(xml_text)
    for doc in xml_text:
        for texttag in (stag for stag in doc if stag.tag == 'text'):
            if len(texttag.findall('p')):
                for paragraph in texttag:
                    text += paragraph.text
            elif texttag.text:
                text += texttag.text
    sentences_split = SENT_TOKENIZER.tokenize(text.strip())
    count_vocab(sentences_split)


def get_gz_files(path2gz):
    """
    Pass text from each gz file in source dir of corpus to parse_xml_data()
    :param path2gz: string: absolute path to data directory
    :return:
    """
    global START_TIME
    START_TIME = time()
    if path2gz[-1] != '/':
        path2gz += '/'
    source_files = glob.glob(path2gz + '/*.gz')

    # TEST
    # print("Source files: " + str(source_files))
    # TEST

    for src_f in source_files:
        text = ""
        with gzip.open(src_f, 'rb') as gz_read:
            line_count = 0
            for line in gz_read:
                text += line.decode('utf-8')
                line_count += 1
            parse_xml_data(text)


def dump_counts(outfile_name):
    # word \t count \t context_word,ctxt_count \t ...
    with gzip.open(outfile_name, 'wb') as lm_out:
        for word in VOCABULARY:
            cnt_ctxt = VOCABULARY[word]
            line_out = word + '\t' + str(cnt_ctxt[0])
            contexts = cnt_ctxt[1]
            for ctx_tok in contexts:
                line_out += '\t' + ctx_tok + ',' + str(contexts[ctx_tok])
            line_out += '\n'
            lm_out.write(line_out.encode('utf-8'))


if __name__ == '__main__':
    num_args = 3
    if len(argv) == num_args:
        # div_path - path to set of files to process
        # path - abs. path to directory containing [afp_eng, apw_eng, etc.]
        div_path, out_file = argv[1:num_args]
        print("Getting gz files")
        get_gz_files(div_path)

        # COMMENT FOR TEST
        print("VOCABULARY length: " + str(len(VOCABULARY)))
        print("Writing output")
        dump_counts(out_file)
        # COMMENT FOR TEST
        # with open(out_file, 'w') as lm_out:
        #     json.dump(VOCABULARY, lm_out)

        print("Done")
    else:
        print("Got " + str(len(argv)) + " args.  Expected " + str(num_args))
