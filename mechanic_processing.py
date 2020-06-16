import re
from collections import defaultdict, Counter

from nltk.tokenize import word_tokenize


class MechanicProcessing:
    def __init__(self):
        self.lookup_dict = defaultdict(list)

    def add_document(self, string):
        cleaned = re.sub(r'\W+', ' ', string).lower()
        preprocessed_list = word_tokenize(cleaned)
        pairs = self.one_tuple(preprocessed_list)
        for pair in pairs:
            self.lookup_dict[pair[0]].append(pair[1])
        pairs2 = self.two_tuples(preprocessed_list)
        for pair in pairs2:
            self.lookup_dict[tuple([pair[0], pair[1]])].append(pair[2])
        pairs3 = self.three_tuples(preprocessed_list)
        for pair in pairs3:
            self.lookup_dict[tuple([pair[0], pair[1], pair[2]])].append(
                pair[3])

    def one_tuple(self, data):
        if len(data) < 1:
            return
        for i in range(len(data) - 1):
            yield [data[i], data[i + 1]]

    def two_tuples(self, data):
        if len(data) < 2:
            return
        for i in range(len(data) - 2):
            yield [data[i], data[i + 1], data[i + 2]]

    def three_tuples(self, data):
        if len(data) < 3:
            return
        for i in range(len(data) - 3):
            yield [data[i], data[i + 1], data[i + 2], data[i + 3]]

    def one_word(self, string):
        return Counter(self.lookup_dict[string]).most_common()[:3]

    def two_words(self, string):
        suggest = Counter(self.lookup_dict[tuple(string)]).most_common()[:3]
        if len(suggest) == 0:
            return self.one_word(string[-1])
        return suggest

    def three_words(self, string):
        suggest = Counter(self.lookup_dict[tuple(string)]).most_common()[:3]
        if len(suggest) == 0:
            return self.two_words(string[-2:])
        return suggest

    def more_words(self, string):
        return self.three_words(string[-3:])

    def predict(self, string):
        if len(self.lookup_dict) > 0:
            tokens = string.split(" ")
            if len(tokens) == 1:
                return self.one_word(string)
            elif len(tokens) == 2:
                return self.two_words(string.split(" "))
            elif len(tokens) == 3:
                return self.three_words(string.split(" "))
            elif len(tokens) > 3:
                return self.more_words(string.split(" "))
        return
