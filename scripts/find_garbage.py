from sys import argv


def count_garbage(suspect):
    garbage_types = 0
    garbage_tokens = 0
    with open(suspect, 'r') as sus_in:
        for line in sus_in:
            token, count = line.strip().split('\t')[:2]
            if 'Ð' in token:
                garbage_types += 1
                garbage_tokens += int(count)
    return [garbage_types, garbage_tokens]


if __name__ == '__main__':
    input_file = argv[1]
    g_types, g_tokens = count_garbage(input_file)
    print(str(g_types), str(g_tokens))