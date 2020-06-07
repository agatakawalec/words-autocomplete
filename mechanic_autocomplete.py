import numpy as np
import sys
from collections import Counter
from pynput.keyboard import Key, Listener


data_file = open('data.txt')

data_list = [line.strip().split() for line in data_file]

messages = np.array(data_list)

all_words = [word for line in data_list for word in line]

count_words = Counter(all_words)

unique_words = np.unique(all_words)


def find_word(char):
    possibilities = unique_words[np.char.startswith(unique_words, char)]
    count_poss = [(k, v) for k, v in count_words.items() if k in possibilities]
    count_poss = sorted(count_poss, key=lambda tup: tup[1], reverse=True)
    return [k for k, _ in count_poss[:4]]


INPUT = ''


def on_press(key):
    global INPUT

    if key == Key.backspace:
        INPUT = INPUT[0: -1]

    else:
        INPUT = INPUT + key.char

        sys.stdout.write("\033[F")
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[F")

    words_found = find_word(INPUT)
    for _ in range(4 - len(words_found)):
        print('                             ')

    for el in words_found:
        print(el + '                             ')
    print('input: ', INPUT, '           ')


def on_release(key):
    if key == Key.esc:
        # Stop listener
        return False

with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    print('\n\n\n\n\n')
    listener.join()
