from sys import argv
from statistics import stdev, mean


def score_stats(trans_file):
    st_devs = []
    means = []
    for line in open(trans_file, 'r'):
        translations = line.strip().split('\t')[1]
        scores = [float(pair.split(',')[1]) for pair in translations.split(';')]
        if len(scores) > 1:
            st_devs.append(stdev(scores))
            means.append(mean(scores))
        else:
            st_devs.append(0)
    print("Mean of means: " + str(mean(means)))
    print("Std. deviation of means: " + str(stdev(means)))
    print("Mean of standard deviation: " + str(mean(st_devs)))
    print("Std. deviation of std. deviations: " + str(stdev(st_devs)))
    # print("Standard deviations: ")
    # for std in st_devs:
    #     print(str(std))


if __name__ == '__main__':
    num_args = 2
    if len(argv) == num_args:
        translation_file = argv[1]
        score_stats(translation_file)
    else:
        print("Incorrect number of arguments")
