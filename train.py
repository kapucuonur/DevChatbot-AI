import json
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
import pickle
import random
import os
import logging

# Gerekli NLTK verilerini indir
nltk.download('punkt')
nltk.download('stopwords')

# Logging ayarları
logging.basicConfig(filename='training.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

STOPWORDS = set(stopwords.words('english'))

# intents.json dosyasını yükle
def load_intents():
    try:
        with open('data/intents.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logging.error("Hata: intents.json dosyası bulunamadı.")
        return {"intents": []}
    except json.JSONDecodeError:
        logging.error("Hata: intents.json geçerli bir JSON dosyası değil.")
        return {"intents": []}

# Verileri işle
def preprocess_data(intents):
    words = []
    classes = []
    documents = []
    ignore_chars = ['?', '!', '.', ',']

    for intent in intents['intents']:
        for pattern in intent['patterns']:
            # Tokenize et ve gereksiz kelimeleri temizle
            word_list = word_tokenize(pattern)
            word_list = [w.lower() for w in word_list if w not in ignore_chars and w not in STOPWORDS]
            words.extend(word_list)
            documents.append((word_list, intent['tag']))
            if intent['tag'] not in classes:
                classes.append(intent['tag'])

    # Kelimeleri ve sınıfları sıralı hale getir
    words = sorted(set(words))
    classes = sorted(set(classes))

    # Eğitim verilerini hazırla
    training = []
    output_empty = [0] * len(classes)

    for doc in documents:
        bag = [1 if word in doc[0] else 0 for word in words]
        output_row = list(output_empty)
        output_row[classes.index(doc[1])] = 1
        training.append([bag, output_row])

    random.shuffle(training)
    training = np.array(training, dtype=object)

    train_x = list(training[:, 0])
    train_y = list(training[:, 1])

    return words, classes, train_x, train_y

# Modeli oluştur
def build_model(input_shape, output_shape):
    model = Sequential([
        Dense(128, input_shape=(input_shape,), activation='relu'),
        Dropout(0.5),
        Dense(64, activation='relu'),
        Dropout(0.5),
        Dense(output_shape, activation='softmax')
    ])

    model.compile(loss='categorical_crossentropy', optimizer=SGD(learning_rate=0.01, momentum=0.9, nesterov=True), metrics=['accuracy'])
    return model

# Modeli ve diğer dosyaları kaydet
def save_model_and_data(model, words, classes):
    if not os.path.exists('models'):
        os.makedirs('models')

    model.save('models/chatbot_model.h5')

    with open('models/words.pickle', 'wb') as handle:
        pickle.dump(words, handle, protocol=pickle.HIGHEST_PROTOCOL)

    label_encoder = LabelEncoder()
    label_encoder.fit(classes)
    with open('models/label_encoder.pickle', 'wb') as handle:
        pickle.dump(label_encoder, handle, protocol=pickle.HIGHEST_PROTOCOL)

# Ana fonksiyon
def main():
    intents = load_intents()
    if not intents["intents"]:
        return

    words, classes, train_x, train_y = preprocess_data(intents)

    # Verileri eğitim ve test olarak ayır
    train_x, test_x, train_y, test_y = train_test_split(train_x, train_y, test_size=0.2, random_state=42)

    model = build_model(len(train_x[0]), len(train_y[0]))

    # Erken durdurma mekanizması ekle
    early_stop = EarlyStopping(monitor='loss', patience=10, restore_best_weights=True)

    # Modeli eğit
    history = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1, callbacks=[early_stop])

    # Test seti üzerinde değerlendir
    test_predictions = model.predict(np.array(test_x))
    test_predictions = np.argmax(test_predictions, axis=1)
    test_y_labels = np.argmax(test_y, axis=1)

    accuracy = accuracy_score(test_y_labels, test_predictions)
    report = classification_report(test_y_labels, test_predictions, target_names=classes)

    logging.info(f"Test Accuracy: {accuracy}")
    logging.info(f"Classification Report:\n{report}")

    save_model_and_data(model, words, classes)
    logging.info("Model ve diğer dosyalar başarıyla kaydedildi.")

if __name__ == '__main__':
    main()