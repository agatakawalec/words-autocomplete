import shutil
import sys
from collections import Counter

import numpy as np
from colorama import Fore, Style
from pynput.keyboard import Key, Listener

from ai_processing import AIProcessing

data_file = open('data1.txt')

ai = AIProcessing()

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
    columns = shutil.get_terminal_size()[0]

    sys.stdout.write("\033[8F")

    print(' ' * columns)
    print(' ' * columns)
    print('-' * columns)

    for _ in range(5 - len(to_print)):
        print(' ' * columns)

    for i in to_print:
        print(i, ' ' * (columns - len(i) - 1))


INPUT = ''
TEXT = []
CHOSEN_OPTION_ID = 0
CHOSEN_OPTION = ''
CHOSEN_OPTION_SIZE = 0
NEW_WORD = False


def on_press(key):
    global NEW_WORD, INPUT, TEXT, CHOSEN_OPTION
    global CHOSEN_OPTION_ID, CHOSEN_OPTION_SIZE

    if key == Key.backspace:
        if len(INPUT) == 0:
            TEXT = TEXT[:-1]
            NEW_WORD = True
        else:
            INPUT = INPUT[0: -1]
            NEW_WORD = False
        print()
    elif key == Key.enter:
        TEXT.append(CHOSEN_OPTION)
        INPUT = ''
        NEW_WORD = True

    elif key == Key.tab or key == Key.down:
        if CHOSEN_OPTION_ID < CHOSEN_OPTION_SIZE - 1:
            CHOSEN_OPTION_ID += 1
        else:
            CHOSEN_OPTION_ID = 0
    elif key == Key.up:
        if CHOSEN_OPTION_ID > 0:
            CHOSEN_OPTION_ID -= 1
        else:
            CHOSEN_OPTION_ID = CHOSEN_OPTION_SIZE - 1
    elif key == Key.space:
        TEXT.append(INPUT)
        INPUT = ''
        NEW_WORD = True
    else:
        if hasattr(key, 'char'):
            INPUT = INPUT + key.char
            NEW_WORD = False

    to_print = []
    if NEW_WORD:
        if len(TEXT) != 0:
            words_found = ai.predict(TEXT[-1])
        else:
            words_found = find_word('')
        if len(words_found) == 0:
            words_found = find_word('')
    else:
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
        print()
        return False


with Listener(on_press=on_press, on_release=on_release) as listener:
    print(chr(27) + "[2J")
    print('\n\n')
    listener.join()
