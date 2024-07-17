// Display the back-to-top button when scrolling
window.onscroll = function() {
    toggleBackToTopButton();
};

function toggleBackToTopButton() {
    let backToTopButton = document.getElementById('back-to-top');
    if (document.body.scrollTop > 200 || document.documentElement.scrollTop > 200) {
        backToTopButton.style.display = "block"; // Make the button visible
    } else {
        backToTopButton.style.display = "none"; // Hide the button
    }
}

function scrollToTop() {
    let messages = document.getElementById('messages');
    messages.scrollTop = messages.scrollHeight; // Scroll to the bottom of the chat container instead
}

// Add event listener for user input to handle the "Enter" key for sending messages
document.getElementById('user-input').addEventListener('keypress', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault(); // Prevent adding a new line
        sendMessage(); // Send the message
    }
});

function sendMessage() {
    let userInput = document.getElementById('user-input').value;
    let messages = document.getElementById('messages');

    if (!userInput.trim()) return;

    // Create and display user message
    let userMessage = document.createElement('div');
    userMessage.className = 'user-message';
    userMessage.textContent = userInput;
    messages.appendChild(userMessage);

    scrollToBottom(); // Scroll to bottom after new message

    // Create "Bot is typing..." message
    let loadingMessage = document.createElement('div');
    loadingMessage.className = 'bot-message';
    loadingMessage.id = 'loading-message';
    loadingMessage.textContent = 'Bot is typing...';
    messages.appendChild(loadingMessage);

    scrollToBottom(); // Scroll after bot is typing message

    // Simulate a delay for the bot's response
    setTimeout(() => {
        fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: userInput }),
        })
        .then(response => response.json())
        .then(data => {
            // Remove the "Bot is typing..." message
            messages.removeChild(loadingMessage);

            // Create and display bot's response message
            let botMessage = document.createElement('div');
            botMessage.className = 'bot-message';
            botMessage.innerHTML = formatResponse(data.response);
            messages.appendChild(botMessage);

            scrollToBottom(); // Scroll after bot's message
        })
        .catch(error => {
            // Remove the "Bot is typing..." message
            messages.removeChild(loadingMessage);

            // Create and display error message
            let errorMessage = document.createElement('div');
            errorMessage.className = 'bot-message';
            errorMessage.textContent = 'Error: ' + error.message;
            messages.appendChild(errorMessage);

            scrollToBottom(); // Scroll after error message
        });
    }, 1500); // Simulated delay for typing

    document.getElementById('user-input').value = ''; // Clear input field
}

// Format response for markdown-like styling
function formatResponse(response) {
    return response.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                  .replace(/\*(.*?)\*/g, '<em>$1</em>')
                  .replace(/\n/g, '<br>');
}

function setQuestion(question) {
    document.getElementById('user-input').value = question;
}

function getGreetingBasedOnTime() {
    const hour = new Date().getHours();
    if (hour >= 5 && hour < 12) {
        return "Good morning! ☀️";
    } else if (hour >= 12 && hour < 18) {
        return "Good afternoon! 🌤️";
    } else if (hour >= 18 && hour < 22) {
        return "Good evening! 🌙";
    } else {
        return "Good night! 🌃";
    }
}

function getRandomQuestion() {
    const questions = [
        "How are you today?",
        "How is your day going?",
        "How are things going?",
        "How's everything?",
        "How are you feeling today?"
    ];
    const randomIndex = Math.floor(Math.random() * questions.length);
    return questions[randomIndex];
}

// Scroll to the bottom of the chat container
function scrollToBottom() {
    let messages = document.getElementById('messages');
    setTimeout(() => {
        messages.scrollTop = messages.scrollHeight; // Scroll to the bottom of the chat container
    }, 100); // Add a small delay for smooth scrolling
}

// Fetch the initial welcome message on page load
window.onload = function() {
    let messages = document.getElementById('messages');

    // Get greeting based on the time of day
    const greeting = getGreetingBasedOnTime();
    const question = getRandomQuestion();

    // Add greeting and question to chat
    let botMessage = document.createElement('div');
    botMessage.className = 'bot-message';
    botMessage.textContent = `${greeting} ${question}`;
    messages.appendChild(botMessage);

    // Scroll to the bottom of the chat
    scrollToBottom();
};

// Simulate typing delay for the bot's response
function simulateTypingDelay(response, callback) {
    const typingDelay = Math.random() * 2 + 1; // Random delay between 1 and 3 seconds
    setTimeout(() => {
        callback(response);
    }, typingDelay * 1000); // Convert to milliseconds
}
