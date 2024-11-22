// DOM Elements
const chatMessages = document.getElementById('chatMessages');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');
const chatForm = document.getElementById('chatForm');
const mobileSidebarToggle = document.getElementById('mobileSidebarToggle');
const sidebar = document.getElementById('sidebar');

// Chat Configuration
const CHAT_CONFIG = {
    user: { 
        name: 'You',
        avatar: 'https://ui-avatars.com/api/?background=random'
    },
    assistant: { 
        name: 'PlanIt',
        avatar: '/static/images/planit-avatar.png' // You'll need to add this image
    }
};

// Message Templates
const messageTemplates = {
    user: (message) => `
        <div class="chat-message user-message">
            <div class="max-w-3xl mx-auto px-4">
                <div class="flex items-start gap-4">
                    <img src="${CHAT_CONFIG.user.avatar}" alt="User Avatar" class="w-8 h-8 rounded-full mt-1" />
                    <div class="flex-1">
                        <p class="text-copy-primary">${message}</p>
                    </div>
                </div>
            </div>
        </div>
    `,
    assistant: (message) => `
        <div class="chat-message assistant-message">
            <div class="max-w-3xl mx-auto px-4">
                <div class="flex items-start gap-4">
                    <img src="${CHAT_CONFIG.assistant.avatar}" alt="PlanIt Avatar" class="w-8 h-8 rounded-full mt-1" />
                    <div class="flex-1">
                        <p class="text-copy-primary whitespace-pre-wrap">${message}</p>
                    </div>
                </div>
            </div>
        </div>
    `,
    typing: () => `
        <div class="chat-message assistant-message" id="typing-indicator">
            <div class="max-w-3xl mx-auto px-4">
                <div class="flex items-start gap-4">
                    <img src="${CHAT_CONFIG.assistant.avatar}" alt="PlanIt Avatar" class="w-8 h-8 rounded-full mt-1" />
                    <div class="flex items-center space-x-2">
                        <div class="typing-indicator text-copy-secondary">Thinking</div>
                    </div>
                </div>
            </div>
        </div>
    `
};

// Chat History Management
class ChatHistory {
    constructor() {
        this.messages = [];
        this.currentPlan = null;
    }

    addMessage(role, content) {
        this.messages.push({ role, content, timestamp: new Date() });
        this.saveToLocalStorage();
    }

    startNewPlan() {
        this.currentPlan = {
            id: Date.now(),
            title: 'New Travel Plan',
            messages: []
        };
        this.saveToLocalStorage();
    }

    saveToLocalStorage() {
        localStorage.setItem('chatHistory', JSON.stringify({
            messages: this.messages,
            currentPlan: this.currentPlan
        }));
    }

    loadFromLocalStorage() {
        const saved = localStorage.getItem('chatHistory');
        if (saved) {
            const { messages, currentPlan } = JSON.parse(saved);
            this.messages = messages;
            this.currentPlan = currentPlan;
        }
    }
}

// Initialize Chat
const chatHistory = new ChatHistory();

// Message Handler
class MessageHandler {
    static async send(message) {
        // Add user message
        MessageHandler.addToChat('user', message);
        chatHistory.addMessage('user', message);

        // Show typing indicator
        MessageHandler.showTypingIndicator();

        try {
            // Send to backend
            const response = await fetch('/api/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({ message })
            });

            if (!response.ok) throw new Error('Failed to get response');

            const data = await response.json();
            MessageHandler.removeTypingIndicator();
            MessageHandler.addToChat('assistant', data.response);
            chatHistory.addMessage('assistant', data.response);

        } catch (error) {
            console.error('Error:', error);
            MessageHandler.removeTypingIndicator();
            MessageHandler.addToChat('assistant', 'I apologize, but I encountered an error. Please try again.');
        }
    }

    static addToChat(role, message) {
        const template = messageTemplates[role](message);
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = template;
        chatMessages.appendChild(tempDiv.firstElementChild);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    static showTypingIndicator() {
        if (!document.getElementById('typing-indicator')) {
            const template = messageTemplates.typing();
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = template;
            chatMessages.appendChild(tempDiv.firstElementChild);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }

    static removeTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) indicator.remove();
    }
}

// Event Listeners
chatForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const message = userInput.value.trim();
    if (message) {
        MessageHandler.send(message);
        userInput.value = '';
        userInput.style.height = 'auto';
        sendButton.disabled = true;
    }
});

// Auto-resize textarea
userInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
    sendButton.disabled = !this.value.trim();
});

// Mobile sidebar toggle
mobileSidebarToggle?.addEventListener('click', () => {
    sidebar.classList.toggle('hidden');
});

// Suggestion handler
window.suggestPrompt = function(button) {
    const promptText = button.querySelector('p:last-child').textContent.replace(/['"]/g, '');
    userInput.value = promptText;
    userInput.focus();
    userInput.dispatchEvent(new Event('input'));
};

// New chat handler
window.startNewChat = function() {
    chatHistory.startNewPlan();
    chatMessages.innerHTML = '';
    // Add welcome message
    MessageHandler.addToChat('assistant', 'Hello! I\'m ready to help you plan your next adventure. What type of trip would you like to plan?');
};
