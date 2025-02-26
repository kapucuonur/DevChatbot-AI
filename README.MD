# Chatbot Assistant 🤖

Welcome to **Chatbot Assistant**, a smart and interactive chatbot designed to help you with various topics such as programming, software development, artificial intelligence, and more! This chatbot leverages the **GROQ API** to provide intelligent and context-aware responses.

---

## 🌟 Features

- **Interactive Chat**: Ask questions and get instant responses from the chatbot.
- **GROQ API Integration**: Utilizes the GROQ API for advanced natural language processing.
- **Markdown Support**: Responses are formatted with Markdown for better readability.
- **Responsive Design**: Works seamlessly on both desktop and mobile devices.
- **Dark/Light Theme**: Switch between dark and light themes for a comfortable experience.

---

## 🛠️ Tech Stack

### Frontend

- **HTML5**: Structure of the web application.
- **CSS3**: Styling and layout.
- **JavaScript**: Interactive functionality.
- **Markdown**: Formatting bot responses.

### Backend

- **Python**: Core programming language.
- **Flask**: Web framework for handling requests.
- **GROQ API**: For intelligent chatbot responses.

### Tools & Libraries

- **Git**: Version control.
- **Docker**: Containerization for deployment.
- **python-dotenv**: For managing environment variables.
- **NPM**: Package management.
- **Webpack**: Bundling assets.

---

## 🚀 Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- Flask (`pip install flask`)
- python-dotenv (`pip install python-dotenv`)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/chatbot-assistant.git
   cd chatbot-assistant
   Set up a virtual environment (optional but recommended):
   ```
2. **Create a virtual environment**:
   python -m venv venv
   source venv/bin/activate # On Windows, use `venv\Scripts\activate`
   Install dependencies:

3.**install dependencies:**
pip install -r requirements.txt
Set up environment variables:

4.**install dependencies:**
Create a .env file in the root directory.

Add your GROQ API key to the .env file:

GROQ_API_KEY=your_api_key_here

5.**Run the application:**
python app.py
Access the application:

6.**Access the application:**
Open your browser and go to http://127.0.0.1:5000.

📖 Usage
1.Ask Questions: Type your question in the input box and press Enter or click the Send button.

2.Explore Topics: Use the predefined buttons to ask common questions about programming, development, AI, and coding tips.

3.Switch Themes: Toggle between dark and light themes using the theme button.

📂 Project Structure

chatbot-assistant/
│
├── app.py # Flask application
├── requirements.txt # Python dependencies
├── .env # Environment variables (not included in version control)
├── static/ # Static files (CSS, JS, images)
│ ├── css/
│ │ └── styles.css # Custom styles
│ └── js/
│ └── script.js # Interactive JavaScript
├── templates/ # HTML templates
│ └── index.html # Main HTML file
└── README.md # Project documentation

🤝 Contributing
Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1.Fork the repository.

2.Create a new branch:

git checkout -b feature/your-feature-name

3.Make your changes and commit them:

git commit -m "Add your feature"

4.Push to the branch:

git push origin feature/your-feature-name
Open a pull request and describe your changes.

📄 License
This project is licensed under the MIT License. See the LICENSE file for details.

🙏 Acknowledgments
.Flask: For providing a simple and powerful web framework.

.GROQ API: For enabling intelligent chatbot responses.

.Markdown: For making text formatting easy and readable.
