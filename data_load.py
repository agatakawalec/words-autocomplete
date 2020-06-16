import json
import os
import re


def remove_accents(input_text):
    strange = 'ążźćńółęś'
    ascii_replacements = 'azzcnoleś'
    translator = str.maketrans(strange, ascii_replacements)
    return input_text.translate(translator)


regex_links = '^http.*'
regex_stays = '\w|\d|\s|(|)'

with open('files/message_1.json') as input_file:
    with open('data_pl.txt', 'a', encoding='utf-8',
              errors='replace') as output_file:
        data = json.load(input_file)
        for x in (data[u'messages']):
            if 'content' in x:
                for text in x[u'content'].encode('iso-8859-1').decode(
                        'utf-8').strip().lower():
                    after_reg = re.search(regex_stays, text)
                    output_file.write(after_reg.group(0))
            output_file.write('\n')

with open('data_pl.txt', 'r') as file:
    lines = file.readlines()

with open('data1.txt', 'w') as file:
    for line in lines:
        if not re.match(regex_links, line):
            file.write(remove_accents(line))

os.remove('data_pl.txt')
