from flask import Flask, request, jsonify, render_template
import os
from groq import Groq
from dotenv import load_dotenv
app = Flask(__name__)
load_dotenv()
# Set your Groq API key
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise Exception("GROQ_API_KEY environment variable is not set.")

client = Groq(api_key=groq_api_key)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']

    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": user_input}],
            model="llama-3.3-70b-versatile",
        )

        reply = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error: {e}")
        reply = "I'm sorry, but I'm unable to process your request at the moment."

    return jsonify({"response": reply})

@app.route('/start', methods=['GET'])
def start():
    welcome_message = "Hello! I'm here to help you with development, programming, AI, and more. Ask me anything!"
    return jsonify({"response": welcome_message})

if __name__ == '__main__':
    app.run(debug=True)
