from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from nltk.tokenize import RegexpTokenizer
from numpy import array


class AIProcessing:

    def __init__(self):
        self.models = [load_model('model1'), load_model('model2'),
                       load_model('model3')]

        tok = RegexpTokenizer(r'\w+')
        data1 = tok.tokenize(open('data1.txt').read().lower())
        data2 = tok.tokenize(open('data2.txt').read().lower())
        data3 = tok.tokenize(open('data3.txt').read().lower())
        self.tokenizers = [Tokenizer(), Tokenizer(), Tokenizer()]
        self.tokenizers[0].fit_on_texts([data1])
        self.tokenizers[1].fit_on_texts([data2])
        self.tokenizers[2].fit_on_texts([data3])

    def predict(self, in_text):
        result = []
        yhats = []

        try:
            for i in range(3):
                encoded = self.tokenizers[i].texts_to_sequences([in_text])[0]
                encoded = array(encoded)
                yhats.append(
                    self.models[i].predict_classes(encoded, verbose=0))
        except AttributeError:
            return []

        for i in range(3):
            out_word = ''
            for word, index in self.tokenizers[i].word_index.items():
                if index == yhats[i]:
                    out_word = word
                    break
            result.append(out_word)

        return list(set(result))
