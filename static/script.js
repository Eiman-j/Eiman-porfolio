const chatToggle = document.getElementById('chat-toggle');
const chatWindow = document.getElementById('chat-window');
const chatClose = document.getElementById('chat-close');
const chatSend = document.getElementById('chat-send');
const chatInput = document.getElementById('chat-input');

chatToggle.addEventListener('click', () => {
    // Toggle visibility
    if (chatWindow.style.display === 'none') {
        chatWindow.style.display = 'flex';
        chatInput.focus(); // Auto-focus the input box
    } else {
        chatWindow.style.display = 'none';
    }
});

chatClose.addEventListener('click', () => {
    chatWindow.style.display = 'none';
});

// Cursor logic for newly added chat elements so they expand the custom dot
document.querySelectorAll('#chat-toggle, #chat-close, #chat-send').forEach(el => {
    el.addEventListener('mouseenter', () => {
      document.getElementById('cursor').style.width = '20px';
      document.getElementById('cursor').style.height = '20px';
      document.getElementById('cursorTrail').style.width = '60px';
      document.getElementById('cursorTrail').style.height = '60px';
    });
    el.addEventListener('mouseleave', () => {
      document.getElementById('cursor').style.width = '12px';
      document.getElementById('cursor').style.height = '12px';
      document.getElementById('cursorTrail').style.width = '36px';
      document.getElementById('cursorTrail').style.height = '36px';
    });
});


async function sendMessage() {
    const message = chatInput.value.trim();

    if (!message) return;

    // 1. Display User Message
    appendMessage("You", message, "user-message-class");
    chatInput.value = ''; // clear input

    try {
        // Show a temporary "typing..." indicator
        const chatMessages = document.getElementById('chat-messages');
        const typingDiv = document.createElement('div');
        typingDiv.id = "typing-indicator";
        typingDiv.className = "bot-message-class";
        typingDiv.innerHTML = `<strong>Eiman (Clone Bot)</strong> <span style="opacity:0.5">Typing...</span>`;
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        // 2. Send data to Flask backend
        const response = await fetch('https://eiman-porfolio-backend.onrender.com/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();
        
        // Remove typing indicator
        document.getElementById('typing-indicator').remove();

        // 3. Display AI reply
        appendMessage("Eiman (Clone Bot)", data.reply, "bot-message-class");

    } catch (error) {
        console.error("Error communicating with backend:", error);
        if(document.getElementById('typing-indicator')) document.getElementById('typing-indicator').remove();
        appendMessage("System", "Network error. Make sure your Flask server is running!", "error-class");
    }
}

function appendMessage(sender, text, className) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = className;
    messageDiv.innerHTML = `<strong>${sender}</strong> ${text}`;
    
    chatMessages.appendChild(messageDiv);
    
    // Auto-scroll to the bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Allow sending with buttons
chatSend.addEventListener('click', sendMessage);

// Allow sending with Enter key
chatInput.addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});