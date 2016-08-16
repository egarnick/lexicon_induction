from nltk.metrics import edit_distance


def lev_dist(worda, wordb):
    return edit_distance(worda, wordb) / max(len(worda), len(wordb))


if __name__ == '__main__':
    print(lev_dist('late-ripening', 'late-inning'))
