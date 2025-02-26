# train.py
import json
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical

# Load intents file
with open('data/intents.json') as file:
    intents = json.load(file)

def preprocess_data(intents):
    training_sentences = []
    training_labels = []
    labels = []
    responses = []

    for intent in intents['intents']:
        for pattern in intent['patterns']:
            training_sentences.append(pattern)
            training_labels.append(intent['tag'])
        responses.append(intent['responses'])
        if intent['tag'] not in labels:
            labels.append(intent['tag'])

    # Encode labels
    lbl_encoder = LabelEncoder()
    lbl_encoder.fit(training_labels)
    training_labels = lbl_encoder.transform(training_labels)

    # Tokenize the sentences
    vocab_size = 1000
    embedding_dim = 16
    max_length = 20
    oov_token = "<OOV>"

    tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=vocab_size, oov_token=oov_token)
    tokenizer.fit_on_texts(training_sentences)
    sequences = tokenizer.texts_to_sequences(training_sentences)
    padded_sequences = tf.keras.preprocessing.sequence.pad_sequences(sequences, maxlen=max_length)

    return padded_sequences, training_labels, lbl_encoder, tokenizer

x_train, y_train, lbl_encoder, tokenizer = preprocess_data(intents)
y_train = to_categorical(y_train)

# Build model
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Embedding(1000, 16, input_length=20))
model.add(tf.keras.layers.GlobalAveragePooling1D())
model.add(tf.keras.layers.Dense(16, activation='relu'))
model.add(tf.keras.layers.Dense(len(lbl_encoder.classes_), activation='softmax'))

# Compile model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train model
model.fit(np.array(x_train), np.array(y_train), epochs=200, batch_size=5, verbose=1)

# Save model
model.save('models/chatbot_model.h5')

# Save tokenizer and label encoder
import pickle

with open('models/tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('models/label_encoder.pickle', 'wb') as handle:
    pickle.dump(lbl_encoder, handle, protocol=pickle.HIGHEST_PROTOCOL)
