document.getElementById('chat-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const inputField = document.getElementById('user-input');
    const message = inputField.value.trim();
    if (!message) return;
    
    // Clear input
    inputField.value = '';
    inputField.style.height = 'auto'; // reset textarea height
    
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
        appendBotMessage({
            answer: 'Sorry, there was an error processing your request. Is the backend running?',
            is_in_scope: true,
            sources: []
        });
    }
});

// Auto-resize textarea
const tx = document.getElementById('user-input');
tx.setAttribute('style', 'height:' + (tx.scrollHeight) + 'px;overflow-y:hidden;');
tx.addEventListener("input", OnInput, false);

// Press Enter to submit (Shift+Enter for newline)
tx.addEventListener("keydown", function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        document.getElementById('chat-form').dispatchEvent(new Event('submit'));
    }
});

function OnInput() {
  this.style.height = 'auto';
  this.style.height = (this.scrollHeight) + 'px';
  if (this.scrollHeight > 200) {
      this.style.overflowY = 'auto';
  } else {
      this.style.overflowY = 'hidden';
  }
}

function appendMessage(text, className) {
    const chatContent = document.querySelector('.chat-content');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${className}`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = text;
    
    // Add dummy avatar for HTML structure compatibility (hidden in CSS for user)
    const avatarDiv = document.createElement('div');
    avatarDiv.className = 'avatar';
    
    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(contentDiv);
    chatContent.appendChild(messageDiv);
    scrollToBottom();
}

function appendBotMessage(data) {
    const chatContent = document.querySelector('.chat-content');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    
    const avatarDiv = document.createElement('div');
    avatarDiv.className = 'avatar';
    avatarDiv.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a10 10 0 1 0 10 10H12V2Z"></path><path d="M12 12 2.1 7.1"></path><path d="M12 12l9.9 4.9"></path></svg>`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    // Parse basic markdown formatting
    let formattedText = data.answer.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Split into paragraphs based on newlines
    const paragraphs = formattedText.split('\n').filter(p => p.trim() !== '');
    paragraphs.forEach(p => {
        const pTag = document.createElement('p');
        pTag.innerHTML = p;
        contentDiv.appendChild(pTag);
    });
    
    // Add sources if available
    if (data.sources && data.sources.length > 0) {
        const sourcesDiv = document.createElement('div');
        sourcesDiv.className = 'sources';
        
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
        scopeWarning.className = 'out-of-scope-warning';
        scopeWarning.textContent = '⚠️ Out of Scope';
        contentDiv.appendChild(scopeWarning);
    }
    
    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(contentDiv);
    chatContent.appendChild(messageDiv);
    scrollToBottom();
}

function showTypingIndicator() {
    const chatContent = document.querySelector('.chat-content');
    const typingId = 'typing-' + Date.now();
    
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message';
    typingDiv.id = typingId;
    
    typingDiv.innerHTML = `
        <div class="avatar">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a10 10 0 1 0 10 10H12V2Z"></path><path d="M12 12 2.1 7.1"></path><path d="M12 12l9.9 4.9"></path></svg>
        </div>
        <div class="message-content">
            <div class="typing-indicator">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>
        </div>
    `;
    
    chatContent.appendChild(typingDiv);
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
    chatContainer.scrollTo({
        top: chatContainer.scrollHeight,
        behavior: 'smooth'
    });
}

document.getElementById('clear-btn').addEventListener('click', () => {
    const chatContent = document.querySelector('.chat-content');
    const welcomeMessage = chatContent.firstElementChild;
    chatContent.innerHTML = '';
    if (welcomeMessage) {
        chatContent.appendChild(welcomeMessage);
    }
});
