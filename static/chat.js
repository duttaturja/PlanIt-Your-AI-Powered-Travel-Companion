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
        avatar: '/static/images/planit-avatar.png'
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
                    <div class="flex-1">
                        <p class="text-copy-secondary typing-indicator">Thinking</p>
                    </div>
                </div>
            </div>
        </div>
    `
};

class MessageHandler {
    constructor() {
        this.isProcessing = false;
    }

    async send(message) {
        if (this.isProcessing) return;
        this.isProcessing = true;

        try {
            // Add user message to chat
            this.addToChat('user', message);
            
            // Show typing indicator
            this.showTypingIndicator();
            
            // Send message to backend
            const response = await fetch('/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message })
            });

            const data = await response.json();
            
            if (data.status === 'success') {
                // Remove typing indicator and add assistant's response
                this.removeTypingIndicator();
                this.addToChat('assistant', data.response);
            } else {
                throw new Error(data.error || 'Failed to get response');
            }
        } catch (error) {
            console.error('Error:', error);
            this.removeTypingIndicator();
            this.addToChat('assistant', 'Sorry, I encountered an error. Please try again.');
        } finally {
            this.isProcessing = false;
            userInput.value = '';
            userInput.style.height = 'auto';
            sendButton.disabled = true;
        }
    }

    addToChat(role, message) {
        const template = messageTemplates[role];
        if (template) {
            chatMessages.insertAdjacentHTML('beforeend', template(message));
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }

    showTypingIndicator() {
        chatMessages.insertAdjacentHTML('beforeend', messageTemplates.typing());
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    removeTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) {
            indicator.remove();
        }
    }
}

// Initialize Message Handler
const messageHandler = new MessageHandler();

// Event Listeners
chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const message = userInput.value.trim();
    if (message) {
        await messageHandler.send(message);
    }
});

userInput.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
    sendButton.disabled = !this.value.trim();
});

mobileSidebarToggle?.addEventListener('click', () => {
    sidebar?.classList.toggle('hidden');
});

// Suggestion handler
function suggestPrompt(button) {
    const promptText = button.querySelector('p:last-child').textContent.replace(/['"]/g, '');
    userInput.value = promptText;
    userInput.focus();
    userInput.dispatchEvent(new Event('input'));
}

// New chat handler
async function startNewChat() {
    try {
        const response = await fetch('/clear-chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const data = await response.json();
        if (data.status === 'success') {
            chatMessages.innerHTML = '';
            userInput.value = '';
            userInput.style.height = 'auto';
            sendButton.disabled = true;
        } else {
            console.error('Failed to clear chat:', data.error);
        }
    } catch (error) {
        console.error('Error clearing chat:', error);
    }
}
