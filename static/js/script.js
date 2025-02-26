document.getElementById('user-input').addEventListener('keypress', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault(); // Yeni satır eklemeyi engelle
        sendMessage(); // Mesajı gönder
    }
});

function sendMessage() {
    let userInput = document.getElementById('user-input').value;
    let messages = document.getElementById('messages');

    // Boş mesaj göndermeyi engelle
    if (!userInput.trim()) return;

    // Kullanıcı mesajını sohbete ekle
    let userMessage = document.createElement('div');
    userMessage.className = 'user-message';
    userMessage.textContent = userInput;
    messages.appendChild(userMessage);

    // Yükleme göstergesi ekle
    let loadingMessage = document.createElement('div');
    loadingMessage.className = 'bot-message';
    loadingMessage.textContent = 'Bot is typing...';
    messages.appendChild(loadingMessage);

    // Sunucuya mesajı gönder
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userInput }),
    })
    .then(response => response.json())
    .then(data => {
        // Yükleme göstergesini kaldır
        messages.removeChild(loadingMessage);

        // Bot yanıtını sohbete ekle
        let botMessage = document.createElement('div');
        botMessage.className = 'bot-message';
        botMessage.innerHTML = formatResponse(data.response);
        messages.appendChild(botMessage);

        // Sohbeti en altına kaydır
        messages.scrollTop = messages.scrollHeight;
    })
    .catch(error => {
        // Yükleme göstergesini kaldır
        messages.removeChild(loadingMessage);

        console.error('Error:', error);
        let errorMessage = document.createElement('div');
        errorMessage.className = 'bot-message';
        errorMessage.textContent = 'Error: ' + error.message;
        messages.appendChild(errorMessage);
    });

    // Input alanını temizle
    document.getElementById('user-input').value = '';
}

function formatResponse(response) {
    // Markdown benzeri formatlama
    return response.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                  .replace(/\*(.*?)\*/g, '<em>$1</em>')
                  .replace(/\n/g, '<br>');
}

function setQuestion(question) {
    document.getElementById('user-input').value = question;
}

// Sayfa yüklendiğinde hoş geldin mesajını getir
window.onload = function() {
    let messages = document.getElementById('messages');

    fetch('/start', {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        // Botun hoş geldin mesajını ekle
        let botMessage = document.createElement('div');
        botMessage.className = 'bot-message';
        botMessage.innerHTML = formatResponse(data.response);
        messages.appendChild(botMessage);

        // Sohbeti en altına kaydır
        messages.scrollTop = messages.scrollHeight;
    })
    .catch(error => {
        console.error('Error:', error);
        let errorMessage = document.createElement('div');
        errorMessage.className = 'bot-message';
        errorMessage.textContent = 'Failed to load initial message, please try again later.';
        messages.appendChild(errorMessage);
    });
};