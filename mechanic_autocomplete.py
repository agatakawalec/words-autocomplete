import numpy as np
import sys
from collections import Counter
from pynput.keyboard import Key, Listener
from colorama import Fore, Style

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


def print_lines(to_print):
    sys.stdout.write("\033[8F")

    print('     ' * 10)
    print('     ' * 10)
    print('------------------------------------------------')

    for _ in range(5 - len(to_print)):
        print('     ' * 10)

    for i in to_print:
        print(i, '     ' * 10)


INPUT = ''
TEXT = []
CHOSEN_OPTION_ID = 0
CHOSEN_OPTION = ''
CHOSEN_OPTION_SIZE = 0


def on_press(key):
    global INPUT, TEXT, CHOSEN_OPTION, CHOSEN_OPTION_ID, CHOSEN_OPTION_SIZE

    if key == Key.backspace:
        if len(INPUT) == 0:
            TEXT = TEXT[:-1]
        else:
            INPUT = INPUT[0: -1]
        print()
    elif key == Key.enter:
        TEXT.append(CHOSEN_OPTION)
        INPUT = ''

    elif key == Key.tab:
        if CHOSEN_OPTION_ID < CHOSEN_OPTION_SIZE - 1:
            CHOSEN_OPTION_ID += 1
        else:
            CHOSEN_OPTION_ID = 0
    elif key == Key.space:
        TEXT.append(INPUT)
        INPUT = ''
    else:
        if hasattr(key, 'char'):
            INPUT = INPUT + key.char

    to_print = []

    words_found = find_word(INPUT)
    CHOSEN_OPTION_SIZE = len(words_found)

    if CHOSEN_OPTION_ID >= CHOSEN_OPTION_SIZE:
        CHOSEN_OPTION_ID = CHOSEN_OPTION_SIZE - 1

    for n, el in enumerate(words_found):
        if n == CHOSEN_OPTION_ID:
            to_print.append(Fore.GREEN + el + Style.RESET_ALL)
            CHOSEN_OPTION = el

        else:
            to_print.append(el)

    to_print.append('input: ' + ' '.join(TEXT) + ' ' + INPUT)
    print_lines(to_print)


def on_release(key):
    if key == Key.esc:
        return False


with Listener(on_press=on_press, on_release=on_release) as listener:
    print('\n\n\n\n\n\n\n\n\n')
    listener.join()
