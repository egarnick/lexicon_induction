from sys import argv
from glob import glob

# For testing: -1 to process all
CUTOFF = -1

"""
Combine all separately processed Morfessor-output segment counts into one file
Output format - each line relates to one segment with 5 tab-separated fields:

<segment><TAB>'mono'<TAB><mono_count><TAB>'mult'<TAB><mult_count>
"""


def combine_scounts(scounts_dir):
    """
    Return dictionary of combination of segment counts
    :param scounts_dir: string: path to segment counts file directory
    :return: dict: {segment: {'mono': count. 'mult': count}, ...}
    """
    segcounts_dict = {}         # {segment: {'mono': ct, 'mult': ct}, ...}
    num_files = 0
    for seg_file in glob(scounts_dir + '/*.counts'):
        num_files += 1
        temp_scount_dict = {}
        for line in open(seg_file, 'r'):
            line_split = line.strip().split('\t')
            temp_scount_dict[line_split[0]] = \
                {line_split[1]: int(line_split[2]),
                 line_split[3]: int(line_split[4])}
        for seg in temp_scount_dict:
            try:
                segcounts_dict[seg]['mono'] += temp_scount_dict[seg]['mono']
                segcounts_dict[seg]['mult'] += temp_scount_dict[seg]['mult']
            except KeyError:
                segcounts_dict[seg] = {'mono': temp_scount_dict[seg]['mono'],
                                       'mult': temp_scount_dict[seg]['mult']}
        if not num_files % 10:
            print("Processed " + str(num_files) + " counts files")
        if num_files == CUTOFF:
            break
    print("Total segment count: " + str(len(segcounts_dict)))
    return segcounts_dict


def dump_scounts(segcounts_dict, out_file):
    """
    Print segcounts_dict, tab-separated: segment 'mono' count 'mult' count
    :param segcounts_dict: dict: segment counts for 'mono' and 'mult'
    :param out_file: string: name of output file
    """
    with open(out_file, 'w') as segs_out:
        for seg in segcounts_dict:
            mono_mult = segcounts_dict[seg]
            segs_out.write('\t'.join([seg,
                                      'mono', str(mono_mult['mono']),
                                      'mult', str(mono_mult['mult'])]) +
                           '\n')


if __name__ == '__main__':
    num_args = 3
    if len(argv) == num_args:
        # Arguments:
        # segcounts_dir - directory with segment counts files
        # output_file - name for results file
        segcounts_dir, output_file = argv[1:num_args]
        scount_dict = combine_scounts(segcounts_dir)
        dump_scounts(scount_dict, output_file)
    else:
        print("Wrong number of args")

