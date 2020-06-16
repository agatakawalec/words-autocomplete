from keras.layers import Dense
from keras.layers import Embedding
from keras.layers import LSTM
from keras.models import Sequential
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical
from nltk.tokenize import RegexpTokenizer
from numpy import array

text = open('data1.txt').read().lower()
tok = RegexpTokenizer(r'\w+')
data = tok.tokenize(text)

tokenizer = Tokenizer()
tokenizer.fit_on_texts([data])
encoded = tokenizer.texts_to_sequences([data])[0]
vocab_size = len(tokenizer.word_index) + 1

sequences = list()
for i in range(1, len(encoded)):
    sequence = encoded[i - 1:i + 1]
    sequences.append(sequence)

sequences = array(sequences)
X, y = sequences[:, 0], sequences[:, 1]
y = to_categorical(y, num_classes=vocab_size)

model = Sequential()
model.add(Embedding(vocab_size, 10, input_length=1))
model.add(LSTM(50))
model.add(Dense(vocab_size, activation='softmax'))
print(model.summary())

model.compile(loss='categorical_crossentropy', optimizer='adam',
              metrics=['accuracy'])
model.fit(X, y, epochs=50, verbose=2)
model.save('model1')
