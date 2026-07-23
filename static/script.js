document.getElementById('chat-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const inputField = document.getElementById('user-input');
    const message = inputField.value.trim();
    if (!message) return;
    
    // Clear input
    inputField.value = '';
    
    // Add user message to chat
    appendMessage(message, 'user-message');
    
    // Show typing indicator
    const typingId = showTypingIndicator();
    
    try {
        const response = await fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: message })
        });
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        const data = await response.json();
        
        // Remove typing indicator
        removeElement(typingId);
        
        // Add bot response
        appendBotMessage(data);
        
    } catch (error) {
        removeElement(typingId);
        appendMessage('Sorry, there was an error processing your request. Is the backend running?', 'bot-message');
    }
});

function appendMessage(text, className) {
    const chatContainer = document.getElementById('chat-container');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${className}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = text;
    
    messageDiv.appendChild(contentDiv);
    chatContainer.appendChild(messageDiv);
    scrollToBottom();
}

function appendBotMessage(data) {
    const chatContainer = document.getElementById('chat-container');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    
    const avatarDiv = document.createElement('div');
    avatarDiv.className = 'avatar';
    avatarDiv.textContent = '🤖';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    // Parse markdown-like bold (very basic)
    let formattedText = data.answer.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    formattedText = formattedText.replace(/\n/g, '<br>');
    
    contentDiv.innerHTML = formattedText;
    
    // Add sources if available
    if (data.sources && data.sources.length > 0) {
        const sourcesDiv = document.createElement('div');
        sourcesDiv.className = 'sources';
        sourcesDiv.textContent = 'Sources: ';
        
        data.sources.forEach(source => {
            const span = document.createElement('span');
            span.className = 'source-tag';
            span.textContent = source;
            sourcesDiv.appendChild(span);
        });
        
        contentDiv.appendChild(sourcesDiv);
    }
    
    if (!data.is_in_scope) {
        const scopeWarning = document.createElement('div');
        scopeWarning.style.marginTop = '10px';
        scopeWarning.style.color = '#ef4444';
        scopeWarning.style.fontSize = '0.8rem';
        scopeWarning.textContent = '⚠️ Out of Scope';
        contentDiv.appendChild(scopeWarning);
    }
    
    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(contentDiv);
    chatContainer.appendChild(messageDiv);
    scrollToBottom();
}

function showTypingIndicator() {
    const chatContainer = document.getElementById('chat-container');
    const typingId = 'typing-' + Date.now();
    
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message';
    typingDiv.id = typingId;
    
    typingDiv.innerHTML = `
        <div class="avatar">🤖</div>
        <div class="message-content">
            <div class="typing-indicator">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>
        </div>
    `;
    
    chatContainer.appendChild(typingDiv);
    scrollToBottom();
    return typingId;
}

function removeElement(id) {
    const el = document.getElementById(id);
    if (el) {
        el.remove();
    }
}

function scrollToBottom() {
    const chatContainer = document.getElementById('chat-container');
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

document.getElementById('clear-btn').addEventListener('click', () => {
    const chatContainer = document.getElementById('chat-container');
    const welcomeMessage = chatContainer.firstElementChild;
    chatContainer.innerHTML = '';
    if (welcomeMessage) {
        chatContainer.appendChild(welcomeMessage);
    }
});
