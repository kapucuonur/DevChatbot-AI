from flask import Flask, request, jsonify, render_template, session
import os
import re
import json
import random
from groq import Groq
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Session için gizli anahtar
load_dotenv()

# Groq API ayarları
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise Exception("GROQ_API_KEY environment variable is not set.")

client = Groq(api_key=groq_api_key)

# intents.json dosyasını yükle
def load_intents():
    try:
        with open('data/intents.json', 'r', encoding='utf-8') as file:
            data = file.read()
            if data.strip().startswith("<!DOCTYPE html>"):  # HTML yanıtını kontrol et
                raise ValueError("Hata: intents.json yerine bir HTML sayfası yükleniyor!")
            return json.loads(data)
    except FileNotFoundError:
        print("Hata: intents.json dosyası bulunamadı.")
        return {"intents": []}
    except json.JSONDecodeError:
        print("Hata: intents.json geçerli bir JSON formatında değil.")
        return {"intents": []}

def get_random_response(intent):
    # Debug: Print the tag being processed
    print(f"Processing tag: {intent['tag']}")

    # Fixed responses for these tags (NO RANDOMNESS)
    if intent["tag"] in ["coding_tips", "junior_developer", "ai", "development", "programming_languages"]:
        print("Returning fixed response (no randomness).")  # Debug print
        return intent["responses"][0]  # Always return the first response

    # Random responses for these tags (APPLY RANDOMNESS)
    if intent["tag"] in ["greeting", "how_are_you", "user_name"]:
        print("Returning random response.")  # Debug print
        return random.choice(intent["responses"])  # Randomly select a response

    # Default behavior for all other tags (NO RANDOMNESS)
    print("Returning first response (no randomness).")  # Debug print
    return intent["responses"][0]  # Always return the first response

def extract_name(user_input):
    match = re.search(r"(?:my name is|i am|i'm|called|call me)\s+(\w+)", user_input, re.IGNORECASE)
    return match.group(1) if match else None

# Kullanıcı girdisine göre yanıt döndüren fonksiyon
def get_response(user_input):
    intents = load_intents()
    if not intents["intents"]:
        return "Üzgünüm, şu an yanıt veremiyorum."

    for intent in intents["intents"]:
        if user_input.lower() in [p.lower() for p in intent["patterns"]]:
            return get_random_response(intent)  # Use get_random_response for random/fixed logic

    return None  # Eğer intents.json içinde yoksa, Groq API'ye geçilecek

# Kullanıcı girişini işleyen ana fonksiyon
def handle_user_input(user_input):
    user_name = session.get('user_name')

    # Kullanıcı adını kontrol et ve kaydet
    if not user_name:
        extracted_name = extract_name(user_input)
        if extracted_name:
            session['user_name'] = extracted_name
            user_name = extracted_name

    # intents.json içinde yanıt bulmaya çalış
    response = get_response(user_input)
    if response:
        if user_name:  # Replace [name] with the actual user name
            return response.replace("[name]", user_name)
        return response

    # Eğer intents.json içinde yoksa, Groq API'sini kullan
    try:
        groq_response = client.chat.completions.create(
            messages=[{"role": "user", "content": user_input}],
            model="llama-3.3-70b-versatile",
        )
        reply = groq_response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error: {e}")
        reply = "I'm sorry, but I'm unable to process your request at the moment."

    if user_name:  # Replace [name] with the actual user name
        return reply.replace("[name]", user_name)
    return reply

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json['message']  # JSON formatında input bekliyoruz
    except KeyError:
        return jsonify({"response": "Please provide a valid message key in your request."}), 400

    reply = handle_user_input(user_input)
    return jsonify({"response": reply})

@app.route('/start', methods=['GET'])
def start():
    welcome_message = "Hello! I'm here to help you with development, programming, AI, and more. Ask me anything!"
    return jsonify({"response": welcome_message})

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5001, debug=True)